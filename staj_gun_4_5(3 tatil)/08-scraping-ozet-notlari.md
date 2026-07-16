# Web Scraping Özet ve Karşılaştırma Notlarım

Bu iki gün boyunca farklı web scraping yöntemlerini, kütüphanelerini ve framework'lerini araştırıp denedim. Hangi yöntemin hangi senaryoda en iyi çalıştığını, karşılaştığım temel problemleri ve çözümlerini buraya özet olarak çıkarttım.

---

## 🛠️ Yöntemlerin Karşılaştırması

Denediğim 4 temel yöntemin (BS4, Selenium, Scrapy, API Reverse Eng.) artı ve eksileri:

| Yöntem | Hız | Geliştirme Kolaylığı | Güvenilirlik / Sağlamlık | En İyi Kullanım Yeri |
| :--- | :--- | :--- | :--- | :--- |
| **requests + BS4** | ⚡ Hızlı | Simple | ⚠️ Tasarım değişirse kırılır | Statik sayfalar, küçük/orta ölçekli projeler |
| **Selenium** | 🐌 Yavaş | Orta | ⚠️ Ağ yavaşlığına duyarlı | Bol JS render içeren, giriş/tıklama gerektiren siteler |
| **Scrapy** | 🚀 Çok Hızlı | Hard | 🛡️ Yüksek (Pipeline mimarisi) | Büyük ölçekli crawling işleri, veri boru hatları (pipeline) |
| **API Reverse Eng.** | 🏎️ En Hızlı | Kolay (Bulunca) | 💎 Çok Yüksek (JSON formatı sabit kalır) | Arka planda JSON API kullanan her türlü site |

---

## 🧭 Web Scraping Karar Ağacı

Bir siteden veri çekmek istediğimde izleyeceğim yol haritası:

1. **Sitede açık veya gizli bir API var mı?**
   - **Evet:** `requests` ile doğrudan API endpoint'ini çağır (Reverse Engineering). HTML parse etmekle uğraşma.
   - **Hayır:** Adım 2'ye geç.

2. **Sayfa kaynağında (Ctrl+U) veri görünüyor mu?**
   - **Evet (Statik Site):** `requests` + `BeautifulSoup` kullan veya yüksek performans gerekiyorsa `httpx` + `selectolax` ikilisini seç.
   - **Hayır (Dinamik Site):** Adım 3'ye geç.

3. **Veri tarayıcıda scroll yapınca mı yoksa tıklayınca mı geliyor?**
   - **Scroll/Click (Infinite Scroll / AJAX):** `Selenium` kullan veya istek hızını artırmak için `playwright` dene.

---

## ⚠️ Karşılaşılan Yaygın Hatalar ve Çözümleri

### 1. `403 Forbidden` veya `429 Too Many Requests` Hatası
- **Neden:** Sunucu bir bot olduğumuzu anladı ya da çok hızlı istek attığımız için bizi limitledi.
- **Çözüm:** 
  - İstek atarken header kısmına gerçek bir tarayıcı `User-Agent` bilgisi ekle.
  - İsteklerin arasına `time.sleep(1)` gibi beklemeler koy.
  - Çok büyük işlerde IP adresimizin engellenmesini önlemek için Proxy rotasyonu kullan.

### 2. `UnicodeEncodeError` (Terminalde Türkçe karakter / emoji hatası)
- **Neden:** Windows terminallerinin varsayılan karakter kodlamasının (genelde CP1254) UTF-8 karakterleri basamaması.
- **Çözüm:** Python dosyalarının en başına terminal çıktısını UTF-8'e zorlayan şu kod bloğunu ekle:
  ```python
  import sys
  import io
  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
  ```

### 3. Selenium'da Elementin Bulunamaması Hatası (`NoSuchElementException`)
- **Neden:** Sayfa henüz yüklenmeden (özellikle JS yavaş çalışıyorsa) Selenium'un elementi aramaya çalışması.
- **Çözüm:** `time.sleep()` yerine Selenium'un explicit wait (`WebDriverWait` ve `ExpectedConditions`) mekanizmasını kullan. Element sayfada belirene kadar beklesin.

---

## ⚖️ Etik ve Yasal Sınırlar

Scraping yaparken başımın ağrımaması için kendime hatırlatmalar:
- **robots.txt:** Hedef sitenin `/robots.txt` dosyasını mutlaka oku. İzin verilmeyen dizinleri tarama.
- **Sunucu Yükü:** Saniyede onlarca istek atıp sunucuyu çökertme (DoS yapma).
- **Kişisel Veri:** İsim, e-posta, telefon gibi kişisel verileri (KVKK / GDPR kapsamında) izinsiz çekip kaydetme.
- **Telif Hakları:** Ticari verileri kopyalayıp kendi sitende yayınlama, telif hakkı ihlali yapma.
