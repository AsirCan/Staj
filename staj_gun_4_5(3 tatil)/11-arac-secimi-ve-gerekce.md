# AI Kodlama Asistanı Seçimim ve Gerekçesi

Benchmark verilerini ve kendi çalışma ortamımı değerlendirdikten sonra staj projelerinde ve günlük yazılım geliştirme süreçlerimde kullanmak üzere yapay zeka destekli kodlama düzenimi belirledim.

---

## 1. Tercih Ettiğim Kurulum

Başka bir editöre (Cursor vb.) geçmek yerine, mevcut geliştirme ortamımı aşağıdaki iki otonom araç üzerine kurmayı tercih ettim:
1. **Antigravity IDE:** Gelişmiş agent yetenekleri sunan, kod yazıp terminalde test edebilen akıllı geliştirme ortamı.
2. **Claude Code (CLI):** Doğrudan terminal üzerinden çalışan, Git entegrasyonu olan ve hızlı kod düzenleme işlerinde kullanılan otonom CLI asistanı.

---

## 2. Neden Bu Kurulumu Seçtim? (Gerekçeler)

### A. Maliyet ve Mevcut Kaynakların Değerlendirilmesi
Cursor Pro gibi özel IDE'ler aylık 20$ gibi abonelik ücretlerine sahip. Benim halihazırda GPT, Claude ve Gemini modellerine (API veya Web üzerinden) erişimim var. 
- **Çözüm:** Antigravity ve Claude Code gibi araçlar, halihazırda sahip olduğum Claude Fable ile Gemini 1.5 Pro / 3.5 Flash modellerini tam potansiyeliyle (API üzerinden) kullanmamı sağlıyor. Ekstra bir IDE aboneliği ödemek zorunda kalmıyorum.

### B. Otonom Terminal ve Test Yeteneği
Basit sohbet eklentileri (klasik Copilot vb.) kod üretip bırakır; o kodu çalıştırmak, hataları okuyup kopyalamak yine yazılımcıya düşer.
- **Çözüm:** Claude Code ve Antigravity terminali okuyabilir, test komutlarını yürütebilir. Örneğin, scraping örneklerini çalıştırırken aldığım cp1254 karakter kodlaması hatasını bu araçlar terminal çıktısından okuyup koda otomatik `TextIOWrapper` ekleyerek çözdüler. Bu seviyede bir otonomi işleri inanılmaz hızlandırıyor.

### C. Proje ve Araç Esnekliği
Özel yapay zeka editörleri (Cursor vb.) seni kendi IDE arayüzüne kilitler. Oysa terminal tabanlı **Claude Code** ve akıllı agent ortamları her türlü IDE (VS Code, PyCharm vb.) ile yan yana çalışabilir. Geliştirici istediği editörde kalmaya devam ederken arka planda bu güçlü agent'ları terminalden çalıştırabilir.

---

## 3. "Tek Araç Fanatikliği" Yerine Duruma Göre Model Seçimi

Vibe coding yaparken tek bir araca veya modele bağlı kalmak mantıklı değil. Süreç içinde şu stratejiyi uyguluyorum:
- **Claude Fable (Claude Code ile):** Zor mantık hatalarını çözmek, sıfırdan algoritmalar yazmak ve API Reverse Engineering gibi karmaşık işlerde birinci tercihim.
- **Gemini 1.5 Pro / 3.5 Flash (Antigravity ile):** Projenin tamamını (tüm dizin yapısını, yazılmış tüm notları ve kodları) tek seferde analiz ettirmek ve büyük refactoring (kod düzenleme) kararları almak için geniş bağlam penceresini kullanıyorum.
- **GPT 5.6:** Hızlı prototip üretme, genel veri formatlama ve hızlı mantıksal sorgularda tercih ediyorum.
