# Seçilen Araçların Kullanım ve Dokümantasyon Notları

Seçtiğim otonom geliştirme araçları olan **Claude Code** ve **Antigravity IDE** için resmi dokümantasyonlardan derlediğim, verimliliği artıran önemli kullanım bilgilerini ve pratik ipuçlarını buraya not aldım.

---

## 1. Claude Code (CLI) Dokümantasyon Özetleri

Claude Code, terminalden doğrudan Anthropic API'sini kullanarak çalışan otonom bir geliştirme asistanıdır.

### A. Kurulum ve Başlatma
Node.js ortamı yüklü ise terminalden şu komutla kurulur ve başlatılır:
```bash
npm install -g @anthropic-ai/claude-code
claude
```
*İlk çalıştırmada Anthropic API anahtarını tanımlamak veya tarayıcı üzerinden giriş yapmak gerekir.*

### B. Temel Komutlar ve Kullanım
Claude terminali açıldıktan sonra normal konuşma dilinde görevler verilebilir. Ayrıca özel slash komutları vardır:
- `/bug [hata mesajı]` — Belirtilen hatayı analiz eder ve projede ilgili dosyaları düzelterek çözer.
- `/explain [kod/sembol]` — Seçilen dosyanın veya fonksiyonun ne işe yaradığını detaylı açıklar.
- `/test` — Projedeki testleri tespit edip çalıştırır, kırılan testleri otomatik onarır.
- `/init` — Projeye özel kurallar ve hedefler belirleyen bir yapılandırma dosyası oluşturur.
- `/exit` — Claude Code oturumunu kapatır.

---

## 2. Antigravity IDE Kullanım Kılavuzu

Antigravity, yapay zeka agent yeteneklerini doğrudan geliştirme ortamına entegre eder.

### A. Agentic İş Akışı
Antigravity sadece kod yazmakla kalmaz, belirli araçlar (tools) kullanarak tüm süreci yönetir:
- **Planlama Aşaması:** Görev verildiğinde önce `implementation_plan.md` dosyası oluşturarak yapılacak adımları ve test planını kullanıcı onayına sunar.
- **Dosya İşlemleri:** `view_file` ile kodları okur, `replace_file_content` veya `multi_replace_file_content` ile nokta atışı düzenleme yapar (tüm dosyayı baştan yazmak yerine sadece değişen satırları değiştirerek API maliyetini azaltır).
- **Yürütme:** `run_command` ile sanal ortamı (venv) aktifleştirip kodları test eder.

### B. Slash Commands (Kısayollar)
Kullanıcı arayüzünde hızlı süreç yönetimi sağlayan komutlar:
- `/goal` — AI asistanına uzun süreli, otonom ve derinlemesine bir hedef tanımlar.
- `/grill-me` — AI asistanının planı uygulamadan önce tasarımı netleştirmek için kullanıcıyı soru-cevap mülakatına almasını sağlar.
- `/learn` — AI asistanının gelecekteki görevlerde de hatırlaması için projeye özel bir kuralı/öğrenimi kaydetmesini sağlar.

---

## 3. `.claudecoderules` ve Özel Kurallar (Rules) Kullanımı

AI agent'ların projenin tarzına, mimari kurallarına ve kod stiline uymasını sağlamak için kök dizinde kural dosyaları tanımlayabiliriz.

Örnek bir kural tanımlaması:
- Proje dizinine `.claudecoderules` veya `.cursorrules` dosyası oluşturulup içine şu tarz yönergeler yazılır:
  ```text
  - Python kodlarında her zaman UTF-8 terminal encoding uyumluluğu sağla.
  - Kodlarda placeholder (geçici kod) bırakma, çalışan tam sürümleri yaz.
  - Türkçe karakter ve emoji kullanımında cp1254 uyumluluğuna dikkat et.
  ```
- Agent bu dosyayı otomatik olarak okur ve tüm kod yazım süreçlerinde bu kurallara sadık kalır.

---

## 4. Güvenlik ve Limit Hatırlatmaları
- **Terminal Yetkileri:** Agent'lar terminalde komut çalıştırırken (örn: veritabanı silme, paket kurma) her zaman kullanıcıdan onay ister. Bilinmeyen komutları onaylamadan önce mutlaka göz ucuyla kontrol et.
- **API Token Tüketimi:** Otonom döngüler (hata ara -> düzelt -> tekrar test et) çok fazla token harcayabilir. Bu yüzden agent'a iş verirken hedefi olabildiğince daraltmak (örn: "tüm projeyi refactor et" yerine "BeautifulSoup scriptindeki veri kaydetme fonksiyonunu düzelt") API maliyetini düşürür.
