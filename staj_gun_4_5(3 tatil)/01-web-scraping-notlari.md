# Web Scraping Notları

Web scraping hakkında araştırdıklarımı ve öğrendiklerimi topladım.

---

## Web Scraping Nedir?

Kısaca bir web sitesindeki verileri kod yazarak otomatik şekilde çekme işi.
Normalde biz tarayıcıda bir sayfayı açıp gözümüzle okuyoruz, scraping'de ise
bir script aynı sayfayı indirip HTML'ini parçalara ayırıyor ve içinden istediğimiz
bilgiyi alıyor.

### Nerelerde kullanılıyor?

- Fiyat karşılaştırma (e-ticaret sitelerinden ürün fiyatlarını çekip kıyaslamak)
- Haber/içerik toplama (farklı kaynaklardan haberleri bir yere toplamak)
- Araştırma amaçlı veri seti oluşturma (akademik veya pazar araştırması)
- Değişiklik takibi (bir ürünün fiyatı düştüğünde bildirim alma gibi)
- Makine öğrenmesi için veri toplamak

### Scraping mi API mi?

Eğer bir site zaten API sunuyorsa (mesela hava durumu siteleri, GitHub vs.) o zaman
scraping'e gerek yok, direkt API'yi kullanmak hem daha güvenilir hem daha kolay.
Scraping daha çok API olmadığında veya API'nin kısıtlı/ücretli olduğu durumlarda devreye giriyor.

---

## Yasal ve Etik Tarafı

Bu kısmı özellikle araştırdım çünkü bilinçsizce yapılırsa yasal sorun çıkabilir.

### robots.txt

Her sitenin kök dizininde bir `robots.txt` dosyası var (mesela `https://google.com/robots.txt`).
Bu dosya aslında "şu sayfaları taramayın, şu sayfalar serbest" diyen bir rehber.

Örnek:
```
User-agent: *
Disallow: /private/
Disallow: /admin/
Crawl-delay: 10
```

Burada diyor ki: tüm botlar için `/private/` ve `/admin/` yasak, ayrıca istekler arası
en az 10 saniye bekleyin. Teknik olarak zorlayıcı bir şey değil ama uyulması gereken
bir görgü kuralı gibi düşünülebilir. Uymazsanız yasal sıkıntıya girebilirsiniz.

### Dikkat edilmesi gerekenler

- **Kişisel veri çekmek** (isim, e-mail, telefon) KVKK ve GDPR kapsamında sıkıntı.
  İzin olmadan kişisel veri toplamak cezai sorumluluk doğurabilir.
- **Çoğu sitenin kullanım koşullarında (ToS)** scraping yasaklanmış, bunu ihlal etmek
  sözleşme ihlali sayılabilir.
- **Sunucuyu yoracak kadar hızlı istek atmak** DoS saldırısı olarak değerlendirilebilir.
- **CAPTCHA bypass etmek** çoğu yerde yasadışı.
- **Login gerektiren alanları izinsiz scrape etmek** riskli bir bölge.

### Etik scraping nasıl olur?

1. robots.txt'i oku ve uy.
2. İstekler arası 1-2 saniye bekle (sunucuyu boğma).
3. User-Agent header'ı ile kendini tanımla.
4. Sadece ihtiyacın olan veriyi çek, tüm siteyi indirme.
5. Kişisel verilere dokunma.
6. API varsa API kullan.

---

## Statik vs Dinamik Siteler

Bu ayrımı anlamak önemli çünkü kullanacağımız yöntemi doğrudan belirliyor.

### Statik site

Sunucu isteğe karşılık hazır HTML döner, tüm veri HTML'in içinde zaten var.
Tarayıcıda Ctrl+U yapınca (sayfa kaynağını görüntüle) istediğin veriyi orada görebilirsin.

Bu tür sitelere `requests` + `BeautifulSoup` ile erişmek yeterli. Hızlı ve basit.

Örnekler: Wikipedia, basit blog siteleri, Books to Scrape.

### Dinamik site

Sunucu önce neredeyse boş bir HTML iskeleti + JavaScript gönderir.
Asıl içerik JavaScript çalıştıktan sonra (AJAX/fetch ile) yüklenir.
Ctrl+U yapınca içerik görünmez ama F12 ile Elements sekmesinde görünür.

Bu tür siteler için `Selenium` veya `Playwright` gibi bir tarayıcı otomasyon aracı lazım
çünkü bunlar gerçek tarayıcı açıp JS'yi çalıştırabiliyorlar. Ya da arka plandaki API'yi
bulup direkt onu çağırabilirsin (API reverse engineering).

Örnekler: React/Vue/Angular ile yapılmış siteler, infinite scroll olan sayfalar.

### Nasıl anlarsın?

1. Sayfada sağ tık → "Sayfa Kaynağını Görüntüle"
2. Çekmek istediğin veri orada mı bak.
   - Varsa → Statik → `requests + BS4` yeterli.
   - Yoksa → Dinamik → `Selenium/Playwright` gerekir ya da API reverse engineering.

| | Statik | Dinamik |
|---|--------|---------|
| Veri HTML'de mi? | Evet | Hayır, JS yüklüyor |
| requests yeterli mi? | Evet | Hayır |
| Hız | Çok hızlı | Yavaş (tarayıcı açılıyor) |
| Kaynak tüketimi | Düşük | Yüksek (RAM, CPU) |

---

## HTTP Temelleri

Scraping'in altında HTTP var. Bilmem gereken şeyleri topladım.

### İstek metotları

- **GET** — Veri almak için. Scraping'de en çok bu kullanılıyor, sayfayı çekmek için.
- **POST** — Veri göndermek için. Form submit etme, arama sorgusu gönderme gibi.
- **PUT / DELETE** — Güncelleme ve silme, scraping'de pek kullanılmıyor.
- **HEAD** — Sadece header bilgisini almak, dosya boyutu kontrolü falan.

### Durum kodları (Status codes)

Sunucunun "ne oldu" cevabı. Bunları bilmek şart çünkü bir şey ters gittiğinde
hatayı anlamak lazım.

| Kod | Anlamı | Ne yapmalı |
|-----|--------|-----------|
| 200 | Başarılı | Veri geldi, parse et |
| 301/302 | Yönlendirme | requests otomatik takip ediyor |
| 403 | Erişim engellendi | Header'ları kontrol et, user-agent ekle |
| 404 | Sayfa bulunamadı | URL yanlış olabilir |
| 429 | Çok fazla istek | Yavaşla, bekle, rate limit aşılmış |
| 500 | Sunucu hatası | Tekrar dene |

### Headers

Her HTTP isteğiyle beraber header'lar gidiyor. Scraping'de en önemlileri:

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8",
    "Referer": "https://www.google.com/"
}
```

- **User-Agent:** Hangi tarayıcı olduğumuzu söylüyor. Varsayılan `python-requests`
  yazıyorsa çoğu site engelliyor, gerçek bir Chrome user-agent'ı koymak lazım.
- **Referer:** Nereden geldiğimizi gösteriyor, bazı siteler bunu kontrol ediyor.
- **Cookie:** Oturum bilgisi taşıyor, login gereken sayfalarda gerekli.

### Session kullanımı

```python
import requests

session = requests.Session()
session.get("https://example.com")          # cookie'ler kaydedilir
response = session.get("https://example.com/data")  # cookie'ler otomatik gider
```

Session nesnesi cookie'leri otomatik taşıdığı için birden fazla istekte tutarlılık sağlıyor.

### URL yapısı

```
https://www.example.com/products/search?q=laptop&page=2&sort=price
         │                    │                │
         domain               path             query parameters
```

Query parametreleri önemli — arama sonuçlarını, sayfa numaralarını, filtreleri
bunlarla kontrol ediyoruz. Mesela `page=1`, `page=2` diye giderek tüm sayfalardaki
veriyi çekebiliriz (pagination).

---

## Anti-Scraping Mekanizmaları

Siteler botları engellemek için çeşitli yöntemler kullanıyor. Hem bunları bilip
etik davranmak hem de karşılaştığımda ne olduğunu anlamak için araştırdım.

### User-Agent kontrolü

En basit koruma. Sunucu gelen isteğin User-Agent'ına bakıyor, `python-requests`
gibi bot imzası görürse engelliyor.

Çözüm: Gerçek tarayıcı user-agent'ı göndermek.

### IP bazlı rate limiting / banlama

Aynı IP'den çok hızlı istek gelirse 429 döner veya IP'yi tamamen engeller.

Çözüm: İstekler arası `time.sleep()` koymak, rastgele bekleme süresi kullanmak.
İleri seviye: proxy rotasyonu (farklı IP'lerden istek).

### CAPTCHA

"Ben robot değilim" doğrulaması. Bunu programatik çözmek hem zor hem çoğu durumda
yasadışı. Site CAPTCHA koymuşsa "scraping istemiyorum" demiş oluyor.

### JavaScript challenge

Sayfa yüklenmeden önce JS çalıştırılıyor. `requests` JS çalıştıramadığı için
sayfaya erişemiyor. Selenium/Playwright gibi gerçek tarayıcı kullanan araçlar lazım.

### Cloudflare koruması

Browser fingerprinting, JS challenge, CAPTCHA karışımı profesyonel bir koruma.
Bunu aşmak çok zor ve etik olarak da tartışmalı. Genelde bu seviyede koruma varsa
o siteyi scrape etmememiz gerektiğini anlıyorum.

### Honeypot tuzakları

Sayfada CSS ile gizlenmiş linkler konuyor (display: none). İnsan görmez ama bot
tüm linkleri takip eder. O linke giden bot tespit edilip engelleniyor.

Çözüm: Parse ederken sadece görünür elementleri seçmek.

---

## Yöntemler — Genel Karşılaştırma

| Yöntem | Araç | Ne Zaman | Artısı | Eksisi |
|--------|------|----------|--------|--------|
| HTML Parse | requests + BS4 | Statik siteler | Hızlı, basit | JS içerik çekemez |
| Tarayıcı Otomasyon | Selenium / Playwright | Dinamik siteler | Her şeyi çeker | Yavaş, ağır |
| Framework | Scrapy | Büyük çaplı işler | Hızlı, async | Öğrenmesi zor |
| API Reverse Eng. | requests + DevTools | API kullanan siteler | En temiz veri | Her yerde olmaz |

### Hangisini ne zaman kullanayım?

> **🔍 Veri çekmek istiyorum**
>
> **1)** Site resmi API sunuyor mu?
> - ✅ Evet → **API kullan** (requests ile JSON çek)
> - ❌ Hayır → 2. adıma geç
>
> **2)** Ctrl+U'da (sayfa kaynağı) veri görünüyor mu?
> - ✅ Evet → **requests + BeautifulSoup**
> - ❌ Hayır → 3. adıma geç
>
> **3)** DevTools Network sekmesinde API çağrısı var mı?
> - ✅ Evet → **API Reverse Engineering** (requests ile o endpoint'i çağır)
> - ❌ Hayır → 4. adıma geç
>
> **4)** JavaScript render gerekiyor →  **Selenium / Playwright**

---

## Kullanılacak Kütüphaneler

| Kütüphane | Ne işe yarıyor | Kurulum |
|-----------|---------------|---------|
| `requests` | HTTP istekleri göndermek | `pip install requests` |
| `beautifulsoup4` | HTML parse etmek | `pip install beautifulsoup4` |
| `lxml` | Hızlı HTML parser (BS4 ile beraber) | `pip install lxml` |
| `selenium` | Tarayıcı otomasyonu | `pip install selenium` |
| `playwright` | Modern tarayıcı otomasyonu | `pip install playwright` sonra `playwright install` |
| `scrapy` | Scraping framework | `pip install scrapy` |
| `httpx` | Async HTTP client | `pip install httpx` |
| `pandas` | Veriyi CSV/JSON'a kaydetmek | `pip install pandas` |

---

## Genel iş akışı

1. Hedef belirle — hangi siteden, hangi veriyi çekeceğim?
2. Siteyi incele — robots.txt oku, yapıya bak, statik mi dinamik mi anla.
3. Yöntem seç — yukarıdaki karar ağacına göre.
4. Tek sayfa için çalışan bir script yaz.
5. Genişlet — pagination ekle, hata yönetimi koy.
6. Veriyi kaydet — JSON, CSV veya veritabanına yaz.
7. Temizlik — çekilen veriyi düzenle, gereksizleri at.
