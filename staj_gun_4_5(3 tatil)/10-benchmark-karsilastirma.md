# Vibe Coding Araçları Benchmark Karşılaştırması
### Güncelleme: 16 Temmuz 2026 verilerine göre yeniden yazılmıştır

---

## ⚠️ Önce: Orijinal tablodaki temel sorunlar

Karşılaştırmayı güncellerken dört yapısal sorunla karşılaştım, bunları düzelttim:

1. **"Aider Leaderboard" bir araç değil, model metriğidir.** Aider Polyglot benchmark'ı, Claude Code / Cursor / Antigravity gibi *araçları* değil, çıplak *LLM'leri* Aider'ın kendi harness'i içinde test eder. Bir IDE'ye "Aider Leaderboard: %85" gibi bir skor atamak metodolojik bir hata — her araç farklı bir model (hatta çoklu model) kullanıyor ve kendi agent harness'iyle çalışıyor.
2. **Resmi Aider Polyglot tablosu güncel değil.** aider.chat'teki resmi liste en son **20 Kasım 2025**'te güncellenmiş; Sonnet 5, Opus 4.8, Fable 5, Gemini 3.x veya GPT-5.6 gibi hiçbir 2026 modeli listede yok. En yüksek skor hâlâ GPT-5 (high) %88.0, en iyi Claude girdisi ise Mayıs 2025 tarihli eski Opus 4 (%72.0).
3. **Model isimleri güncelliğini yitirmiş.** "Claude Fable" Claude Code'un varsayılan modeli değil (varsayılan Sonnet 5'tir); Antigravity artık Gemini 1.5 değil Gemini 3.5 Flash kullanıyor; Codex Temmuz 2026 itibarıyla GPT-5.6 ailesine geçti.
4. **Cursor'un terminal erişimi yok iddiası yanlış.** Cursor'un Agent modu 2024 sonundan beri terminal komutlarını doğrudan çalıştırabiliyor; 2026'da Cloud/Background Agent'lar tamamen otonom şekilde izole VM'lerde terminal kullanıyor.

Aşağıdaki tablo ve analizler bu düzeltmeler ışığında yeniden yazıldı.

---

## 1. Güncellenmiş Karşılaştırma Tablosu

| Özellik | Claude Code (CLI) | Google Antigravity 2.0 | Cursor | OpenAI Codex | Cline (VS Code vb.) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Varsayılan / öne çıkan model** | Claude Sonnet 5 (varsayılan); Opus 4.8 (ağır işler); Fable 5 opsiyonel `/model fable`; Haiku 4.5 (hızlı) | Gemini 3.5 Flash (varsayılan, GA 19 Mayıs 2026); Gemini 3.1 Pro, Claude Sonnet 4.5, GPT-OSS seçenek olarak | Çoklu seçim: Claude, GPT, Gemini, Grok, DeepSeek + kendi modeli Composer 2.5 | GPT-5.6 ailesi (9 Temmuz 2026 GA): Sol / Terra / Luna | Çoklu seçim (BYOK): 30+ sağlayıcı — Claude, GPT, Gemini, yerel Ollama, OpenRouter |
| **Context window** | 200K standart; 1M (Opus/Sonnet 4.6 kuşağından itibaren GA, ek ücretsiz) | 1.048.576 token (Gemini 3.5 Flash), 65K max çıktı | Varsayılan ~200K (pratikte ~10-15K'ye kısaltılır); Max Mode modelin tam limitine çıkarır (bazı modellerde 1M) | 1.050.000 token (API); ürün arayüzünde daha düşük bir üst sınırla sunulabilir | Tamamen seçilen modele bağlı |
| **Çoklu dosya düzenleme** | 🟢 Tam otonom | 🟢 Tam otonom + paralel alt-agent orkestrasyon | 🟢 Tam otonom (Agent modu); Composer 2.5 ile ölçekli refactor | 🟢 Tam otonom; Ultra modda 4 paralel alt-agent | 🟢 Tam otonom (Plan/Act) |
| **Terminal kontrolü** | 🟢 Var — doğrudan (CLI'nin kendisi) | 🟢 Var — Antigravity CLI (`agy`) ve masaüstü uygulaması shell'i doğrudan çalıştırır | 🟢 Var — Agent modu komutları doğrudan çalıştırır; "Auto-run" ile tam otonom, Cloud/Background Agent izole VM'de çalışır | 🟢 Var — onay ayarları yapılandırılabilir | 🟢 Var — varsayılan onaylı, "auto-approve"/"YOLO" ile otonom |
| **Kullanım arayüzü** | CLI (terminal), VS Code/JetBrains eklentisi, masaüstü, web, mobil | Masaüstü uygulama + CLI + SDK + Managed Agents API | Özel IDE (VS Code fork'u) + `cursor-agent` CLI | CLI, IDE eklentisi, web, yeni birleşik ChatGPT masaüstü uygulaması (9 Temmuz 2026'dan itibaren) | VS Code eklentisi (ayrıca JetBrains, Cursor, Windsurf, Zed, Neovim, önizleme CLI) |
| **Fiyatlandırma (Temmuz 2026)** | API kullanım bazlı: Sonnet 5 $2/$10 (31 Ağu 2026'ya dek tanıtım fiyatı, sonra $3/$15), Opus 4.8 $5/$25, Fable 5 $10/$50; ayrıca Pro/Max abonelik planları | Bireysel kullanım ücretsiz; Google AI Ultra $100/ay (5x kullanım limiti) | Hobby ücretsiz; Pro $20/ay, Pro+ $60/ay, Ultra $200/ay, Teams $40/kullanıcı/ay, Enterprise özel | ChatGPT Plus/Pro/Business/Edu/Enterprise'a dahil; API: Sol $5/$30, Terra $2.5/$15, Luna $1/$6 (1M token) | Eklenti ücretsiz (açık kaynak); yalnızca kullanılan modelin API maliyeti |

---

## 2. Modellerin Güncel Benchmark Performansı

Bu tablo, yukarıdaki araçların **arkasındaki modellerin** aynı ölçütteki (mümkün olduğunca) performansını gösterir. 2026 ortası itibarıyla SWE-bench Verified artık **doymuş ve kısmen kontamine** kabul ediliyor (OpenAI kendi ölçümlerini bu ölçütten çekti); bu yüzden Scale AI'ın **SWE-bench Pro**'su ve ajan/terminal görevleri için **Terminal-Bench 2.1** daha anlamlı referanslar haline geldi.

| Model | SWE-bench Pro (vendor-aggregate, Haz–Tem 2026) | Terminal-Bench 2.1 | Not |
| :--- | :--- | :--- | :--- |
| **Claude Fable 5** | %80.3 (en yüksek aktif skor) | — | Cyber/bio/kimya sorgularında güvenlik sınıflandırıcısı otomatik olarak Opus 4.8'e düşer |
| **Claude Opus 4.8** | %69.2 | — | Claude Code'daki "ağır iş" modeli |
| **Claude Sonnet 5** | %63.2 | — | Claude Code'un varsayılanı |
| **GPT-5.6 Sol** | %64.6 | %88.8 (Ultra modda %91.9) | Codex'in en güçlü katmanı |
| **GPT-5.6 Terra** | %63.4 | — | Codex'in dengeli katmanı |
| **GPT-5.6 Luna** | %62.7 | — | Codex'in hızlı/ucuz katmanı |
| **Gemini 3.5 Flash** | — | %76.2 | Antigravity 2.0'ın varsayılanı; MCP Atlas %83.6 |

> **Not:** Bu rakamlar büyük ölçüde satıcı tarafından bildirilen (vendor-reported) veya üçüncü taraf agregatör sitelerinden derlenmiş rakamlardır; farklı scaffold/harness'ler kullanıldığından bire bir karşılaştırılabilir değildir. 2026 ortasında SWE-bench/Aider/Terminal-Bench ekosistemi oldukça parçalı durumda — aynı model için kaynaktan kaynağa 10-20 puanlık farklar görebilirsiniz. Kesin ve güncel sayılar için swebench.com ve aider.chat/docs/leaderboards resmi sayfalarına bakılması önerilir.

---

## 3. Metrik Analizleri

### A. Aider Leaderboard — neden doğrudan kullanılamıyor
Aider Polyglot, 225 zor Exercism görevini 6 dilde (C++, Go, Java, JavaScript, Python, Rust) test eder ve *modelleri* Aider'ın kendi diff/edit formatı üzerinden puanlar. Resmi tablo Kasım 2025'ten beri güncellenmemiş olduğu için bugünün modellerini (Sonnet 5, Opus 4.8, Fable 5, GPT-5.6, Gemini 3.5) içermiyor. Üçüncü taraf siteler daha yeni sayılar bildirse de (ör. Opus 4.5 için %89.4 iddiası), bunlar Aider'ın kendi resmi koşumundan değil, satıcı beyanlarından derleniyor — yani orijinal tablodaki gibi bunu doğrudan bir "araç" metriği olarak sunmak yanıltıcı olur.

### B. SWE-bench'in dönüşümü: Verified → Pro
SWE-bench Verified, üst düzey modellerin %85-95 bandında kümelenmesiyle ayırt edicilik gücünü kaybetti; OpenAI'ın kendi denetimi, "çözülemeyen" en zor sorunların %59'unda hatalı test senaryoları olduğunu ortaya çıkardı. Bu yüzden 2026'da endüstri, Scale AI'ın kontaminasyona dirençli **SWE-bench Pro**'suna (1.865 gerçek görev, 41 profesyonel repo) kaydı. Bu ölçütte skorlar %55-80 bandına düşüyor — yani "hangi araç gerçekten daha iyi kod yazıyor" sorusuna daha gerçekçi bir cevap veriyor.

### C. Context Window ve Kod Tabanı Dizinleme
- **Gemini 3.5 Flash** (Antigravity 2.0) 1.048.576 token'lık pencereyle geliyor — tüm orta ölçekli bir kod tabanını tek seferde görebiliyor.
- **Claude Code**, Opus/Sonnet 4.6 kuşağından itibaren 1M token pencereyi standart fiyata (ek "uzun bağlam" primi olmadan) GA olarak sunuyor.
- **GPT-5.6**, API'de 1.05M token pencereye sahip; Codex ürün yüzeyinde bu genellikle daha düşük bir sınırla (önceki nesilde 400K) sunuluyordu — GPT-5.6 için ürün-seviyesi sınır henüz net biçimde belgelenmedi.
- **Cursor**, varsayılan modda pratikte ~10-15K token'a kısaltıyor; "Max Mode" açıldığında modelin tam kapasitesine (bazı modellerde 1M'e kadar) çıkıyor ama bu modda token başına API fiyatlandırması geçerli oluyor.
- **Cline**, kendi context limiti yok — tamamen kullanıcının seçtiği modele bağlı.

### D. Otonom Yetenekler (Agentic Power) — düzeltilmiş görünüm
2025 sonu/2026 başı itibarıyla **tüm beş araç da** terminal komutlarını çalıştırabiliyor; farklılık *ne kadar onay gerektiği* ve *paralellik* düzeyinde:
- **Claude Code**: CLI olduğu için terminal zaten ana arayüz; agent team'ler saatler süren otonom oturumlar çalıştırabiliyor.
- **Antigravity 2.0**: Masaüstü + CLI + tarayıcı alt-agent'ı ile UI doğrulaması dahil uçtan uca otonomi; zamanlanmış (cron benzeri) arka plan görevleri de var.
- **Cursor**: Agent modu varsayılan olarak adım adım onay istiyor, ama "Auto-run" (eski adıyla YOLO mod) ve Cloud/Background Agent'lar tamamen otonom çalışıyor; Mayıs 2026'da Cloud Agents ile izole VM'lerde tam bağımsız çalışma geldi.
- **Codex**: Onay seviyeleri yapılandırılabilir; Ultra modda 4 paralel alt-agent ile geniş refactor'lar hızlandırılıyor.
- **Cline**: Felsefe gereği varsayılan olarak her adımda onay ister (en "temkinli" araç), ama auto-approve/"Lazy Teammate Mode" ile bu kapatılabiliyor.

---

## 4. Diğer Popüler Vibe Coding Araçları

İlk tablo yalnızca 5 aracı kapsıyordu; ama ekosistem çok daha geniş. İşte sık karşılaşılan diğer araçlar:

| Araç | Model(ler) | Terminal Kontrolü | Fiyatlandırma (Temmuz 2026) | Not |
| :--- | :--- | :--- | :--- | :--- |
| **GitHub Copilot** | Çoklu seçim: Claude Opus 4.5–4.8, Sonnet 4–4.6, Haiku 4.5, Fable 5; GPT-5.5, GPT-5.4, GPT-5.3-Codex; Gemini 3.5 Flash, Gemini 3.1 Pro; Microsoft'un kendi **MAI-Code-1-Flash**'ı | 🟢 Var — Agent modu VS Code + JetBrains'te GA (Mart 2026'dan beri) | Free (sınırlı); 1 Haziran 2026'dan beri kullanım bazlı "AI Credit" (1 kredi = $0.01): Pro $10/ay, Pro+ $39/ay, yeni Max $100/ay, Business $19/kullanıcı, Enterprise $39/kullanıcı | En geniş model seçimine sahip araç; GitHub/VS Code'a doğal entegre |
| **Windsurf → Devin Desktop (Cognition)** | Kendi modeli **SWE-1.6** (varsayılan, Cerebras donanımında ~950 tok/sn) + Claude, GPT, Gemini seçenekleri | 🟢 Var — Cascade / Devin Local ajanı doğrudan terminal çalıştırır | Free, Pro $20/ay, Max $200/ay, Teams $40-80/kullanıcı, Enterprise özel | 2 Haziran 2026'da Windsurf'ten Devin Desktop'a yeniden markalandı; eski Cascade ajanı 1 Temmuz 2026'da emekli edildi, yerini Devin Local aldı |
| **AWS Kiro** | Claude Sonnet 4.5 tabanlı | 🟢 Var | Free: 50 kredi/ay | Amazon'un "spec-driven" (özellik/şartname odaklı) IDE'si |
| **Kilo Code** | Çoklu seçim (BYOK): 500+ model, sıfır komisyonla | 🟢 Var | Açık kaynak, ücretsiz eklenti (MIT) — yalnızca API maliyeti | Cline ailesinden; VS Code + JetBrains |
| **OpenCode** | Çoklu seçim (BYOK) | 🟢 Var | Açık kaynak, ücretsiz (MIT) | En çok GitHub yıldızına sahip açık kaynak ajan (172K+) |
| **Aider (CLI)** | Çoklu seçim (BYOK) | 🟢 Var (terminal-native) | Açık kaynak, ücretsiz (Apache-2.0) | Bu belgedeki "Aider Leaderboard" ölçütünün asıl kaynağı olan araç |
| **Goose (Block)** | Çoklu seçim (BYOK), MCP entegrasyonu | 🟢 Var | Açık kaynak, ücretsiz (Apache-2.0) | Square/Cash App'in arkasındaki Block tarafından geliştirildi; Linux Foundation'a taşındı |
| **Google Gemini CLI → Antigravity CLI** | Gemini modelleri | 🟢 Var | Kişisel hesapta ücretsiz (günde 1.000 istek) | Gemini CLI, 18 Haziran 2026'dan itibaren ücretsiz/Pro istekleri durduruyor; yerini Antigravity CLI (`agy`) alıyor |

---

## 5. Sadece GPT/Claude/Gemini Değil: Ekosistemdeki Diğer Modeller

Yukarıdaki araçların çoğu (özellikle Cursor, Cline, Kilo Code, OpenCode, Copilot) tek bir sağlayıcıya kilitli değil — BYOK ile istediğiniz modeli takabiliyorsunuz. En sık karşılaşılan "büyük 3 dışı" modeller:

| Model / Aile | Geliştirici | Nerede kullanılıyor | Öne çıkan benchmark notu |
| :--- | :--- | :--- | :--- |
| **DeepSeek (V3.2 / R1 / V4)** | DeepSeek (Çin) | Cursor, Cline, Kilo Code, OpenCode, Aider | Aider Polyglot'ta $1.3 maliyetle %74.2 — en iyi fiyat/performans oranlarından biri; V4 Pro Max SWE-bench Verified'de %80.6 (açık ağırlıklı modeller arasında lider adaylarından) |
| **Grok (xAI)** | xAI | Cursor | Grok 4 (high): Aider Polyglot %79.6 |
| **Qwen (Alibaba)** | Alibaba | Cline, Kilo Code, OpenCode (Ollama/OpenRouter üzerinden) | Qwen3.6 Plus: SWE-bench Verified %78.8 |
| **Kimi K2 / K2.5 / K2.6** | Moonshot AI | Cline, Kilo Code, OpenCode | Kimi K2.6: SWE-bench Verified %80.2 (açık ağırlıklı) |
| **GLM (Zhipu AI)** | Zhipu AI | Cline, Kilo Code, OpenCode | GLM-5.2: FrontierSWE'de Opus 4.8'e yalnızca 0.7 puan geride, GPT-5.5'i geçiyor (%74.4 vs %72.6), çıktı token'ı başına $4.40 |
| **MiniMax (M2.5/M2.7)** | MiniMax | Cline, Kilo Code | MiniMax M2.5: SWE-bench Verified %80.2, açık ağırlıklı modeller arasında üst sırada |
| **Mistral (Codestral, Medium 3.5)** | Mistral AI | Cline, Kilo Code, OpenCode | Mistral Medium 3.5: SWE-bench Verified %77.6 |
| **Llama** | Meta | Cline, Kilo Code, OpenCode (Ollama ile yerel) | Genelde yerel/gizlilik odaklı kullanım için tercih ediliyor |
| **GPT-OSS** | OpenAI (açık ağırlıklı) | Antigravity (ilk sürümü) | OpenAI'ın açık kaynak modeli; ücretsiz/yerel çalıştırılabilir |
| **SWE-1.6** *(özel/proprietary)* | Cognition | Windsurf / Devin Desktop | Cerebras donanımında ~950 tok/sn; SWE-1.5'e göre SWE-bench Pro'da %10+ iyileşme |
| **Composer 2.5 / Composer-1 / Sonic** *(özel/proprietary)* | Cursor (Anysphere) | Cursor | Artificial Analysis Coding Agent Index'te 62 puan (yalnızca üst düzey Opus varyantlarının gerisinde), görev başına $0.07 ile en ucuz yüksek-puanlı ajanlardan |
| **MAI-Code-1-Flash** *(özel/proprietary)* | Microsoft | GitHub Copilot | Sürekli güncellenen bir model; performansı zamanla değişebilir |

> **Genel çıkarım:** 2026 ortasında "vibe coding" ekosistemi artık üç büyük laboratuvarla (OpenAI/Anthropic/Google) sınırlı değil. Çin merkezli DeepSeek/Qwen/Kimi/GLM/MiniMax modelleri özellikle **fiyat/performans** açısından güçlü rakip haline geldi; ayrıca Cognition (Windsurf/Devin) ve Cursor gibi araç şirketleri artık kendi özel/proprietary modellerini geliştirip varsayılan olarak sunuyor.

---

## 6. Kısa Özet Tablosu — Hangi Araç Ne Zaman Mantıklı?

| Senaryo | Önerilen araç |
| :--- | :--- |
| Terminal-native, derin CI/CD otomasyonu, MCP entegrasyonu | Claude Code |
| Google ekosistemi (Firebase/Android/AI Studio), çok ajanlı paralel görevler | Antigravity 2.0 |
| Görsel IDE deneyimi + model seçme özgürlüğü | Cursor |
| ChatGPT ekosistemine bağımlı ekipler, GitHub PR/code review odaklı | Codex |
| Ücretsiz/açık kaynak, kendi API anahtarınla tam kontrol | Cline |

---

## Kaynaklar
- Aider LLM Leaderboards (resmi) — aider.chat/docs/leaderboards
- Anthropic — Claude modelleri genel bakış ve Claude Code model yapılandırma dokümantasyonu (platform.claude.com, code.claude.com)
- Google — I/O 2026 geliştirici duyuruları, Antigravity 2.0 ve Gemini 3.5 Flash model kartı (blog.google, deepmind.google, ai.google.dev)
- OpenAI — GPT-5.6 duyurusu ve Codex değişiklik günlüğü (openai.com, developers.openai.com)
- Cursor — resmi model/fiyatlandırma dokümantasyonu (cursor.com/docs)
- Cline — resmi GitHub deposu (github.com/cline/cline)
- GitHub — Copilot desteklenen modeller dokümantasyonu ve resmi fiyatlandırma sayfası (docs.github.com, github.com/features/copilot/plans)
- Cognition / Windsurf — Devin Desktop rebranding ve SWE-1.6 duyuruları (çeşitli üçüncü taraf incelemeler, Haziran 2026)
- SWE-bench Pro / Terminal-Bench 2.1 / genel model karşılaştırma agregatörleri (morphllm.com, codingfleet.com, lushbinary.com, firecrawl.dev) — vendor-reported rakamlar, dikkatle ele alınmalı

*Bu belge 16 Temmuz 2026 tarihli web araması sonuçlarına dayanmaktadır. AI araç ekosistemi haftalık hızla değiştiği için sayıları kullanmadan önce ilgili resmi sayfaları tekrar kontrol etmeniz önerilir.*
