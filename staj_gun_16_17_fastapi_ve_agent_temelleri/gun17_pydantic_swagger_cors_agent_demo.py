"""
Gün 17 - Pydantic Validation, CORS, Custom Swagger & AI Agent Demo Betiği
Çalıştırmak için:
    uvicorn gun17_pydantic_swagger_cors_agent_demo:app --reload
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional
import asyncio
import time

# 1. FastAPI Uygulama Nesnesi (Swagger UI Özelleştirilmiş)
app = FastAPI(
    title="Gün 17 - Pydantic, CORS & AI Agent API",
    description="""
    Bu API, Gün 17 ders müfredatı kapsamında geliştirilmiştir.
    
    ### Özellikler:
    * **Pydantic Validation:** Tip kontrolleri, e-posta formatı, sayı kısıtlamaları.
    * **CORS:** Frontend uygulamaları için güvenli izin yapılandırması.
    * **Response Model:** Şifre gibi hassas verilerin yanıttan gizlenmesi.
    * **AI Agent Endpoint:** Akışlı (Streaming) LLM cevabı simülasyonu.
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 2. CORS (Cross-Origin Resource Sharing) Yapılandırması
origins = [
    "http://localhost:3000",      # React / Next.js yerel sunucu
    "http://127.0.0.1:5500",      # VS Code Live Server
    "http://localhost:8080",      # Vue / Angular dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Pydantic Modelleri (Gelen İstek & Giden Yanıt)
# ---------------------------------------------------------

# Gelen İstek Modeli (Şifre içerir)
class KullaniciKayitInput(BaseModel):
    kullanici_adi: str = Field(..., min_length=3, max_length=20, description="3-20 karakter arası kullanıcı adı")
    eposta: EmailStr = Field(..., description="Geçerli bir e-posta adresi")
    parola: str = Field(..., min_length=6, description="En az 6 karakterli parola")
    yas: int = Field(..., ge=18, le=100, description="Kullanıcı yaşı 18 ile 100 arasında olmalıdır")

    @field_validator("kullanici_adi")
    @classmethod
    def kullanici_adi_alphanumeric_olmali(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Kullanıcı adı sadece harf ve rakamlardan oluşabilir!")
        return v

# Giden Yanıt Modeli (Şifre İÇERMEZ)
class KullaniciKayitOutput(BaseModel):
    user_id: int
    kullanici_adi: str
    eposta: EmailStr
    kayit_zamani: float


# ---------------------------------------------------------
# AI Agent Modelleri
# ---------------------------------------------------------
class AgentTaskRequest(BaseModel):
    agent_id: str = Field(..., description="Tetiklenecek Yapay Zeka Ajanının ID'si")
    prompt: str = Field(..., min_length=5, description="Ajana verilecek görev veya soru")
    max_tokens: int = Field(default=512, ge=64, le=4096)


# ---------------------------------------------------------
# Endpointler
# ---------------------------------------------------------

@app.post(
    "/auth/kayit/", 
    response_model=KullaniciKayitOutput,
    status_code=status.HTTP_201_CREATED,
    tags=["Kullanıcı Yönetimi"],
    summary="Pydantic Doğrulamalı Kullanıcı Kaydı"
)
def kullanici_kayit(veri: KullaniciKayitInput):
    """
    Gelen JSON verisini Pydantic ile doğrular.
    Parolayı veritabanına kaydeder fakat `response_model` sayesinde yanıt JSON'ına dahil etmez.
    """
    yeni_user = {
        "user_id": 999,
        "kullanici_adi": veri.kullanici_adi,
        "eposta": veri.eposta,
        "parola": veri.parola,  # Filtrelenecek
        "kayit_zamani": time.time()
    }
    return yeni_user


async def llm_agent_stream_generator(prompt: str):
    """LLM Yanıt Akış Simülatörü (Server-Sent Events)"""
    tokens = [
        "Ajan", "analizini", "başlattı.", "İşleniyor...", 
        "Sonuç:", f"'{prompt}'", "görevi", "başarıyla", "tamamlandı."
    ]
    for token in tokens:
        yield f"data: {token}\n\n"
        await asyncio.sleep(0.4)

@app.post(
    "/agent/run/", 
    tags=["Yapay Zeka Ajanı"],
    summary="AI Ajanına Görev Gönder ve Akışlı Yanıt Al"
)
async def ai_agent_calistir(req: AgentTaskRequest):
    """
    Yapay Zeka Ajanına görev gönderir ve yanıtı canlı Streaming (Akış) olarak döndürür.
    """
    return StreamingResponse(
        llm_agent_stream_generator(req.prompt),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("gun17_pydantic_swagger_cors_agent_demo:app", host="127.0.0.1", port=8000, reload=True)
