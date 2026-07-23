# Transformer'ın İçini Açmak — Ayrıntılı İnceleme

Transformer'ın kuş bakışı yapısını görmek başlangıç için yeterli değil. Bir sonraki adım: bloğun içindeki tek tek bileşenleri anlamak. Bu bölümde şu konular sırayla ele alınıyor:

1. Positional Encoding — sıra bilgisi mimariye nasıl giriyor
2. Self-Attention (Q, K, V) — mekanizmanın kalbi
3. Multi-Head Attention — birden çok "bakış açısı"
4. Causal Mask — decoder-only modellerin sırrı
5. Feed-Forward Network (FFN)
6. Layer Normalization ve RMSNorm
7. Residual Connections
8. Token Prediction — çıktı nasıl üretiliyor

Bu, Transformer mimarisi içinde en zor kısım. Aşağıda yavaş yavaş, örneklerle ilerleniyor.

---

## 1. Positional Encoding — Sıra Bilgisi Nereden Geliyor?

Self-attention doğası gereği pozisyona duyarsız. Şu iki cümleyi düşünelim:

- "Kedi köpeği kovaladı."
- "Köpek kediyi kovaladı."

Kelime kümesi aynı (`{kedi, köpek, kovaladı}`) ama anlam tamamen zıt. Attention mekanizması sadece kelime setine bakıyorsa bu iki cümleyi aynı görecek. Bu kabul edilemez.

Çözüm: **her token embedding'ine, o tokenin cümledeki konumunu belirten bir "pozisyon vektörü" ekle.** Böylece aynı kelime farklı pozisyonda farklı temsile sahip olur.

Bunu yapmanın birkaç yöntemi geliştirildi. En önemlileri:

### 1a) Sinusoidal Positional Encoding (Orijinal 2017 Yaklaşımı)

Farklı frekanslarda sinüs ve kosinüs değerlerinden oluşan bir vektör:

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

Burada `pos` tokenın konumu (0, 1, 2, ...), `i` embedding vektörünün boyut indeksi, `d_model` embedding boyutu.

Bu formül biraz karmaşık görünse de yaptığı iş şu: her pozisyon için, farklı frekanslarda salınan sinüs ve kosinüs değerlerinden oluşan benzersiz bir "parmak izi" üretiyor. Alt boyutlar hızlı salınıyor (yakın pozisyonları ayırt ediyor), üst boyutlar yavaş (uzun mesafede farklılaşıyor).

Bu tasarımın güzel yanı: **iki pozisyon arasındaki fark trigonometrik özdeşliklerle temsil edilebiliyor.** `PE(pos + k)` `PE(pos)` cinsinden lineer bir dönüşümdür. Yani model "3 pozisyon ötede" gibi bir kavramı öğrenebilir.

Ayrıca sinusoidal encoding sabit (öğrenilmiyor). Eğitim sırasında görmediği daha uzun dizilere teorik olarak jeneralize olabilir. Pratikte bu jeneralleştirme sınırlı ama en azından mümkün.

### 1b) Öğrenilebilir (Learned) Positional Embedding

Basit alternatif: pozisyon için de bir embedding tablosu yap, eğitim sırasında öğren.

```python
pos_emb = nn.Embedding(max_seq_len, d_model)
x = token_emb + pos_emb(torch.arange(seq_len))
```

- **Avantaj:** model kendi seçiyor, veriye göre esnek.
- **Dezavantaj:** eğitim zamanı `max_seq_len`'i geçemez. Yani 512 tokenle eğitirsen 1000 tokenlik girdiyle çalıştıramazsın (tablo yok).

GPT-2, GPT-3 gibi eski modeller bu yöntemi kullandı. Modern LLM'ler daha çok RoPE'a geçti.

### 1c) RoPE (Rotary Positional Embedding) — Modern Standart

Llama, Mistral, Qwen, DeepSeek, ChatGLM — hepsi RoPE kullanıyor.

Fikri şu: pozisyon bilgisini embedding'e **eklemek** yerine, Q ve K vektörlerini pozisyona göre **döndürmek**. Attention hesabında Q ile K'nın iç çarpımı zaten kullanılıyor; bu iç çarpım artık iki tokenın **relatif** mesafesine duyarlı hale geliyor.

Matematiksel olarak: her `(x_2i, x_2i+1)` çifti 2 boyutlu bir düzlem gibi ele alınıyor ve pozisyona göre `θ = pos / 10000^(2i/d)` açısı kadar döndürülüyor. Bunu Q ve K'nın her ikisine uygulayınca, attention skoru dönme açılarının farkına bağlı hale geliyor.

Bunun iki büyük avantajı var:

- **Relatif pozisyon:** Attention skorları "iki tokenın arasındaki mesafeye" duyarlı. Klasik absolute encoding'ler gibi mutlak pozisyona bağlı değil.
- **Extrapolation potansiyeli:** Eğitildiği bağlam uzunluğundan daha uzun dizilere makul biçimde jeneralize edebiliyor. YaRN, NTK-aware scaling gibi tekniklerle bu potansiyel daha da genişletilebiliyor.

Bugün 128K, 200K, hatta 1M token bağlamlı modellerin çoğunun RoPE tabanlı olması tesadüf değil. RoPE'un doğası uzun bağlam ölçeklendirmesine daha uygun.

### 1d) ALiBi (Attention with Linear Biases)

Bir başka yaklaşım: pozisyon embedding'i hiç kullanma, ama attention skorlarına doğrudan **mesafe cezası** ekle. İki token birbirinden ne kadar uzaksa, attention skoru o kadar cezalandırılıyor. Basit ve etkili ama RoPE kadar yaygınlaşmadı. MPT modelleri kullandı.

---

## 2. Self-Attention — Query, Key, Value

Bu kısım Transformer'ın kalbi. Adım adım gitmek şart.

### 2a) Sezgi — Kütüphane Analojisi

Bir kütüphaneye gidip birine bir soru sorduğunuzu hayal edin:

- **Query (Q):** Sizin sorunuz. "Fransız Devrimi hakkında bilgi lazım."
- **Key (K):** Her kitabın etiketi, sırt yazısı, anahtar kelime listesi.
- **Value (V):** Kitabın kendisi, içerdiği bilgi.

Yaptığınız işlem:
1. Sorunuzu (Q) her kitabın etiketiyle (K) karşılaştırıyorsunuz. Bir "uygunluk skoru" üretiyorsunuz.
2. Bu skorları normalize ediyorsunuz (softmax) — hangi kitaba yüzde kaç ağırlık vermeliyim?
3. Bu ağırlıklarla kitapların içeriklerini (V) topluyorsunuz.

Transformer'da her token hem soru sorabiliyor hem de cevap veriyor. Yani her token için Q, K ve V vektörleri üretiliyor. Sonra herkes herkese bakıyor.

### 2b) Matematiksel Formül

Klasik formül şudur (Scaled Dot-Product Attention):

```
Attention(Q, K, V) = softmax( (Q · Kᵀ) / √d_k ) · V
```

Adım adım açalım:

**Adım 1: Q, K, V'yi hesapla.**

Girdi olarak `X` matrisi geliyor (shape: `seq_len × d_model`). Bunu üç ayrı öğrenilebilir matrisle çarpıyoruz:

```
Q = X · W_Q       shape: (seq_len × d_k)
K = X · W_K       shape: (seq_len × d_k)
V = X · W_V       shape: (seq_len × d_v)
```

`W_Q`, `W_K`, `W_V` eğitilebilir ağırlık matrisleri. Genelde `d_k = d_v = d_model / n_heads`.

**Adım 2: Uygunluk skorları — `Q · Kᵀ`**

Bu bir `(seq_len × seq_len)` matris üretir. `[i][j]` girişi = i. tokenın Q vektörü ile j. tokenın K vektörünün iç çarpımı = i. tokenın j. tokene ne kadar "dikkat etmesi" gerektiği (ham skor).

**Adım 3: Ölçekleme — `/ √d_k`**

Neden bu bölme kritik? `d_k` büyüdükçe iç çarpımlar da büyür. Bu da softmax'a çok ekstrem (uçlarda) değerler girmesine neden olur. Softmax çıktıları neredeyse 0 veya 1'e yapışır, gradyanlar yok olur (vanishing gradient). Ölçekleme bunu düzeltir.

Örnek: `d_k = 64` için `√d_k = 8`. Yani skorlar 8'e bölünerek yumuşatılıyor.

**Adım 4: Softmax**

Her satır (yani her Q için) 0-1 arası bir olasılık dağılımına dönüşür. `softmax([2.1, 0.5, 3.7]) ≈ [0.16, 0.03, 0.81]` gibi. "Bu Q için hangi K'ya yüzde kaç dikkat vereceğim" ağırlıkları.

**Adım 5: `· V`**

Bu ağırlıklarla `V` vektörlerini topla. Sonuç: her token için, diğer tokenlerden ağırlıklı biçimde toplanmış yeni bir vektör. Bu vektör artık **bağlamı** (context) taşıyor — kendisi + diğer tokenlerin ilgili kısımları.

### 2c) Somut Örnek

Diyelim ki cümlemiz "The cat sat" (3 token). Basit sayılarla düşünelim:

- Q, K, V hepsi 3 vektör. Diyelim `d_k = 2`.
- `Q · Kᵀ` sonucu 3×3 matris:

```
        the   cat   sat
the  [  2.1   0.4   0.3 ]
cat  [  0.5   3.2   0.7 ]
sat  [  0.2   1.1   2.4 ]
```

- √2'ye böl (`≈ 1.41`), sonra softmax uygula. "cat" satırı için:
```
softmax([0.35, 2.26, 0.50]) ≈ [0.13, 0.71, 0.16]
```

- "cat" token'ı en çok kendisine (%71), sonra "sat"a (%16), sonra "the"ye (%13) bakıyor. Bu ağırlıklarla V vektörlerini topluyor.

- Yeni "cat" temsili artık cümle bağlamıyla zenginleşmiş. Salt "cat" embedding'i değil, "cat" + "sat" + "the" bilgisinin ağırlıklı toplamı.

### 2d) Self-Attention vs Cross-Attention

- **Self-attention:** Q, K, V'nin üçü de aynı diziden geliyor. Tokenler kendi aralarında haberleşiyor. Decoder-only LLM'lerdeki her attention bu tipte.
- **Cross-attention:** Q bir diziden, K/V başka bir diziden geliyor. Encoder-decoder modellerde decoder'ın encoder'a baktığı katman bu. Ayrıca çok-modlu (multimodal) modellerde (ör. görüntü → metin) sık kullanılıyor.

---

## 3. Multi-Head Attention

Tek bir attention hesabı, tek bir "bakış açısı"nı temsil ediyor. Ama bir cümlede aynı anda birçok farklı ilişki türü olabilir:

- Gramatik ilişkiler (özne-yüklem)
- Anlamsal ilişkiler (eş anlamlı, karşıt)
- Uzun mesafe eş-referanslar (bir zamir hangi isme atıfta bulunuyor)
- Konu-yorum ilişkileri

Tek bir attention başlığıyla bunların hepsini yakalamak zor. Çözüm: **h tane paralel attention başlığı çalıştır**. Her biri kendi öğrenilmiş `W_Q_i`, `W_K_i`, `W_V_i` matrislerine sahip. Her biri farklı ilişki türlerine odaklanabilir.

Formal olarak:

```
d_model = 512, n_heads = 8
d_k = d_v = d_model / n_heads = 64

head_i = Attention(X · W_Q_i, X · W_K_i, X · W_V_i)
MultiHead(X) = Concat(head_1, ..., head_h) · W_O
```

Sonuç `W_O` (çıkış projeksiyon matrisi) ile karışıp `d_model` boyutuna geri dönüyor. Böylece bloğun girişi ve çıkışı aynı boyutta oluyor, katmanlar üst üste rahat konabiliyor.

### Gözlem: Head'ler Ne Öğreniyor?

İnterpretability araştırmaları (Anthropic, Google Brain gibi ekiplerden) bazı head'lerin gerçekten belirgin uzmanlaşmalar öğrendiğini gösteriyor:

- **"Induction heads"** — geçen bir örüntüyü tekrar görürsen aynı devamı bekle (`A B ... A → B`).
- **"Coreference heads"** — bir zamiri, atıfta bulunduğu isme bağla.
- **"Positional heads"** — sadece bir önceki ya da bir sonraki tokene bak.

Bu head'ler tasarım gereği bu görevi öğrenmiyor; kendiliğinden ortaya çıkıyor.

### Modern Varyantlar: MQA, GQA

Multi-head attention'ın en büyük dezavantajı: inference sırasında **KV-cache** çok yer kaplıyor. Bir token üretildiğinde önceki tüm tokenlerin K ve V vektörleri saklanmak zorunda; her yeni token için attention'ı sıfırdan hesaplamak yerine bu cache kullanılıyor.

Bu cache'i küçültmek için iki varyant çıktı:

- **MQA (Multi-Query Attention):** Tüm head'ler tek bir K, V paylaşıyor. Q'lar hâlâ farklı. Cache neredeyse `1/n_heads` oranında küçülüyor. Kalitede küçük bir düşüş var ama servis maliyeti dramatik azalıyor.
- **GQA (Grouped-Query Attention):** MQA ile MHA arasında bir orta yol. Head'ler `g` gruba ayrılıyor, her grup bir K/V paylaşıyor. Llama-2 70B ile popülerleşti. Kalite/verimlilik dengesi en iyi seçenek olarak görülüyor. Llama 3, Mistral, Qwen — hepsi GQA kullanıyor.

Bu üç varyant matematik olarak aynı, sadece K/V paylaşım stratejileri farklı.

---

## 4. Causal Mask (Decoder-only Modellerin Sırrı)

Decoder-only bir LLM eğitirken şu problem var: modelin 5. tokeni tahmin ederken, 6., 7., 8. tokenlere bakması yasak. Zaten üretmeye çalıştığı token onlar; onlara bakabilseydi görev anlamsız olurdu.

Çözüm basit: attention skoru matrisinin üst üçgenine `-∞` (pratikte `-1e9` gibi çok büyük negatif) ekle. Softmax bu değerleri 0 yapar. Sonuç: her token sadece kendisine ve önceki tokenlere bakabilir.

```
Skor matrisi (mask uygulanmadan önce):

       t1    t2    t3    t4
t1  [  s11   s12   s13   s14 ]
t2  [  s21   s22   s23   s24 ]
t3  [  s31   s32   s33   s34 ]
t4  [  s41   s42   s43   s44 ]

Mask uygulandıktan sonra (üst üçgen -∞):

       t1    t2    t3    t4
t1  [  s11  -∞    -∞    -∞  ]
t2  [  s21   s22  -∞    -∞  ]
t3  [  s31   s32   s33  -∞  ]
t4  [  s41   s42   s43   s44 ]
```

Softmax sonrası üst üçgen tamamen 0 olur. Her satır bir olasılık dağılımı ama sadece "geçmişe" ağırlık veriyor.

Encoder-only modellerde (BERT gibi) causal mask kullanılmaz — çünkü hedef bir sonrakini tahmin etmek değil, tüm cümleyi anlamak. Encoder-decoder modellerin decoder tarafı yine causal mask kullanır.

---

## 5. Feed-Forward Network (FFN)

Self-attention "her token, diğerlerinden ne çekti" adımı. FFN ise "her token, çektiği bilgiyi kendi başına nasıl işledi" adımı. Attention'dan gelen vektöre iki katmanlı bir MLP uyguluyor. Her token bağımsız olarak, aynı MLP'den geçiyor (position-wise).

### 5a) Klasik FFN

```
FFN(x) = W_2 · GELU(W_1 · x + b_1) + b_2
```

Boyutlar:
- Girdi: `d_model` (ör. 4096)
- Ara: `d_ff = 4 · d_model` (ör. 16384) — bu 4 çarpanı klasik ama zorunlu değil
- Çıktı: `d_model`

Yani "genişlet — non-linearity — daralt" mantığı. Modelin parametrelerinin büyük bir kısmı burada. Örneğin Llama-2 7B'de bir bloktaki FFN parametreleri, attention parametrelerinden yaklaşık 2 kat fazla.

### 5b) Aktivasyon: GELU vs SwiGLU

Klasik olarak ReLU kullanılıyordu. Ama Transformer'lar GELU'yu daha çok sevdi:

```
GELU(x) = x · Φ(x)      // Φ = standart normal CDF
```

Sezgisel olarak: ReLU sert kesim (negatif gir → 0), GELU yumuşak (negatif değerler az da olsa geçirilir). Gradyan akışı daha temiz. BERT, GPT-2 ile başlayıp standart oldu.

**SwiGLU** — modern LLM'lerin ekmeği. Llama, Mistral, Qwen, DeepSeek hepsi kullanıyor:

```
SwiGLU(x) = (W_1 · x) ⊙ Swish(W_gate · x)     // ⊙ = element-wise çarpım
FFN(x) = W_2 · SwiGLU(x)
```

Burada iki paralel projeksiyon var; biri "kapı" gibi çalışıyor (Swish aktivasyonu ile). Bu sayede model daha seçici karar verebiliyor. Parametre biraz daha çok (3 matris) ama pratik olarak daha kaliteli sonuç veriyor.

SwiGLU kullanan modellerde `d_ff = 8/3 · d_model` alınıyor genelde, klasik FFN ile aynı parametre sayısını korumak için.

---

## 6. LayerNorm ve RMSNorm

Derin ağlarda katmandan katmana değerlerin ölçeği kayabiliyor. Bir katmanın çıktısı 0.001 civarındayken, diğerininki 1000 civarında olabilir. Bu, eğitim stabilitesini bozar. Çözüm: her katmanın çıktısını normalize etmek.

### 6a) LayerNorm

Orijinal Transformer'ın kullandığı:

```
LN(x) = γ ⊙ (x - μ) / √(σ² + ε) + β
```

- `μ`, `σ²`: bu tokenın `d_model` boyutundaki ortalaması ve varyansı
- `γ, β`: öğrenilebilir ölçek ve kaydırma parametreleri
- `ε`: numerik stabilite için küçük sabit (ör. 1e-5)

**Neden LayerNorm, BatchNorm değil?** BatchNorm batch içindeki farklı örnekler arasında normalize eder. Değişken uzunluklu sekanslarda (NLP'de standart) bu tuhaflaşıyor. LayerNorm örnek içinde normalize eder, sekans uzunluğundan bağımsız çalışır.

### 6b) Pre-Norm vs Post-Norm

Orijinal Transformer post-norm kullanıyordu:

```
x → Sublayer(x) → +x → LayerNorm(...)     // önce sublayer, sonra norm
```

Modern LLM'ler pre-norm kullanıyor:

```
x → LayerNorm(x) → Sublayer(...) → +x     // önce norm, sonra sublayer
```

Fark neden önemli? Post-norm derin ağlarda gradyanları kararsız yapıyor, çok dikkatli learning rate warmup gerektiriyor. Pre-norm daha dayanıklı — 100+ katmanlı modelleri eğitmek pre-norm sayesinde kolaylaştı.

### 6c) RMSNorm — Daha da Basit

Llama ve türevleri LayerNorm yerine RMSNorm kullanıyor:

```
RMSNorm(x) = γ ⊙ x / √(mean(x²) + ε)
```

Fark: ortalama çıkarımını atlıyor, sadece root-mean-square'a bölüyor. Bir işlem az, hesap %10-20 daha hızlı, pratikte eşit kalitede. Sadeleştirmenin kazandırdığı bir örnek.

---

## 7. Residual (Skip) Connections

Her sublayer'ın çıktısı, girdisiyle toplanıyor:

```
x_new = x + Sublayer(x)
```

Bu, ResNet'ten (2015, görüntü) gelen fikir. Şu yararları sağlıyor:

- **Gradyan akışı:** backprop sırasında gradyanların derin katmanlar arasından kaybolmadan geçebilmesi. Zincir kuralında `∂L/∂x` hesaplanırken bir yol her zaman "kısayol" olarak identity gradyanı taşıyor.
- **Identity öğrenimi:** Sublayer sıfır dönerse çıktı girdiye eşit kalır. Model "hiçbir şey yapmama"yı kolayca öğrenebiliyor. Bu, gereksiz katmanların pasifleşmesine izin veriyor.
- **Derinlik mümkün oluyor:** Residual olmadan 20+ katmanlı Transformer eğitmek pratik olarak zor. 96 katmanlı GPT-3 gibi modeller olmazdı.

---

## 8. Token Prediction — Çıktı Nasıl Üretiliyor?

N Transformer bloğu sonrasında her token için `d_model` boyutlu bir vektör var. Şimdi bunu dağarcık boyutuna projelenmek lazım:

```
logits = h · W_LM         shape: (seq_len × vocab_size)
```

`W_LM` genellikle input embedding tablosunun transpozu olarak paylaşılıyor (weight tying).

### Sampling Stratejileri

Son tokenın `vocab_size` boyutlu logit vektörüne softmax uygulanınca bir olasılık dağılımı çıkıyor. Şimdi bu dağılımdan bir token seçmek lazım. Çeşitli stratejiler var:

- **Greedy:** her adımda en yüksek olasılıklı tokeni seç. Deterministic ama tekrar edici, sıkıcı metin üretiyor. Aynı prompt her zaman aynı çıktıyı veriyor.
- **Top-k sampling:** en yüksek olasılıklı `k` tokendan sample et. `k = 50` yaygın. Çeşitlilik ekliyor.
- **Top-p (Nucleus) sampling:** olasılığı yüksekten aşağıya sırala; kümülatif olasılığın `p`'yi geçtiği tokene kadar olanları al. Bunlar arasından sample. `p = 0.9` yaygın. En pratik seçim.
- **Temperature:** softmax'tan önce logit'i `T`'ye böl. `T < 1` daha keskin (deterministic'e yakın). `T > 1` daha rastgele (yaratıcı). `T = 0` neredeyse greedy'ye eşit.

Modern sistemler genelde şu ayarları kullanıyor:

- **Sohbet:** `temperature = 0.7`, `top_p = 0.9`
- **Kod:** `temperature = 0.2`, `top_p = 0.95` (daha deterministic)
- **Yaratıcı yazma:** `temperature = 1.0-1.2`, `top_p = 0.9`

### KV-Cache — Inference Optimizasyonu

Bir tokenı üretmek için modeli çalıştırdığımızda, önceki tüm tokenler için attention hesaplamış oluyoruz. Bir sonraki tokeni ürettiğimizde bu hesabı sıfırdan yapmak gereksiz. Bu yüzden K ve V matrisleri cache'te tutuluyor. Sadece yeni tokenın Q'su ile eski K'lar arasında attention hesaplanıyor.

Bu, uzun bağlamlarda inference'ı dramatik hızlandırıyor. Ama KV-cache çok bellek yiyor. Örneğin 32K bağlamlı bir 70B model için KV-cache 10+ GB olabiliyor. MQA, GQA, MLA gibi varyantlar bu problemi hafifletmek için geliştirildi.

---

## Bir Tam Blok Diyagram

Tüm bileşenleri birleştirirsek, bir modern decoder-only Transformer bloğu şöyle görünüyor:

```
                girdi x (shape: seq × d_model)
                        │
                ┌───────▼────────┐
                │   RMSNorm      │
                └───────┬────────┘
                        │
                ┌───────▼──────────────────────────┐
                │  Multi-Head Self-Attention       │
                │  ─ RoPE ile Q, K'ya rotasyon     │
                │  ─ GQA gruplu K, V               │
                │  ─ Causal mask uygulanıyor       │
                └───────┬──────────────────────────┘
                        │
                        ⊕──── x (residual)
                        │
                ┌───────▼────────┐
                │   RMSNorm      │
                └───────┬────────┘
                        │
                ┌───────▼─────────────┐
                │  SwiGLU FFN         │
                │  ─ d_model → d_ff   │
                │  ─ Gated activation │
                │  ─ d_ff → d_model   │
                └───────┬─────────────┘
                        │
                        ⊕──── önceki (residual)
                        │
                        ▼
                   sıradaki bloğa
```

Bu blok modelde 30-100 kez tekrarlanıyor. Her seferinde tokenlerin temsili biraz daha zenginleşiyor, biraz daha soyut hale geliyor.

---

## Genel İzlenim

Transformer bloğu son derece minimal bir mimari. Sadece dört ana bileşen (attention, FFN, norm, residual) ve bir pozisyon kodlaması. Ama bu minimal yapı, doğru şekilde ölçeklendirildiğinde inanılmaz genelci bir öğrenme sistemi haline geliyor.

En önemli fark: bu mimari **her tokenın her tokene bakmasına izin veriyor**. Bilgi akışı sınırsız. Katmanlar üst üste geldikçe kaç kez birinci token ile son token arasında bilgi taşınmış oluyor — sınırsız hop sayısı. Bu, RNN'in en büyük darboğazının tam tersi.

Ama her hesap `O(n²)`. Uzun bağlamlarda bu ciddi bir maliyet. Şu an araştırmanın büyük bir kısmı bu maliyetin nasıl düşürüleceğine dair (FlashAttention, Sliding Window, State Space Models, Linear Attention). Yani Transformer bitmiş bir konu değil; hâlâ evrimleşiyor.
