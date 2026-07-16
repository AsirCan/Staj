# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""
02 - BeautifulSoup Örnekleri
requests + BeautifulSoup4 ile statik sitelerde web scraping denemeleri.

Denenen siteler:
  1) Books to Scrape   — kitap bilgileri (isim, fiyat, rating)
  2) Quotes to Scrape  — alıntılar, yazarlar, etiketler
  3) Real Python Fake Jobs — iş ilanları
  4) Hacker News       — başlıklar ve puanlar

Her örnekte çekilen veri JSON olarak kaydediliyor.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os

# -------------------------------------------------------------------
# Yardımcı fonksiyonlar
# -------------------------------------------------------------------

def save_json(data, filename):
    """Çekilen veriyi JSON dosyasına kaydet."""
    out_dir = os.path.join(os.path.dirname(__file__), "veriler")
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> {len(data)} kayıt '{filepath}' dosyasına kaydedildi.\n")


def get_soup(url, headers=None):
    """URL'den HTML çek ve BeautifulSoup nesnesi döndür."""
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # hata varsa exception fırlat
    return BeautifulSoup(response.text, "lxml")


# ===================================================================
# ÖRNEK 1: Books to Scrape — Kitap Bilgileri
# ===================================================================
# Site: http://books.toscrape.com/
# Çekilecek: Kitap adı, fiyat, rating, stok durumu
# Yöntem: requests + BS4 (statik site, CSS selectors)

def scrape_books():
    print("=" * 60)
    print("ÖRNEK 1: Books to Scrape — Kitap Bilgileri")
    print("=" * 60)

    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_books = []

    # Rating kelimelerini sayıya çevirmek için
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    # İlk 3 sayfayı çekelim (toplamda 50 sayfa var ama demo için 3 yeter)
    for page in range(1, 4):
        url = base_url.format(page)
        print(f"  Sayfa {page} çekiliyor: {url}")

        soup = get_soup(url)
        books = soup.select("article.product_pod")

        for book in books:
            title = book.select_one("h3 a")["title"]
            price = book.select_one("p.price_color").text.strip()
            # Rating class'tan geliyor: "star-rating Three" gibi
            rating_class = book.select_one("p.star-rating")["class"][1]
            rating = rating_map.get(rating_class, 0)
            in_stock = "In stock" in book.select_one("p.instock").text

            all_books.append({
                "baslik": title,
                "fiyat": price,
                "puan": rating,
                "stokta": in_stock
            })

        time.sleep(1)  # istekler arası bekleme

    save_json(all_books, "books_to_scrape.json")
    # İlk 3 kitabı göster
    for book in all_books[:3]:
        print(f"  {book['baslik']} | {book['fiyat']} | Puan: {book['puan']}")
    print(f"  ... toplam {len(all_books)} kitap çekildi.\n")

    return all_books


# ===================================================================
# ÖRNEK 2: Quotes to Scrape — Alıntılar
# ===================================================================
# Site: http://quotes.toscrape.com/
# Çekilecek: Alıntı metni, yazar, etiketler
# Yöntem: requests + BS4 + pagination (next butonu takip)

def scrape_quotes():
    print("=" * 60)
    print("ÖRNEK 2: Quotes to Scrape — Alıntılar")
    print("=" * 60)

    base_url = "http://quotes.toscrape.com"
    all_quotes = []
    url = base_url + "/page/1/"

    page_num = 1
    while url and page_num <= 5:  # en fazla 5 sayfa
        print(f"  Sayfa {page_num} çekiliyor: {url}")
        soup = get_soup(url)

        quotes = soup.select("div.quote")
        for quote in quotes:
            text = quote.select_one("span.text").text.strip()
            author = quote.select_one("small.author").text.strip()
            tags = [tag.text for tag in quote.select("a.tag")]

            all_quotes.append({
                "alinti": text,
                "yazar": author,
                "etiketler": tags
            })

        # Sonraki sayfa linki var mı?
        next_btn = soup.select_one("li.next a")
        if next_btn:
            url = base_url + next_btn["href"]
            page_num += 1
        else:
            url = None

        time.sleep(1)

    save_json(all_quotes, "quotes_to_scrape.json")
    for q in all_quotes[:3]:
        print(f"  \"{q['alinti'][:60]}...\" - {q['yazar']}")
    print(f"  ... toplam {len(all_quotes)} alıntı çekildi.\n")

    return all_quotes


# ===================================================================
# ÖRNEK 3: Real Python Fake Jobs — İş İlanları
# ===================================================================
# Site: https://realpython.github.io/fake-jobs/
# Çekilecek: Pozisyon, şirket, lokasyon, tarih
# Yöntem: requests + BS4 (tek sayfa, tüm veri orada)

def scrape_fake_jobs():
    print("=" * 60)
    print("ÖRNEK 3: Real Python Fake Jobs — İş İlanları")
    print("=" * 60)

    url = "https://realpython.github.io/fake-jobs/"
    print(f"  Sayfa çekiliyor: {url}")

    soup = get_soup(url)
    cards = soup.select("div.card-content")

    all_jobs = []
    for card in cards:
        title = card.select_one("h2.title").text.strip()
        company = card.select_one("h3.subtitle").text.strip()
        location = card.select_one("p.location").text.strip()
        date = card.select_one("time")
        date_text = date.text.strip() if date else "Tarih yok"

        all_jobs.append({
            "pozisyon": title,
            "sirket": company,
            "lokasyon": location,
            "tarih": date_text
        })

    save_json(all_jobs, "fake_jobs.json")
    for job in all_jobs[:3]:
        print(f"  {job['pozisyon']} @ {job['sirket']} | {job['lokasyon']}")
    print(f"  ... toplam {len(all_jobs)} ilan çekildi.\n")

    return all_jobs


# ===================================================================
# ÖRNEK 4: Hacker News — Başlıklar ve Puanlar
# ===================================================================
# Site: https://news.ycombinator.com/
# Çekilecek: Başlık, link, puan, yorum sayısı
# Yöntem: requests + BS4 (statik sayfa)

def scrape_hacker_news():
    print("=" * 60)
    print("ÖRNEK 4: Hacker News — Başlıklar ve Puanlar")
    print("=" * 60)

    url = "https://news.ycombinator.com/"
    print(f"  Sayfa çekiliyor: {url}")

    soup = get_soup(url)

    all_stories = []
    # Hacker News'in HTML yapısı: .titleline içinde başlık ve link var
    title_rows = soup.select("tr.athing")

    for row in title_rows:
        title_el = row.select_one("span.titleline > a")
        if not title_el:
            continue

        title = title_el.text.strip()
        link = title_el.get("href", "")

        # Puan ve yorum bilgisi bir sonraki tr'de (.subtext içinde)
        subtext = row.find_next_sibling("tr")
        score_el = subtext.select_one("span.score") if subtext else None
        score = score_el.text.strip() if score_el else "0 points"

        comment_links = subtext.select("a") if subtext else []
        comments = "0"
        for a in comment_links:
            if "comment" in a.text.lower():
                comments = a.text.strip()
                break

        all_stories.append({
            "baslik": title,
            "link": link,
            "puan": score,
            "yorumlar": comments
        })

    save_json(all_stories, "hacker_news.json")
    for s in all_stories[:5]:
        print(f"  {s['baslik'][:55]}... | {s['puan']}")
    print(f"  ... toplam {len(all_stories)} haber çekildi.\n")

    return all_stories


# ===================================================================
# ÇALIŞTIR
# ===================================================================

if __name__ == "__main__":
    print("\nBeautifulSoup Scraping Ornekleri Basliyor...\n")

    scrape_books()
    scrape_quotes()
    scrape_fake_jobs()
    scrape_hacker_news()

    print("Tum ornekler tamamlandi!")
    print("Cekilen veriler 'cekilen_veriler/' klasorunde JSON olarak kaydedildi.")
