"""Retriever + Ollama uretim katmani."""

from __future__ import annotations

from collections import OrderedDict
import re

import requests

from app.config import Settings
from app.schemas import ChatResponse, HealthResponse, Source
from app.vector_store import ChromaLyricsStore, EmptyIndexError, RetrievedChunk


class OllamaUnavailableError(RuntimeError):
    """Ollama sunucusu ya da secili model kullanilamaz oldugunda yukseltilir."""


SYSTEM_PROMPT = """You are a careful music-analysis assistant, not Kanye West.
Use only the retrieved Kanye West lyric passages as evidence. Analyze recurring
themes such as ambition, vulnerability, conflict, faith, family, fame and
self-criticism. Reply strictly in the exact language used by the user (if user asks in Turkish, reply ONLY in Turkish; if in English, reply ONLY in English). Never output Chinese, Thai, or any non-target language text under any circumstances. Do not claim personal memories, do not present yourself as the artist, and do not invent a song or lyric. Do not reproduce or quote any lyric verbatim, even a short phrase; paraphrase every lyric idea in your own words. Never use quotation marks for lyrics and never use placeholder wording such as "relevant lyric excerpt". Mention the relevant song titles naturally when useful."""


class ChatService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.from_env()
        self.store = ChromaLyricsStore(self.settings)

    def _ollama_available(self) -> bool:
        try:
            response = requests.get(f"{self.settings.ollama_base_url}/api/tags", timeout=3)
            return response.ok
        except requests.RequestException:
            return False

    def health(self) -> HealthResponse:
        available = self._ollama_available()
        return HealthResponse(
            status="healthy" if available else "degraded",
            collection_count=self.store.count(),
            ollama_model=self.settings.ollama_model,
            ollama_available=available,
        )

    @staticmethod
    def _comparison_instruction(required_titles: list[str]) -> str:
        """Make an explicit multi-song request an output contract for the LLM."""
        if not required_titles:
            return ""
        titles = ", ".join(required_titles)
        if len(required_titles) == 1:
            return f"The user explicitly named {titles}. Discuss that song directly and name it in the answer."
        headings = " and ".join(required_titles)
        return (
            f"The user explicitly named these songs: {titles}. This is a comparison request: you MUST "
            f"discuss every named song, use clear sections headed {headings}, then end with a direct comparison. "
            "Do not substitute a different song or focus on only one title."
        )

    def _ask_ollama(self, user_content: str, system_prompt: str = SYSTEM_PROMPT) -> str:
        try:
            response = requests.post(
                f"{self.settings.ollama_base_url}/api/chat",
                json={
                    "model": self.settings.ollama_model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content},
                    ],
                    "stream": False,
                    "options": {"temperature": 0.2, "num_predict": 400},
                },
                timeout=self.settings.ollama_timeout_seconds,
            )
            response.raise_for_status()
            answer = response.json().get("message", {}).get("content", "").strip()
        except (requests.RequestException, ValueError) as exc:
            raise OllamaUnavailableError(
                "Ollama'ya ulasilamadi. `ollama serve` ve secili modelin kurulu oldugunu kontrol edin."
            ) from exc
        if not answer:
            raise OllamaUnavailableError("Ollama bos bir yanit dondurdu.")
        return answer

    def _generate(
        self, user_message: str, chunks: list[RetrievedChunk], required_titles: list[str] | None = None
    ) -> str:
        required_titles = required_titles or []
        evidence = "\n\n".join(
            f"[Song: {chunk.metadata['song']}; Album: {chunk.metadata.get('album', '')}]\n{chunk.text}"
            for chunk in chunks
        )
        instruction = self._comparison_instruction(required_titles)
        user_content = (
            f"{instruction}\n\nRetrieved context:\n{evidence}"
            f"\n\nUser question: {user_message}\nAnswer:"
        ).strip()
        answer = self._ask_ollama(user_content)
        missing_titles = [title for title in required_titles if title.casefold() not in answer.casefold()]
        if missing_titles:
            repair_user_content = (
                f"Your previous answer omitted required song titles. Write a complete replacement "
                f"answer to the user question. It must explicitly cover every one of these songs: {', '.join(required_titles)}. "
                "For a comparison, use a separate heading for each song and a final comparison. Do not quote lyrics."
                f"\n\nRetrieved context:\n{evidence}\n\nUser question: {user_message}\nAnswer:"
            )
            answer = self._ask_ollama(repair_user_content)
        song_titles = {str(chunk.metadata["song"]) for chunk in chunks}
        return self._remove_direct_quotes(answer, song_titles)

    @staticmethod
    def _remove_direct_quotes(answer: str, song_titles: set[str] | None = None) -> str:
        """Remove possible verbatim lyrics without exposing an ugly placeholder."""
        normalized_titles = {title.casefold() for title in song_titles or set()}

        def replace(match: re.Match[str]) -> str:
            quoted_text = match.group(0)[1:-1].strip()
            # Preserve song titles or single/double word terms (e.g., "Faith", "Jesus") rather than wiping them into empty gaps
            if quoted_text.casefold() in normalized_titles or len(quoted_text.split()) <= 2:
                return quoted_text
            return ""

        cleaned = re.sub(r'["\u201c][^"\u201d]{1,240}["\u201d]', replace, answer)
        cleaned = re.sub(r"\s+([,.;:!?])", r"\1", cleaned)
        return re.sub(r"[ \t]{2,}", " ", cleaned).strip()

    @staticmethod
    def _merge_chunks(primary: list[RetrievedChunk], secondary: list[RetrievedChunk], limit: int) -> list[RetrievedChunk]:
        """Keep song-specific evidence first, without duplicate chunks."""
        result: list[RetrievedChunk] = []
        seen: set[tuple[str, int]] = set()
        for chunk in [*primary, *secondary]:
            key = (str(chunk.metadata.get("song", "")), int(chunk.metadata.get("chunk_index", -1)))
            if key not in seen:
                result.append(chunk)
                seen.add(key)
            if len(result) >= limit:
                break
        return result

    @staticmethod
    def _sources(chunks: list[RetrievedChunk]) -> list[Source]:
        sources: OrderedDict[str, Source] = OrderedDict()
        for chunk in chunks:
            song = str(chunk.metadata["song"])
            if song not in sources:
                sources[song] = Source(
                    song=song,
                    album=str(chunk.metadata.get("album") or "") or None,
                    year=int(chunk.metadata.get("year") or 0) or None,
                    similarity=round(chunk.similarity, 3),
                    source_url=str(chunk.metadata.get("source_url") or "") or None,
                )
        return list(sources.values())

    @staticmethod
    def _insufficient_context_response(user_message: str) -> ChatResponse:
        turkish_markers = ("\u015f", "\u011f", "\u0131", "\u00e7", "\u00f6", "\u00fc", " nas\u0131l", "hangi", "nedir", " m\u0131", "mi")
        is_turkish = any(marker in user_message.casefold() for marker in turkish_markers)
        reply = (
            "Bu soru se\u00e7ilmi\u015f Kanye West \u015fark\u0131 s\u00f6zleriyle yeterince desteklenmiyor; "
            "yorum uydurmak yerine veri setindeki \u015fark\u0131larla ilgili daha somut bir soru sorabilirsin."
            if is_turkish
            else "This question is not sufficiently supported by the selected Kanye West lyrics, "
            "so I will not invent an interpretation. Please ask about a song or theme in the corpus."
        )
        return ChatResponse(
            status="insufficient_context",
            reply=reply,
            retrieved_context="No lyric passage met the minimum similarity threshold.",
            sources=[],
        )

    def chat(self, user_message: str) -> ChatResponse:
        required_titles = self.store.mentioned_song_titles(user_message) or []
        named_chunks = [
            chunk
            for title in required_titles
            for chunk in (self.store.search_song(user_message, title, top_k=1) or [])
        ]
        semantic_chunks = self.store.search(user_message, self.settings.top_k) or []
        chunks = self._merge_chunks(
            named_chunks,
            semantic_chunks,
            max(self.settings.top_k, len(named_chunks)),
        )
        if not named_chunks and not any(chunk.similarity >= self.settings.min_similarity for chunk in chunks):
            return self._insufficient_context_response(user_message)
        sources = self._sources(chunks)
        context = "Retrieved song passages: " + ", ".join(source.song for source in sources)
        return ChatResponse(
            reply=self._generate(user_message, chunks, required_titles),
            retrieved_context=context,
            sources=sources,
        )

    def translate(self, text: str, target_language: str = "Turkish") -> str:
        try:
            all_titles = self.store.all_song_titles()
        except Exception:
            all_titles = []
        
        song_titles_str = ", ".join(f"'{title}'" for title in all_titles) if all_titles else "song titles"
        system_prompt = (
            "You are an expert professional music translator. "
            "CRITICAL RULE: DO NOT translate proper nouns, artist names, album names, or song titles under any circumstances. "
            f"Song titles such as {song_titles_str} MUST remain strictly in their original English names (for example, NEVER translate 'Jesus Walks' to 'İsa Yürür' or 'All Falls Down' to 'Tüm Bunlar Düşüyor')."
        )
        prompt = (
            f"Translate the following music analysis text into fluent, natural {target_language}. "
            "Keep all song titles in their original English form. "
            "Do not add intro or outro commentary. Output ONLY the translated text:\n\n"
            f"{text}"
        )
        translated = self._ask_ollama(prompt, system_prompt=system_prompt)
        
        # Safety post-processing for common song title mistranslations
        replacements = {
            "İsa Yürür": "Jesus Walks",
            "İsa walks": "Jesus Walks",
            "Güçlüer": "Stronger",
            "Tüm Bunlar Düşüyor": "All Falls Down",
            "Kalpsiz": "Heartless",
            "Aşırı Hafif Işın": "Ultralight Beam",
            "Izgaradan Uzak": "Off the Grid",
            "Altın Arayıcı": "Gold Digger",
            "Siyah Kafa": "Black Skinhead",
        }
        for tr_name, en_name in replacements.items():
            translated = re.sub(rf"\b{re.escape(tr_name)}\b", en_name, translated, flags=re.IGNORECASE)
        return translated


__all__ = ["ChatService", "EmptyIndexError", "OllamaUnavailableError"]
