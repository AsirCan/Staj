# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""
07 - Farkli Site & Kaynak Denemeleri

Daha once ogrendigimiz yontemleri farkli site ve kaynaklarda deniyoruz.
Her denemede: hedef site, kullanilan yontem, cekilen veri turu not ediliyor.

Denenen Siteler:
  1) Scrape This Site - Ulkeler     (BS4, tablo parse)
  2) HTTPBin                         (requests, header/cookie/IP analizi)
  3) Wikipedia - Programlama Dilleri (BS4, tablo scraping)
  4) GitHub Trending                 (BS4, gercek dunya sitesi)
  5) JSONPlaceholder                 (API, fake REST endpoint)
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time


def save_json(data, filename):
    """Cekilen veriyi module ozel veriler klasorune kaydet."""
    out_dir = os.path.join(os.path.dirname(__file__), "veriler")
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> {len(data)} kayit '{filepath}' dosyasina kaydedildi.\n")


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


# ===================================================================
# DENEME 1: Scrape This Site - Ulkeler Tablosu
# ===================================================================
# Site: https://www.scrapethissite.com/pages/simple/
# Yontem: requests + BS4
# Zorluk: Kolay-Orta (tablo parse etme)

def scrape_countries():
    print("=" * 60)
    print("DENEME 1: Scrape This Site - Ulkeler")
    print("=" * 60)

    url = "https://www.scrapethissite.com/pages/simple/"
    print(f"  Sayfa cekiliyor: {url}")

    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")

    countries = []
    for item in soup.select("div.col-md-4.country"):
        name = item.select_one("h3.country-name")
        capital = item.select_one("span.country-capital")
        population = item.select_one("span.country-population")
        area = item.select_one("span.country-area")

        countries.append({
            "ulke": name.text.strip() if name else "",
            "baskent": capital.text.strip() if capital else "",
            "nufus": population.text.strip() if population else "",
            "alan_km2": area.text.strip() if area else ""
        })

    save_json(countries, "scrapethissite_ulkeler.json")
    for c in countries[:3]:
        print(f"  {c['ulke']} | Baskent: {c['baskent']} | Nufus: {c['nufus']}")
    print(f"  ... toplam {len(countries)} ulke cekildi.\n")


# ===================================================================
# DENEME 2: HTTPBin - HTTP Istek/Yanit Testi
# ===================================================================
# Site: https://httpbin.org/
# Yontem: requests
# Amac: Header, cookie, IP bilgisi test etme (scraping degil ama HTTP bilgisi icin onemli)

def test_httpbin():
    print("=" * 60)
    print("DENEME 2: HTTPBin - HTTP Istek Testi")
    print("=" * 60)

    results = {}

    # 1. IP adresimiz
    try:
        res = requests.get("https://httpbin.org/ip", headers=HEADERS, timeout=10)
        if res.status_code == 200:
            results["ip"] = res.json()
            print(f"  IP Adresimiz: {results['ip']}")
        else:
            print(f"  IP cekerken hata olustu. Status: {res.status_code}")
    except Exception as e:
        print(f"  IP cekerken baglanti hatasi: {e}")

    # 2. Gonderdigimiz header'lar
    try:
        res = requests.get("https://httpbin.org/headers", headers=HEADERS, timeout=10)
        if res.status_code == 200:
            results["headers"] = res.json()
            print(f"  User-Agent: {results['headers'].get('headers', {}).get('User-Agent', 'yok')}")
        else:
            print(f"  Headers cekerken hata olustu. Status: {res.status_code}")
    except Exception as e:
        print(f"  Headers cekerken baglanti hatasi: {e}")

    # 3. Cookie testi
    try:
        session = requests.Session()
        session.get("https://httpbin.org/cookies/set/test_cookie/merhaba_dunya", headers=HEADERS, timeout=10)
        res = session.get("https://httpbin.org/cookies", headers=HEADERS, timeout=10)
        if res.status_code == 200:
            results["cookies"] = res.json()
            print(f"  Cookie Testi: {results['cookies']}")
        else:
            print(f"  Cookies cekerken hata olustu. Status: {res.status_code}")
    except Exception as e:
        print(f"  Cookies cekerken baglanti hatasi: {e}")

    # 4. Delayed response (sunucu gecikme testi)
    try:
        start = time.time()
        res = requests.get("https://httpbin.org/delay/2", headers=HEADERS, timeout=10)
        elapsed = time.time() - start
        results["delay_test"] = {"beklenen_sure": 2, "gercek_sure": round(elapsed, 2)}
        print(f"  Gecikme Testi: {elapsed:.2f}sn (2sn beklendi)")
    except Exception as e:
        print(f"  Delay testi yapilamadi: {e}")

    save_json([results], "httpbin_test.json")
    print("  HTTP bilgi testleri tamamlandi.\n")


# ===================================================================
# DENEME 3: Wikipedia - Programlama Dilleri Tablosu
# ===================================================================
# Site: https://en.wikipedia.org/wiki/Comparison_of_programming_languages
# Yontem: requests + BS4
# Zorluk: Orta (karmasik tablo yapisi)

def scrape_wikipedia_table():
    print("=" * 60)
    print("DENEME 3: Wikipedia - Programlama Dilleri Tablosu")
    print("=" * 60)

    url = "https://en.wikipedia.org/wiki/List_of_programming_languages"
    print(f"  Sayfa cekiliyor: {url}")

    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")

    # Sayfadaki alfabetik listelerdeki dilleri cek
    languages = []
    for div in soup.select("div.div-col"):
        for li in div.select("li"):
            link = li.select_one("a")
            if link:
                languages.append({
                    "dil": link.text.strip(),
                    "wiki_link": "https://en.wikipedia.org" + link.get("href", "")
                })

    save_json(languages, "wikipedia_programlama_dilleri.json")
    for lang in languages[:5]:
        print(f"  {lang['dil']}")
    print(f"  ... toplam {len(languages)} programlama dili cekildi.\n")


# ===================================================================
# DENEME 4: GitHub Trending (Gercek Dunya Sitesi)
# ===================================================================
# Site: https://github.com/trending
# Yontem: requests + BS4
# Zorluk: Orta (gercek site, HTML yapisi degisebilir)

def scrape_github_trending():
    print("=" * 60)
    print("DENEME 4: GitHub Trending Repos")
    print("=" * 60)

    url = "https://github.com/trending"
    print(f"  Sayfa cekiliyor: {url}")

    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")

    repos = []
    for article in soup.select("article.Box-row"):
        name_tag = article.select_one("h2 a")
        desc_tag = article.select_one("p")
        lang_tag = article.select_one("span[itemprop='programmingLanguage']")
        stars_tag = article.select("a.Link")

        repo_name = name_tag.text.strip().replace("\n", "").replace(" ", "") if name_tag else ""
        description = desc_tag.text.strip() if desc_tag else ""
        language = lang_tag.text.strip() if lang_tag else "Belirtilmemis"

        # Gunluk yildiz bilgisi
        daily_stars = ""
        star_tags = article.select("span.d-inline-block")
        for st in star_tags:
            if "stars" in st.text:
                daily_stars = st.text.strip()
                break

        repos.append({
            "repo": repo_name,
            "aciklama": description[:100],
            "dil": language,
            "gunluk_yildiz": daily_stars
        })

    save_json(repos, "github_trending.json")
    for r in repos[:3]:
        print(f"  {r['repo']} | {r['dil']} | {r['gunluk_yildiz']}")
    print(f"  ... toplam {len(repos)} trending repo cekildi.\n")


# ===================================================================
# DENEME 5: JSONPlaceholder - Fake REST API
# ===================================================================
# Site: https://jsonplaceholder.typicode.com/
# Yontem: requests (REST API)
# Amac: GET/POST istek pratigi

def fetch_jsonplaceholder():
    print("=" * 60)
    print("DENEME 5: JSONPlaceholder - REST API Pratigi")
    print("=" * 60)

    # GET - Postlari cek
    print("  GET /posts - Postlar cekiliyor...")
    res = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts = res.json()[:10]  # ilk 10 post

    post_data = []
    for p in posts:
        post_data.append({
            "id": p["id"],
            "baslik": p["title"],
            "govde": p["body"][:80],
            "kullanici_id": p["userId"]
        })

    # POST - Yeni bir post olustur (fake, gercekten kaydetmiyor)
    print("  POST /posts - Yeni post olusturuluyor (fake)...")
    new_post = requests.post(
        "https://jsonplaceholder.typicode.com/posts",
        json={"title": "Test Post", "body": "Scraping calismasi", "userId": 1}
    )
    post_data.append({
        "id": new_post.json().get("id"),
        "baslik": "Test Post (POST ile olusturuldu)",
        "govde": "Scraping calismasi",
        "kullanici_id": 1,
        "http_metodu": "POST",
        "status_code": new_post.status_code
    })

    # GET - Kullanicilari cek
    print("  GET /users - Kullanicilar cekiliyor...")
    res = requests.get("https://jsonplaceholder.typicode.com/users")
    users = res.json()

    user_data = []
    for u in users:
        user_data.append({
            "id": u["id"],
            "isim": u["name"],
            "email": u["email"],
            "sehir": u["address"]["city"],
            "sirket": u["company"]["name"]
        })

    save_json(post_data, "jsonplaceholder_posts.json")
    save_json(user_data, "jsonplaceholder_users.json")

    for p in post_data[:2]:
        print(f"  Post #{p['id']}: {p['baslik'][:50]}")
    for u in user_data[:2]:
        print(f"  Kullanici: {u['isim']} | {u['email']} | {u['sehir']}")
    print(f"  ... {len(post_data)} post + {len(user_data)} kullanici cekildi.\n")


# ===================================================================
# CALISTIR
# ===================================================================

if __name__ == "__main__":
    print("\nFarkli Site & Kaynak Denemeleri Basliyor...\n")

    scrape_countries()
    test_httpbin()
    scrape_wikipedia_table()
    scrape_github_trending()
    fetch_jsonplaceholder()

    print("Tum site denemeleri tamamlandi!")
    print("Sonuclar '07-site-denemeleri/veriler/' klasorune kaydedildi.")
