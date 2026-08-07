"""Sarki sozu temizleme ve anlamli parcalara bolme islemleri."""

from __future__ import annotations

import re


MIN_CHUNK_SIZE = 200
MAX_CHUNK_SIZE = 400


def clean_lyrics(raw_text: str) -> str:
    """Gereksiz bosluklari temizler, bolum etiketlerini korur."""
    lines: list[str] = []
    for raw_line in raw_text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = re.sub(r"\s+", " ", raw_line).strip()
        if not line or line.lower() in {"lyrics", "you might also like"}:
            continue
        lines.append(line)
    return "\n".join(lines)


def _split_long_line(line: str, max_size: int) -> list[str]:
    """400 karakteri gecen tek satiri kelime sinirlarindan ayirir."""
    if len(line) <= max_size:
        return [line]

    words = line.split()
    pieces: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > max_size:
            pieces.append(current)
            current = word
        else:
            current = candidate
    if current:
        pieces.append(current)
    return pieces


def chunk_lyrics(
    raw_text: str,
    min_size: int = MIN_CHUNK_SIZE,
    max_size: int = MAX_CHUNK_SIZE,
) -> list[str]:
    """Sarki sozlerini mumkun oldugunca satir butunlugunu koruyarak boler.

    Son kucuk parca oncekiyle birlesebiliyorsa birlestirilir. Cok kisa bir
    sarki icin tek parca donmek, veriyi tamamen kaybetmekten daha iyidir.
    """
    if not 0 < min_size <= max_size:
        raise ValueError("min_size 0'dan buyuk ve max_size'dan kucuk olmali")

    lines = [
        piece
        for line in clean_lyrics(raw_text).split("\n")
        for piece in _split_long_line(line, max_size)
    ]
    if not lines:
        return []

    chunks: list[str] = []
    current = ""
    for line in lines:
        candidate = f"{current}\n{line}".strip()
        if current and len(candidate) > max_size:
            chunks.append(current)
            current = line
        else:
            current = candidate
    if current:
        chunks.append(current)

    if len(chunks) > 1 and len(chunks[-1]) < min_size:
        merged = f"{chunks[-2]}\n{chunks[-1]}"
        if len(merged) <= max_size:
            chunks[-2:] = [merged]
        else:
            # Son iki parcayi kelime sinirinda yeniden dengele. Bu yalnizca
            # son kucuk parcanin minimum hedefe ulasmasi icin devreye girer.
            lower_bound = min_size
            upper_bound = len(merged) - min_size
            candidates = [
                index
                for index, character in enumerate(merged)
                if character.isspace() and lower_bound <= index <= upper_bound
            ]
            if candidates:
                split_at = min(candidates, key=lambda index: abs(index - len(merged) / 2))
                chunks[-2:] = [merged[:split_at].strip(), merged[split_at:].strip()]

    return chunks
