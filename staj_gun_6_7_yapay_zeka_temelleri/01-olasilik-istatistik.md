# Olasılık ve İstatistiğin Yapay Zeka ile Bağlantısı

## 0. Önce hafif bir hatırlatma — olasılık ve istatistik ne demekti?

- **Olasılık (probability)**: "gelecekte bir şeyin olma şansı ne?" sorusuna cevap verir. Elimizde kural veya dağılım var, ondan tahmin üretiyoruz.
  Örnek: Adil bir zar attığımda 6 gelme olasılığı = 1/6.
- **İstatistik (statistics)**: elimizde bir sürü **veri** var, buradan "bu veriyi üreten süreç neye benziyor?" diye çıkarım yapıyoruz.
  Örnek: 1000 kere zar atılır, 6'nın kaç kez geldiğine bakılıp zarın adil olup olmadığına karar verilir.

Yani ikisi birbirinin tersi gibi:
- Olasılık: **model → veri** yönünde çalışır ("bu modele göre ne bekliyoruz?").
- İstatistik: **veri → model** yönünde çalışır ("bu veri hangi modeli işaret ediyor?").

Yapay zeka aslında tam olarak bu **ikinci yönü** otomatikleştirmeye çalışıyor: elimizde bir sürü veri var, arkasındaki modeli/dağılımı bilgisayara öğret. Bu yüzden bağlantı bu kadar sıkı.

---

## 1. Kısa cevap (tek cümle özet)

Yapay zeka dediğimiz şey büyük oranda **istatistiksel öğrenme**. Model dünyayı anlamıyor, verinin **dağılımını** öğreniyor. Bir soru sorulduğunda "en olası cevap ne?" diye tahmin ediyor.

Bunu bir kere kabul edince, aşağıdaki her şey yerine oturuyor:
- Modelin çıktısı → **olasılık dağılımı**.
- Modelin öğrenme kuralı → **verinin olabilirliğini (likelihood) en büyükleme**.
- Modelin başarısı → **istatistiksel genelleme** (görmediği veride de tutması).

Aşağıda bunlar tek tek ele alınıyor.

---

## 2. Model neden olasılık üretiyor?

Yaygın bir yanılgı: "model kedi mi köpek mi diyor" gibi düşünmek. Aslında model direkt bir sayı vermiyor, bir **dağılım** veriyor.

### 2.1 Basit örnek: kedi-köpek sınıflandırıcı

Bir fotoğraf modele verildiğinde çıkışta şuna benzer bir şey gelir:

```
P(kedi | fotoğraf) = 0.87
P(köpek | fotoğraf) = 0.13
```

- Buradaki `|` "verildiğinde" demek. "Fotoğraf verildiğinde kedi olma olasılığı 0.87" diye okunuyor.
- İki değer topluyor: `0.87 + 0.13 = 1.00`.
- Bunu üreten şey **softmax** denen bir fonksiyon. Modelin ham çıktısını (logits) alıp 0-1 arasında olasılığa çeviriyor, toplamı 1 yapıyor.
- Biz sonunda "hangisi en yüksek" (argmax) diyerek "kedi" cevabına ulaşıyoruz. Ama karar bizim; modelin verdiği tabakta dağılım var.

### 2.2 Neden dağılım da tek cevap değil?

Birkaç sebep var:
1. **Belirsizlik gerçek.** Bulanık, kısmen gözüken bir hayvan fotoğrafında "%50-%50" cevabı daha dürüst.
2. **Karar mantığını dışarıda kurabiliyoruz.** Örneğin tıbbi teşhiste %70 kanser bile "biopsiye gönder" demek için yeterli. Modeli değiştirmeden eşiği (threshold) değiştirebiliyoruz.
3. **Modelin ne kadar emin olduğunu ölçüyoruz.** `[0.51, 0.49]` demekle `[0.99, 0.01]` demek arasında dünya kadar fark var; ilki güvensiz, ikincisi güvenli. Buna **confidence** ya da **uncertainty** deniyor.

### 2.3 LLM'de ne oluyor peki?

Aynı şey. ChatGPT, Claude, Gemini — hepsi bir sonraki **token** için tüm kelime haznesi üstünde bir dağılım üretiyor.

Diyelim ki tokenizer'da 50000 farklı token var. Model şu an "Türkiye'nin başkenti" diye bir cümle görüyor. Çıkışta 50000 elemanlı bir olasılık dağılımı üretiyor:

```
P(sonraki_token = "Ankara" | "Türkiye'nin başkenti") = 0.92
P(sonraki_token = "İstanbul" | "Türkiye'nin başkenti") = 0.04
P(sonraki_token = "başkenti"  | ...) = 0.001
...
```

Sonra oradan bir **örnekleme** (sampling) yapıyor. Yöntem birkaç tane:
- **Greedy**: her seferinde en olasıyı al ("Ankara").
- **Top-k**: en yüksek k tanesi arasından ağırlıklı çek.
- **Top-p (nucleus)**: toplam olasılığı %90 (veya belirlediğimiz p) olan kümenin içinden çek.
- **Temperature**: dağılımı yayıp toplayan bir ayar. Yüksek temperature = daha "yaratıcı" ama saçmalayabilir; düşük = tutucu ve tekrar edici.

### 2.4 Buradan çıkan temel sonuç

"AI gerçekten düşünüyor mu?" sorusunun istatistik cevabı: hayır. Model **veriden çıkardığı olasılık dağılımından örnekleme** yapıyor. Zeki gibi görünmesi, dağılımın gerçekten çok iyi öğrenilmiş olmasından.

Bunu anlamadan halüsinasyon, temperature ayarı, sampling yöntemleri, "aynı promptu sorsam neden farklı cevap veriyor" hep havada kalıyor. Bir kere olasılık gözlüğüyle bakınca hepsi birden anlaşılır oluyor.

---

## 3. Ortalama, varyans, dağılım — bunlar sadece ders konusu değil, kod içinde var

Bu kavramlar teorik ders konusu gibi görünse de eğitim kodunun her adımında karşımıza çıkıyor.

### 3.1 Ortalama (mean)

Basit: `mean = (x1 + x2 + ... + xn) / n`. AI'daki yerleri:

- **Veri normalize etme.** Piksellerin ortalamasını çıkarıp `(x - mean) / std` yapıyoruz. Bunu yapmadan model çok yavaş öğreniyor.
- **Loss hesabı.** Batch içindeki 32 örneğin loss'unu tek tek hesaplayıp **ortalamasını** alıyoruz. Sonra o ortalamaya göre parametre güncelleniyor.
- **Batch Normalization / Layer Normalization.** Ara katmanlarda çıkan aktivasyonların ortalamasını sıfıra çekmek → eğitimi stabilize ediyor.

Yani ortalama, kodun her adımında karşımızda.

### 3.2 Varyans (variance) ve standart sapma (std)

Varyans = "veri ortalamadan ne kadar sapıyor?"nun karesi. Std = varyansın karekökü, aynı birimde ölçüyor.

- **Ağırlık başlatma (weight initialization).** Bir sinir ağını sıfırlarla başlatırsan hiç öğrenmiyor; rastgele başlatırsan ama "yanlış varyansla" başlatırsan gradyanlar patlıyor ya da yok oluyor (exploding / vanishing gradients).
  Çözüm: **Xavier (Glorot) init** ve **He init** gibi yöntemler. Bunların özü, her katmandaki ağırlıkların varyansını, o katmanın giriş/çıkış boyutuna göre ayarlamak. Formüller doğrudan istatistik: `Var(W) = 1/n` veya `2/n` tarzı.
- **Normalizasyon.** `(x - mean) / std` derken paydadaki `std`, verinin dağılım genişliğini standartlaştırıyor.
- **Sinyal-gürültü.** Regularization tekniklerinin (dropout, weight decay) çoğu, aslında gürültünün varyansını kontrol etmekle ilgili.

### 3.3 Dağılım (distribution)

Bir dağılım, bir değişkenin hangi değerleri hangi olasılıkla aldığını söylüyor. AI'da sürekli görüyoruz.

#### Normal (Gauss) dağılımı

Meşhur çan eğrisi. Ortalama etrafında yoğunlaşıp uzaklaştıkça olasılık düşüyor.

Nerede kullanılıyor:
- Ağırlık başlatma çoğunlukla normal dağılımdan çekilir.
- Model bazı çıktıları normal dağılım varsayımıyla üretir (regresyonda hata dağılımı normal kabul edilir).
- **Variational Autoencoder (VAE)** gibi modellerde gizli uzay normal dağılımlı olacak şekilde eğitilir.

Normal dağılım "belirsizliğin en doğal hali" olarak düşünülebilir, çünkü **Merkezi Limit Teoremi**'ne göre bir sürü küçük bağımsız etki toplandığında sonuç normal dağılıma yaklaşır. Bu yüzden bu dağılım hemen her yerde karşımıza çıkar.

#### Bernoulli dağılımı

Sadece iki değer: 0 ya da 1. "Yazı-tura" dağılımı.

- İkili sınıflandırmada (spam / spam değil) tam olarak bu dağılım kullanılır.
- Modelin çıktısı bir tek `p` sayısı olur, "1 olma olasılığı".
- Loss olarak **binary cross-entropy** kullanılır.

#### Kategorik (multinoulli) dağılım

Bernoulli'nin çok sınıflı hali. K farklı sonuçtan biri.

- Kedi-köpek-kuş sınıflandırmasında bu var.
- **LLM'de bir sonraki token seçimi de bir kategorik dağılım** (50000 kategori).
- Softmax çıktısı = kategorik dağılım parametreleri.
- Loss olarak **cross-entropy** kullanılır.

#### Uniform dağılım

Tüm değerler eşit olasılıklı. AI'de:
- İlk ağırlık başlatmaların bir kısmında (Uniform Xavier).
- Dropout maskesi çekerken.
- Data augmentation'da rastgele parametre seçerken.

#### Kısa çıkarım

Modelin her kritik adımında (init → forward → loss → sampling) bir **dağılım varsayımı** var. Bu yüzden BatchNorm mu LayerNorm mu, MSE mi cross-entropy mi, temperature ne yapıyor sorularının hepsinin cevabı bir dağılıma dayanıyor.

---

## 4. Bayes teoremi ve sınıflandırma bağlantısı

Bu kavramı somutlaştırmanın en etkili yollarından biri klasik spam filtresi örneğidir.

### 4.1 Formül

```
P(A | B) = ( P(B | A) * P(A) ) / P(B)
```

Türkçesi: "B'yi gördükten sonra A'nın olma ihtimali" = "A'yken B'nin çıkma ihtimali" × "A'nın en baştan olma ihtimali" / "B'nin toplamda çıkma ihtimali".

Terimlerin adları:
- `P(A)` → **prior** (önsel, veriyi görmeden önceki inanç).
- `P(B | A)` → **likelihood** (A doğruysa B'yi görme olasılığı).
- `P(A | B)` → **posterior** (sonsal, veriyi gördükten sonraki inanç).

Bayes teoremi aslında şunu diyor: bir şey hakkında bir ön inanç vardır; yeni bir veri gelir; bu inanç güncellenir.

### 4.2 Spam filtresi örneği (adım adım)

Diyelim ki mail geldi, içinde "kazandınız" kelimesi var. Bu mailin spam olma olasılığı ne?

Bildiklerimizi yazalım (uydurma sayılar):
- `P(spam) = 0.4` → gelen mailleri sayıp bulduk, %40'ı spammiş. Bu prior.
- `P("kazandınız" | spam) = 0.7` → spam mailerin %70'inde bu kelime geçiyor. Likelihood.
- `P("kazandınız" | spam değil) = 0.05` → normal maillerin %5'inde geçiyor.

`P("kazandınız")` toplam olasılığını hesaplayalım (marjinalizasyon):
```
P("kazandınız") = 0.7 * 0.4 + 0.05 * 0.6 = 0.28 + 0.03 = 0.31
```

Şimdi Bayes:
```
P(spam | "kazandınız") = (0.7 * 0.4) / 0.31 = 0.28 / 0.31 ≈ 0.90
```

Yani bu kelimeyi görünce mailin spam olma olasılığı %40'tan %90'a çıkıyor. Çok temiz bir güncelleme.

### 4.3 AI'daki yeri

- **Naive Bayes sınıflandırıcı**: yıllarca spam filtreleri, doküman sınıflandırma bu formülle yapıldı. "Naive" (saf) demesinin sebebi, kelimeleri birbirinden bağımsız kabul etmesi. Basit ama çok işe yarıyor.
- **Modern sinir ağları da aslında `P(sınıf | veri)` tahmin ediyor.** Formülü doğrudan hesaplamak yerine veriden öğreniyorlar ama işin sonunda ürettikleri şey posterior.
- **Bayesian deep learning**: ağırlıkları tek sayı değil, dağılım olarak öğrenmek. Model bize sadece cevabı değil, "ne kadar emin olduğunu" da veriyor. Güvenlik-kritik uygulamalarda (medikal, otonom araç) önemli.

Kısacası, sınıflandırma problemi = **koşullu olasılık tahmini**. Bunu bir kere kabul edince pek çok yöntem birbirine bağlanıyor.

---

## 5. Maximum Likelihood → Loss fonksiyonu

Loss fonksiyonları çoğu zaman ezberlenir: "sınıflandırmada cross-entropy, regresyonda MSE". Peki neden? Hepsi tek bir ilkeden, Maximum Likelihood'dan çıkıyor.

### 5.1 Maximum Likelihood Estimation (MLE) nedir?

Şöyle bir mantık: elimizde veri var (`x1, x2, ..., xn`). Bu veriyi üreten bir dağılım var ama dağılımın parametreleri (`θ`) bilinmiyor.

Sorumuz: "Öyle bir `θ` seçelim ki, elimizdeki verinin ortaya çıkma olasılığı **en yüksek** olsun."

Formal:
```
θ* = argmax_θ  P(veri | θ)
```

Yani "parametreleri şuna ayarlarsam, bu veriyi görme ihtimalim en büyük olur" sorusunun cevabı.

### 5.2 Neden logaritma alıyoruz?

Verinin olasılığı aslında bir çarpım:
```
P(veri | θ) = P(x1|θ) * P(x2|θ) * ... * P(xn|θ)
```

Bir sürü küçük sayıyı çarpınca (0.01, 0.03, 0.001 gibi) sonuç çok küçülüyor, bilgisayar yuvarlıyor. Buna **underflow** deniyor. Ayrıca çarpımları türev almak da zor.

Çözüm: logaritma alalım. Logaritma monotonik olduğu için `argmax` değişmez. Çarpım toplama dönüşür:
```
log P(veri | θ) = log P(x1|θ) + log P(x2|θ) + ... + log P(xn|θ)
```

### 5.3 Eksisini alıp minimize etmek

Optimizasyon algoritmalarımız (gradient descent) genelde **minimize** üzerine kurulu, `argmin`. O yüzden eksisini alıp problemi ters çeviriyoruz:
```
θ* = argmin_θ  - Σ log P(x_i | θ)
```

İşte bu ifade, **negatif log-likelihood** (NLL). Modern derin öğrenmedeki loss fonksiyonlarının doğrudan kendisi.

### 5.4 Cross-entropy örneği (adım adım)

Sınıflandırma için verinin dağılımı kategorik. Modelin verdiği olasılık `q`, gerçek etiket `y` (one-hot).

Tek örnek için:
```
- log P(y | model) = - Σ_k  y_k * log q_k
```

Bu direkt cross-entropy formülü. Bütün veri üstünden ortalarsak, klasik cross-entropy loss çıkıyor.

Yani cross-entropy = **kategorik dağılım için MLE**. Ezberlenecek bir formül değil, türetilmiş bir sonuç.

### 5.5 MSE örneği

Regresyon için hataların normal dağıldığını varsayarsak (ortalama = modelin tahmini, sabit varyans), o zaman:
```
P(y | x, θ) = normal_pdf(y ; mean = model(x), var = σ²)
```

Log alıp eksisini yazınca, sabitleri atınca:
```
NLL ∝ Σ (y - model(x))²
```

Bu da **MSE**. Yani MSE = **normal dağılım varsayımı altında MLE**.

### 5.6 Binary cross-entropy

Bernoulli için de aynı türetme geçerli, sonucunda binary cross-entropy formülü çıkıyor.

### 5.7 Bu bakışın kazandırdığı sezgi

Yeni bir problemle karşılaşınca sorulacak temel soru: **"Veri hangi dağılıma benziyor?"** Cevaba göre uygun loss türetilebilir.

Örnek:
- Sayma verisi (etkinlik sayısı, tıklama sayısı) → **Poisson** dağılımı → Poisson NLL loss.
- Fiyat tahmini gibi çarpık (asimetrik) dağılımlarda MSE her zaman iyi olmayabilir → farklı loss seçimi.

Bu bakış, loss fonksiyonu seçmeyi ezberden çıkarıp bir tercih meselesine dönüştürüyor.

---

## 6. Örneklem, anakütle, bias-variance dengesi

Bu bölüm, "modelim eğitimde harikayken neden gerçek dünyada rezil oluyor?" sorusunun cevabı.

### 6.1 Anakütle (population) ve örneklem (sample)

- **Anakütle**: gerçekte var olan tüm veri. Örneğin dünyadaki tüm kedi fotoğrafları. Ulaşamayız.
- **Örneklem**: bizim toplayıp elimizde tuttuğumuz, o anakütleden çekilmiş küçük bir alt küme.

Model aslında anakütleyi hiç görmüyor, sadece örneklemi görüyor. Örneklem anakütleyi ne kadar iyi temsil ediyorsa model o kadar iyi **genellenir** (generalize eder).

Buradan çıkan pratik dersler:
- Örneklem dengesizse (mesela veride %95 kedi %5 köpek varsa) model dengesiz öğrenir.
- Örneklem küçükse rastlantısal örüntüleri gerçek sanır.
- Örneklem tek bir kaynaktan geliyorsa (mesela sadece stok fotoğraflar) model gerçek hayat fotoğrafında bozulur (**distribution shift**).

### 6.2 Bias-variance trade-off

Bu kavram şöyle çalışıyor. Modelin toplam hatası kabaca iki bileşene ayrılıyor:

- **Bias (yanlılık)**: modelin varsayımlarının basitliğinden gelen hata. Model çok basitse veriyi anlayacak esneklikte değildir → **underfitting**. Sonuç: train loss yüksek, validation loss da yüksek.
- **Variance (varyans)**: modelin veriye aşırı uyum sağlamasından gelen hata. Model çok karmaşıksa, örneklemi ezberler ama yeni veride bozulur → **overfitting**. Sonuç: train loss çok düşük, validation loss yüksek.

Bunlar birbirinin tersi çalışıyor:
- Modeli büyüttükçe bias azalır, variance artar.
- Küçülttükçe tersi olur.
- Amaç ikisinin toplamını minimize eden **tatlı noktayı** bulmak.

Not: son yıllarda "double descent" diye bir gözlem var — çok büyük modellerde variance beklenenden farklı davranabiliyor. LLM'ler o çizginin ötesinde. Ama temel sezgi hâlâ geçerli.

### 6.3 Overfitting'e karşı ne yapıyoruz?

Bunların neredeyse hepsi "variance'ı düşürme" tekniği:
- **Daha fazla veri toplamak** (en etkilisi).
- **Data augmentation** (görüntü döndürme, kırpma, metinlerde parafraz).
- **Regularization** (L1/L2, weight decay) — ağırlıklara ceza koyarak modeli sadeleşmeye zorluyor.
- **Dropout** — eğitim sırasında rastgele nöronları kapatmak, ağı belirli yollara bağımlı olmaktan çıkarıyor.
- **Early stopping** — validation loss yükselmeye başladığı anda eğitimi durdurmak.
- **Basit model seçmek** — bazen 100M parametre yerine 10M parametre yeter.

### 6.4 Train / Validation / Test setleri

Overfitting'i fark edebilmek için veriyi üçe ayırıyoruz:
- **Train**: model bunu görerek öğrenir.
- **Validation (dev)**: model bunu görmez, ama biz eğitim sırasında bunu üstünde ölçüp hiperparametre kararı veriyoruz (learning rate, model boyutu vb.).
- **Test**: model **ve biz** karar süreci boyunca bunu hiç kullanmayız. Tek amacı, sonda gerçekçi bir performans ölçmek.

Test setine bakıp kararlar verirsek, farkında olmadan modeli o sete "overfit" ederiz ve gerçek dünya sonucu kötü olur. Buna **data leakage** (veri sızıntısı) deniyor. Bir kere test setiyle karar verildiyse artık o test set bozulmuş sayılır.

---

## 7. "Peki AI neden çalışıyor?" — istatistik cevabı

Buraya kadarki tüm kavramlar birleştirildiğinde ortaya çıkan cevap şu:

> Yapay zeka çalışıyor çünkü **veri bir dağılımdan geliyor** ve model o dağılımı yeterince iyi taklit etmeyi öğrenebiliyor. Yeni bir giriş geldiğinde, model o girişin dağılımın hangi bölgesine düştüğünü tahmin edip oradan bir çıktı üretiyor.

Yani "zeka" değil, **istatistiksel yakınlık**. LLM'in "Türkiye'nin başkenti neresi?" sorusuna "Ankara" demesi, dünyayı bildiğinden değil; eğitim verisinde bu iki kelimenin çok güçlü olasılıksal bağı olduğundan.

Bu bakış birçok davranışı da açıklıyor:

- **Halüsinasyon**: model, eğitim dağılımında az gördüğü ya da hiç görmediği bir bölgede kendinden emin bir çıktı üretebilir. İstatistik dilinde: modelin extrapolate ettiği bir bölge.
- **Prompt engineering**: girdiyi değiştirince koşullu olasılık `P(cevap | prompt)` değişir, çıktı da değişir. Prompt'a örnek eklemek (few-shot) modelin koşulunu daraltıyor.
- **Fine-tuning**: modelin gördüğü dağılımı bizim istediğimiz yöne kaydırmak.
- **RAG (Retrieval-Augmented Generation)**: prompt'a ek bilgi vererek koşullu dağılımı zenginleştirmek.
- **Temperature ayarı**: modelin çıktı dağılımını daha sivri ya da daha yayvan yapmak.

Hepsi aynı çekirdeği farklı bir noktadan yontuyor.

---

## 8. Özet şema

Kavramlar arasındaki bağlantıyı gösteren bir zihinsel harita:

```
[ İstatistik / Olasılık ]
        │
        ├── Dağılım kavramı ──► Modelin çıktısı softmax (olasılık) verir.
        │
        ├── Ortalama / Varyans ──► Normalize, weight init, BatchNorm / LayerNorm.
        │
        ├── Farklı dağılımlar ──► Bernoulli (ikili), Kategorik (çok sınıflı),
        │                        Normal (regresyon), Uniform (rastgelelik).
        │
        ├── Bayes teoremi ──► Sınıflandırma = koşullu olasılık tahmini.
        │
        ├── Maximum Likelihood ──► Cross-entropy, MSE, binary cross-entropy — hepsi buradan.
        │
        ├── Örneklem vs. Anakütle ──► Genelleme problemi.
        │
        └── Bias-Variance ──► Underfitting / Overfitting, regularization, dropout,
                              early stopping mantığı.
```

---

## 9. Daha ileri araştırılabilecek konular

- **Cross-entropy vs. KL divergence** ilişkisi: cross-entropy = entropi + KL divergence eşitliği.
- **Bayesian deep learning**: "model ne kadar emin?" sorusuna klasik sinir ağlarında tam cevap yok; Bayesian yaklaşımlar bu boşluğu doldurmaya çalışıyor.
- **Kalibrasyon (calibration)**: model %90 dediğinde gerçekten %90 haklı çıkıyor mu? Modern büyük modeller çoğunlukla overconfident; ölçüm için "reliability diagram" kullanılıyor.
- **Double descent**: klasik bias-variance eğrisinin ötesindeki modern gözlem — model kapasitesi arttıkça hata bir noktada tekrar düşüyor.

---

## 10. Sonraki başlıkla bağlantı

Bir sonraki konu: **notebook tabanlı programlama** (`02-notebook-programlama.md`).

Bağlantısı şu: istatistiksel keşif (EDA — Exploratory Data Analysis) yapmak için notebook ortamı biçilmiş kaftan. Verinin dağılımına bakmak, histogramını çizmek, ortalama-varyansını görmek, hızlıca modeli deneyip loss eğrisini izlemek — hepsi hücre hücre çalışmaya çok uygun.

Yani istatistik "neden" sorusunun cevabıysa, notebook "nasıl bakarım" sorusunun cevabı.

---

**Durum:** Tamamlandı. Bir sonraki dosya: `02-notebook-programlama.md`.
