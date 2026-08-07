"""FastAPI istek ve yanit semalari."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=100, examples=["ogrenci_01"])
    message: str = Field(min_length=1, max_length=2_000, examples=["Runaway parcasinda hangi duygu baskin?"])

    @field_validator("user_id", "message")
    @classmethod
    def reject_whitespace_only_values(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Bu alan yalnizca bosluklardan olusamaz.")
        return value.strip()


class Source(BaseModel):
    song: str
    album: str | None = None
    year: int | None = None
    similarity: float = Field(ge=0, le=1)
    source_url: str | None = None


class ChatResponse(BaseModel):
    status: str = "success"
    persona: str = "Kanye West Lyrics Analyst"
    reply: str
    retrieved_context: str
    sources: list[Source]


class TranslateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5_000)
    target_language: str = Field(default="Turkish")


class TranslateResponse(BaseModel):
    translated_text: str


class HealthResponse(BaseModel):
    status: str
    collection_count: int
    ollama_model: str
    ollama_available: bool
