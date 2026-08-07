"""FastAPI giris noktasi. Swagger: /docs"""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ChatRequest, ChatResponse, HealthResponse, TranslateRequest, TranslateResponse
from app.service import ChatService, EmptyIndexError, OllamaUnavailableError


app = FastAPI(
    title="Kanye West RAG Persona Chatbot API",
    version="1.0.0",
    description="Yerel Ollama + ChromaDB ile sarki sozu temelli RAG chatbot.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.chat_service = None


def get_service(request: Request) -> ChatService:
    if request.app.state.chat_service is None:
        request.app.state.chat_service = ChatService()
    return request.app.state.chat_service


@app.get("/api/v1/health", response_model=HealthResponse, tags=["system"])
def health(service: ChatService = Depends(get_service)) -> HealthResponse:
    return service.health()


@app.post("/api/v1/chat", response_model=ChatResponse, tags=["chat"])
def chat(payload: ChatRequest, service: ChatService = Depends(get_service)) -> ChatResponse:
    try:
        return service.chat(payload.message)
    except EmptyIndexError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except OllamaUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/api/v1/translate", response_model=TranslateResponse, tags=["chat"])
def translate(payload: TranslateRequest, service: ChatService = Depends(get_service)) -> TranslateResponse:
    try:
        translated = service.translate(payload.text, payload.target_language)
        return TranslateResponse(translated_text=translated)
    except OllamaUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

