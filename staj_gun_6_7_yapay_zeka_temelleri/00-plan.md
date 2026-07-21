# Yapay Zeka Temelleri — İçindekiler ve Yol Haritası

Bu klasör, yapay zeka temellerini kapsayan bir çalışma serisi. Amaç: **ML → Deep Learning → NLP → Transformer → LLM** zincirini uçtan uca birleştiren bir referans oluşturmak. Konular tek tek uzmanlık gerektirse de burada odak "yapay zeka arkada nasıl çalışıyor" sorusunun cevabını çıkarmak.

İçerik iki tematik bölümde toplandı:

- **Birinci bölüm — Temeller & ML/DL Zemini:** matematik bağlantısı, notebook ortamı, framework kıyası, ML ve DL kavramları, PyTorch pratiği.
- **İkinci bölüm — NLP → Transformer → LLM Ekosistemi:** token / embedding, Transformer mimarisi ve parçaları, "Attention Is All You Need", LLM karşılaştırması, Hugging Face keşfi.

---

## Birinci Bölüm — Temeller & ML / DL Zemini

Bu bölümün amacı: "model" dediğimiz şey aslında ne, nasıl eğitiliyor, hangi araçla yazılıyor sorularını netleştirmek.

### 1) Olasılık ve İstatistiğin Yapay Zeka İle Bağlantısı → `01-olasilik-istatistik.md`
- Modelin çıktısı neden olasılık (0-1 arası dağılım)?
- Ortalama, varyans, dağılım (normal, Bernoulli, kategori) niye önemli?
- Bayes yaklaşımı ve sınıflandırma bağlantısı.
- Maximum Likelihood → loss fonksiyonuyla ilişkisi (özellikle cross-entropy).
- Örneklem / anakütle / bias-variance dengesi.
- "Neden AI çalışır?" sorusunun istatistik cevabı: veri dağılımını öğrenmek.

### 2) Hücre / Notebook Tabanlı Programlama → `02-notebook-programlama.md`
- Jupyter / Colab / Kaggle Notebook nedir, hücre mantığı ne işe yarıyor.
- Neden data science ve ML'de standart: parça parça deneme, ara çıktıyı görme, grafik gömme.
- Ne zaman notebook, ne zaman düz `.py` script tercih edilmeli.
- Hangi projelerde şart: EDA, model prototipleme, veri temizleme, öğretim materyali.
- Hangi projelerde önerilmez: prod servis, otomasyon, uzun ömürlü kod.

### 3) ML Temeli → `03-ml-temelleri.md`
- **Model:** girdi → çıktı eşlemesi yapan fonksiyon.
- **Parametre:** modelin öğrendiği sayılar (ağırlıklar, bias).
- **Eğitim (training):** parametreleri veriye göre ayarlama süreci.
- **Loss:** modelin ne kadar yanlış olduğunu ölçen sayı (MSE, cross-entropy).
- **Train / Validation / Test:** neden 3'e böldüğümüz, her birinin görevi, veri sızıntısı (data leakage) neden problem.
- Küçük şema: veri → model → tahmin → loss → parametre güncelleme döngüsü.

### 4) Deep Learning Temeli → `04-deep-learning-temelleri.md`
- **Neural Network:** katmanlardan (layer) oluşan parametrik fonksiyon.
- **Weight / bias:** her katmandaki öğrenilebilir parametreler.
- **Forward pass:** girişi katmanlardan geçirip çıktı üretmek.
- **Loss → Backpropagation:** loss'un gradyanının katmanlara geri yayılması (zincir kuralı).
- **Gradient Descent:** parametreleri gradyan yönünün tersine küçük adımlarla güncellemek.
- **Optimizer:** SGD, Momentum, Adam, AdamW; hangi durumda hangisi.
- **Activation Functions:** neden non-lineerlik lazım; ReLU vs. GELU farkı, günümüz LLM'lerinde neden GELU/SwiGLU tercih ediliyor.
- **Batch / Epoch:** neden mini-batch, epoch kaç kez veriyi tarar.
- **Overfitting:** train loss düşerken validation loss yükselirse ne oluyor, çözümler (regularization, dropout, early stopping, data augmentation).

### 5) Framework Karşılaştırması: PyTorch vs. TensorFlow (ve diğerleri) → `05-pytorch-vs-tensorflow.md`
- PyTorch, TensorFlow (+Keras), JAX, ONNX, scikit-learn, Hugging Face `transformers` gibi kütüphaneler arasındaki fark: framework mi, kütüphane mi, SDK mi?
- Dinamik graph (PyTorch) vs. statik graph (klasik TF) farkı.
- Araştırma vs. üretim kullanımı: PyTorch neden araştırmada baskın, TF neden production/mobile'da öne çıkıyor.
- Küçük bir kıyaslama tablosu (topluluk, kaynak, kolaylık, ekosistem, mobil, üretim, öğrenme eğrisi).
- Hangi proje türünde hangi araç: LLM ince ayar → PyTorch + HF; mobil sınıflandırma → TFLite; klasik ML → scikit-learn.

### 6) PyTorch "60 Minute Blitz" Uygulaması → `06-pytorch-60-min-blitz/`
- Resmi PyTorch tutorial'ının 4 bölümünü sırayla geçiyorum:
  1. Tensor temelleri
  2. Autograd
  3. Neural Networks (`nn.Module`)
  4. CIFAR10 üzerinde küçük eğitim örneği
- Amaç: yukarıdaki teorik kavramların (forward, loss, backward, optimizer.step) kodda nasıl göründüğünü görmek.
- Alt klasörde `.py` dosyaları + `notlar.md`.

---

## İkinci Bölüm — NLP, Transformer ve LLM Ekosistemi

Bu bölümün amacı: bugünkü LLM'lerin (ChatGPT, Claude, Gemini vb.) nasıl çalıştığını mimari düzeyde anlamak.

### 7) NLP'ye Giriş — Token & Embedding → `07-nlp-token-embedding.md`
- NLP nedir, klasik NLP (kural tabanlı, TF-IDF, n-gram) vs. modern LLM tabanlı NLP.
- Farklar / ortak yönler: günümüz LLM'leri de NLP problemi çözüyor ama artık istatistiksel/simgesel değil, öğrenilmiş temsillerle çözüyor.
- Token: karakter, kelime, subword (BPE, WordPiece, SentencePiece) farkı; neden subword tercih ediliyor.
- Embedding: token → vektör dönüşümü; benzer anlamlı tokenlerin uzayda yakın olması ne demek.
- Cosine similarity ile embedding'lerin yakınlığını hissettiren örnek.

### 8) Transformer Mimarisi — Genel Bakış → `08-transformer-mimarisi.md`
- Transformer neden önemli: RNN/LSTM'in sıralı çalışma zorunluluğunu kırdı, paralel eğitilebilir hale getirdi.
- Ana bloklar özetle: input → tokenizer → embedding → (+ positional encoding) → N x Transformer Block → çıktı head.
- Encoder-only (BERT), decoder-only (GPT/Claude/Llama), encoder-decoder (T5) ayrımı: hangisi hangi tür göreve uygun.

### 9) Transformer'ın İçini Açmak → `09-transformer-detay.md`
- **Positional Encoding:** attention sırayı görmediği için pozisyon bilgisini nereden alıyor; sinusoidal vs. öğrenilebilir vs. RoPE.
- **Attention (Q, K, V):**
  - Q, K, V'nin sezgisel anlamı.
  - Scaled dot-product attention formülünün mantığı.
  - Softmax ile "hangi tokene ne kadar bakılıyor" ağırlıkları.
- **Multi-head Attention:** neden birden çok başlık; her başlık farklı ilişki türü öğrenebiliyor.
- **Transformer Block:**
  - Layer Norm (pre-norm vs. post-norm farkı).
  - Feed-Forward Network (genelde `d_model → 4 · d_model → d_model`, arada GELU/SwiGLU).
  - Residual bağlantılar neden şart.
- **Token prediction:** decoder-only modellerde bir sonraki tokeni tahmin görevi (causal masking), softmax → olasılık dağılımı → sampling / greedy / top-k / top-p.

### 10) "Attention Is All You Need" Makalesinin Önemi → `10-attention-is-all-you-need.md`
- Makalenin ana iddiası: tamamen attention tabanlı, recurrence/convolution kullanmayan bir mimari.
- Neden devrim: paralel eğitim, uzun bağımlılıklarda çok daha iyi, büyük veriyle iyi ölçeklenme.
- Etkileri: BERT, GPT ailesi, LLM patlaması, hatta multimodal (ViT, Whisper, Stable Diffusion cross-attention) modellere yayılması.
- "Bu makale çıkmasaydı bugünkü LLM'ler olur muydu" sorusuna kısa bir yorum.

### 11) Farklı Popüler LLM Mimarilerinin Karşılaştırması → `11-llm-mimari-karsilastirma.md`
- İnceleyeceğim aile örnekleri: GPT (OpenAI), Claude (Anthropic), Gemini (Google), Llama (Meta), Mistral / Mixtral, DeepSeek, Qwen.
- Karşılaştırma kriterleri:
  - Encoder-only / decoder-only / encoder-decoder.
  - Attention varyantı: MHA, GQA, MQA, MLA, FlashAttention.
  - Positional encoding: RoPE, ALiBi vb.
  - Aktivasyon / FFN: GELU, SwiGLU.
  - MoE (Mixture of Experts).
  - Bağlam uzunluğu.
  - Açık ağırlık (Llama, Mistral, Qwen, DeepSeek) vs. kapalı (GPT, Claude, Gemini).
- Kıyaslama tablosu + öne çıkan mimari farklar (MoE, RoPE, MLA gibi).

### 12) Hugging Face Keşfi → `12-huggingface-kesif.md`
- Hugging Face nedir, neden "AI'nin GitHub'ı" deniyor.
- Ana bölümler: Models, Datasets, Spaces, Papers, Docs, Leaderboards (Open LLM Leaderboard, LMSYS Arena).
- `transformers`, `datasets`, `accelerate`, `peft`, `trl`, `diffusers` kütüphanelerinin ne işe yaradığı.
- Küçük bir "hello world" örneği (küçük bir modelle text generation).
- Trend olan modeller / veri setleri.

---

## Çalışma İlkesi

Konular birbirinden bağımsız değil; her başlık bir öncekinin üstüne oturuyor. Her bölüm için üç soru işlevsel:

- Bu kavram, üstteki konuyla nasıl bağlanıyor?
- Bu olmasa, bir üstteki nasıl bozulurdu?
- Bir LLM eğitilmek istense bu kavram nerede karşımıza çıkar?

---

## Dosya Haritası

```
staj_gun_6_7_yapay_zeka_temelleri/
├── 00-plan.md                          (bu dosya — içindekiler)
├── 01-olasilik-istatistik.md
├── 02-notebook-programlama.md
├── 03-ml-temelleri.md
├── 04-deep-learning-temelleri.md
├── 05-pytorch-vs-tensorflow.md
├── 06-pytorch-60-min-blitz/
│   ├── 01-tensor.py
│   ├── 02-autograd.py
│   ├── 03-nn-module.py
│   ├── 04-cifar10.py
│   └── notlar.md
├── 07-nlp-token-embedding.md
├── 08-transformer-mimarisi.md
├── 09-transformer-detay.md
├── 10-attention-is-all-you-need.md
├── 11-llm-mimari-karsilastirma.md
└── 12-huggingface-kesif.md
```

Sıra ile 01'den 12'ye kadar okununca yapay zekanın temellerinden LLM ekosistemine kadar bir zincir oluşuyor.
