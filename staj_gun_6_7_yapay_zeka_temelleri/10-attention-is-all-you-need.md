# "Attention Is All You Need" Makalesinin Önemi

Modern derin öğrenme tarihinin en önemli birkaç makalesinden biri, muhtemelen en önemlisi: "Attention Is All You Need". 2017 yılında NeurIPS'te yayınlandı. Bu makale, günümüzde tanıdığımız tüm büyük dil modellerinin temelinde yatan **Transformer** mimarisini tanıttı.

Orijinal arxiv linki: https://arxiv.org/abs/1706.03762

---

## Künye

- **Başlık:** Attention Is All You Need
- **Yazarlar:** Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin
- **Kurumlar:** Google Brain, Google Research, University of Toronto (Aidan Gomez)
- **Yayın:** Advances in Neural Information Processing Systems (NIPS/NeurIPS) 2017
- **Sayfa sayısı:** 15
- **Atıf sayısı:** 100.000+ (bilim tarihinin en çok atıf alan makalelerinden biri)

Başlığın kendisi bilinçli bir manifesto. O tarihte NLP alanında "attention" bir yardımcı katmandı — LSTM ya da GRU tabanlı seq2seq modelleri güçlendirmek için kullanılan bir eklenti. Yazarlar diyor ki: "hayır, attention sadece bir yardımcı değil, tek başına yeterli. Recurrence ve convolution'a gerek yok." Bu iddia o günün NLP camiasında oldukça cesur bir tez.

---

## Makalenin Ana İddiası

Makalenin abstract'ında ve girişinde savunulan tez tek cümlede özetlenebilir:

> **"Recurrence ve convolution kullanmadan, tamamen attention mekanizmalarına dayanan yeni bir sekans dönüşümü (sequence-to-sequence) mimarisi öneriyoruz. Bu mimari çeviri kalitesinde en yeni sonuçları geçiyor, çok daha az eğitim süresi alıyor ve doğası gereği paralelleştirilebilir."**

O günlerin standart sekans modeli RNN/LSTM tabanlıydı. Herkes şunu düşünüyordu: "sekans veriyi işlemek için sekansı sırayla adımlamalıyız." Bu makale bu varsayımı reddetti ve sekansın tamamına aynı anda bakan bir modelin daha iyi çalışabileceğini gösterdi. Bu paradigma değişimi bugünkü LLM patlamasının kökeni.

---

## Önerilen Mimarinin Ana Bileşenleri

Makale beş ana yenilik/tasarım kararı içeriyor. Her biri sonraki yıllarda milyonlarca modelde standart haline gelecek.

### 1) Scaled Dot-Product Attention

Basit ama etkili attention formülü:

```
Attention(Q, K, V) = softmax( (Q · Kᵀ) / √d_k ) · V
```

Bu formülün orijinal makaleden gelen iki önemli katkısı var:

- **√d_k ile ölçekleme:** iç çarpımların büyüklüğü `d_k` (key boyutu) ile büyüyor. Bu, softmax'a çok ekstrem değerler girmesini ve gradyanların yok olmasını engeller. Basit bir ekleme ama eğitim stabilitesi için kritik.
- **Matris formunda ifade:** attention'ı bir matris çarpımı olarak yazmak, GPU'da paralel hesaplanmasını mümkün kılıyor.

### 2) Multi-Head Attention

Tek bir attention başlığı yerine `h` paralel başlık:

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) · W_O
head_i = Attention(Q · W_Q_i, K · W_K_i, V · W_V_i)
```

Her başlığın kendi öğrenilebilir projeksiyon matrisleri var. Her başlık farklı ilişki türlerine odaklanabilir. Makalenin ablation tablosunda tek başlıklı vs çok başlıklı karşılaştırması yapılıyor — 8 başlık en iyi sonucu veriyor.

### 3) Positional Encoding

Attention sıraya duyarsız olduğu için pozisyon bilgisi elle enjekte edilmek zorunda. Sinüs ve kosinüs tabanlı sabit bir formül öneriliyor:

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

Makalede ayrıca "learned positional embedding" ile karşılaştırma yapıyorlar; benzer sonuç aldıklarını, sinusoidal'i tercih etme sebebinin eğitim zamanından uzun dizilere teorik jeneralizasyon umudu olduğunu belirtiyorlar.

### 4) Encoder-Decoder Yapı

Orijinal Transformer 6 encoder katmanı + 6 decoder katmanından oluşuyor. Bu, ilk uygulamanın makine çevirisi olmasından kaynaklanıyor:

- **Encoder:** kaynak cümleyi (İngilizce) işleyip anlam vektörlerine dönüştürüyor.
- **Decoder:** encoder'ın çıktısına ve o ana kadar üretilmiş hedef tokenlere bakarak sıradaki tokeni tahmin ediyor (Almanca'ya çeviri için).
- **Cross-attention:** decoder'ın encoder'a bakabilmesini sağlayan katman.

Modern LLM'ler bu ayrımı büyük ölçüde bıraktı — decoder-only tek başına yeterli hale geldi. Ama encoder-decoder yapı hâlâ çeviri, özetleme gibi bazı görevlerde tercih ediliyor.

### 5) Position-wise Feed-Forward Network

Attention'dan sonra, her token için ayrı ayrı çalışan iki katmanlı bir MLP:

```
FFN(x) = W_2 · ReLU(W_1 · x + b_1) + b_2
```

Boyutlar: `d_model = 512, d_ff = 2048`. Yani `d_ff = 4 · d_model` — bu oran sonrasında bir konvansiyon oldu.

### Layer Normalization + Residual Connections

Bunlar makalenin kendi buluşu değil, önceden var olan tekniklerdi. Ama Transformer'ı çalıştırabilmek için kritik olduğu için özenle entegre edilmişler.

- **Residual (skip) bağlantılar:** ResNet'ten (2015) gelen fikir. Gradyanların derin katmanlardan geçmesini sağlıyor.
- **Layer Normalization:** her katmanın çıktısını normalize ediyor. Eğitim stabilitesi için şart.

---

## Deneysel Sonuçlar

Makale iki çeviri görevinde ölçüldü:

### WMT 2014 İngilizce-Almanca

- Transformer (base): **BLEU 27.3**
- Transformer (big): **BLEU 28.4**
- O güne kadar en iyi: **BLEU 26.3** (Google'ın kendi Neural Machine Translation modeli)

### WMT 2014 İngilizce-Fransızca

- Transformer (big): **BLEU 41.8**
- En yüksek önceki sonuç: **BLEU 40.4**

Sadece iki puanlık iyileşme küçük görünebilir ama iki nokta önemli:

- Bu daha önceki en iyi sonuçları geçmek için o güne kadar yapılmış tüm gelişmelerin bir yıllık toplamından fazla ilerleme demek. BLEU skorlarında bu tür sıçramalar nadirdi.
- Aynı zamanda eğitim süresi dramatik olarak daha kısaydı. En iyi RNN modelleri hafta hafta eğitim isterken, Transformer 3.5 gün / 8 GPU (base) — 3.5 gün / 8 GPU (big) sürdü. O günün ekonomisinde bu çok hızlıydı.

### Ablation Tablosu (Table 3)

Makalenin en değerli parçalarından biri. Her tasarım kararının etkisini teker teker ölçüyorlar:

- Head sayısı (1, 4, 8, 16, 32): en iyi 8-16 arası
- Attention key boyutu (`d_k`)
- Model boyutu, katman sayısı
- Dropout oranı
- Learned vs sinusoidal positional encoding: fark yok denecek kadar az

Bu tablonun kendisi sonraki araştırmalara bir metodolojik model oldu — "her tasarım kararını ölçün" prensibi.

---

## Neden "Devrim"?

Makalenin önemini dört ana başlıkta topluyorum.

### 1) Paralel Eğitim Mümkün Oldu

RNN sıralı — bir sonraki adımı hesaplamak için önceki adımı beklemek zorundaydı. Transformer bir dizinin tüm tokenlerini aynı anda işleyebiliyor. Bu, GPU'nun paralel hesap yeteneğini tam olarak kullanabilmek demek.

Sonucu: model boyutu ve veri seti agresif biçimde büyütülebilir hale geldi. Bu doğrudan **scaling laws** (ölçekleme kanunları) araştırmalarına yol açtı — "model boyutu × veri × hesap" ile performansın nasıl arttığının kanıtlanması. GPT-3 gibi modellerin varlığı bu ölçekleme sayesinde mümkün oldu.

### 2) Uzun Mesafe Bağımlılıklar Kolaylaştı

RNN'de 500. tokene ulaşmak için önce 499 kez `f()` fonksiyonundan geçmek gerek. İlk tokenın bilgisi 500 kere sıkıştırılıp yeniden şekilleniyor, çoğu zaman kayboluyor. Transformer'da her token her tokene doğrudan bakabiliyor. Mesafe kavramı ortadan kalkıyor.

Bu sayede uzun paragrafları, çok cümleli akıl yürütmeleri, hatta tüm bir kod dosyasını modellemek mümkün oldu.

### 3) Transfer Learning Patlaması

Makaleden sonraki yaklaşık bir yıl içinde ortaya çıkan modeller:

- **GPT-1** (Haziran 2018) — Transformer decoder + büyük ölçekli önceki eğitim
- **BERT** (Ekim 2018) — Transformer encoder + masked language modeling
- **GPT-2** (Şubat 2019) — büyük ölçek, "zero-shot" yetenekler, çok daha genel modeller
- **T5, RoBERTa, XLNet, BART, ALBERT, ELECTRA, DeBERTa...** hepsi Transformer türevi

Bir mimari, bir alanın tamamını yenilemiş oldu. Bu boyutta bir yeknesaklık NLP tarihinde daha önce hiç olmamıştı.

### 4) NLP'nin Ötesine Yayıldı

Bu, 2017'de yazarların bile beklemediği bir sonuç. Transformer sadece dil için değil, başka modaliteler için de baskın mimari haline geldi:

- **Vision Transformer (ViT, 2020):** görüntüleri "patch" olarak tokenize et, Transformer'a ver. CNN'in görüntüde 10 yıllık hakimiyetini sarstı.
- **Whisper (2022):** ses tanıma. Encoder-decoder Transformer, çok dilli.
- **Stable Diffusion, DALL-E:** görüntü üretimi. Cross-attention Transformer blokları metin koşullaması için.
- **AlphaFold 2:** protein katlanma tahmini. Attention tabanlı.
- **RT-2, PaLM-E:** robotik. Vision-language-action modelleri.
- **AlphaZero, MuZero:** bazı takviye öğrenme sistemleri de attention benzeri mekanizmalar kullanıyor.

Bu genellik, Transformer'ın sadece bir "NLP mimarisi" olmadığını, daha genel bir bilgi işleme aracı olduğunu gösteriyor.

---

## Makalenin Dikkat Çeken Diğer Yönleri

**Yazımın temizliği.** 8 sayfada bir mimarinin tanıtımı, matematiksel tanımları, deneyleri, ablation'ları — hepsi net ve tekrar edilebilir biçimde. Deep learning makaleleri her zaman bu kadar özenli değil. Bu makale bir metodolojik iyi örnek.

**Karmaşıklık analizi (Table 1).** Self-attention `O(n² · d)`, recurrent `O(n · d²)`, convolutional `O(k · n · d²)`. Kısa dizilerde attention avantajlı (bugünkü çoğu senaryo). Ama uzun dizilerde `n²` bir dert — sonrasında bu dert FlashAttention, Sparse Attention, Linear Attention gibi araştırmalarla saldırıya uğradı.

**Attention görselleştirmeleri (Section 6.4).** Bazı head'lerin gerçekten anlamlı örüntüler öğrendiğini gösteriyorlar. Bir head bir zamiri, ait olduğu isme bağlıyor. Başka bir head bir sayı ifadesini konteksti içindeki ilgili kelimeye bağlıyor. Bu görselleştirmeler interpretability araştırmalarının başlangıç noktasından biri.

**Öğrenmediğim / atlanmış detaylar.** Label smoothing parametresi (0.1) neden bu değer, warmup schedule matematik detayı, BLEU hesabı — bunlar makalenin ana mesajından çok pratik eğitim ipuçları. Bir makaleyi ilk okumada bu tür detaylara girmek gerekmiyor.

---

## Bu Makale Olmasaydı Ne Olurdu?

Alandan uzak da olsa şöyle bir spekülasyon yapmak istiyorum:

LLM'ler yine muhtemelen olurdu, ama daha yavaş gelirdi. Belki 2025 yerine 2030'lar. Çünkü asıl darboğaz "paralel eğitilebilir bir sekans modeli" idi. Transformer bunu çözdü.

Alternatifler de vardı:

- **CNN tabanlı seq2seq modeller (ByteNet, WaveNet, ConvS2S).** Paralel olabiliyorlardı ama uzun mesafe bağımlılıklar için sürekli receptive field genişletme problemi vardı.
- **LSTM optimize etme.** Belki daha büyük LSTM'ler daha uzun süre eğitilerek benzer sonuçlara ulaşabilirdi ama pratik olarak zor.
- **State-space modeller (Mamba, S4).** Bunlar 2020'lerin sonlarında gündeme geldi. Belki daha erken keşfedilseydi Transformer'a benzer bir sıçrama yapabilirlerdi. Ama bugün bile Transformer'a rakip değiller.

Yani Transformer bir zorunluluktu belki de — ama tam olarak bu ekip, tam bu zamanlamayla önerdi ve alanı 5-10 yıl ileri taşıdı. Bugünkü ChatGPT, Claude, Gemini gibi sistemlerin varlığının kökeni doğrudan bu 15 sayfalık makale.

---

## Kısaca

- Transformer'ı tanıtan makale.
- Sekans işlemenin sıralı olması varsayımını yıktı.
- Paralel eğitim mümkün oldu → ölçek dramatik büyüdü → LLM'ler ortaya çıktı.
- NLP'nin ötesine yayıldı, tüm derin öğrenmenin standart mimarisi haline geldi.
- 100.000+ atıfla bilim tarihinin en etkili makalelerinden biri.

Bir mimarinin bir alanın tamamını bu kadar radikal değiştirmesi çok nadir. Belki de bilim tarihinde ancak on-on beş yılda bir denk gelinen bir olay.
