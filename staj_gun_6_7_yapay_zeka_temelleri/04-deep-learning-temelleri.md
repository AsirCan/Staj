# Deep Learning Temelleri

## 1. Deep Learning ML'den nasıl farklı?

Aslında farklı değil, ML'in bir alt dalı. Fark şu: modelin **birden fazla katmanlı** ve **çok sayıda parametreli** olması.

- Klasik ML: doğrusal regresyon, karar ağacı, SVM. Genelde tek bir "matematiksel biçim".
- Deep Learning: küçük fonksiyonları (katmanları) üst üste yığıp çok büyük ve esnek bir model kuruyoruz. "Deep" (derin) dediğimiz şey katman sayısının fazla olması.

Neden bu iş oldu?
1. **Veri patladı.** İnternet, sensörler → milyonlarca örnek.
2. **GPU'lar geldi.** Matris çarpımlarını paralel yapmak DL'in temeli.
3. **Katmanlı modellerin** görüntü, ses, metin gibi karmaşık verilerde klasik ML'i açık ara geçtiği görüldü.

---

## 2. Neural Network (sinir ağı) nedir?

En basit tanım: **peş peşe dizilmiş katmanlardan oluşan bir fonksiyon**.

Bir katman, girişini bir matris çarpımı + toplama + doğrusal olmayan bir dönüşümden geçiriyor. Bunu üst üste koyunca çok karmaşık bir fonksiyon elde ediyoruz.

Görsel şu:

```
Giriş (x)  →  [Layer 1]  →  [Layer 2]  →  ...  →  [Layer N]  →  Çıkış (y)
```

Her katmanın kendi **weight** ve **bias**'ları var; bunlar öğrenilebilir parametreler.

### 2.1 Beyin analojisi (dikkatli kullanmak lazım)

"Sinir ağı" adı biyolojik nöronlardan geliyor ama modern sinir ağları biyolojik beynin bir modeli değil. Sadece isim benzerliği var. Biraz ilham almış, o kadar. Bu konuda kafamı fazla karıştırmayacağım.

Kabaca: yapay bir "nöron" =
```
çıktı = aktivasyon( w1*x1 + w2*x2 + ... + wn*xn + b )
```
Yani girişlerin ağırlıklı toplamını al, bir aktivasyon fonksiyonundan geçir. Bu tek bir nöron. Katmanda birçok nöron var, ağda birçok katman.

---

## 3. Layer (Katman)

Bir katman, birçok nöronu bir arada tutuyor. Aynı girişi alıp farklı ağırlıklarla farklı çıktılar üretiyorlar.

Matematiksel olarak:
```
y = aktivasyon( W · x + b )
```
- `x` boyutu: (n_giriş,)
- `W` boyutu: (n_çıkış, n_giriş) — ağırlık matrisi
- `b` boyutu: (n_çıkış,) — bias vektörü
- `y` boyutu: (n_çıkış,) — bu katmanın çıktısı, sonraki katmanın girdisi

Yani bir katman = **matris çarpımı + bias eklemesi + aktivasyon fonksiyonu**.

### 3.1 Yaygın katman türleri

- **Dense / Linear / Fully Connected**: yukarıda anlattığım. Her giriş her nörona bağlı.
- **Convolutional (CNN)**: görüntü için. Küçük filtreler görüntü üstünde kayıyor, yerel örüntü yakalıyor.
- **Recurrent (RNN, LSTM, GRU)**: dizisel veri için. Bir öncekinin çıktısını da girdi olarak alıyor.
- **Attention / Transformer katmanı**: modern NLP'nin temeli. Ayrı bir dosyada detaylı ele aldım.
- **Normalization katmanları (BatchNorm, LayerNorm)**: eğitim stabilitesi için.
- **Dropout**: eğitimde rastgele nöron kapatarak overfitting'e karşı.

Şimdilik ilk türü (Dense) yeterli, geri kalanı sırayla göreceğim.

---

## 4. Weight ve Bias

**Weight (ağırlık)**: bir girişin çıktıya ne kadar etki edeceğini belirleyen sayı.
**Bias (sabit terim)**: her nörona eklenen sabit, "sıfır girişte bile bir çıktı" verebilme kabiliyeti.

Basit örnek: `y = w1*x1 + w2*x2 + b`
- `w1 = 2`, `w2 = 5`, `b = 1` ise → `y = 2*x1 + 5*x2 + 1`.
- `x2`'nin etkisi `x1`'in etkisinin 2.5 katı.
- Girişler 0 olsa bile `y = 1`.

Bir modelin parametre sayısı = tüm katmanlardaki weight + bias sayısı.

### 4.1 Parametre sayısı hesabı (küçük örnek)

3 katmanlı bir ağ:
- Katman 1: 784 → 128 (yani 784 boyutlu girişi 128 boyutlu çıktıya çeviriyor)
- Katman 2: 128 → 64
- Katman 3: 64 → 10

Parametreler:
- Katman 1: 784 * 128 = 100.352 weight + 128 bias = 100.480
- Katman 2: 128 * 64 = 8.192 + 64 = 8.256
- Katman 3: 64 * 10 = 640 + 10 = 650
- **Toplam: ~109.386 parametre**

Bu küçük bir modelin sayısı. LLM'lerdeki milyarlar bu mantığın çok büyütülmüş hali.

### 4.2 Ağırlık başlatma (initialization)

Ağırlıkları sıfırla başlatırsak model hiç öğrenmez (her nöron aynı şeyi yapar). Rastgele başlatmak da yetmez, doğru **varyansla** başlatmak lazım.

- **Xavier / Glorot init**: sigmoid, tanh için uygun.
- **He init**: ReLU, GELU için uygun (daha büyük varyans).

Neden önemli: yanlış varyansla başlatırsan gradyanlar patlar ya da yok olur. Modern framework'ler doğru olanı otomatik yapıyor ama arkada olan bu.

---

## 5. Forward Pass (İleri Yayılım)

**Girişin katmanlar boyunca ilerleyip çıktıya dönmesi.**

Şöyle akıyor:

```
x → [Katman 1: W1·x + b1, sonra aktivasyon] = a1
   → [Katman 2: W2·a1 + b2, sonra aktivasyon] = a2
   → [Katman 3: W3·a2 + b3, sonra softmax] = y_tahmin
```

Yani her katman kendinden önceki katmanın çıktısını alıp kendi hesabını yapıyor. Model bir "boru hattı" gibi.

Forward pass'in çıktısı: tahmin (`y_tahmin`).

Elimizde gerçek etiket (`y_gerçek`) varsa, ikisinin arasındaki farkı **loss** ile ölçüyoruz. Loss tek bir sayı.

---

## 6. Backpropagation (Geri Yayılım)

Bu deep learning'in en can alıcı fikri. Ilk okuduğumda karmaşık geldi ama özü aslında **zincir kuralı**.

### 6.1 Neden gerekli?

Modelde milyonlarca parametre var. Her birinin loss'u nasıl etkilediğini (yani "türevi"ni) bilmemiz lazım ki güncelleyebilelim. Elle hesaplamak imkansız. Backprop bu türevleri sistemli olarak hesaplayan algoritma.

### 6.2 Zincir kuralı hatırlatması

Kalkülüsten:
```
Eğer y = f(g(x)) ise, dy/dx = f'(g(x)) * g'(x)
```

Yani iç içe fonksiyonların türevini, dıştan içe doğru çarparak buluyoruz.

### 6.3 Sinir ağında ne oluyor?

Loss'u en son katmanın çıktısına göre türeyebiliyoruz kolayca. Onun bir önceki katmanı etkilediğini biliyoruz. Zincir kuralı ile geriye doğru **her katmanın gradyanını** hesaplıyoruz.

Görsel:
```
Loss  ←  Layer N  ←  Layer N-1  ←  ...  ←  Layer 1  ←  Giriş
       gradient        gradient              gradient
       burada          burada                burada
       hesaplanır      hesaplanır            hesaplanır
```

Yani **forward pass sağdan-sola gitti, backward pass soldan-sağa geliyor**. Bu yüzden "geri yayılım" (backpropagation).

### 6.4 PyTorch'ta ne yapıyoruz?

Bu ürkütücü matematiği PyTorch bizim için hallediyor:
```python
loss.backward()
```
Tek satırla bütün ağa gradyanlar yayılıyor. Bu yüzden pratik olarak backprop'u elle yazmak zorunda değiliz, ama nasıl çalıştığını bilmek şart.

### 6.5 Autograd (otomatik türev)

PyTorch'un `autograd` diye bir motoru var. Sen forward pass'i yazarken, o arka planda "hesap grafiği" (computational graph) tutuyor. `.backward()` çağırınca bu grafik boyunca gradyanları hesaplıyor. Bunu 06'daki PyTorch Blitz'de kod üstünde göreceğim.

---

## 7. Gradient Descent (Gradyan İnişi)

Gradyanları biliyoruz. Şimdi parametreleri güncelleyeceğiz. Kural:

```
yeni_θ = eski_θ - learning_rate * gradyan
```

Neden **eksi** işaretli:
- Gradyan, loss'un artış yönünü gösteriyor.
- Biz azaltmak istiyoruz, o yüzden ters yöne gidiyoruz.

Neden **learning rate** (öğrenme oranı):
- Adım büyüklüğünü kontrol ediyor.
- Çok büyükse minimumu atlar (etrafında zıplar).
- Çok küçükse çok yavaş öğrenir ya da yerel minimuma sıkışır.
- Tipik değerler: 0.001 - 0.0001 arası (deep learning için).

### 7.1 Kayak metaforu

Loss fonksiyonunu bir dağ manzarası gibi düşün. Amacın en alçak noktaya inmek.
- Bulunduğun noktada yamacın eğimine bakıyorsun (gradyan).
- Eğimin ters yönüne bir adım atıyorsun (yeni_θ).
- Ne kadar büyük adım atacağın learning rate ile belirleniyor.
- Sonunda vadinin dibine iniyorsun (loss minimum).

Ama dikkat: gerçek loss manzarası milyon boyutlu, bir sürü tepe ve vadi var. **Global minimum** yerine **yerel minimum**a takılabiliyoruz. Modern derin ağlarda bu genelde çok sorun olmuyor, çünkü yerel minimumlar bile yeterince iyi.

### 7.2 Batch vs Mini-batch vs Stochastic

- **Batch Gradient Descent**: tüm veri üstünden ortalama gradyan hesapla, sonra güncelle. Doğru ama yavaş, büyük veride yapılamaz.
- **Stochastic Gradient Descent (SGD)**: her örnek için ayrı güncelleme. Hızlı ama gürültülü.
- **Mini-batch SGD**: 32-256 örneklik gruplarla güncelleme. Hız ve stabilite dengeli. **En yaygın kullanılan** yaklaşım.

---

## 8. Optimizer'lar (SGD, Adam vs.)

Gradient descent'in daha akıllı versiyonları. Hepsi aynı temel fikri kullanıyor: gradyanın ters yönüne git. Ama farklı iyileştirmeler ekliyorlar.

### 8.1 SGD (vanilya)

En basiti. Yukarıdaki formül aynen:
```
θ = θ - lr * grad
```

### 8.2 SGD + Momentum

Fizikten esinlenmiş. Önceki gradyanları bir "hız" olarak saklıyor, aynı yöne devam ederse hızlanıyor:
```
v = β * v + grad
θ = θ - lr * v
```
Faydası: küçük dalgalanmaları söndürüyor, tutarlı yönlere hızlı ilerliyor. `β = 0.9` tipik.

### 8.3 Adam (en popüleri)

"Adaptive Moment Estimation". Her parametre için ayrı **learning rate ölçeği** tutuyor. Gradyanın ortalamasını ve varyansını takip ediyor, ona göre adım ayarlıyor.

Avantajları:
- Hiperparametre ayarına çok bağımlı değil (default'la genelde iyi çalışır).
- Farklı parametreler için farklı adım büyüklüğü.
- Hızlı yakınsıyor.

Bugün ML'in default'ı Adam.

### 8.4 AdamW

Adam'in "weight decay" (regularization) versiyonu. Adam'ın küçük bir bug'ını düzeltiyor. Modern LLM eğitimlerinde neredeyse standart. GPT, Llama, Claude — hepsi AdamW ile eğitiliyor.

### 8.5 Diğerleri

- **RMSProp**: Adam'ın atası, hala bazı yerlerde.
- **Adagrad**: seyrek verilerde iyi ama learning rate zamanla çok küçülüyor.
- **Lion, Sophia** gibi yeni optimizer'lar da çıktı, tartışma sürüyor.

### 8.6 Nasıl seçerim?

Kendi kısa kural setim:
- **Hiç düşünme, Adam(W) başla.** %90 problemde iyidir.
- Klasik computer vision task'larında SGD + momentum bazen daha iyi genelliyor (araştırmacılar tercih ediyor).
- Yeni optimizer denemek "son %1'i kazanma" işi, temeli oturana kadar gerek yok.

---

## 9. Activation Functions (Aktivasyon Fonksiyonları)

**Neden gerekli?** Sinir ağı sadece matris çarpımlarından ibaret olsaydı, aslında büyük tek bir matris çarpımına eşdeğer olurdu (birkaç lineer katmanın birleşimi lineer kalıyor). O zaman derinliğin faydası olmazdı.

Aktivasyon fonksiyonu → doğrusal olmayan (non-linear) bir bükülme ekliyor. Sayesinde ağ karmaşık ilişkileri öğrenebiliyor.

### 9.1 Sigmoid

```
σ(x) = 1 / (1 + e^(-x))
```
- Çıkışı 0-1 arası.
- Eski dönemin favorisi.
- Sorun: büyük değerlerde gradyan sıfıra çok yaklaşıyor → **vanishing gradient**.
- Bugün: sadece ikili sınıflandırmanın son katmanında (çıktı olasılığa dönmesi için).

### 9.2 Tanh

```
tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))
```
- Çıkışı -1 ile 1 arası.
- Sigmoid'e benzer ama merkezi 0.
- Aynı vanishing gradient sorunu var.
- Bugün: bazı RNN türlerinde hala kullanılıyor.

### 9.3 ReLU (Rectified Linear Unit)

```
ReLU(x) = max(0, x)
```
- Negatiflere 0, pozitifleri olduğu gibi geçirir.
- Basit, hızlı, gradyanı 1 (pozitif tarafta).
- CNN'lerin ve pek çok modern ağın standardı oldu.
- Sorun: negatif tarafta gradyan 0. Bir nöron sürekli negatif çıktı verirse hiç öğrenmez ("**dying ReLU**" problemi).

### 9.4 GELU (Gaussian Error Linear Unit)

```
GELU(x) ≈ x * Φ(x)   // Φ = normal dağılımın CDF'i
```
- ReLU'ya benzer ama daha yumuşak.
- 0 civarında sert değil, kavisli geçiş yapıyor.
- Negatif değerleri tamamen atmıyor, biraz süzüyor.
- **BERT, GPT, Llama gibi modern LLM'lerin çoğunda** kullanılıyor.
- Neden GELU: ampirik olarak transformer'larda daha iyi sonuç veriyor.

### 9.5 SwiGLU (bonus)

- GELU'nun bir varyantı, Llama gibi modern LLM'lerde standart.
- Gate mekanizmasıyla daha ifadesi güçlü bir non-linearity.
- Transformer FFN katmanlarında GELU'nun yerini almaya başladı.

### 9.6 Softmax (çıktı katmanı için)

Çıktı olasılık dağılımı üretmek için. `01-olasilik-istatistik.md`'de anlattım.

### 9.7 Kısa özet

- **Ara katmanlar için**: ReLU (varsayılan), GELU (modern LLM'ler), SwiGLU (yeni).
- **İkili sınıflandırma çıkışı**: Sigmoid.
- **Çok sınıflı çıkış**: Softmax.

---

## 10. Batch ve Epoch

Bu ikisini karıştırmamak lazım.

- **Batch**: modelin bir defada işlediği örnek sayısı. Bir batch işlendikten sonra parametreler güncellenir.
- **Epoch**: tüm eğitim verisinin bir kere baştan sona işlenmesi. 1 epoch = tüm veri 1 kere görüldü.

### 10.1 Örnekle

Diyelim 10.000 örnek var, batch size 100:
- 100 örnek işledik → 1 iterasyon / step / güncelleme.
- 100 batch işlenince tüm veri gördük → 1 epoch.
- 10 epoch koşarsam → toplam 1000 güncelleme.

### 10.2 Batch size seçimi

- Çok küçük (1-8): gürültülü ama sık güncelleme.
- Orta (32-256): en yaygın.
- Çok büyük (1024+): stabil ama az güncelleme. Büyük GPU/TPU gerektiriyor.

Klasik bilgelik: **batch büyüdükçe learning rate'i de büyüt**. (Doğrusal ölçekleme kuralı.)

### 10.3 Kaç epoch?

Duruma göre. Sinyalleri kullanıyoruz:
- Validation loss düşmeye devam ediyor → devam et.
- Validation loss düşmeyi durdurdu / yükselmeye başladı → **early stopping**, dur.

Sabit epoch koymak yerine "validation loss `N` epoch iyileşmezse dur" kuralı çok kullanılır.

---

## 11. Overfitting ve Train / Validation Loss

`01-olasilik-istatistik.md`'de bias-variance olarak anlatmıştım. Burada pratik gözlem:

### 11.1 Eğitim eğrileri

Eğitim boyunca iki loss izliyoruz:
- **Train loss**: modelin eğitim setinde ne kadar iyi.
- **Validation loss**: modelin görmediği veride ne kadar iyi.

3 tipik senaryo:

**Sağlıklı öğrenme:**
```
Train loss:      █████▄▄▂▁▁▁
Validation loss: █████▄▄▃▂▂▂
```
İkisi de birlikte düşüyor. Model öğreniyor ve genelleyebiliyor.

**Underfitting:**
```
Train loss:      █████████████
Validation loss: █████████████
```
İkisi de yüksek kalıyor. Model çok basit ya da yeterince eğitilmedi.

**Overfitting:**
```
Train loss:      ██▄▂▁▁▁▁▁
Validation loss: ██▄▄▄▅▆▇█
```
Train düşüyor, validation önce düşüp sonra yükseliyor. Model ezberliyor.

### 11.2 Çözüm reçetesi

Overfitting görürsem:
1. **Daha fazla veri topla** (varsa en iyisi).
2. **Data augmentation** uygula (görsel/metin için).
3. **Dropout ekle** (rastgele nöron kapatma).
4. **Weight decay / L2 regularization** kullan.
5. **Early stopping** yap.
6. **Model boyutunu küçült**.
7. **Batch normalization** ekle.

Underfitting görürsem:
1. **Modeli büyüt** (daha çok katman, daha çok nöron).
2. **Daha uzun eğit** (epoch sayısını artır).
3. **Learning rate'i ayarla**.
4. **Feature engineering** yap (klasik ML'de daha etkili).

---

## 12. Tam bir eğitim döngüsü (pseudocode)

```
for epoch in range(N_epoch):
    for batch in train_loader:            # 1 iterasyon
        x, y = batch
        y_hat = model(x)                  # forward pass
        loss = loss_fn(y_hat, y)          # loss
        loss.backward()                   # backprop, gradyanları hesapla
        optimizer.step()                  # parametreleri güncelle
        optimizer.zero_grad()             # gradyan buffer'ını sıfırla

    # Her epoch sonunda validation ölç
    val_loss = evaluate(model, val_loader)
    log(epoch, train_loss, val_loss)

    # Erken durma kontrolü
    if val_loss iyileşmiyorsa X epoch:
        break

# En sonda test setinde bir kere ölç
test_metric = evaluate(model, test_loader)
```

PyTorch'ta bu döngü ~15 satırlık gerçek koda dönüşüyor. `06-pytorch-60-min-blitz/` klasöründe göreceğim.

---

## 13. Sonraki başlıkla bağlantı

Bir sonraki konu: **Framework karşılaştırması** (`05-pytorch-vs-tensorflow.md`).

Bağlantısı: yukarıda anlattığım her şey (autograd, backprop, katmanlar, optimizer'lar) framework'lerin bize sağladığı hazır parçalar. Hangi framework hangi işi ne kadar kolaylaştırıyor, ona bakacağım. Sonra `06-` klasöründe PyTorch ile bunları elle koda dökeceğim.

---

**Durum:** Tamamlandı. Bir sonraki dosya: `05-pytorch-vs-tensorflow.md`.
