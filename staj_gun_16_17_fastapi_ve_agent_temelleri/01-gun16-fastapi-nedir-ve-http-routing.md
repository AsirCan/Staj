# Gün 16 - FastAPI Temelleri: Nedir, Ne İşe Yarar, Kıyaslama ve HTTP Routing

Bu ders notu, staj programının **16. Gün** çalışması kapsamında **FastAPI** framework'ünü sıfırdan, en temel kavramlarından başlayarak derinlemesine ve öğretici bir dille anlatmak amacıyla hazırlanmıştır.

---

## 1. FastAPI Nedir ve Ne İşe Yarar?

### API ve Backend Kavramı
Günümüz yazılım dünyasında istemciler (Web tarayıcıları, Mobil uygulamalar, Yapay Zeka Ajanları veya IoT cihazları) ile veritabanları/sunucular arasındaki iletişimi sağlayan köprüye **API (Application Programming Interface)** adı verilir. **Backend** ise iş mantığının, güvenlik kontrollerinin, veritabanı işlemlerinin ve yapay zeka modellerinin çalıştığı arka plan sistemidir.

### FastAPI Doğuşu ve Felsefesi
**FastAPI**, Sebastian Ramírez tarafından geliştirilmiş, modern Python 3.8+ standartlarına (özellikle type hints - tip ipuçlarına) dayalı, yüksek performanslı bir Web framework'üdür.

FastAPI iki güçlü kütüphanenin omuzları üzerinde yükselir:
1. **Starlette:** Web yönlendirmeleri, asenkron (`async/await`) işlemler ve yüksek hızlı HTTP sunucu mantığı için.
2. **Pydantic:** Veri doğrulama, veri serileştirme ve tip kontrolleri için.

```
+---------------------------------------------------------+
|                        FastAPI                          |
+---------------------------------------------------------+
|   Starlette (Web / ASGI)  |   Pydantic (Veri / Tip)     |
+---------------------------+-----------------------------+
|                     Python 3.8+ Type Hints             |
+---------------------------------------------------------+
```

### FastAPI'nin Öne Çıkan Ana Özellikleri

1. **Yüksek Performans (Speed):** Python ekosistemindeki en hızlı web framework'lerinden biridir. Asenkron (ASGI) mimarisi sayesinde Node.js ve Go ile kıyaslanabilir performans sunar.
2. **Hızlı Kod Geliştirme (Fast to Code):** Özellik geliştirme hızını %200 ila %300 oranında artırır.
3. **Daha Az Hata (Fewer Bugs):** Geliştirici hatalarını yaklaşık %40 oranında azaltır. Otomatik tip kontrolleri sayesinde yanlış veri formatları anında yakalanır.
4. **Otomatik Dokümantasyon:** Kodunuzu yazarken ek hiçbir çaba harcamadan `/docs` adresinde **Swagger UI** ve `/redoc` adresinde **ReDoc** arayüzlerini otomatik olarak üretir.
5. **Yapay Zeka ve LLM Uyumu:** Async yapısı ve Pydantic veri modelleri sayesinde LangChain, LlamaIndex, PyTorch ve OpenAI entegrasyonlarında sıkça tercih edilir.

> 💡 **Benzetme:**  
> FastAPI'yi bir restorandaki **garsona** benzetebiliriz. Müşteri (Frontend veya AI Agent) masaya oturduğunda, garson menüyü (Swagger Docs) sunar. Sipariş verildiğinde verilerin doğruluğunu (Pydantic) kapıda kontrol eder; hatalı siparişi mutfağa sokmadan reddeder. Mutfak (Backend / AI Modeli) çalışırken garson diğer masalara asenkron olarak bakmaya devam eder.

---

## 2. FastAPI'nin Diğer Backend Framework'leri ile Karşılaştırılması

Doğru framework'ü seçmek projenin gidişatını belirler. FastAPI'yi popüler diğer alternatiflerle kıyaslayalım:

```
+------------------+---------------+---------------+--------------------+------------------+------------------+------------------+
| Özellik          | FastAPI       | Flask         | Django             | Express (Node)   | Spring Boot (Java)| Go (Gin)        |
+------------------+---------------+---------------+--------------------+------------------+------------------+------------------+
| Mimari Yapı      | ASGI (Async)  | WSGI (Sync)   | WSGI/ASGI (Monolit)| Async Event Loop | Multi-Thread/Sync| Async/Goroutines |
| Veri Doğrulama   | Dahili        | Manuel / Ek   | Dahili (Forms/DRF) | Manuel / Ek      | Annotation/Dahili| Manuel / Binding |
| Otomatik Docs    | Dahili        | Eklenti ile   | Eklenti ile        | Eklenti ile      | Swagger/Springdoc| Eklenti ile      |
| Performans       | Çok Yüksek    | Orta          | Orta               | Yüksek           | Yüksek (Memory Y.)| Aşırı Yüksek     |
| AI/LLM Entegr.   | Çok İyi       | İyi           | Orta               | Zayıf (Python D.)| Zayıf (Python D.)| Orta (SDK Var)   |
| Öğrenme Eğrisi   | Kolay         | Çok Kolay     | Orta-Zor           | Kolay-Orta       | Zor / Verbose    | Orta             |
+------------------+---------------+---------------+--------------------+------------------+------------------+------------------+
```

### A. FastAPI vs. Flask
* **Flask:** Python'ın klasik mikro-framework'üdür. Çok esnektir ancak varsayılan olarak senkrondur (WSGI). Veri doğrulama, tip kontrolü ve dokümantasyon için üçüncü taraf kütüphaneler eklemek gerekir.
* **FastAPI:** Flask'ın esnekliğini alır, üzerine dahili asenkron destek (`async/await`), otomatik Pydantic doğrulaması ve canlı Swagger dokümantasyonu ekler. Yeni projelerde Flask yerine tercih edilmektedir.

### B. FastAPI vs. Django (ve Django REST Framework)
* **Django:** "Batteries-included" (Her şey dahil) felsefesine sahiptir. Dahili ORM, Admin Paneli, Kullanıcı Yetkilendirme ve Template motoru barındıran devasa monolitik bir sistemdir.
* **FastAPI:** Ağır monolitik yapılardan uzak, hafif ve yüksek hızlı microservice (mikroservis) veya REST API ihtiyaçları için tasarlanmıştır. Veritabanı yönetimini yazılımcının özgürlüğüne (SQLAlchemy, SQLModel, Tortoise ORM vb.) bırakır.

### C. FastAPI vs. Express.js (Node.js)
* **Express.js:** JavaScript ekosisteminin asenkron kralıdır. Yüksek eşzamanlılık sunar.
* **FastAPI:** Python'ın yapay zeka, veri bilimi ve makine öğrenimi kütüphaneleri (PyTorch, TensorFlow, Pandas, NumPy) ile doğrudan aynı çalışma ortamında entegre olabilme avantajına sahiptir. Ayrıca TypeScript olmadan pure Python ile tip güvenliği sağlar.

### D. FastAPI vs. Spring Boot (Java)
* **Spring Boot:** Kurumsal (Enterprise) dünyada standartlaşmış, devasa kütüphane ekosistemine ve strict tip güvenliğine sahip Java framework'üdür.
* **FastAPI:** Spring Boot'a kıyasla daha az boilerplate (basmakalıp) kod gerektirir. Daha hızlı ayağa kalkar, bellek tüketimi düşüktür ve Python ekosistemi sayesinde AI/LLM ajan entegrasyonu daha kolaydır.

### E. FastAPI vs. Go (Gin / Fiber)
* **Go (Gin):** Derlenen bir dil olduğu için mikrosaniye seviyesinde yüksek işlem gücü ve düşük bellek kullanımı sunar.
* **FastAPI:** Saf işlemci (CPU) performansında Go daha önde olsa da, FastAPI Python'ın yapay zeka kütüphaneleriyle doğrudan çalışabilmesi, Pydantic doğrulama kolaylığı ve otomatik dokümantasyon desteğiyle AI/LLM backend projelerinde daha pratik bir seçenektir.

---

## 3. İlk FastAPI Uygulaması ve Çalıştırma Mekanizması

FastAPI uygulamalarını çalıştırmak için **ASGI sunucusuna** ihtiyaç duyulur. En popüler ASGI sunucusu **Uvicorn**'dur.

### Kurulum:
```bash
pip install fastapi uvicorn
```

### Kod Örneği (`main.py`):
```python
from fastapi import FastAPI

# 1. Uygulama nesnesini oluşturuyoruz
app = FastAPI(
    title="Staj FastAPI Öğretici Rehberi",
    description="Gün 16 - FastAPI Temel Endpoint Örneği",
    version="1.0.0"
)

# 2. Kök köprü / endpoint tanımlama
@app.get("/")
def ana_sayfa():
    return {
        "mesaj": "FastAPI dünyasına hoş geldiniz!",
        "durum": "Aktif",
        "gun": 16
    }
```

### Uygulamayı Çalıştırma:
```bash
uvicorn main:app --reload
```
* `main`: Python dosyasının adı (`main.py`).
* `app`: Dosya içerisindeki `FastAPI()` nesnesi.
* `--reload`: Kodda değişiklik yapıldığında sunucunun otomatik olarak kendini yeniden başlatmasını sağlar.

---

## 4. HTTP Metotları & Routing (Yönlendirme)

HTTP (Hypertext Transfer Protocol), istemci ile sunucu arasındaki iletişim kurallarını belirler. **Routing (Yönlendirme)** ise istemcinin çağırdığı URL adresine göre hangi Python fonksiyonunun çalışacağını belirleme işlemidir.

```
İstemci (Client) ---- HTTP GET /items/5 ---> FastAPI Router
                 <--- 200 OK JSON ---------  Fonksiyon Çıktısı
```

### A. HTTP Metotları (Veri Operasyonları)

* **GET:** Sunucudan veri okumak/listelemek için kullanılır. Sunucuda durum değişikliği yapmaz.
* **POST:** Sunucuya yeni bir kaynak eklemek/yaratmak için kullanılır.
* **PUT:** Var olan bir kaynağı tamamen güncellemek için kullanılır.
* **DELETE:** Sunucudaki bir kaynağı silmek için kullanılır.

---

### B. `@app.get()` ve `@app.post()` Arasındaki Temel Farklar

| Özellik | `@app.get()` | `@app.post()` |
| :--- | :--- | :--- |
| **Amacı** | Veri Okuma / Sorgulama | Veri Oluşturma / Gönderme |
| **Veri Taşıma Yeri** | URL (Query / Path parametreleri) | Request Body (JSON gövdesi) |
| **Güvenlik** | Düşük (URL tarayıcı geçmişinde saklanır) | Yüksek (Veri gövdede gizlidir) |
| **Veri Boyutu** | Sınırlı (URL uzunluk sınırı var) | Sınırsız (JSON gövdesi büyüktür) |
| **Tarayıcı Önbelleği** | Önbelleklenebilir (Cache edilebilir) | Önbelleklenemez |

---

### C. Path Parameters (Yol Parametreleri)

URL yolunun bir parçası olan dinamik değişkenlerdir.

```python
@app.get("/kullanicilar/{kullanici_id}")
def kullanici_detay(kullanici_id: int):
    # Tip tanımı 'int' olduğu için FastAPI otomatik olarak string'i int'e dönüştürür.
    return {
        "kullanici_id": kullanici_id,
        "bilgi": f"{kullanici_id} ID'li kullanıcının profili."
    }
```
Örnek Çağrı: `GET http://127.0.0.1:8000/kullanicilar/42`

---

### D. Query Parameters (Sorgu Parametreleri)

URL sonuna `?` işareti koyularak eklenen anahtar-değer çiftleridir. Yönlendirme yolunda tanımlanmayan fakat fonksiyona parametre olarak eklenen değişkenler otomatik olarak Query Parametresi kabul edilir.

```python
@app.get("/urunler/")
def urun_listele(kategori: str = "genel", limit: int = 10, aktif_mi: bool = True):
    return {
        "secilen_kategori": kategori,
        "getirilen_adet": limit,
        "durum_filtresi": aktif_mi
    }
```
Örnek Çağrı: `GET http://127.0.0.1:8000/urunler/?kategori=elektronik&limit=5`

---

### E. Explicity POST İsteği Örneği

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GorevModeli(BaseModel):
    baslik: str
    aciklama: str
    tamamlandi: bool = False

@app.post("/gorevler/", status_code=201)
def yeni_gorev_olustur(gorev: GorevModeli):
    # 'gorev' verisi HTTP Request Body içerisinden JSON olarak gelir
    return {
        "durum": "Başarılı",
        "olusturulan_gorev": gorev
    }
```

---

## 5. Gün 16 Özeti ve Değerlendirme

1. **FastAPI**, Starlette ve Pydantic sayesinde hem yüksek performanslı hem de geliştirici dostudur.
2. **Flask** ve **Django**'ya kıyasla modern asenkron mimarisi, otomatik Swagger dokümantasyonu ve dahili Pydantic tipi doğrulama mekanizmasıyla ayrışır.
3. **HTTP Metotlarında** GET sadece okuma amacıyla URL üzerinden parametre taşırken; POST veriyi güvenli şekilde HTTP gövdesinde (Request Body) göndererek yeni kaynak yaratır.
4. **FastAPI**, yapay zeka projelerinde ve LLM agent uygulamalarında yaygın olarak kullanılan bir backend framework'üdür.
