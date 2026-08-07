"""Ham lyrics JSONL dosyasini ChromaDB'ye indeksler."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.config import Settings
from app.vector_store import ChromaLyricsStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Kanye West lyrics RAG indeksleyici")
    parser.add_argument("--reset", action="store_true", help="Mevcut Chroma koleksiyonunu silip yeniden olusturur.")
    args = parser.parse_args()

    input_path = PROJECT_ROOT / "data" / "raw" / "songs.jsonl"
    if not input_path.exists():
        parser.error("data/raw/songs.jsonl bulunamadi. Once collect_lyrics.py calistirin.")

    store = ChromaLyricsStore(Settings.from_env())
    if args.reset:
        store.reset()
    count = store.index_jsonl(input_path, PROJECT_ROOT / "data" / "processed" / "chunks.jsonl")
    print(f"Indekslenen chunk sayisi: {count}")


if __name__ == "__main__":
    main()
