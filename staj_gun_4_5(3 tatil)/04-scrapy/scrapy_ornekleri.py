# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""
04 - Scrapy Framework Örnekleri

Scrapy Nedir?
  - Python ekosistemindeki en güçlü ve profesyonel web crawling/scraping framework'üdür.
  - Asenkron (Twisted tabanlı) çalışır; yani aynı anda yüzlerce isteği çok hızlı işleyebilir.
  - Mimarisi: 
      * Engine: Süreci yönetir.
      * Spider: Sayfaları talep eder, HTML'i parse eder ve veri/link çıkarır.
      * Item Pipeline: Çıkarılan veriyi temizler, doğrular ve veritabanına/dosyaya kaydeder.
      * Downloader Middleware: İstek/Yanıt mekanizmasını özelleştirir (proxy, user-agent rotasyonu vb.).

Bu Script İçeriği:
  1) BookSpider: Books to Scrape sitesinde sayfalar arası gezerek (Pagination) kitapları toplar.
  2) QuoteSpider: Quotes to Scrape sitesinde alıntıları ve yazarları toplar.
  3) JSONWriterPipeline: Çekilen öğeleri özelleştirilmiş pipeline ile JSON'a yazar.
  4) CrawlerProcess: Standalone Python dosyası olarak Scrapy motorunu başlatır.
"""

import scrapy
from scrapy.crawler import CrawlerProcess
import json
import os


# ===================================================================
# PIPELINE: Veriyi Temizleme ve JSON Dosyasına Kaydetme
# ===================================================================

class CustomJsonPipeline:
    """Çekilen öğeleri toplayıp temiz bir JSON dosyasına kaydetmek için Item Pipeline"""
    def open_spider(self, spider):
        out_dir = os.path.join(os.path.dirname(__file__), "veriler")
        os.makedirs(out_dir, exist_ok=True)
        filename = f"scrapy_{spider.name}.json"
        self.filepath = os.path.join(out_dir, filename)
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
        print(f"\n[Scrapy Pipeline] '{spider.name}' tamamlandı -> {len(self.items)} kayıt '{self.filepath}' dosyasına yazıldı.\n")


# ===================================================================
# SPIDER 1: Books to Scrape (Pagination & Link Following)
# ===================================================================

class BookSpider(scrapy.Spider):
    name = "books"
    start_urls = ["http://books.toscrape.com/catalogue/page-1.html"]
    max_pages = 3
    page_count = 1

    custom_settings = {
        'ITEM_PIPELINES': {'__main__.CustomJsonPipeline': 300},
        'LOG_LEVEL': 'INFO'
    }

    def parse(self, response):
        self.logger.info(f"Scrapy taranıyor: {response.url}")

        books = response.css("article.product_pod")
        for book in books:
            yield {
                "baslik": book.css("h3 a::attr(title)").get(),
                "fiyat": book.css("p.price_color::text").get(),
                "stok_durumu": book.css("p.instock.availability::text").getall()[-1].strip(),
                "puan": book.css("p.star-rating::attr(class)").get().split()[-1]
            }

        # Sonraki sayfa linkini takip et (Link Following)
        next_page = response.css("li.next a::attr(href)").get()
        if next_page and self.page_count < self.max_pages:
            self.page_count += 1
            yield response.follow(next_page, callback=self.parse)


# ===================================================================
# SPIDER 2: Quotes to Scrape (Alıntılar & Etiketler)
# ===================================================================

class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com/page/1/"]
    max_pages = 3
    page_count = 1

    custom_settings = {
        'ITEM_PIPELINES': {'__main__.CustomJsonPipeline': 300},
        'LOG_LEVEL': 'INFO'
    }

    def parse(self, response):
        self.logger.info(f"Scrapy taranıyor: {response.url}")

        for quote in response.css("div.quote"):
            yield {
                "alinti": quote.css("span.text::text").get(),
                "yazar": quote.css("small.author::text").get(),
                "etiketler": quote.css("div.tags a.tag::text").getall()
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page and self.page_count < self.max_pages:
            self.page_count += 1
            yield response.follow(next_page, callback=self.parse)


# ===================================================================
# ÇALIŞTIRMA (CrawlerProcess)
# ===================================================================

if __name__ == "__main__":
    print("\n--- Scrapy Framework Crawling Başlatılıyor ---\n")

    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 0.5
    })

    process.crawl(BookSpider)
    process.crawl(QuoteSpider)
    process.start()

    print("\n✅ Scrapy ile tüm taramalar başarıyla bitti!")
