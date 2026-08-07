# Gün 18–20: Kanye West RAG Persona Chatbot

Bu proje, seçilmiş Kanye West şarkı sözlerini yerel bir ChromaDB vektör veritabanında arar ve Ollama üzerindeki bir LLM ile şarkıların temalarını yorumlar. Bot sanatçıyı taklit etmez; yalnızca sözlerdeki temalar üzerine kaynak gösteren bir analiz yapar.

## Mimari

`BeautifulSoup collector -> JSONL -> chunking -> multilingual-e5-small -> ChromaDB -> top-3 retrieval -> Ollama qwen2.5:7b-instruct -> FastAPI -> Modern Monolith Dark Web UI`

## 🚀 Hızlı Kurulum & Çalıştırma (Başka Bilgisayarda)

Projeyi yeni bir bilgisayara indirdiğinizde çalıştırmak son derece kolaydır:

### 1. Yöntem: Tek Tıkla Otomatik Kurulum (Windows)
1. Bilgisayarınızda **Ollama** uygulamasının kurulu olduğundan ve arka planda açık olduğundan emin olun (`ollama pull qwen2.5:7b-instruct`).
2. Proje klasöründeki **`setup.bat`** dosyasına çift tıklayın.
   - *Bu işlem sanal ortamı (`.venv`) oluşturur, bağımlılıkları (`requirements.txt`) yükler, `.env` dosyasını oluşturur ve ChromaDB vektör veritabanını otomatik indeksler.*
3. Kurulum tamamlandıktan sonra **`run.bat`** dosyasına çift tıklayarak uygulamayı başlatın!

### 2. Yöntem: Komut Satırı (PowerShell / Terminal)
```powershell
# 1. Otomatik Kurulum Betiği:
.\setup.bat

# 2. Veya Manuel Kurulum:
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe scripts\collect_lyrics.py --confirm-permission --delay 1.0
.\.venv\Scripts\python.exe scripts\build_index.py --reset

# 3. Uygulamayı Başlatma:
.\run.bat
```

## 🌐 Çalışma Portları & Erişim

- **Kanye West Monolith Dark Web UI:** `http://127.0.0.1:8501` (veya `ui/index.html`)
- **Swagger API Dokümantasyonu:** `http://127.0.0.1:8000/docs`
- **Sağlık Kontrolü:** `http://127.0.0.1:8000/api/v1/health`

- **Kanye West Monolith Dark Web UI:** `http://127.0.0.1:8080` (veya `ui/index.html`)
- **Swagger API Dokümantasyonu:** `http://127.0.0.1:8000/docs`
- **Sağlık Kontrolü:** `http://127.0.0.1:8000/api/v1/health`

Örnek API isteği:

```json
{"user_id":"ogrenci_01", "message":"Runaway şarkısında öz eleştiri nasıl işleniyor?"}
```

## ✨ Dark Monolith Web Arayüzü Özellikleri

- **Near-Black Derinlik (#0a0a0a):** %3 opaklıkta noktasal ızgara deseni (`dot-grid`) ve katmanlı cam efektleri.
- **Canlı Durum Göstergesi:** Gerçek zamanlı ChromaDB bağlantısı ve gecikme süresini gösteren yanıp sönen yeşil durum rozeti (`CHROMADB ONLINE • 14ms`).
- **İkon-Odaklı Gezinti Çubuğu:** Aktif gösterge çizgisi içeren sol navigasyon rayı.
- **ChromaDB İndeks Gezgini (Modal):** Vektör veritabanı boyutlarını (384-D), kosinüs metriğini ve şarkı parça dağılımlarını gösteren modal ekran.
- **Persona & Tema İlişki Grafiği (Modal):** İnanç, Kırılganlık, Aile Sorumluluğu ve Ego temalarını haritalandıran interaktif bilgi grafiği.
- **Komut Paleti Girdisi:** Odaklanma ışıması (`inner glow`), klavye ipuçları ve Türkçe çeviri seçeneği (`Türkçe'ye Çevir`).

## Test

```powershell
.\.venv\Scripts\python.exe -m pytest -o pythonpath=.python-packages
```

Testler chunking sınırlarını, collector HTML ayrıştırmasını, FastAPI şemasını ve boş mesaj doğrulamasını kontrol eder. Canlı Ollama veya gerçek şarkı sözü verisi gerektirmez (`14 passed`).

## Rapor ve Ekran Görüntüleri

`rapor/rapor.md` güncellenmiş ve aşağıdaki görseller `rapor/screenshots/` klasörüne eklenmiştir:

- `rapor/screenshots/swagger-docs.png` — Canlı Swagger API testi.
- `rapor/screenshots/scenario-1-theme.png` — Tema analizi ekran görüntüsü.
- `rapor/screenshots/scenario-2-song-search.png` — Şarkı arama ve kaynak eşleştirme.
- `rapor/screenshots/scenario-3-no-context.png` — Güvenli bağlam dışı durum.
