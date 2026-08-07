from fastapi.testclient import TestClient

from app.main import app
from app.schemas import ChatResponse, HealthResponse, Source


class FakeService:
    def health(self) -> HealthResponse:
        return HealthResponse(status="healthy", collection_count=12, ollama_model="fake", ollama_available=True)

    def chat(self, _message: str) -> ChatResponse:
        return ChatResponse(
            reply="Tematik yorum.",
            retrieved_context="Retrieved song passages: Runaway",
            sources=[Source(song="Runaway", album="MBDTF", year=2010, similarity=0.91)],
        )


def setup_function() -> None:
    app.state.chat_service = FakeService()


def teardown_function() -> None:
    app.state.chat_service = None


def test_chat_endpoint_returns_documented_schema() -> None:
    response = TestClient(app).post("/api/v1/chat", json={"user_id": "test", "message": "What is the theme?"})

    assert response.status_code == 200
    assert response.json()["sources"][0]["song"] == "Runaway"


def test_empty_message_is_rejected() -> None:
    response = TestClient(app).post("/api/v1/chat", json={"user_id": "test", "message": ""})

    assert response.status_code == 422


def test_whitespace_only_message_is_rejected() -> None:
    response = TestClient(app).post("/api/v1/chat", json={"user_id": "test", "message": "   "})

    assert response.status_code == 422


def test_health_endpoint_uses_service() -> None:
    response = TestClient(app).get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["collection_count"] == 12
