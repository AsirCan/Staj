"""ChromaDB ve sentence-transformers icin ince adaptorlu katman."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.chunking import chunk_lyrics
from app.config import Settings


class EmptyIndexError(RuntimeError):
    """Sorgulanabilir dokuman olmadiginda yukseltilir."""


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    metadata: dict[str, Any]
    similarity: float


class EmbeddingModel:
    def __init__(self, model_name: str) -> None:
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(model_name)

    def encode_passages(self, texts: list[str]) -> list[list[float]]:
        return self._model.encode(
            [f"passage: {text}" for text in texts],
            normalize_embeddings=True,
            show_progress_bar=False,
        ).tolist()

    def encode_query(self, text: str) -> list[float]:
        return self._model.encode(
            [f"query: {text}"], normalize_embeddings=True, show_progress_bar=False
        )[0].tolist()


class ChromaLyricsStore:
    def __init__(self, settings: Settings) -> None:
        import chromadb

        settings.chroma_path.mkdir(parents=True, exist_ok=True)
        self._settings = settings
        self._client = chromadb.PersistentClient(path=str(settings.chroma_path))
        self._collection = self._client.get_or_create_collection(
            name=settings.chroma_collection,
            metadata={"hnsw:space": "cosine"},
        )
        self._embedder: EmbeddingModel | None = None

    def _get_embedder(self) -> EmbeddingModel:
        if self._embedder is None:
            self._embedder = EmbeddingModel(self._settings.embedding_model)
        return self._embedder

    def count(self) -> int:
        return self._collection.count()

    @staticmethod
    def _normalise_for_title_match(value: str) -> str:
        """Makes title matching tolerant of punctuation and sentence endings."""
        return " ".join(re.sub(r"[^a-z0-9]+", " ", value.casefold()).split())

    def mentioned_song_titles(self, query: str) -> list[str]:
        """Return corpus titles explicitly written in the user's message."""
        if self.count() == 0:
            raise EmptyIndexError("Vektor veritabani bos. Once build_index.py calistirilmalidir.")

        rows = self._collection.get(include=["metadatas"])
        titles = {
            str(metadata.get("song", "")).strip()
            for metadata in rows.get("metadatas", [])
            if metadata and metadata.get("song")
        }
        normalised_query = f" {self._normalise_for_title_match(query)} "
        matches = [
            title
            for title in titles
            if f" {self._normalise_for_title_match(title)} " in normalised_query
        ]
        return sorted(matches)
    def all_song_titles(self) -> list[str]:
        """Return all distinct song titles in the index."""
        if self.count() == 0:
            return []
        rows = self._collection.get(include=["metadatas"])
        return sorted({
            str(metadata.get("song", "")).strip()
            for metadata in rows.get("metadatas", [])
            if metadata and metadata.get("song")
        })

    def reset(self) -> None:
        self._client.delete_collection(self._settings.chroma_collection)
        self._collection = self._client.get_or_create_collection(
            name=self._settings.chroma_collection,
            metadata={"hnsw:space": "cosine"},
        )

    def index_jsonl(self, input_path: Path, processed_path: Path) -> int:
        """Ham sarki JSONL'ini chunk'layip hem diske hem Chroma'ya yazar."""
        records = [
            json.loads(line)
            for line in input_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        ids: list[str] = []
        documents: list[str] = []
        metadatas: list[dict[str, Any]] = []
        processed_lines: list[str] = []

        for song_index, record in enumerate(records):
            for chunk_index, text in enumerate(chunk_lyrics(record["lyrics"])):
                chunk_id = f"song-{song_index:03d}-chunk-{chunk_index:03d}"
                metadata = {
                    "song": str(record["title"]),
                    "album": str(record.get("album", "")),
                    "year": int(record.get("year", 0) or 0),
                    "chunk_index": chunk_index,
                    "source_url": str(record.get("source_url", "")),
                }
                ids.append(chunk_id)
                documents.append(text)
                metadatas.append(metadata)
                processed_lines.append(json.dumps({"id": chunk_id, "text": text, **metadata}, ensure_ascii=False))

        if not documents:
            raise EmptyIndexError("Indekslenebilecek sarki sozu bulunamadi.")

        embeddings = self._get_embedder().encode_passages(documents)
        self._collection.upsert(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
        processed_path.parent.mkdir(parents=True, exist_ok=True)
        processed_path.write_text("\n".join(processed_lines) + "\n", encoding="utf-8")
        return len(documents)

    @staticmethod
    def _to_retrieved_chunks(result: dict[str, Any]) -> list[RetrievedChunk]:
        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        distances = result["distances"][0]
        return [
            RetrievedChunk(text=text, metadata=metadata, similarity=max(0.0, min(1.0, 1 - float(distance))))
            for text, metadata, distance in zip(documents, metadatas, distances, strict=True)
        ]

    def _search_with_embedding(
        self, query_embedding: list[float], top_k: int, where: dict[str, str] | None = None
    ) -> list[RetrievedChunk]:
        if top_k <= 0:
            return []
        query_args: dict[str, Any] = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            query_args["where"] = where
        return self._to_retrieved_chunks(self._collection.query(**query_args))

    def search(self, query: str, top_k: int) -> list[RetrievedChunk]:
        if self.count() == 0:
            raise EmptyIndexError("Vektor veritabani bos. Once build_index.py calistirilmalidir.")
        embedding = self._get_embedder().encode_query(query)
        return self._search_with_embedding(embedding, min(top_k, self.count()))

    def search_song(self, query: str, song_title: str, top_k: int = 1) -> list[RetrievedChunk]:
        """Retrieve passages only from one known song title."""
        if self.count() == 0:
            raise EmptyIndexError("Vektor veritabani bos. Once build_index.py calistirilmalidir.")
        matching_rows = self._collection.get(where={"song": song_title}, include=["metadatas"])
        available = len(matching_rows.get("ids", []))
        if available == 0:
            return []
        embedding = self._get_embedder().encode_query(query)
        return self._search_with_embedding(embedding, min(top_k, available), {"song": song_title})
