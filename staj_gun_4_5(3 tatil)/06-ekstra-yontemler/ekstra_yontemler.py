# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""
06 - Ekstra Yontemler & Ileri Konular

Bu dosyada standart yontemlerin otesindeki ileri scraping tekniklerini deniyoruz.
Her birinin ne zaman isledigini ve ne avantaj sagladigini anlamak onemli.

Denenen Konular:
  1) httpx + selectolax (Performans odakli requests+BS4 alternatifi)
  2) Async scraping (asyncio + httpx ile ayni anda birden fazla sayfa cekme)
  3) Veriyi SQLite veritabanina kaydetme (JSON yerine yapisal depolama)
"""

import httpx
from selectolax.parser import HTMLParser
import asyncio
import sqlite3
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


# ===================================================================
# ORNEK 1: httpx + selectolax (Hizli Alternatif)
# ===================================================================
# requests yerine httpx: HTTP/2 destekli, async uyumlu, daha hizli.
# BeautifulSoup yerine selectolax: C tabanlı parser, 10-20x daha hızlı HTML parsing.
# Buyuk olcekli scraping projelerinde performans farki cok belirgin.

def scrape_with_httpx():
    print("=" * 60)
    print("ORNEK 1: httpx + selectolax (Performans Odakli)")
    print("=" * 60)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    all_books = []

    with httpx.Client(headers=headers, follow_redirects=True) as client:
        for page in range(1, 4):  # 3 sayfa
            url = f"http://books.toscrape.com/catalogue/page-{page}.html"
            print(f"  Sayfa {page} cekiliyor (httpx): {url}")

            response = client.get(url)
            tree = HTMLParser(response.text)

            books = tree.css("article.product_pod")
            for book in books:
                title_node = book.css_first("h3 a")
                price_node = book.css_first("p.price_color")
                rating_node = book.css_first("p.star-rating")

                all_books.append({
                    "baslik": title_node.attributes.get("title", "") if title_node else "",
                    "fiyat": price_node.text() if price_node else "",
                    "puan": rating_node.attributes.get("class", "").split()[-1] if rating_node else ""
                })

            time.sleep(0.5)

    save_json(all_books, "httpx_books.json")
    for b in all_books[:3]:
        print(f"  {b['baslik']} | {b['fiyat']} | Puan: {b['puan']}")
    print(f"  ... toplam {len(all_books)} kitap httpx+selectolax ile cekildi.\n")

    return all_books


# ===================================================================
# ORNEK 2: Async Scraping (asyncio + httpx)
# ===================================================================
# Normal (senkron) scraping: sayfalari tek tek cekersin, her biri icin beklersin.
# Async scraping: birden fazla sayfayi AYNI ANDA cekersin.
# 10 sayfa x 1sn = senkronda 10sn, async'te ~1-2sn.

async def fetch_page(client, url, page_num):
    """Tek bir sayfayi async olarak cek."""
    response = await client.get(url)
    tree = HTMLParser(response.text)
    quotes = []

    for quote in tree.css("div.quote"):
        text_node = quote.css_first("span.text")
        author_node = quote.css_first("small.author")
        quotes.append({
            "alinti": text_node.text() if text_node else "",
            "yazar": author_node.text() if author_node else "",
            "sayfa": page_num
        })

    print(f"  Sayfa {page_num} tamamlandi ({len(quotes)} alinti)")
    return quotes


async def scrape_async():
    print("=" * 60)
    print("ORNEK 2: Async Scraping (asyncio + httpx)")
    print("=" * 60)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    urls = [(f"http://quotes.toscrape.com/page/{i}/", i) for i in range(1, 6)]

    start_time = time.time()

    async with httpx.AsyncClient(headers=headers) as client:
        # Tum sayfalari ayni anda cek (asyncio.gather)
        tasks = [fetch_page(client, url, num) for url, num in urls]
        results = await asyncio.gather(*tasks)

    elapsed = time.time() - start_time
    all_quotes = [q for page_quotes in results for q in page_quotes]

    save_json(all_quotes, "async_quotes.json")
    for q in all_quotes[:3]:
        print(f"  \"{q['alinti'][:50]}...\" - {q['yazar']}")
    print(f"  ... {len(all_quotes)} alinti {elapsed:.2f} saniyede cekildi (5 sayfa ayni anda!).\n")

    return all_quotes


# ===================================================================
# ORNEK 3: SQLite'a Veri Kaydetme
# ===================================================================
# JSON guzel ama buyuk veride sorgu yapmak zor.
# SQLite: Dosya tabanli, kurulumsuz, SQL ile sorgu yapilabilen veritabani.
# Cekilen verileri buraya kaydedince sonradan filtreleme, siralama, arama cok kolay.

def save_to_sqlite(books, quotes):
    print("=" * 60)
    print("ORNEK 3: SQLite Veritabanina Kaydetme")
    print("=" * 60)

    out_dir = os.path.join(os.path.dirname(__file__), "veriler")
    os.makedirs(out_dir, exist_ok=True)
    db_path = os.path.join(out_dir, "scraping_verileri.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Kitaplar tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kitaplar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baslik TEXT,
            fiyat TEXT,
            puan TEXT
        )
    """)

    # Alıntilar tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alintilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alinti TEXT,
            yazar TEXT,
            sayfa INTEGER
        )
    """)

    # Kitaplari kaydet
    for b in books:
        cursor.execute("INSERT INTO kitaplar (baslik, fiyat, puan) VALUES (?, ?, ?)",
                       (b["baslik"], b["fiyat"], b["puan"]))

    # Alintilari kaydet
    for q in quotes:
        cursor.execute("INSERT INTO alintilar (alinti, yazar, sayfa) VALUES (?, ?, ?)",
                       (q["alinti"], q["yazar"], q.get("sayfa", 0)))

    conn.commit()

    # Ornek SQL sorgusu: 5 yildizli kitaplar
    print("  SQL Sorgusu: Puan='Five' olan kitaplar:")
    five_star = cursor.execute("SELECT baslik, fiyat FROM kitaplar WHERE puan='Five'").fetchall()
    for row in five_star[:3]:
        print(f"    {row[0]} | {row[1]}")
    print(f"    ... toplam {len(five_star)} adet 5 yildizli kitap bulundu.")

    # Ornek SQL sorgusu: Einstein alintilari
    print("\n  SQL Sorgusu: Albert Einstein alintilari:")
    einstein = cursor.execute("SELECT alinti FROM alintilar WHERE yazar LIKE '%Einstein%'").fetchall()
    for row in einstein[:2]:
        print(f"    \"{row[0][:60]}...\"")
    print(f"    ... toplam {len(einstein)} Einstein alintisi bulundu.")

    conn.close()
    print(f"\n  Veritabani '{db_path}' dosyasina kaydedildi.")
    print(f"  {len(books)} kitap + {len(quotes)} alinti SQL tablolarina yazildi.\n")


# ===================================================================
# CALISTIR
# ===================================================================

if __name__ == "__main__":
    print("\nEkstra Yontemler & Ileri Konular Basliyor...\n")

    books = scrape_with_httpx()
    quotes = asyncio.run(scrape_async())
    save_to_sqlite(books, quotes)

    print("Tum ekstra yontem denemeleri tamamlandi!")
    print("Sonuclar '06-ekstra-yontemler/veriler/' klasorune kaydedildi.")
