from app.service import ChatService, SYSTEM_PROMPT


def test_persona_prompt_requires_full_lyric_paraphrasing() -> None:
    assert "Do not reproduce or quote any lyric verbatim" in SYSTEM_PROMPT


def test_direct_quoted_lyrics_are_removed_without_a_placeholder() -> None:
    answer = 'Model "a direct lyric fragment" kullanmamali.'
    assert ChatService._remove_direct_quotes(answer) == "Model kullanmamali."


def test_quoted_song_title_is_preserved() -> None:
    assert ChatService._remove_direct_quotes('"Runaway" guclu bir ornek.', {"Runaway"}) == "Runaway guclu bir ornek."


def test_insufficient_context_response_does_not_include_sources() -> None:
    response = ChatService._insufficient_context_response("What is the capital of France?")
    assert response.status == "insufficient_context"
    assert response.sources == []


def test_comparison_instruction_requires_every_named_song() -> None:
    instruction = ChatService._comparison_instruction(["Power", "All of the Lights"])
    assert "Power" in instruction
    assert "All of the Lights" in instruction
    assert "MUST" in instruction
