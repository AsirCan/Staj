"""Uygulama ayarlarini ortam degiskenlerinden okur."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str
    ollama_model: str
    ollama_timeout_seconds: int
    embedding_model: str
    chroma_collection: str
    chroma_path: Path
    top_k: int
    min_similarity: float

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv(PROJECT_ROOT / ".env")
        return cls(
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/"),
            ollama_model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct"),
            ollama_timeout_seconds=int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "90")),
            embedding_model=os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-small"),
            chroma_collection=os.getenv("CHROMA_COLLECTION", "kanye_west_lyrics"),
            chroma_path=PROJECT_ROOT / "data" / "chroma",
            top_k=int(os.getenv("TOP_K", "3")),
            min_similarity=float(os.getenv("MIN_SIMILARITY", "0.78")),
        )
