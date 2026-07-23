# Transformer Mimarisi — Genel Bakış

Modern yapay zekanın merkezinde tek bir mimari duruyor: **Transformer**. Metin işleyen tüm büyük dil modelleri (GPT, Claude, Gemini, Llama, Mistral, Qwen, DeepSeek), görüntü üreten sistemlerin çoğu (Stable Diffusion, DALL-E), ses tanıma (Whisper), hatta protein katlanma tahmini (AlphaFold 2) — hepsi Transformer'ın türevlerini kullanıyor. 2017'de tanıtılmış ve o zamandan beri bir alternatifi yeşerememiş.

Aşağıda önce Transformer'ın **neden** çıktığını anlamak için ondan önceki mimarilerin (RNN, LSTM) sınırları inceleniyor, sonra Transformer'ın **ne olduğu** kuş bakışı gösteriliyor. İçindeki mekanikler (attention formülü, Q-K-V, multi-head, positional encoding gibi) ayrı bir dosyada ayrıntılı ele alınıyor.

---

## Transformer'dan Önce: RNN ve LSTM'in Dertleri

Transformer'ın önemi kavramak için ondan önce ne kullanıldığını görmek lazım. 2010'ların NLP'sinin sırt kemiği **RNN (Recurrent Neural Network)** ve onun daha gelişmiş formu olan **LSTM (Long Short-Term Memory)** idi.

### RNN'in Ana Fikri

RNN cümleyi baştan sona bir kelime (ya da token) tarayarak "hafıza" (`h`) güncelliyor:

```
h_0 = 0
h_1 = f(h_0, "The")
h_2 = f(h_1, "cat")
h_3 = f(h_2, "sat")
h_4 = f(h_3, "on")
h_5 = f(h_4, "the")
h_6 = f(h_5, "mat")
```

Her adımda `h_t` gizli durumu güncelleniyor; bu, "şu ana kadar okuduklarımın özeti"ni tutuyor. Cümlenin sonundaki `h_6` teorik olarak tüm cümlenin bir temsilini içeriyor.

### RNN'in İki Büyük Sorunu

**Sorun 1: Sıralı olmak zorunda — GPU paralelliğini kullanamıyor**

`h_5`'i hesaplamak için `h_4`'ün hazır olması gerek. `h_4` için `h_3` gerek. Yani cümledeki 100. kelimeye ulaşmak için önce 99 hesaplama yapılması şart. Bu, tanımı gereği paralelleşmiyor.

Modern GPU'lar binlerce paralel iş yapabilmek üzere tasarlandı. RNN bu güçten faydalanamıyor. Milyon parametreli modeller eğitmek makul sürede mümkündü ama milyar parametreli modellere ölçeklenmesi felaket ağır oluyordu.

**Sorun 2: Uzun mesafe bağımlılıklar zayıf**

50. kelimenin, 1. kelimenin bilgisine ulaşabilmesi için o bilginin 50 kez peş peşe `f()` fonksiyonundan geçmesi gerek. Her geçişte biraz kaybediyor, biraz bozuluyor. Sonunda ilk kelime tamamen unutulmuş oluyor.

LSTM bu problemi kısmen çözdü. "Gate" (kapı) mekanizmalarıyla bilginin bazı parçalarını uzun süre saklamayı öğrenebiliyor. Ama yine de bir yerden sonra sınıra dayanıyor. Uzun paragrafları, sayfaları, kitapları modellemek için yeterli değildi.

### Küçük Bir Ara Adım: Bahdanau ve Luong Attention (2014-2015)

Bu iki makale attention'ı ilk kez tanıttı ama Transformer'ın "temel yapıtaşı" olarak değil, RNN'in **yardımcısı** olarak. Çeviri modellerinde decoder'ın encoder'ın gizli durumlarına "hangisine daha çok bakayım" diye ağırlıklı olarak erişebilmesini sağladı. Kalite arttı ama RNN'in çekirdek problemi (paralelleşememe) hâlâ oradaydı.

Bu, "attention faydalı bir eklenti" fikrinin doğduğu an. 2017'ye kadar kimse "peki attention'ı ana yapı yapalım, RNN'i tamamen çıkaralım" demedi.

---

## Transformer'ın Çözümü

2017'de yayınlanan "Attention Is All You Need" makalesi radikal bir öneri getirdi:

> **Sırayı ortadan kaldıralım. Her kelimeye, diğer tüm kelimelere aynı anda bakabilme yeteneği verelim.**

Bunu yapan mekanizma: **self-attention**. Her token, diziye baktığında hangi diğer tokenlere ne kadar "dikkat" edeceğine kendi karar veriyor. Ve bu hesap paralel yapılabiliyor — çünkü bir matris çarpımından ibaret.

Sonuçları çarpıcı:

- **Paralellik:** Bir cümlenin tüm tokenleri aynı anda işlenebiliyor. GPU tam kapasite çalışıyor. Eğitim 10x, 100x hızlanıyor.
- **Uzun mesafe bağımlılık:** 1000. token, 1. token'a doğrudan (tek adımda) bakabiliyor. Mesafe kavramı yok.
- **Ölçeklenebilirlik:** Model derinliği ve genişliği katlanarak büyütülebiliyor. GPT-3, GPT-4, Claude, Gemini gibi modellerin varlığı bu mimari sayesinde mümkün oldu.

Bedelini şurada ödüyor: attention hesabının maliyeti `O(n²)` (n = dizi uzunluğu). 1000 tokenli bir metin için 1.000.000 attention skoru hesaplanıyor. RNN'de bu `O(n)` idi. Ama GPU bu kareyi tek atışta yiyor, pratikte bu tercih edilir hale geldi. Yine de çok uzun bağlamlar (100K, 1M token) için modern optimizasyonlar (FlashAttention, sparse attention, sliding window) gerekiyor.

---

## Bir Transformer'ın Genel Boru Hattı

Aşağıdaki akış, modern bir decoder-only LLM için tipik olan yapıyı gösteriyor:

```
    "Merhaba dünya, nasılsın?"
              │
              ▼
       ┌────────────┐
       │ Tokenizer  │      BPE / SentencePiece
       └────────────┘
              │  (token ID listesi)
              ▼
       ┌────────────┐
       │ Embedding  │      lookup table, d-boyutlu vektörler
       └────────────┘
              │
              +   Positional Encoding    (sıra bilgisi)
              │
              ▼
       ┌────────────────┐
       │  Transformer   │
       │  Block         │  × N kere tekrar
       │  ─────────     │  (GPT-2 için 12, GPT-3 için 96, Llama-3 70B için 80)
       │  · Self-Attn   │
       │  · FFN         │
       │  · LayerNorm   │
       │  · Residual    │
       └────────────────┘
              │
              ▼
       ┌────────────┐
       │ Final Norm │
       └────────────┘
              │
              ▼
       ┌────────────┐
       │  LM Head   │       linear, vocab_size boyutlu skor
       └────────────┘
              │
              ▼
       ┌────────────┐
       │  Softmax   │       olasılık dağılımı
       └────────────┘
              │
              ▼
       Sonraki token seçilir
   (greedy / top-k / top-p / temperature)
```

Bir eğitim döngüsünde bu boru hattı milyarlarca cümle üzerinde çalışıyor. Her adımda modelin ürettiği olasılık dağılımı ile gerçek sonraki tokenin karşılaştırılması sonucu bir kayıp (cross-entropy loss) hesaplanıyor ve gradyanlar geri yayılıyor.

**Küçük not:** Girdinin embedding'i ve çıktıdaki LM Head'in ağırlıkları çoğu modelde **paylaşılıyor** (tied weights). Buna "weight tying" deniyor. Hem parametre tasarrufu hem de pratikte biraz daha iyi çalıştığı için tercih ediliyor.

---

## Üç Aile: Encoder-only, Decoder-only, Encoder-Decoder

Transformer'ın üç farklı kullanım şekli var. Her biri farklı görev türlerine uygun.

### 1) Encoder-only (Örnek: BERT ailesi)

- Tüm cümleyi/paragrafı **aynı anda** okur.
- Her token diğer tüm tokenlere hem sola hem sağa bakabilir (bidirectional).
- **Amacı:** metnin bir "anlam vektörü"nü üretmek.
- **Uygun görevler:** sınıflandırma, duygu analizi, cümle benzerliği, arama (semantic search), Named Entity Recognition, soru cevaplama (extractive QA).
- **Uygun DEĞİL:** metin üretme. Çünkü tek bir seferde tüm cümleyi görüyor, "bir sonrakini tahmin et" oyununu öğrenmesi zor.
- **Örnekler:** BERT, RoBERTa, DeBERTa, DistilBERT.
- **Eğitim hedefi:** Masked Language Modeling — cümlenin bazı tokenleri `[MASK]` ile örtülür, model bunları tahmin etmeye çalışır.

### 2) Decoder-only (Örnek: GPT ailesi) — Modern LLM'ler

- Sadece **sola bakabilir** (causal mask).
- "Şu ana kadar gördüğüm tokenlara bakarak sıradaki tokeni tahmin et" görevine odaklanmış.
- Autoregressive üretim: bir token üretir, geri besler, bir sonrakini üretir, tekrar besler...
- **Uygun görevler:** metin üretme, sohbet, kod üretme, tercüme, özetleme — hemen hemen her şey.
- **Modern gerçek:** yeterince büyük bir decoder-only model, ince ayarla neredeyse tüm NLP görevlerini yapabiliyor.
- **Örnekler:** GPT-2/3/4, Claude, Llama, Mistral, Gemini (çekirdek), Qwen, DeepSeek.
- **Eğitim hedefi:** Causal Language Modeling — her pozisyonda bir sonraki tokeni tahmin et.

### 3) Encoder-Decoder (Örnek: T5, orijinal Transformer)

- İki parça vardır: **encoder** girişi işler ve anlam vektörleri üretir; **decoder** bu vektörlere bakarak çıkışı üretir.
- Aralarında **cross-attention** vardır — decoder her yeni token üretirken encoder'ın çıktısına dönüp bakabiliyor.
- **Uygun görevler:** çeviri, özetleme, girdi-çıktı formatındaki her problem.
- **Örnekler:** T5, BART, mT5, MarianMT.
- Orijinal Transformer makalesi de bu yapıda önerildi (İngilizce-Almanca çeviri için).

### Hangisi Ne Zaman?

Modern eğilim, decoder-only'nin lehine. Zira ölçek büyütüldüğünde tek başına yeterli oluyor. Ancak encoder-only modeller hâlâ:

- **Semantic search / RAG** için hızlı embedding üretmede rakipsiz (BAAI/bge-m3, intfloat/e5 gibi modeller BERT ailesinden).
- **Sınıflandırma** görevlerinde küçük kaynakla iyi sonuç verirler.
- **Metin karşılaştırma** (iki cümle ne kadar benzer) için ekonomik.

Encoder-decoder ise özellikle **formal çeviri** ve **girdi-çıktı yapılandırılmış görevler** için hâlâ tercih edilebiliyor.

---

## Bir Transformer Bloğunun İç Yapısı

Yukarıdaki boru hattında geçen "Transformer Block" aslında birkaç alt katmandan oluşuyor. Klasik "pre-norm" düzende:

```
     girdi x
        │
   ┌────▼────┐
   │LayerNorm│
   └────┬────┘
        │
   ┌────▼──────────────┐
   │ Multi-Head        │
   │ Self-Attention    │       ← Q, K, V burada
   │ (+ causal mask)   │
   └────┬──────────────┘
        │
        +──── x  (residual bağlantı)
        │
   ┌────▼────┐
   │LayerNorm│
   └────┬────┘
        │
   ┌────▼─────────────┐
   │ Feed Forward     │       ← her tokene ayrı ayrı MLP
   │ (SwiGLU / GELU)  │
   └────┬─────────────┘
        │
        +──── önceki  (residual bağlantı)
        │
        ▼
     çıktı → sıradaki bloğun girdisi
```

Bloğun içindeki dört ana bileşen:

- **Self-Attention:** tokenler birbirine bakar, hangisi hangisine ne kadar önem verecek diye ağırlıklar hesaplar, bilgi toplar.
- **Feed-Forward Network (FFN):** her token bağımsız olarak iki katmanlı bir MLP'den geçer. "Toplanan bilgiyi işle" görevini görür.
- **LayerNorm:** girdinin ölçeğini normalize eder. Derin ağlarda eğitim stabilitesi için şart.
- **Residual (skip) bağlantılar:** girdi, sublayer çıktısına eklenir. Gradyanların derin katmanlar arasında akmasını sağlar. Bu ResNet'ten (2015) gelen bir fikir ve olmadan 96 katmanlı Transformer eğitilemezdi.

Bu blok N kere üst üste tekrarlanıyor. Her tekrar, önceki tekrardan gelen temsili biraz daha "zenginleştiriyor". İlk katmanlar daha yerel örüntüler (gramer, yakın kelime ilişkileri), üst katmanlar daha soyut ilişkiler (anlambilim, üslup, mantık) öğreniyor gibi gözleniyor (interpretability araştırmalarında).

---

## Bir Transformer'ın "Büyüklüğü" Neyle Ölçülür?

Bir modelin boyutu genelde dört hiperparametreyle özetlenir:

- **`d_model`** — embedding vektörünün boyutu. Örnekler: 768 (BERT-base), 1024 (BERT-large), 4096 (Llama-2 7B), 12288 (GPT-3).
- **`n_layers`** — kaç Transformer bloğu üst üste. Örnekler: 12 (BERT-base), 32 (Llama-2 7B), 80 (Llama-3 70B), 96 (GPT-3).
- **`n_heads`** — multi-head attention'daki paralel başlık sayısı. Genellikle 8, 12, 16, 32.
- **`d_ff`** — FFN'in ara katman boyutu. Klasik olarak `4 × d_model` alınır (GELU'lu FFN için); SwiGLU kullanan modern LLM'lerde `~2.67 × d_model` (aynı parametre sayısını korumak için).

Ayrıca iki bağlam parametresi:

- **`vocab_size`** — dağarcık boyutu (30K-256K arası).
- **`context_length`** — bir seferde işleyebilecek maks. token sayısı (2K, 4K, 32K, 128K, 1M...).

### Örnek Hesap: Llama-2 7B

- `d_model = 4096, n_layers = 32, n_heads = 32, d_ff = 11008`
- `vocab_size = 32000`
- `context_length = 4096`

Toplam parametre sayısı ≈ 7 milyar. Bunun neden yaklaşık 7B olduğunu hesaplamak istersen:

- Embedding tablosu: `32000 × 4096 ≈ 131M`
- Her Transformer bloğu: attention (`4 × 4096² ≈ 67M`) + FFN (`~3 × 4096 × 11008 ≈ 135M`) ≈ 202M
- 32 blok: `32 × 202M ≈ 6.5B`
- Toplam ≈ 6.7B, buna kalan katmanları (norm ağırlıkları vs.) ekleyince tam 7B

### İnference Belleği

Modeller büyüdükçe VRAM sınırları çıkıyor. Kaba tahmin:

- fp32: parametre başına 4 byte → 7B model için 28 GB
- fp16: parametre başına 2 byte → 14 GB
- int8: parametre başına 1 byte → 7 GB
- int4: parametre başına 0.5 byte → 3.5 GB

Kişisel GPU'da (6 GB VRAM olsa) 7B modeli ancak 4-bit quantize edilmiş olarak yükleyebilirsin. 1B-3B modelleri fp16 olarak rahatça yükleyebilirsin. 70B için 40+ GB'lık server GPU'ları veya bulut servisleri gerekli.

---

## Genel İzlenim

Transformer'ın ne kadar önemli olduğunu kavramak için şuna bakmak lazım: **bir tek mimari, on yıldan az bir sürede tüm derin öğrenme alanına yayıldı.** Metin, görüntü, ses, video, kod, tablosal veri, protein dizilimi — hepsi Transformer varyasyonlarıyla en iyi sonuçları veriyor. Öncesinde her alan kendi mimarisini kullanıyordu (CNN görüntüde, RNN sekansta, MLP tabuloda). Şimdi tek bir mimari her yerde.

Bunun sebebi şu olabilir: attention mekanizması aslında çok genel bir "bilgi toplama" işlemi. Her tokenın (ya da patch'in, frame'in, atomun) birbirine bakıp önemli olanı ayıklaması, doğanın verilerinin çoğunda faydalı olan bir işlem. Bu genelliği neden bu kadar iyi çalıştığının teorik açıklaması hâlâ bir araştırma konusu.
