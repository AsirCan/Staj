# Farklı Site ve Kaynak Denemeleri

Bu klasörde, öğrendiğim farklı scraping yöntemlerini (BS4, API vs.) test etmek için 5 farklı site/kaynak üzerinde denemeler yaptım.

## Denenen Siteler ve Amaçları

1. **Scrape This Site - Ülkeler:**
   - **Yöntem:** `BeautifulSoup` + `requests`
   - **Amaç:** Klasik HTML parse etme yöntemiyle grid/kart yapısındaki verileri çekmek.
   - **Sonuç:** [scrapethissite_ulkeler.json](veriler/scrapethissite_ulkeler.json) (250 ülke verisi).

2. **HTTPBin - İstek Testleri:**
   - **Yöntem:** `requests`
   - **Amaç:** Sunucuya giden header'lar, cookie'ler, kendi IP adresimiz ve delay/gecikme durumlarının response üzerindeki etkilerini anlamak.
   - **Sonuç:** [httpbin_test.json](veriler/httpbin_test.json)

3. **Wikipedia - Programlama Dilleri Listesi:**
   - **Yöntem:** `BeautifulSoup` + `requests`
   - **Amaç:** Gerçek dünya sitelerindeki karmaşık HTML listelerini temiz bir şekilde çekmek.
   - **Sonuç:** [wikipedia_programlama_dilleri.json](veriler/wikipedia_programlama_dilleri.json) (672 dil verisi).

4. **GitHub Trending:**
   - **Yöntem:** `BeautifulSoup` + `requests`
   - **Amaç:** Her gün güncellenen dinamik ve gerçek bir web sayfasını scrape etmek.
   - **Sonuç:** [github_trending.json](veriler/github_trending.json) (Trend olan repolar ve dilleri).

5. **JSONPlaceholder (REST API):**
   - **Yöntem:** `requests` (GET & POST)
   - **Amaç:** API endpoint'leri üzerinden veri okuma (GET) ve veri gönderme (POST) simülasyonları yapmak.
   - **Sonuç:** [jsonplaceholder_posts.json](veriler/jsonplaceholder_posts.json) ve [jsonplaceholder_users.json](veriler/jsonplaceholder_users.json).

## Çalıştırma

Deneme scriptini çalıştırmak için:
```bash
python site_denemeleri.py
```
Çekilen tüm veriler otomatik olarak `veriler/` klasörünün altına kaydedilir.
