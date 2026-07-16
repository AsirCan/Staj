# Vibe Coding Nedir ve Yapay Zeka Destekli Yazılım Araçları

Son dönemde yazılım dünyasında "Vibe Coding" adı verilen yeni bir kavram ve çalışma kültürü ortaya çıktı. Bu notlarda, bu terimin ne anlama geldiğini, geleneksel yazılımdan farkını ve piyasadaki temel araçları inceledim.

---

## 1. Vibe Coding Nedir?

**Vibe Coding**, yazılımcının satır satır kod yazmak yerine, yüksek seviyeli mimari kararlar aldığı, yapay zekayı (AI Agent'ları) yönlendirdiği ve kodun yazılması, hata ayıklanması, test edilmesi gibi operasyonel süreçleri yapay zekaya devrettiği yeni nesil yazılım geliştirme paradigmasıdır.

- **Geleneksel Yazılım:** Yazılımcı algoritmayı kafasında kurar ve syntax (yazım) kurallarına göre satır satır kod yazar.
- **Yapay Zeka Destekli (Autocomplete/Chat):** GitHub Copilot gibi araçlar satır tamamlar veya yan paneldeki chat üzerinden parça kod üretir. Yazılımcı bu kodları kopyalayıp entegre eder.
- **Vibe Coding (Agentic):** Yazılımcı hedefi söyler (örn: "SQLite veritabanı ekle ve verileri buraya kaydet"). Yapay zeka aracı kendi kendine plan yapar, dosyaları bulur, içeriği düzenler, terminali açıp kodu test eder, hata çıkarsa kendi kendine düzeltir. Yazılımcı sadece süreci onaylar veya yönlendirir ("vibe eder").

---

## 2. Piyasada Öne Çıkan Vibe Coding ve Agent Sistemleri

Yapay zeka araçlarını yeteneklerine göre üç ana kategoride sınıflandırabiliriz:

### A. Terminal & Agent Tabanlı Araçlar (CLI/Agent)
- **Claude Code:** Anthropic tarafından geliştirilen, terminal üzerinde çalışan son derece güçlü bir AI agent aracı. Dosya sistemi okuma/yazma, terminal komutları çalıştırma, arama yapma ve projeyi sıfırdan ayağa kaldırma yeteneklerine sahiptir.
- **Aider:** Terminal üzerinden Git reposu ile entegre çalışan, doğrudan kod dosyalarını düzenleyen popüler açık kaynaklı bir komut satırı agent'ı.

### B. Özel Geliştirilmiş Agentic IDE'ler
- **Antigravity IDE:** Gelişmiş agentic kodlama yeteneklerine sahip, dosya okuma/yazma, terminal komutları yürütme, tarayıcı otomasyonu ve görsel arayüz tasarımı (UI generation) yapabilen akıllı kodlama asistanı.
- **Cursor:** VS Code çatallaması (fork) olarak geliştirilen, `@codebase` dizinleme, multi-file edit (composer) özellikleri sunan popüler AI entegreli kod editörü.
- **Windsurf (Codeium):** Cursor benzeri, "Cascade" adı verilen agent özelliği ile projeyi analiz edip bağımsız değişiklikler yapabilen yapay zeka editörü.

### C. Klasik Chat ve Otomatik Tamamlama Eklentileri
- **GitHub Copilot / Chat / Workspace:** VS Code içinde çalışan otomatik kod tamamlama ve sohbet asistanı.
- **Continue.dev / Cline:** VS Code içine kurulan, kendi API anahtarlarımızla (Claude, Gemini vb.) çalışan esnek agent eklentileri.

---

## 3. Temel Modeller ve Entegrasyon
Vibe coding araçları arka planda en güncel büyük dil modellerini (LLM) kullanır. Bu modellerin verimliliği, vibe coding deneyimini doğrudan etkiler:
- **Claude Fable:** Kod yazma mantığı, otonom hata analizi ve agent yetenekleri konusunda şu an sektörün en gelişmiş modelidir (özellikle Claude Code'un arkasındaki ana güçtür).
- **Gemini 1.5 Pro / 3.5 Flash:** Geniş bağlam penceresi sayesinde devasa kod tabanlarını tek seferde analiz etmede mükemmeldir (Antigravity'nin arkasındaki ana güçlerden biridir).
- **GPT 5.6:** Matematiksel mantık ve hızlı kod tamamlama işlerinde son derece kararlı ve hızlıdır (OpenAI'nin kendi **Codex IDE**'si ile bütünleşik olarak kullanılır).
