from scripts.collect_lyrics import extract_lyrics, lyrics_ovh_url


def test_extract_lyrics_from_modern_genius_markup() -> None:
    html = '<div data-lyrics-container>First line<br/>Second line</div>'
    assert extract_lyrics(html) == "First line\nSecond line"


def test_lyrics_ovh_url_encodes_song_title() -> None:
    assert lyrics_ovh_url("Can't Tell Me Nothing") == "https://api.lyrics.ovh/v1/Kanye%20West/Can%27t%20Tell%20Me%20Nothing"
