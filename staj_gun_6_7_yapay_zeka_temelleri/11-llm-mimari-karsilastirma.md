# Popüler LLM Mimarilerinin Karşılaştırılması

Modern büyük dil modellerinin (LLM) çoğu, Transformer'ın çekirdek fikrini paylaşıyor ama her aile kendi optimizasyonlarını, mühendislik seçimlerini ve mimari geliştirmelerini getiriyor. Aşağıda önemli LLM ailelerinin mimarileri karşılaştırılıyor ve öne çıkan farklar tartışılıyor.

Karşılaştırılan aileler:

- **GPT (OpenAI):** GPT-3.5, GPT-4, GPT-4o, o1/o3 (reasoning modelleri)
- **Claude (Anthropic):** Claude 3.5, Claude 4, Claude 5
- **Gemini (Google):** 1.5, 2.0, 2.5
- **Llama (Meta):** 2, 3, 3.1, 3.2, 3.3
- **Mistral / Mixtral (Mistral AI):** 7B, Mixtral 8x7B, Mixtral 8x22B, Codestral
- **DeepSeek (DeepSeek AI):** V2, V3, R1
- **Qwen (Alibaba):** 2, 2.5, 3

Kapalı kaynaklı modellerde (GPT, Claude, Gemini) mimari detayları çoğu zaman şirketler tarafından paylaşılmıyor; bilgi sızıntılara, resmi yarım tanıtımlara ve genel eğilim çıkarımlarına dayalı. Açık kaynak modellerde (Llama, Mistral, DeepSeek, Qwen) tam mimari netliği var.

---

## Karşılaştırma Tablosu (Kaba Halde)

| Model | Tür | Attention | Positional | FFN Aktivasyon | MoE | Norm |
|-------|-----|-----------|------------|----------------|-----|------|
| GPT-3 | Decoder | Standart MHA | Learned | GELU | Yok | LayerNorm |
| GPT-4 (tahmin) | Decoder | (?) | (?) | (?) | Var (8x110B?) | (?) |
| Claude 3+ | Decoder | (?) | (?) | (?) | (?) | (?) |
| Gemini 1.5 | Decoder | Sparse (?) | (?) | (?) | Var | (?) |
| Llama 3 | Decoder | GQA | RoPE | SwiGLU | Yok | RMSNorm |
| Mistral 7B | Decoder | GQA + SWA | RoPE | SwiGLU | Yok | RMSNorm |
| Mixtral 8x7B | Decoder | GQA | RoPE | SwiGLU | Var (8 exp, top-2) | RMSNorm |
| DeepSeek V3 | Decoder | MLA | RoPE | SwiGLU | Var (256 exp + shared) | RMSNorm |
| Qwen 2.5 | Decoder | GQA | RoPE | SwiGLU | Çoğu sürümde yok | RMSNorm |

Kısaltmalar:
- **MHA:** Multi-Head Attention (klasik)
- **GQA:** Grouped-Query Attention
- **MQA:** Multi-Query Attention
- **MLA:** Multi-head Latent Attention (DeepSeek'in buluşu)
- **SWA:** Sliding Window Attention
- **MoE:** Mixture of Experts
- **(?):** kapalı, resmi bilgi yok

---

## Kavramların Açıklaması

Tablodaki teknik terimleri kısa kısa açıklayayım.

### Attention Varyantları

**MHA (Multi-Head Attention):** Orijinal Transformer'daki klasik yapı. Her başlığın kendi K, V matrisleri var. Kaliteli ama KV-cache belleği çok yer kaplar. Inference'ta bu bellek darboğaz olabilir.

**MQA (Multi-Query Attention):** Tüm başlıklar tek bir K, V paylaşır. Sadece Q'lar farklıdır. KV-cache neredeyse `1/n_heads` oranında küçülür. Kalitede küçük bir düşüş olur ama servis maliyeti dramatik biçimde azalır. PaLM ile popülerleşti.

**GQA (Grouped-Query Attention):** MQA ile MHA arasında bir orta yol. Başlıklar `g` gruba ayrılır; her grup bir K/V paylaşır. Örneğin 32 başlık için 8 grup (yani 4 başlık başına bir K/V). Llama-2 70B ile popülerleşti, artık standart. Kalite/verimlilik dengesi en iyi seçenek olarak görülüyor. Llama 3, Mistral, Qwen — hepsi kullanıyor.

**MLA (Multi-head Latent Attention):** DeepSeek'in V2 modelinde tanıttığı yenilik. K ve V'yi düşük boyutlu bir "latent" uzaya sıkıştırıp saklıyor; attention hesabı sırasında dinamik olarak genişletiliyor. KV-cache boyutu dramatik biçimde küçülüyor, hem de kalite düşüşü olmadan (hatta bazı ölçütlerde iyileşerek). DeepSeek V3'ün ucuza servis edilebilmesinin sebeplerinden biri. Yeni ve etkili bir buluş; muhtemelen diğer laboratuvarlar da adapte edecek.

**SWA (Sliding Window Attention):** Her token sadece kendisinden önceki `W` (pencere) kadar tokene bakar. Attention maliyeti `O(n · W)` oluyor, `O(n²)` yerine. Ama katmanlar üst üste geldikçe "efektif" bağlam genişliyor — 4. katmandaki bir token, birinci katmanın bilgisini `W` kadar geriye taşıyabiliyor. Mistral 7B'nin ana yeniliği. Uzun bağlamlarda bellek dostu.

**FlashAttention:** Mimari değil, **implementation optimizasyonu**. Attention hesabını GPU üzerinde bellek-verimli ve numerik olarak stabil biçimde çalıştıran bir algoritma. Neredeyse tüm modern eğitim/inference kütüphaneleri altta bunu kullanıyor. FlashAttention-2, FlashAttention-3 sürümleri daha da hızlı.

### Positional Encoding

**Öğrenilebilir absolute embedding:** GPT-2, GPT-3 kullandı. Basit ama eğitim uzunluğunu geçemez.

**RoPE (Rotary Positional Embedding):** Llama, Mistral, DeepSeek, Qwen, ChatGLM — hepsi kullanıyor. Q ve K vektörlerini pozisyona göre döndürerek relatif konum bilgisini attention hesabına gömüyor. Uzun bağlamlara extrapolate etme yeteneği var. 128K, 200K, 1M bağlamlı modellerin çoğu RoPE tabanlı.

**ALiBi (Attention with Linear Biases):** Basit alternatif — attention skorlarına mesafe cezası ekle. MPT modelleri kullandı. RoPE kadar yaygınlaşmadı.

### FFN Aktivasyon

**GELU + Linear:** Klasik. BERT, GPT-2, GPT-3.

**SwiGLU:** Modern LLM'lerin ekmeği. Llama, Mistral, Qwen, DeepSeek hepsi kullanıyor. Kaliteli ama biraz daha çok parametre içeriyor.

### Norm

**LayerNorm:** Orijinal Transformer.

**RMSNorm:** Llama ile popülerleşti. Mean çıkarımını atlıyor, sadece RMS'e bölüyor. Bir işlem az, hesap %10-20 daha hızlı, eşit kalitede.

### MoE (Mixture of Experts)

Klasik Transformer'da her tokenın aynı FFN'den geçmesi zorunlu. MoE bu yapıyı değiştiriyor: tek bir büyük FFN yerine N tane küçük FFN ("expert") ve bir router. Router her token için hangi 1-2 expert'ın çalışacağına karar veriyor (top-k routing).

- **Aktif parametre << toplam parametre.** Mixtral 8x7B toplam 47B parametre ama inference'ta her token için sadece ~13B kullanıyor.
- **Kazanç:** aynı FLOPs (hesap) bütçesiyle çok daha yüksek kapasite. Model "büyük" ama "hızlı" davranıyor.
- **Kayıp:** eğitim daha çetrefilli (load balancing, expert collapse dertleri), inference'ta yine de tüm 47B parametre bellekte olmak zorunda.
- **Kullananlar:** Mixtral, DeepSeek V3, GPT-4 (tahmin), Gemini 1.5.

---

## Aile Aile İnceleme

### GPT Ailesi (OpenAI)

- **GPT-3 (2020):** 175B parametre, 96 katman, `d_model = 12288`. Tamamen klasik Transformer decoder — MHA, learned positional embedding, GELU FFN. O tarih için devasa bir ölçekleme.
- **GPT-3.5 / ChatGPT (2022):** GPT-3 tabanlı ama RLHF (Reinforcement Learning from Human Feedback) ile insana hizalanmış. Mimari değişikliği kısıtlı; asıl fark eğitim sürecinde.
- **GPT-4 (2023):** Ayrıntılar resmi olarak paylaşılmadı. Genel tahmin: MoE (8 x 110B expert, top-2 routing gibi), 1.8T toplam parametre. Multimodal yetenekler (görüntü + metin).
- **GPT-4o (2024):** Multimodal (metin + görüntü + ses) native olarak — ses ve görüntü ayrı encoderla değil, tek bir modelde işleniyor. Detay yine kapalı.
- **o1, o3 (2024-2025):** Reasoning modelleri. Mimari klasik Transformer ama eğitim ve inference paradigması farklı: model normal cevap üretmeden önce uzunca bir "düşünce zinciri" (chain of thought) üretiyor. Bu düşünce sırasında test-time compute yatırım yapılıyor.

### Claude Ailesi (Anthropic)

- Mimari detaylar büyük ölçüde kapalı.
- Kesin bilinen: decoder-only Transformer tabanlı, constitutional AI eğitim metodolojisi, geniş bağlam (200K token).
- Claude 3.5, 4, 5 sürümlerinde giderek artan reasoning, kod, matematik yeteneği.
- Claude 4/5 "extended thinking" modu — o1 benzeri düşünme zinciri.
- MoE kullanıp kullanmadığı doğrulanmadı.

### Gemini Ailesi (Google DeepMind)

- Gemini 1.0'dan itibaren multimodal (metin + görüntü + ses + video native).
- **Gemini 1.5 Pro:** 1M token bağlam. Bu boyuta ulaşmak için Sparse Mixture of Experts, ring attention gibi teknikler kullanılıyor gibi (kesin doğrulanmadı).
- **Gemini 2.0, 2.5:** Reasoning yeteneği, agent yetenekleri (tool use, computer use) öne çıkıyor.
- 1M bağlam pratikte kullanılabilir mi ayrı bir soru — "lost in the middle" problemi (uzun bağlamın ortasındaki bilginin unutulması) hâlâ araştırılan bir konu.

### Llama Ailesi (Meta)

En detaylı bildiğimiz aile, çünkü açık kaynak ve tech report'lar yayınlıyor.

- **Llama 2 (2023):** 7B, 13B, 70B varyantları. 70B GQA kullanıyor, küçükler MHA. RoPE, SwiGLU, RMSNorm.
- **Llama 3 (2024):** 8B, 70B, 405B. Tümü GQA. Bağlam 8K → sonrasında 128K'ya genişletildi. Tokenizer 32K → 128K'ya çıkarıldı (çok dilli iyileşme).
- **Llama 3.1 / 3.2 / 3.3:** İnce ayar, veri kalitesi geliştirmeleri, multimodal (3.2 vision).
- Meta çok değerli teknik raporlar yayınlıyor: veri karışımı, training dinamikleri, RLHF metodolojisi.

### Mistral Ailesi (Mistral AI)

Fransız laboratuvarı, hızlı ve zarif modelleriyle tanınıyor.

- **Mistral 7B (2023):** GQA + Sliding Window Attention. Küçük ama Llama-2 13B'yi çoğu benchmark'ta geçiyordu. SWA'nın popülerleşmesinde belirleyici.
- **Mixtral 8x7B (2023):** İlk büyük ölçekli açık MoE modeli. 47B toplam, ~13B aktif. Kalite/hız oranı olağanüstü.
- **Mixtral 8x22B:** Daha büyük MoE.
- **Codestral:** Kod için özel eğitilmiş varyant.
- **Mistral Large 2:** Kapalı, ticari.

### DeepSeek Ailesi (DeepSeek AI)

Çin merkezli, açık ağırlıklarını yayınlayan ve son 1-2 yılın en dikkat çekici modellerini üreten laboratuvar.

- **DeepSeek V2 (2024):** MLA'yı ilk tanıtan model. Fine-grained expert MoE (birçok küçük expert + shared expert).
- **DeepSeek V3 (2024):** 671B toplam, ~37B aktif MoE. GPT-4 sınıfına yakın performans. Auxiliary-loss-free load balancing (kendi buluşları).
- **DeepSeek R1 (2025):** Reasoning modeli. o1 benzeri düşünce zinciri, ama tamamen açık ağırlıklarla. Reinforcement learning tabanlı eğitim (Group Relative Policy Optimization).

DeepSeek'in belki en dikkat çekici yanı: mimari inovasyon (MLA) + verimlilik odaklı mühendislik (FP8 eğitim, MoE optimizasyonları) + açık paylaşım kombinasyonu. Bir modeli GPT-4 sınıfına yakın performansta ~5.5M dolara eğitebildiklerini raporluyorlar — sektör ortalamasının çok altında.

### Qwen Ailesi (Alibaba)

- Çin merkezli, güçlü çok dilli (Türkçe dahil) yetenek.
- **Qwen 2.5 (2024):** 0.5B'den 72B'ye kadar boyutlar. Standart Llama benzeri mimari — decoder-only, GQA, RoPE, SwiGLU, RMSNorm.
- **Qwen 3 (2025):** Daha büyük, MoE varyantları da geliyor.
- Kod (Qwen-Coder), matematik (Qwen-Math) için özelleşmiş sürümler.
- Küçük modellerin (0.5B, 1.5B, 3B) kalitesi kişisel donanımda çalıştırmak için ideal.

---

## Öne Çıkan Fikirler

Bu ailelerdeki mimari yeniliklerin bir kısmının yaygınlaşması bekleniyor. Öne çıkan dördü:

### DeepSeek'in MLA'sı

KV-cache LLM inference'ının en büyük bellek yiyicilerinden biri. GQA bunu 4-8x küçültüyor ama MLA çok daha agresif — K/V'yi bir latent uzayda temsil edip ihtiyaç halinde genişletiyor. Kaliteden neredeyse hiç ödün vermeden bellek dramatik düşüyor.

Somut bir örnek: 32K bağlamda klasik MHA ile bir 70B modelin KV-cache'i 20+ GB olabilir. MLA ile bu 5 GB'a inebiliyor. Bu, aynı GPU'da 4 kat daha fazla eşzamanlı sohbet demek — servis maliyeti çok düşüyor.

### Mistral'ın Sliding Window Attention + Rolling Buffer

SWA hem hesap hem bellek açısından bir kazanç. Her katmanda `O(W)` bakışla `O(n)` toplam hesap. Katmanlar üst üste geldikçe efektif bağlam büyüyor. KV-cache'i rolling buffer olarak tutabiliyorsun — sabit bellek, sonsuz uzunlukta stream işleme imkanı.

### DeepSeek V3'ün Load Balancing Yaklaşımı

MoE'de router'ın yükü expertlara adil dağıtması gerekir. Yoksa bazı expert'lar sürekli meşgul olur, diğerleri boş kalır — model yarım kapasite çalışır. Klasik çözüm: auxiliary loss (yükü dengelemeye zorla). DeepSeek V3 bu ekstra loss'u atmış, yerine router'a bias ekleyip dinamik olarak ayarlıyor. Eğitim daha stabil, kalite daha iyi.

### Reasoning Modelleri (o1, R1, Claude Extended Thinking)

Bu bir mimari değişikliği değil, **paradigma değişikliği**. Aynı Transformer'ı kullanıyorlar ama eğitim ve inference stratejisi farklı. Model normal cevap üretmeden önce uzun bir "düşünme" (chain of thought) üretiyor, sonra sonucu yazıyor.

- Eğitim: chain of thought'lu cevaplar üzerinde ince ayar + RL (reinforcement learning) ile "iyi düşünen" davranışları pekiştirme.
- Inference: model daha çok token üretiyor (10x, 100x fazla) → daha çok hesap → daha iyi cevap.

Bu 2024-2025'in en büyük paradigma değişimlerinden biri. Ölçekleme sadece **eğitim zamanı** hesabında değil, **inference zamanı** hesabında da yapılabiliyor. GPT-o1, DeepSeek R1, Claude "extended thinking", Gemini "thinking" — hepsi bu yolda.

---

## Diğer Modellerin Kullanmadığı Fikirler

Belirli bir aileye özgü olan ama diğerlerine henüz yayılmamış birkaç şey:

- **MLA (DeepSeek özel).** Muhtemelen kısa süre içinde diğer laboratuvarlar da adapte edecek. Kazanç çok belirgin.
- **Mamba / State-Space Modelleri.** Transformer değil — attention yerine "state-space" dinamik sistemi kullanıyor. `O(n)` maliyet, çok uzun bağlama uygun. Mamba-2, Jamba (hibrit), Zamba gibi modeller ortaya çıkıyor. Ama saf LLM performansında hâlâ Transformer'ın gerisinde.
- **BitNet / Ternary Weights.** Microsoft'un araştırması. Ağırlıklar sadece {-1, 0, +1} olabilir. Bellek 32x küçülüyor. Prod'da yaygın değil ama enerji tasarrufu açısından ilginç.
- **Diffusion Language Models.** Metni sağdan sola değil, gürültüden temizleyerek üretme fikri. Şimdilik küçük ölçekli, araştırma aşamasında.

---

## Bir Genel Gözlem: LLM ≠ Sadece Mimari

Modern LLM'ler karşılaştırılırken sadece mimariye bakmak yanıltıcı. Bir modelin kalitesini belirleyen faktörler:

1. **Mimari** — %10-20 katkı (Transformer varyantları arasında).
2. **Ölçek** — parametre sayısı × eğitim tokeni.
3. **Veri kalitesi** — trilyonlarca token, ama iyi temizlenmiş, iyi filtrelenmiş.
4. **İnce ayar (post-training):** SFT (Supervised Fine-Tuning) + RLHF/DPO/KTO gibi hizalama algoritmaları. Bu adım "helpful, harmless, honest" bir asistanı üretiyor.
5. **Inference altyapısı:** KV-cache optimizasyonları, batching, speculative decoding, sistem prompt tasarımı, tool use altyapısı.

Yani "Llama 3 8B vs Qwen 2.5 7B daha iyi mi" sorusunun cevabı mimariye değil, yukarıdaki her katmandaki mühendislik kalitesine bağlı. Ve bunun için birçok benchmark var:

- **MMLU:** çok konulu sınav soruları
- **GPQA:** graduate-level bilim soruları
- **HumanEval, MBPP:** kod üretimi
- **GSM8K, MATH:** matematik
- **BBH:** akıl yürütme
- **LMSYS Arena:** insan tercihine dayalı Elo puanı — belki en gerçekçi

Otomatik benchmark'lar bir modelin bir kısım yeteneklerini ölçüyor ama pratikte kullanmak için LMSYS Arena Elo daha gerçekçi bir sinyal veriyor.

---

## Kısaca

- Modern LLM'lerin çoğu benzer bir formülü paylaşıyor: **Decoder-only Transformer + RoPE + SwiGLU + RMSNorm + GQA + (varsa) MoE**.
- Farkı yaratan asıl şeyler: ölçek, veri kalitesi, hizalama, inference altyapısı.
- Mimari inovasyon bitmedi — MLA (DeepSeek), SWA (Mistral), reasoning modelleri (o1/R1) gibi buluşlar hâlâ oluyor.
- Açık kaynak modeller (Llama, Mistral, DeepSeek, Qwen) kapalı modellere yakın performansta; bazı ölçütlerde geçiyorlar.
- Sektörün büyük eğilimi: multimodal, çok uzun bağlam, reasoning, agent yetenekleri.

## Kaynaklar

- Llama 3 tech report: https://ai.meta.com/research/publications/the-llama-3-herd-of-models/
- Mistral 7B paper: https://arxiv.org/abs/2310.06825
- Mixtral of Experts: https://arxiv.org/abs/2401.04088
- DeepSeek-V3 tech report: https://arxiv.org/abs/2412.19437
- DeepSeek-R1 paper: https://arxiv.org/abs/2501.12948
- Qwen2 tech report: https://arxiv.org/abs/2407.10671
- GPT-4 technical report: https://arxiv.org/abs/2303.08774
- FlashAttention: https://arxiv.org/abs/2205.14135
- FlashAttention-2: https://arxiv.org/abs/2307.08691
- RoFormer (RoPE): https://arxiv.org/abs/2104.09864
- GQA: https://arxiv.org/abs/2305.13245
- SwiGLU (GLU Variants): https://arxiv.org/abs/2002.05202
