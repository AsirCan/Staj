# Önemli MCP Sunucuları ve Ne İşe Yaradıkları

**MCP (Model Context Protocol):** Anthropic'in geliştirdiği, yapay zeka modellerini (Claude, Cursor vb.) harici araçlara ve veri kaynaklarına bağlayan açık standart. "AI için USB-C portu" gibi düşünülebilir.

---

## Geliştirici Araçları

| MCP | Ne İşe Yarar | Ücret |
|---|---|---|
| **GitHub MCP** | Repo, issue, pull request, kod arama ve CI/CD yönetimi | Ücretsiz |
| **Serena** ⭐ | Kodun sembol düzeyinde (fonksiyon/sınıf) anlaşılması ve güvenli refactoring; AI'a IDE düzeyinde kod anlama yeteneği verir, token tüketimini ciddi düşürür | Ücretsiz |
| **Context7** ⭐ | Kütüphanelerin güncel dokümantasyonunu AI'a verir; uydurma/eski API kodu yazma sorununu tek başına çözer | Freemium |
| **Zen MCP** ⭐ | Claude'un başka AI modellerine (Gemini, GPT vb.) danışmasını sağlar; zor problemlerde çoklu model görüşü alınır | Ücretsiz (model API anahtarı gerekir) |
| **Task Master** ⭐ | Gereksinim dokümanını (PRD) otomatik görev listesine böler ve AI'ı adım adım yönetir | Ücretsiz (model API anahtarı gerekir) |
| **TestSprite MCP** ⭐ | Yazılan kodu otomatik test eder: test planı oluşturur, frontend/backend testlerini çalıştırır ve hata raporu üretir | Freemium |
| **Filesystem MCP** | Yerel dosyalara güvenli okuma/yazma erişimi | Ücretsiz |
| **Sequential Thinking** | Karmaşık problemlerde adım adım düşünme yeteneği ekler | Ücretsiz |
| **21st.dev Magic** | Doğal dille modern UI bileşenleri (React) üretir | Freemium |

## Veritabanları

| MCP | Ne İşe Yarar | Ücret |
|---|---|---|
| **PostgreSQL MCP** | Doğal dille SQL sorgusu, şema okuma, veri inceleme | Ücretsiz |
| **Supabase MCP** | Supabase projesini (DB, auth, storage) AI ile yönetme | Freemium |
| **SQLite MCP** | Yerel geliştirme veritabanlarını sorgulama | Ücretsiz |

## Web Arama & Scraping

| MCP | Ne İşe Yarar | Ücret |
|---|---|---|
| **Firecrawl MCP** | Web sitelerini temiz Markdown'a çevirir (scraping) | Freemium |
| **Exa MCP** | Anlam bazlı (semantik) web araması | Freemium |
| **Tavily MCP** | LLM'ler için optimize edilmiş web araması | Freemium |
| **Brave Search MCP** | Gizlilik odaklı web araması | Freemium |
| **Fetch MCP** | Herhangi bir URL'nin içeriğini getirir | Ücretsiz |

## Tarayıcı Otomasyonu

| MCP | Ne İşe Yarar | Ücret |
|---|---|---|
| **Playwright MCP** | AI'ın tarayıcıyı kontrol etmesi: test, form doldurma, UI doğrulama | Ücretsiz |
| **Chrome DevTools MCP** ⭐ | AI kendi yazdığı kodu tarayıcıda ölçüp debug eder: performans analizi, ağ incelemesi, konsol logları | Ücretsiz |
| **Puppeteer MCP** | Basit ekran görüntüsü ve sayfa etkileşimi | Ücretsiz |
| **Browserbase** | Bulutta yönetilen tarayıcı oturumları (CI/CD için) | Ücretli |

## Üretkenlik & Proje Yönetimi

| MCP | Ne İşe Yarar | Ücret |
|---|---|---|
| **Notion MCP** | Notion sayfa ve veritabanlarını okuma/yazma | Freemium |
| **Slack MCP** | Kanal mesajlarını okuma, mesaj gönderme | Freemium |
| **Linear MCP** | Issue oluşturma ve proje takibi | Freemium |
| **Jira MCP** | Kurumsal görev ve workflow yönetimi | Freemium |

## Bulut & DevOps

| MCP | Ne İşe Yarar | Ücret |
|---|---|---|
| **AWS MCP** | Lambda, S3, ECS gibi AWS servislerini yönetme | Freemium |
| **Cloudflare MCP** ⭐ | Workers, DNS ve Cloudflare API erişimi; "Code Mode" ile 2.500+ endpoint'i sadece 2 araçla sunarak token sorununa çözüm getirdi | Freemium |
| **Vercel MCP** | Deployment yönetimi (Next.js vb.) | Freemium |
| **Docker MCP** | Container yönetimi ve güvenli MCP çalıştırma | Ücretsiz |
| **Kubernetes MCP** | Cluster kaynaklarını yönetme, Helm kurulumu | Ücretsiz |
| **Sentry MCP** | Uygulama hatalarını ve stack trace'leri inceleme | Freemium |

## Diğer

| MCP | Ne İşe Yarar | Ücret |
|---|---|---|
| **Figma MCP** | Figma tasarımlarını koda çevirme | Freemium |
| **Stripe MCP** | Ödeme, abonelik ve fatura yönetimi | Freemium |
| **Memory MCP** | Oturumlar arası kalıcı hafıza (bilgi grafiği) | Ücretsiz |
| **Zapier MCP** ⭐ | 9.000+ uygulamaya tek noktadan bağlantı; kod yazmadan otomasyon | Freemium |

---

## Claude Code için En İyi MCP'ler

1. **Context7** – güncel dokümantasyon
2. **GitHub MCP** – repo yönetimi
3. **Playwright MCP** – tarayıcıda test/doğrulama
4. **Serena** – büyük kod tabanlarında semantik düzenleme
5. **PostgreSQL/Supabase MCP** – veritabanı erişimi

> Not: Filesystem, Memory ve Sequential Thinking Claude Code'da gereksizdir çünkü bu yetenekler zaten yerleşiktir.

## Cursor için En İyi MCP'ler

1. **Context7** – güncel dokümantasyon
2. **GitHub MCP** – repo yönetimi
3. **Firecrawl MCP** – web scraping
4. **Figma MCP** – tasarımdan koda
5. **Playwright MCP** – tarayıcı otomasyonu

> Not: Cursor'da toplam **40 araç sınırı** vardır; bu yüzden 4–6 sunucudan fazlası önerilmez.

---

**Not:** ⭐ = topluluk tarafından "devrim yaratan / oyun değiştiren" olarak kabul edilen MCP'ler.
**Freemium** = sunucu açık kaynak/ücretsiz ama servisin API anahtarı belli bir kullanımdan sonra ücretlidir.
