# Makine Öğrenmesi (ML) Temelleri

## 1. Önce büyük resim: ML ne demek?

Klasik programlamada iş şöyle akar:
```
Kural + Veri → Program → Çıktı
```
Sen kuralı yazarsın, program veriye uygulayıp çıktı verir.

Makine öğrenmesinde iş **tersinden** akıyor:
```
Veri + Çıktı → Program (ML algoritması) → Kural (model)
```
Bir sürü örnek (girdi, çıktı ikilisi) veriyorsun; algoritma bu örneklerden bir **kural** (model) çıkarıyor. Sonra yeni girdi geldiğinde bu kural cevap üretiyor.

Bu yüzden ML "programlamanın tersine mühendisliği" gibi. Kural yazmak yerine, örneklerden kural türetmesini istiyorsun.

### Üç ana tür (kısa)

- **Supervised (gözetimli)**: her veri örneğinin cevabı var. Kedi/köpek etiketli fotoğraflar gibi. En yaygın tür.
- **Unsupervised (gözetimsiz)**: cevap yok. Model veri içindeki yapıyı kendi çıkarıyor (kümeleme, boyut indirgeme).
- **Reinforcement (pekiştirmeli)**: model bir ortamda hareket ediyor, ödül-ceza ile öğreniyor. Oyun oynayan AI'lar (AlphaGo) böyle.

Bundan sonrasını supervised üstünden anlatacağım — ML'in %90'ı zaten bu.

---

## 2. Model nedir?

En basit tanım: **model, girdiyi çıktıya dönüştüren bir fonksiyon**.

```
y = f(x)
```

Buradaki `f` bizim model. `x` giriş, `y` çıkış.

Ama düz fonksiyondan farkı: modelin içinde **öğrenilebilir sayılar** var. Bu sayılara **parametre** diyoruz.

### 2.1 Basit örnek: doğrusal regresyon

Diyelim ki bir evin fiyatını tahmin etmek istiyorum, tek girdim var: metrekare.

```
fiyat = w * metrekare + b
```

Burada `w` ve `b` iki parametre. Model bu iki sayıyı öğrenerek çalışıyor.

- `w` (weight, ağırlık) → metrekarenin fiyata etkisi (mesela 25000).
- `b` (bias, sabit terim) → başlangıç değer (mesela 100000).

Eğitim sonunda mesela şu sayılara ulaşabilir:
```
fiyat = 25000 * metrekare + 100000
```
Yani 100 metrekarelik ev için tahmin: `25000 * 100 + 100000 = 2.600.000 TL`.

### 2.2 Model türleri (üstten bakış)

Aynı problem için birçok farklı model kurabiliyoruz:

- **Doğrusal modeller**: yukarıdaki gibi. Basit, hızlı, açıklanabilir.
- **Karar ağaçları / Random Forest / XGBoost**: veriyi if-else ağaçlarına bölerek karar veriyor. Tablo verilerde çok iyi.
- **Sinir ağları (neural networks)**: birçok katmanlı, milyonlarca parametreli modeller. Görüntü, ses, metin gibi karmaşık verilerde şart.
- **K-Nearest Neighbors, SVM**: klasikler.

Genelde:
- **Küçük, tablo formatındaki veri** → XGBoost / LightGBM sıklıkla en iyisi.
- **Görüntü, ses, metin** → Deep learning (özellikle CNN / Transformer).

### 2.3 Model = "hipotez sınıfı"

Bir modele karar verdiğinde aslında "bu problemin cevabı şu formüle uyuyor" diyorsun. Doğrusal model dersen, "cevap bir doğrudur" varsayımı yapıyorsun. Neural network dersen "cevap çok daha karmaşık bir fonksiyon olabilir" varsayımı yapıyorsun.

Bu yüzden model seçimi = **hipotez sınıfı seçimi**. Bunun altını çizmek istiyorum çünkü ilk başta "model = kod" gibi düşünmüştüm, aslında matematiksel bir seçimmiş.

---

## 3. Parametre nedir?

**Modelin öğrendiği sayılar.**

- Doğrusal regresyon: `w` ve `b` (toplam 2 sayı).
- Küçük bir sinir ağı: birkaç bin ile birkaç milyon sayı.
- GPT-4 gibi büyük LLM: yaklaşık 1 trilyon parametre.

Bir modelin "büyüklüğü" dediğimizde genelde parametre sayısını kastediyoruz.

### 3.1 Parametre ≠ Hiperparametre

Bu ayrımı ilk başta karıştırmıştım.

- **Parametre**: modelin **eğitim sırasında** öğrendiği sayı. Sen dokunmazsın, veriden gelir. Örnek: `w`, `b`.
- **Hiperparametre**: modelin nasıl eğitileceğini belirleyen, **sen elle** ayarladığın sayı. Örnek: learning rate, katman sayısı, batch size, epoch sayısı.

Hiperparametreler modelin **öğrenme sürecini** tanımlar. Parametreler ise **sonuç modelin ne olduğunu** tanımlar.

### 3.2 Model boyutu neden önemli?

- Çok az parametre → model karmaşık ilişkileri yakalayamaz (**underfitting**).
- Çok fazla parametre → model veriyi ezberler, yeni veride bozulur (**overfitting**).
- Doğru boyut → problemin ihtiyacına göre değişir.

---

## 4. Eğitim (Training) nedir?

Eğitim = **parametreleri veriye göre en iyi hale getirme süreci**.

Genel akış (bu döngü ML'in kalbi):

```
1. Elde eğitim verisi var: (x1, y1), (x2, y2), ...
2. Modelin parametreleri rastgele başlar.
3. Bir örnek al: (x, y).
4. Modele soru sor: y_tahmin = model(x).
5. Ne kadar yanıldığını ölç: loss = fark(y_tahmin, y).
6. Loss'u düşürecek şekilde parametreleri biraz güncelle.
7. Diğer örneğe geç, 3'e dön.
8. Bütün veriyi bir kere tarayınca 1 epoch bitmiş olur. Yeterince epoch koştur.
```

Bu döngüye **training loop** deniyor. Deep Learning bölümünde (`04-`) her adımını tek tek açacağım. Burada sadece kavramsal bakalım.

### 4.1 "Öğrenmek" ne demek matematiksel olarak?

Modelin doğru cevapları verecek parametreleri bulmak → **optimizasyon problemi**.

```
En iyi parametreler = argmin (loss over training data)
```

Yani: "Öyle parametreler bul ki, eğitim verisindeki toplam yanılgı minimum olsun."

Bu optimizasyonu genelde **gradient descent** ile yapıyoruz — 04-Deep Learning bölümünde detaya inecek.

### 4.2 Küçük hayal örneği

Bir çocuğun bisiklete binmeyi öğrenmesi gibi düşün:
- İlk denemede düşer (yüksek loss).
- Ebeveyn "biraz sola yatır" der (parametre güncellemesi).
- Tekrar dener, biraz daha uzun gider (loss azalır).
- Bu döngü onlarca kez tekrarlanır.
- Sonunda bisiklete binmeyi öğrenir (loss düşük).

ML eğitimi aslında bu döngünün matematiksel hali.

---

## 5. Loss nedir?

**Loss = modelin ne kadar yanlış olduğunu ölçen tek sayı.**

Amacımız bu sayıyı **küçültmek**. 0 olması = mükemmel tahmin. Ama pratikte 0'a yaklaşırsak zaten overfit olmuşuzdur.

### 5.1 Regresyonda: MSE (Mean Squared Error)

Sayı tahmin ediyorsak (ev fiyatı, sıcaklık vb.):

```
MSE = ortalama( (y_gerçek - y_tahmin)² )
```

Karesi almanın iki sebebi:
1. İşaret önemsizleşir (2 fazla mı 2 eksik mi olduğu değil, ne kadar uzak olduğu önemli).
2. Büyük hataları çok daha fazla cezalandırır (5 birim hata, 25 puan; 10 birim hata, 100 puan).

### 5.2 İkili sınıflandırmada: Binary Cross-Entropy

Spam / spam değil gibi problemlerde:

```
BCE = - [ y * log(p) + (1-y) * log(1-p) ]
```

`p` modelin "1 olma" olasılığı tahmini. Gerçek `y` 1'se, model 1'e ne kadar yakın diyorsa loss o kadar düşük.

### 5.3 Çok sınıflı sınıflandırmada: Categorical Cross-Entropy

Kedi/köpek/kuş gibi. En çok kullanılan loss. Modelin doğru sınıfa verdiği olasılığın logaritmasını eksi işaretle alıyoruz. Model %90 dediyse loss küçük; %10 dediyse büyük.

Not: bunların hepsinin **istatistiksel türetimi** var, `01-olasilik-istatistik.md`'de MLE bölümünde yazdım.

### 5.4 Loss ≠ Metric

Sık karıştırılan bir ayrım:
- **Loss**: eğitim sırasında modelin optimize etmeye çalıştığı sayı. Sürekli, türevlenebilir olmalı.
- **Metric**: sonucu değerlendirmek için baktığımız insan-dostu sayı. Accuracy, F1, AUC, precision, recall gibi.

Örnek: sınıflandırmada loss "cross-entropy" olabilir ama biz sonuca "accuracy" ile bakabiliriz. Bunlar farklı işler yapıyor.

---

## 6. Train / Validation / Test

Bu üçü eğitim disiplininin temeli. Karıştırmamak lazım.

### 6.1 Ne için var?

Elimizdeki veriyi üçe bölüyoruz:

- **Train set (eğitim)** — model bunu görerek öğrenir. Parametreler bu setten güncellenir.
- **Validation set (doğrulama, dev)** — model bunu görmez ama biz eğitim sırasında burada ölçüm yapıp **hiperparametre kararları** veririz. "Learning rate 0.001 mi 0.0001 mi daha iyi?" gibi.
- **Test set** — model **ve biz** karar aşamasında bunu **hiç** kullanmayız. Sadece en sonda gerçek dünya performansını ölçmek için bir kere bakılır.

### 6.2 Neden 3 tane?

Sadece train + test olsaydı:
- Train'de model iyi
- Test'te ölçtük, sonuç kötü çıktı, "modeli değiştireyim" diyip tekrar test'e baktık
- Aslında test setine göre modelimizi ayarladık — test seti "eğitim setine" dönüştü, artık gerçekçi ölçüm veremez
- Bu **data leakage**.

Validation, işte bu "sürekli baktığımız" set — bozulmasına razı olduğumuz. Test dokunulmaz kalıyor.

### 6.3 Tipik oranlar

Küçük-orta veride:
- Train: %70
- Validation: %15
- Test: %15

Çok büyük veride (milyonlarca örnek):
- Train: %98
- Validation: %1
- Test: %1

Çünkü %1 bile milyonlar demek, yeterli.

### 6.4 K-fold Cross Validation

Az veride tek train/val bölünmesi güvenilmez olabilir. Alternatif: veriyi K parçaya böl (mesela 5). Her seferinde 1 parçayı validation yap, 4'ünü train. Bunu 5 kez tekrarla, sonuçları ortala.

- Avantaj: veri az olsa bile güvenilir ölçüm.
- Dezavantaj: 5 kere eğitim gerekli, deep learning'de pahalı. Genelde klasik ML'de kullanılır.

### 6.5 Data Leakage — dikkat edilecek şeyler

Eğitim setine sızıntı olması modeli haksız yere iyi göstermesi demek. Örnekler:

- Preprocessing'i (mean, std hesaplama) tüm veri üstünden yapıp sonra bölmek. **Doğru olan**: sadece train üstünde hesaplamak, val/test'e onu uygulamak.
- Aynı kullanıcının farklı örneklerinin hem train hem test'e düşmesi. Model kişiyi tanıyıp cevap veriyor.
- Zaman serisi verisinde geleceği eğitim setinde görmek — gerçek hayatta olmayacak bir avantaj.

Ben genelde bu tuzağa düşme ihtimalim en yüksek olan yerin, "veriyi zaman ekseninden ayırmak" olduğunu okudum. Zaman serilerinde train hep test'ten önce olmalı.

---

## 7. Bir eğitim döngüsünün "resmi"

Şematik olarak:

```
                 ┌──────────┐
                 │ Train    │
                 │ verisi   │
                 └────┬─────┘
                      │  (küçük batch)
                      ▼
   ┌────────┐   Forward pass
   │ Model  │──────────────► y_tahmin
   │ (θ)    │                    │
   └────┬───┘                    ▼
        │            Loss(y_gerçek, y_tahmin)
        │                        │
        │   ◄────Gradient────────┘
        │
        └──► θ'yı biraz güncelle (optimizer)

   Sonuç: 1 batch bitti. Sıradaki batch. Bütün veri bitince → 1 epoch.
   Yeterince epoch geçince → eğitim tamam.

   ────
   Ara sıra Validation setinde loss ve metric ölç.
   Eğitim biterse → Test setinde bir kere ölç → rapor.
```

Bu şemayı Deep Learning bölümünde (`04-`) satır satır PyTorch koduna dönüştüreceğim.

---

## 8. Küçük scikit-learn örneği (kavramları koda döktüm)

Notebook'ta çalıştırabileceğim minimum örnek:

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 1. Veri
X, y = load_iris(return_X_y=True)

# 2. Train / Test bölmesi
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Model (hipotez sınıfı seçimi: logistic regression)
model = LogisticRegression(max_iter=200)

# 4. Eğitim — parametreler burada öğrenilir
model.fit(X_train, y_train)

# 5. Tahmin
y_pred = model.predict(X_test)

# 6. Değerlendirme (metric)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Öğrenilen parametreler (weights):", model.coef_)
print("Öğrenilen bias:", model.intercept_)
```

Burada:
- `model = LogisticRegression(...)` → **hipotez sınıfını** seçtim.
- `model.fit(...)` → **eğitim** (parametre optimizasyonu).
- `model.coef_`, `model.intercept_` → **öğrenilmiş parametreler**.
- `accuracy_score(...)` → **metric** (loss'tan farklı).

Bu 15 satırlık örnekte bütün ML kavramları var. Sadece loss'un adı gizli — scikit-learn arka planda kendi hallediyor.

---

## 9. Sonraki başlıkla bağlantı

Bir sonraki konu: **Deep Learning temelleri** (`04-deep-learning-temelleri.md`).

Bağlantısı çok direkt: ML'in yaptığı işin çok daha büyük ve katmanlı hali deep learning. Yukarıdaki eğitim döngüsü aynısı, sadece model "sinir ağı" oluyor, parametre sayısı milyona / milyarların hızla çıkıyor ve gradyanı hesaplamak için **backpropagation** gibi özel bir yol lazım.

---

**Durum:** Tamamlandı. Bir sonraki dosya: `04-deep-learning-temelleri.md`.
