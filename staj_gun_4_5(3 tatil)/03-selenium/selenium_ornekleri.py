# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""
03 - Selenium Ornekleri
Selenium ile dinamik (JavaScript ile render edilen) sitelerde scraping denemeleri.

Selenium neden gerekli?
  - requests + BS4 sadece statik HTML'i cekebilir.
  - Bazi siteler icerigi JavaScript ile yukluyor (React, Vue, Angular vs.)
  - Bu sitelerde sayfa kaynaginda (Ctrl+U) icerik gorunmuyor.
  - Selenium gercek bir tarayici acip JS'yi calistirarak icerigi yukluyor.

Denenen siteler:
  1) Quotes to Scrape (JS modu) — JS ile render edilen alinti sayfasi
  2) Scrape This Site (AJAX)   — AJAX ile yuklenen hokey takimi verileri
  3) Quotes to Scrape (Scroll) — Infinite scroll denemesi
  4) Headless mode ornegi       — Tarayici acmadan arka planda calisma
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time
import os


def save_json(data, filename):
    """Cekilen veriyi JSON dosyasina kaydet."""
    out_dir = os.path.join(os.path.dirname(__file__), "veriler")
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> {len(data)} kayit '{filepath}' dosyasina kaydedildi.\n")


def create_driver(headless=False):
    """Chrome WebDriver olustur. headless=True ise tarayici gorunmez."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Bot algilanmasini azaltmak icin
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)  # element bulunamazsa 5 sn bekle
    return driver


# ===================================================================
# ORNEK 1: Quotes to Scrape (JS Versiyonu)
# ===================================================================
# Site: http://quotes.toscrape.com/js/
# Neden Selenium? Icerik JavaScript ile yukleniyor, requests ile cekilemez.
# Ctrl+U yapinca icerik gorunmuyor, sadece JS kodu var.

def scrape_quotes_js():
    print("=" * 60)
    print("ORNEK 1: Quotes to Scrape (JS Versiyonu)")
    print("=" * 60)

    driver = create_driver(headless=True)
    all_quotes = []

    try:
        for page in range(1, 4):  # ilk 3 sayfa
            url = f"http://quotes.toscrape.com/js/page/{page}/"
            print(f"  Sayfa {page} cekiliyor: {url}")
            driver.get(url)

            # JS'nin icerigi yuklemesini bekle
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.quote"))
            )

            quotes = driver.find_elements(By.CSS_SELECTOR, "div.quote")
            for quote in quotes:
                text = quote.find_element(By.CSS_SELECTOR, "span.text").text
                author = quote.find_element(By.CSS_SELECTOR, "small.author").text
                tags = [tag.text for tag in quote.find_elements(By.CSS_SELECTOR, "a.tag")]

                all_quotes.append({
                    "alinti": text,
                    "yazar": author,
                    "etiketler": tags
                })

            time.sleep(1)

    finally:
        driver.quit()

    save_json(all_quotes, "quotes_js_selenium.json")
    for q in all_quotes[:3]:
        print(f"  \"{q['alinti'][:50]}...\" - {q['yazar']}")
    print(f"  ... toplam {len(all_quotes)} alinti cekildi (JS renderli site!).\n")

    return all_quotes


# ===================================================================
# ORNEK 2: Scrape This Site — AJAX ile Yuklenen Veri
# ===================================================================
# Site: https://www.scrapethissite.com/pages/ajax-javascript/
# Neden Selenium? Filmler yila tiklaninca AJAX ile yukleniyor.

def scrape_ajax_movies():
    print("=" * 60)
    print("ORNEK 2: Scrape This Site - AJAX Filmler")
    print("=" * 60)

    driver = create_driver(headless=True)
    all_movies = []

    try:
        url = "https://www.scrapethissite.com/pages/ajax-javascript/"
        print(f"  Sayfa aciliyor: {url}")
        driver.get(url)

        # Yil linklerini bul ve tiklayarak verileri cek
        year_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.year-link"))
        )

        years_to_click = [link.text.strip() for link in year_links[:5]]  # ilk 5 yil
        print(f"  Bulunan yillar: {years_to_click}")

        for year_text in years_to_click:
            # Her yil icin linki tekrar bul (sayfa degisebilir)
            year_link = driver.find_element(By.LINK_TEXT, year_text)
            year_link.click()
            print(f"  {year_text} yilina tiklandi, veriler yukleniyor...")

            # AJAX'in verileri yuklemesini bekle
            time.sleep(2)

            # Film verilerini cek
            movies = driver.find_elements(By.CSS_SELECTOR, "tr.film")
            for movie in movies:
                cols = movie.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 4:
                    all_movies.append({
                        "film": cols[0].text.strip(),
                        "aday_sayisi": cols[1].text.strip(),
                        "odul_sayisi": cols[2].text.strip(),
                        "en_iyi_film": cols[3].text.strip() if len(cols) > 3 else ""
                    })

    finally:
        driver.quit()

    save_json(all_movies, "ajax_movies.json")
    for m in all_movies[:3]:
        print(f"  {m['film']} | Aday: {m['aday_sayisi']} | Odul: {m['odul_sayisi']}")
    print(f"  ... toplam {len(all_movies)} film cekildi (AJAX ile yuklenen veri!).\n")

    return all_movies


# ===================================================================
# ORNEK 3: Quotes to Scrape — Infinite Scroll
# ===================================================================
# Site: http://quotes.toscrape.com/scroll
# Neden Selenium? Sayfa asagi indikce yeni icerik yukleniyor (infinite scroll).
# Pagination yok, scroll yaparak daha fazla veri cekiyoruz.

def scrape_infinite_scroll():
    print("=" * 60)
    print("ORNEK 3: Quotes to Scrape - Infinite Scroll")
    print("=" * 60)

    driver = create_driver(headless=True)
    all_quotes = []

    try:
        url = "http://quotes.toscrape.com/scroll"
        print(f"  Sayfa aciliyor: {url}")
        driver.get(url)

        # Birkaç kez scroll yapalim
        last_height = driver.execute_script("return document.body.scrollHeight")

        for scroll_num in range(1, 6):  # 5 kez scroll
            # Sayfanin en altina scroll
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"  Scroll {scroll_num} yapildi, yeni icerik bekleniyor...")
            time.sleep(2)  # AJAX'in yuklenmesini bekle

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("  Daha fazla icerik yok, scroll durduruluyor.")
                break
            last_height = new_height

        # Tum alintilari cek
        quotes = driver.find_elements(By.CSS_SELECTOR, "div.quote")
        for quote in quotes:
            text = quote.find_element(By.CSS_SELECTOR, "span.text").text
            author = quote.find_element(By.CSS_SELECTOR, "small.author").text

            all_quotes.append({
                "alinti": text,
                "yazar": author
            })

    finally:
        driver.quit()

    save_json(all_quotes, "infinite_scroll_quotes.json")
    for q in all_quotes[:3]:
        print(f"  \"{q['alinti'][:50]}...\" - {q['yazar']}")
    print(f"  ... toplam {len(all_quotes)} alinti cekildi (infinite scroll!).\n")

    return all_quotes


# ===================================================================
# ORNEK 4: Headless vs Normal Mod Karsilastirmasi
# ===================================================================
# Headless mod: Tarayici penceresi acilmadan arka planda calisir.
# Avantaj: Daha hizli, daha az kaynak kullaniyor, sunucuda calisabilir.
# Dezavantaj: Debug etmesi zor (goremiyorsun ne oluyor).

def headless_comparison():
    print("=" * 60)
    print("ORNEK 4: Headless vs Normal Mod Karsilastirma")
    print("=" * 60)

    url = "http://quotes.toscrape.com/"

    # Headless mod
    start = time.time()
    driver = create_driver(headless=True)
    driver.get(url)
    title_headless = driver.title
    quotes_count = len(driver.find_elements(By.CSS_SELECTOR, "div.quote"))
    driver.quit()
    headless_time = time.time() - start

    # Normal mod (gorunur tarayici)
    start = time.time()
    driver = create_driver(headless=False)
    driver.get(url)
    title_normal = driver.title
    driver.quit()
    normal_time = time.time() - start

    print(f"  Headless mod: {headless_time:.2f} saniye | Baslik: {title_headless}")
    print(f"  Normal mod:   {normal_time:.2f} saniye | Baslik: {title_normal}")
    print(f"  Headless {normal_time/headless_time:.1f}x daha hizli.\n")

    # Not: Headless modda bile ayni veri cekilebiliyor.
    print(f"  Headless modda {quotes_count} alinti bulundu (ayni sonuc).\n")


# ===================================================================
# CALISTIR
# ===================================================================

if __name__ == "__main__":
    print("\nSelenium Scraping Ornekleri Basliyor...\n")
    print("Not: Selenium gercek bir Chrome tarayici aciyor.")
    print("     ChromeDriver otomatik yonetiliyor (Selenium 4+).\n")

    scrape_quotes_js()
    scrape_ajax_movies()
    scrape_infinite_scroll()
    headless_comparison()

    print("Tum Selenium ornekleri tamamlandi!")
    print("Cekilen veriler 'cekilen_veriler/' klasorunde JSON olarak kaydedildi.")
    print("\n--- BS4 vs Selenium Karsilastirma ---")
    print("BS4:      Hizli, hafif, statik siteler icin yeterli.")
    print("Selenium: Yavas ama JS render edebiliyor, click/scroll yapabiliyor.")
    print("Kural:    Once BS4 dene, islemezse Selenium kullan.")
