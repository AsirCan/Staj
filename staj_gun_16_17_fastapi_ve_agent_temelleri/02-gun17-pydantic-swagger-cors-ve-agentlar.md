# Gün 17 - Pydantic Veri Doğrulama, Swagger UI, CORS ve Yapay Zeka Ajanları Entegrasyonu

Bu ders notu, staj programının **17. Gün** çalışması kapsamında **Pydantic veri doğrulama mimarisi**, **Swagger UI / ReDoc dokümantasyonu**, **CORS güvenlik ayarları** ve **Yapay Zeka Ajanlarının (AI Agents) FastAPI ile entegrasyonunu** öğretici bir anlatımla ele almaktadır.

---

## 1. Pydantic ile Veri Doğrulama (Data Validation)

### Pydantic Nedir?
**Pydantic**, Python'da tip belirteçlerini (Type Hints) kullanarak veri doğrulama (validation) ve ayar yönetimi (settings management) sağlayan en popüler kütüphanedir. FastAPI, gelen HTTP isteklerini ve giden yanıtları otomatik olarak Pydantic modelleriyle doğrular.

```
İstemci JSON Gönderir ----> [ Pydantic BaseModel Kontrolü ] ----> Geçerli Veri -> Python Objesi
                                     |
                                     +---> Hatalı Veri -> 422 Unprocessable Entity (Otomatik Hata)
```

### Neden Veri Doğrulama Gereklidir?
İstemcilerden (Frontend, Mobil, AI Agent) gelen veriler çoğu zaman eksik, yanlış tipte veya zararlı olabilir. Örneğin:
* `yas` alanına kelime ("yirmi") yazılması,
* `email` alanının geçersiz olması,
* Zorunlu bir alanın JSON içinde gönderilmemesi.

Pydantic olmadan bu kontrolleri yapmak onlarca `if-else` satırı gerektirirdi. Pydantic ile tek bir sınıf tanımıyla tüm bu kontroller otomatik yapılır.

---

### A. Temel `BaseModel` ve Tip Kontrolü

```python
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class KullaniciKayitModeli(BaseModel):
    kullanici_adi: str
    eposta: EmailStr  # E-posta formatını otomatik doğrular
    yas: int
    biyografi: Optional[str] = None  # İsteğe bağlı alan
    hobi_listesi: List[str] = []
```

---

### B. `Field` Nesnesi ile Gelişmiş Kısıtlamalar ve Varsayılan Değerler

`Field` fonksiyonu; alanlara minimum/maksimum değerler, dize uzunluk kısıtlamaları, regex desenleri ve açıklama metinleri eklememizi sağlar.

```python
from pydantic import BaseModel, Field

class UrunEklemeModeli(BaseModel):
    urun_adi: str = Field(
        ..., 
        min_length=2, 
        max_length=50, 
        description="Ürünün pazardaki adı"
    )
    fiyat: float = Field(
        ..., 
        gt=0, 
        description="Fiyat sıfırdan büyük olmalıdır (gt = greater than)"
    )
    stok_adedi: int = Field(
        default=100, 
        ge=0, 
        description="Stok negatif olamaz (ge = greater than or equal)"
    )
```

---

### C. Özel Doğrulayıcılar (`@field_validator`)

Pydantic'in `@field_validator` dekoratörü ile kendi iş mantığınızı ve karmaşık kurallarınızı tanımlayabilirsiniz.

```python
from pydantic import BaseModel, field_validator

class SiparisModeli(BaseModel):
    siparis_kodu: str
    adet: int

    @field_validator("siparis_kodu")
    @classmethod
    def kod_formatini_kontrol_et(cls, deger: str) -> str:
        if not deger.startswith("SIP-"):
            raise ValueError("Sipariş kodu mutlaka 'SIP-' ile başlamalıdır!")
        return deger
```

---

### D. Gelen ve Giden JSON Verilerinin Ayrıştırılması (Response Model)

Güvenlik prensipleri gereği, istemciden alınan veri ile istemciye dönülen veri aynı olmamalıdır. Örneğin kullanıcı kayıt olurken şifre gönderir; ancak cevaptaki JSON'da şifre **asla** yer almamalıdır.

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

# Gelen İstek Modeli (Şifre içerir)
class KullaniciKayitRequest(BaseModel):
    kullanici_adi: str
    eposta: EmailStr
    parola: str

# Giden Yanıt Modeli (Şifre İÇERMEZ)
class KullaniciKayitResponse(BaseModel):
    id: int
    kullanici_adi: str
    eposta: EmailStr

@app.post("/kayit-ol/", response_model=KullaniciKayitResponse, status_code=201)
def kayit_ol(veri: KullaniciKayitRequest):
    # Veritabanına kaydetme simülasyonu
    yeni_kullanici = {
        "id": 101,
        "kullanici_adi": veri.kullanici_adi,
        "eposta": veri.eposta,
        "parola": veri.parola  # Otomatik filtrelenecek!
    }
    return yeni_kullanici  # response_model sayesinde 'parola' istemciye gitmez.
```

> 💡 **Benzetme:**  
> Pydantic, bir havaalanındaki **Pasaport Kontrol Memuru** gibi çalışır. Yolcunun (JSON verisi) kimliğini, vize süresini ve evraklarını tek tek denetler. Eksik evrak varsa yolcuyu uçağa (backend iş fonksiyonuna) almaz ve kapıda sebebiyle geri çevirir (422 hatası).

---

## 2. Swagger UI ve ReDoc: Otomatik Dokümantasyon

FastAPI, OpenAPI standartlarına tam uyumludur. Uygulamanız başladığı anda iki farklı arayüz otomatik hazırlanır:

1. **Swagger UI (`http://127.0.0.1:8000/docs`):** Interaktif API test arayüzüdür. Tarayıcı üzerinden doğrudan POST, GET, PUT istekleri atılabilir.
2. **ReDoc (`http://127.0.0.1:8000/redoc`):** Temiz, okunabilir, üretime hazır ve detaylı bir dokümantasyon sayfası sunar.

```
                       +---> /docs  (Swagger UI - İnteraktif Test)
                       |
FastAPI koda bakar --->+
                       |
                       +---> /redoc (ReDoc - Temiz Dokümantasyon)
```

### Swagger Arayüzünü Özelleştirme:
```python
from fastapi import FastAPI

app = FastAPI(
    title="Akıllı Asistan API",
    description="""
    Bu API, Yapay Zeka Ajanları için tasarlanmıştır.
    * **Veri Doğrulama:** Pydantic ile yapılmıştır.
    * **Güvenlik:** CORS korumalıdır.
    """,
    version="2.1.0",
    docs_url="/docs",      # Swagger URL'si
    redoc_url="/redoc"     # ReDoc URL'si
)

@app.get("/tahlil/", tags=["Sağlık Servisi"], summary="Kan Tahlili Analizi")
def tahlil_et():
    """
    Bu endpoint yapay zeka ajanının kan tahlili sonuçlarını analiz etmesini sağlar:
    - **Parametreler:** JSON formatında değerler.
    - **Dönüş:** Risk raporu.
    """
    return {"durum": "Normal"}
```

---

## 3. CORS (Cross-Origin Resource Sharing) Güvenlik İzinleri

### CORS Nedir?
**CORS (Çapraz Orijin Kaynak Paylaşımı)**, web tarayıcılarının uyguladığı **Same-Origin Policy (Aynı Orijin Politikası)** adlı güvenlik kuralını yöneten bir mekanizmadır.

### Orijin (Origin) Nelerden Oluşur?
Bir orijin 3 bileşenden oluşur: **Protokol + Domain + Port**
* `http://localhost:3000` (React Frontend)
* `http://localhost:8000` (FastAPI Backend)

Bu iki adres farklı portlarda çalıştığı için **Farklı Orijin (Cross-Origin)** kabul edilir. Eğer FastAPI'de CORS izni verilmezse, React uygulaması backend'e istek attığında tarayıcı isteği engeller ve konsolda şu hatayı basar:
`Access to fetch at 'http://localhost:8000/' from origin 'http://localhost:3000' has been blocked by CORS policy.`

---

### FastAPI'de `CORSMiddleware` Entegrasyonu

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# İzin verilecek istemci orijinleri listesi
origins = [
    "http://localhost:3000",      # React / Next.js yerel sunucusu
    "http://127.0.0.1:5500",      # Live Server
    "https://benim-frontend-sitem.com", # Canlıdaki web sitesi
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Belirtilen domain'lere izin ver
    allow_credentials=True,     # Cookie ve yetkilendirme başlıklarına izin ver
    allow_methods=["*"],         # Tüm HTTP metotlarına (GET, POST, PUT, DELETE vb.) izin ver
    allow_headers=["*"],         # Tüm HTTP başlıklarına (Headers) izin ver
)
```

> ⚠️ **Güvenlik Uyarısı:** Canlı ortamlarda (Production) `allow_origins=["*"]` (tüm dünyayaya açık) yapmak ciddi güvenlik risklerine yol açar. Yalnızca güvendiğiniz frontend adreslerini listeye eklemelisiniz.

> 💡 **Benzetme:**  
> CORS, sitenizin kapısındaki **Güvenlik Görevlisi** gibi çalışır. Gelen ziyaretçinin yaka kartına (Origin) bakar. Listede (allow_origins) adı yazıyorsa içeri alır, yazmıyorsa tarayıcı seviyesinde erişimi bloklar.

---

## 4. Yapay Zeka Ajanları (AI Agents) ve LLM Sistemlerinde FastAPI'nin Rolü

Yapay zeka uygulamaları (LangChain, AutoGen, CrewAI veya özel RAG mimarileri) kullanıcıyla veya harici sistemlerle iletişim kurarken bir backend katmanına ihtiyaç duyar. FastAPI bu noktada yaygın bir tercih haline geldi.

```
[ Kullanıcı / Arayüz ] <---> [ FastAPI Backend ] <---> [ LLM / AI Agent / VectorDB ]
                                  |
                        Async Streaming Response
                        Structured Tool Outputs
```

### Yapay Zeka Ajanları İçin FastAPI'nin Avantajları:

1. **Async Yapısı (`async def`):** OpenAI / Anthropic API çağrıları veya Vektör Veritabanı aramaları I/O-bound (giriş-çıkış beklemeli) işlemlerdir. Async endpointler sayesinde sunucu LLM yanıtını beklerken diğer kullanıcıların isteklerini kilitlenmeden işler.
2. **Yapılandırılmış Çıktılar (Structured Outputs):** LLM'den alınan JSON cevabı Pydantic modeline aktarılarak veri bütünlüğü garanti altına alınır.
3. **Tool Calling Endpoints:** AI Ajanının (örneğin "Hava durumunu getir", "Veritabanında ara") çağırabileceği fonksiyonlar FastAPI endpoint'i olarak dışa açılır.
4. **Streaming (Akışlı) Yanıtlar:** LLM cevaplarının ekrana kelime kelime düşmesi için `StreamingResponse` sınıfı kullanılır.

---

### Örnek Yapay Zeka Ajan Endpoint Kodu:

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import asyncio

app = FastAPI(title="AI Agent Tool & Response Service")

class AgentSoruRequest(BaseModel):
    kullanici_id: str
    soru: str = Field(..., min_length=3, description="Kullanıcının ajana sorduğu soru")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

# Simüle Edilmiş Asenkron LLM Akış Fonksiyonu
async def llm_cevap_akisi(soru: str):
    cevap_kelimeleri = f"Ajandan Cevap: '{soru}' sorusunu aldım ve derinlemesine analiz ediyorum... İşlem tamamlandı.".split()
    for kelime in cevap_kelimeleri:
        yield f"data: {kelime}\n\n"
        await asyncio.sleep(0.3)  # LLM jenerasyon simülasyonu

@app.post("/agent/soru-sor/")
async def agent_soru_cevapla(request: AgentSoruRequest):
    """
    AI Ajanına soru gönderir ve cevabı streaming (akış) formatında canlı döner.
    """
    return StreamingResponse(
        llm_cevap_akisi(request.soru), 
        media_type="text/event-stream"
    )
```

---

## 5. Gün 17 Özeti ve Değerlendirme

1. **Pydantic**, Python tiplerini kullanarak HTTP isteklerini ve yanıtlarını doğrulayan esnek ve güçlü bir kütüphanedir.
2. **Swagger UI ve ReDoc**, kod yazılırken eşzamanlı olarak üretilen interaktif API dokümantasyon araçlarıdır.
3. **CORS**, tarayıcıların farklı origin'ler arası güvenlik kısıtlamalarını yönetir ve `CORSMiddleware` ile FastAPI'ye güvenle entegre edilir.
4. **Yapay zeka ajan mimarilerinde**, FastAPI asenkron performansı, Pydantic tip güvencesi ve streaming yanıt desteğiyle öne çıkan bir backend seçeneğidir.
