from app.chunking import MAX_CHUNK_SIZE, MIN_CHUNK_SIZE, chunk_lyrics, clean_lyrics


def test_clean_lyrics_removes_empty_lines_and_normalizes_whitespace() -> None:
    assert clean_lyrics(" Lyrics \n\n  first    line \n second line \n") == "first line\nsecond line"


def test_chunking_keeps_normal_sized_chunks_in_bounds() -> None:
    lyrics = "\n".join(f"This is a meaningful lyric line number {number} about pressure and hope." for number in range(1, 30))
    chunks = chunk_lyrics(lyrics)

    assert len(chunks) > 1
    assert all(MIN_CHUNK_SIZE <= len(chunk) <= MAX_CHUNK_SIZE for chunk in chunks)


def test_short_song_is_not_discarded() -> None:
    assert chunk_lyrics("A short but meaningful lyric.") == ["A short but meaningful lyric."]

