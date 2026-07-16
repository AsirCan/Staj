# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""
05 - API Reverse Engineering Örnekleri

API Reverse Engineering Nedir?
  - Modern web siteleri kullanıcı arayüzünü yüklerken verileri arka planda JSON formatında 
    REST veya GraphQL API endpoint'lerinden çeker (Fetch / AJAX).
  - Tarayıcının Geliştirici Araçları (F12 DevTools) -> Network -> Fetch/XHR filtresini 
    kullanarak bu gizli endpoint'leri tespit ederiz.
  - HTML DOM parse etmek yerine doğrudan veriyi üreten API sunucusuna istek atarız.

Avantajları:
  1. Hız: HTML download ve DOM parse maliyeti yok.
  2. Temizlik: Veri doğrudan düzenli JSON nesnesi olarak gelir.
  3. Güvenilirlik: Tasarım/CSS değişse bile API yapısı kolay kolay kırılmaz.
  4. Performans: Selenium gibi ağır tarayıcı çalıştırmak gerekmez.

Denenen Örnekler:
  1) Hacker News Firebase REST API — Top Stories & Detayları
  2) REST Countries API          — Ülke Nüfus, Başkent ve Bölge Verileri
  3) DummyJSON E-Commerce API    — Ürünler, Fiyatlar ve Stok Bilgileri
"""

import requests
import json
import os
import time


def save_json(data, filename):
    """Çekilen veriyi modüle özel veriler klasörüne kaydet."""
    out_dir = os.path.join(os.path.dirname(__file__), "veriler")
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> {len(data)} kayıt '{filepath}' dosyasına kaydedildi.\n")


# ===================================================================
# ÖRNEK 1: Hacker News Firebase API
# ===================================================================

def fetch_hacker_news_api():
    print("=" * 60)
    print("ÖRNEK 1: Hacker News Firebase REST API (Doğrudan JSON)")
    print("=" * 60)

    top_ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    print(f"  Top story ID'leri çekiliyor: {top_ids_url}")

    response = requests.get(top_ids_url)
    top_ids = response.json()[:15]  # İlk 15 haberi alalım

    stories = []
    for story_id in top_ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        item_res = requests.get(item_url)
        item_data = item_res.json()

        stories.append({
            "id": item_data.get("id"),
            "baslik": item_data.get("title"),
            "yazar": item_data.get("by"),
            "puan": item_data.get("score"),
            "url": item_data.get("url", ""),
            "yorum_sayisi": item_data.get("descendants", 0)
        })
        time.sleep(0.1)

    save_json(stories, "hacker_news_api.json")
    for s in stories[:3]:
        print(f"  📰 {s['baslik']} | Puan: {s['puan']} | Yazar: {s['yazar']}")
    print(f"  ... toplam {len(stories)} haber doğrudan API üzerinden çekildi.\n")


# ===================================================================
# ÖRNEK 2: PokeAPI (Açık REST API Endpoint'i)
# ===================================================================

def fetch_pokemon_api():
    print("=" * 60)
    print("ÖRNEK 2: PokeAPI (Doğrudan REST JSON Endpoint'i)")
    print("=" * 60)

    url = "https://pokeapi.co/api/v2/pokemon?limit=30"
    headers = {"User-Agent": "Mozilla/5.0"}
    print(f"  İstek atılıyor: {url}")

    res = requests.get(url, headers=headers)
    pokemon_list = []

    if res.status_code == 200:
        results = res.json().get("results", [])
        for p in results:
            pokemon_list.append({
                "isim": p.get("name").capitalize(),
                "detay_url": p.get("url")
            })

    save_json(pokemon_list, "pokeapi_pokemon.json")
    for p in pokemon_list[:3]:
        print(f"  ⚡ {p['isim']} | Detay Endpoint: {p['detay_url']}")
    print(f"  ... toplam {len(pokemon_list)} karakter verisi JSON olarak çekildi.\n")


# ===================================================================
# ÖRNEK 3: DummyJSON Products API (E-Ticaret Veri Endpoint'i)
# ===================================================================

def fetch_dummyjson_products():
    print("=" * 60)
    print("ÖRNEK 3: DummyJSON Products API (E-Ticaret Ürünleri)")
    print("=" * 60)

    url = "https://dummyjson.com/products?limit=30"
    print(f"  İstek atılıyor: {url}")

    res = requests.get(url)
    all_products = []

    if res.status_code == 200:
        data = res.json()
        products = data.get("products", [])
        for p in products:
            all_products.append({
                "id": p.get("id"),
                "urun_adi": p.get("title"),
                "marka": p.get("brand"),
                "kategori": p.get("category"),
                "fiyat": f"${p.get('fiyat', p.get('price'))}",
                "puan": p.get("rating"),
                "stok": p.get("stock")
            })

    save_json(all_products, "dummyjson_products_api.json")
    for p in all_products[:3]:
        print(f"  🛒 {p['urun_adi']} | Fiyat: {p['fiyat']} | Kategori: {p['kategori']}")
    print(f"  ... toplam {len(all_products)} ürün JSON olarak çekildi.\n")


# ===================================================================
# ÇALIŞTIRMA
# ===================================================================

if __name__ == "__main__":
    print("\n🚀 API Reverse Engineering Örnekleri Başlıyor...\n")

    fetch_hacker_news_api()
    fetch_pokemon_api()
    fetch_dummyjson_products()

    print("✅ Tüm API Reverse Engineering denemeleri başarıyla tamamlandı!")
    print("   Sonuçlar '05-api-reverse-engineering/veriler/' klasörüne kaydedildi.")
