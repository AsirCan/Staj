# Gün 14 - Örnekleme ve Çıktı Parametreleri

Görevlendirmenin 5. bölümü. Bugüne kadar modelin **ne bildiğiyle** (RAG) ve **nasıl
davrandığıyla** (fine-tuning, istem) ilgilendim. Bu bölüm modelin **cevabı nasıl
seçtiğiyle** ilgili.

---

## 0. Önce: Model Cevabı Nasıl Üretiyor?

Parametreleri anlamak için önce şunu netleştirmem gerekti.

LLM tek seferde cümle üretmiyor. Her adımda **tek bir token** üretiyor, sonra o
tokenı girdiye ekleyip bir sonrakini üretiyor. Ve her adımda ürettiği şey aslında
bir token değil, sözlükteki **bütün tokenlar için bir olasılık dağılımı**.

Örnek: "Türkiye'nin başkenti" girdisi için model şöyle bir dağılım üretiyor:

| Token | Olasılık |
|---|---|
| Ankara | 0.89 |
| İstanbul | 0.06 |
| burada | 0.02 |
| bir | 0.01 |
| ... | ... |

Sonra bu dağılımdan **bir tane seçmesi** gerekiyor. İşte örnekleme parametreleri
tam olarak bu seçim işini ayarlıyor.

En basit seçim "en yüksek olasılıklıyı al" (greedy). Ama bu her zaman aynı cevabı
üretiyor ve metin tekdüze, tekrarlı oluyor. Bu yüzden rastgelelik katılıyor,
parametreler de bu rastgeleliği kontrol ediyor.

Teknik detay: modelin ham çıktısı olasılık değil, **logit** denilen ham skorlar.
Bunlar softmax'tan geçirilerek olasılığa çevriliyor. Gün 12'de MiniBrain'in çıkışına
aktivasyon koymamamın sebebi de buydu; çıktı ham logit olarak kalıyor.

---

## 1. Context (Bağlam Penceresi)

### Ne olduğu

Modelin bir seferde işleyebildiği maksimum token sayısı. **Girdi ve çıktının
toplamı** bu sınıra dahil.

Diğer parametrelerden farkı: bu bir örnekleme parametresi değil, **kapasite sınırı**.
Yaratıcılığı etkilemiyor, neyin görülebildiğini belirliyor.

### Neden kritik

Bağlam penceresi RAG'in doğrudan sebebi. Şirketin 4000 sayfalık dokümanı hiçbir
pencereye sığmıyor; o yüzden ilgili parçalar seçilip veriliyor.

### Yönetimi

Bugün bağlam mühendisliği başlığında yazdıklarım burada uygulanıyor:

- **Parçalama ve seçme:** Her şeyi değil, alakalı olanı koymak
- **Özetleme:** Uzayan konuşmalarda eski turları özete indirmek
- **Kayan pencere:** Sadece son N turu tutmak
- **Sıkıştırma:** Getirilen parçalardan alakasız cümleleri atmak

### Pencere büyükse sorun biter mi?

Bitmiyor. Üç sebep var:

1. **Maliyet:** Token başına ödeme yapılıyor, pencereyi doldurmak faturayı büyütüyor.
2. **Gecikme:** Uzun bağlam daha yavaş işleniyor.
3. **Ortada kaybolma (lost in the middle):** Model bağlamın başına ve sonuna,
   ortasından daha çok dikkat ediyor. Uzun bağlamın ortasına gömülen kritik bilgi
   gözden kaçabiliyor.

Bu yüzden pratikte kural şu: **pencereyi doldurmak değil, doğru doldurmak.**

---

## 2. Temperature (Sıcaklık)

### Ne yapıyor

Olasılık dağılımının **keskinliğini** ayarlıyor. Matematiksel olarak logitler
softmax'tan geçmeden önce sıcaklığa bölünüyor:

```
olasılık = softmax(logit / T)
```

Bu tek bölme işlemi şunu yapıyor:

- **T < 1** → logit farkları büyür → dağılım **keskinleşir** → yüksek olasılıklı
  token daha da baskın olur
- **T = 1** → modelin ham dağılımı, değişiklik yok
- **T > 1** → logit farkları küçülür → dağılım **düzleşir** → düşük olasılıklı
  tokenlar da şans kazanır

### Etkisi

| T | Davranış | Uygun olduğu iş |
|---|---|---|
| 0 | Hep en olasıyı seçer, deterministik | Sınıflandırma, veri çıkarma, RAG |
| 0.1 - 0.3 | Çok kararlı, az çeşitlilik | Kod, teknik cevap, özetleme |
| 0.7 - 0.8 | Dengeli (çoğu API'nin varsayılanı) | Sohbet, genel kullanım |
| 1.0 - 1.3 | Yaratıcı, öngörülemez | Hikaye, beyin fırtınası |
| > 1.5 | Genelde tutarsız, bazen anlamsız | Nadiren |

### RAG'de neden düşük tutuluyor?

Bugün halüsinasyon engelleme başlığında not etmiştim. Yüksek sıcaklıkta model
düşük olasılıklı tokenları da seçebiliyor; bağlamda yazan ifadeden sapıp kendi
ezberine kayma ihtimali artıyor. RAG'de amaç yaratıcılık değil sadakat olduğu için
sıcaklık düşük tutuluyor.

### Önemli ayrım

Sıcaklık modeli "daha akıllı" ya da "daha aptal" yapmıyor. Modelin bildiği aynı,
sadece bildiklerinden hangisini seçtiği değişiyor.

---

## 3. Top-K Örnekleme

### Ne yapıyor

Her adımda sadece **en olası K token** dikkate alınıyor, geri kalanı tamamen
eleniyor. Olasılıklar bu K token arasında yeniden normalize edilip seçim yapılıyor.

K=1 ise greedy seçime eşit oluyor.

### Amacı

Uzun kuyruğu kesmek. Sözlükte 50.000 token var ve çoğunun olasılığı sıfıra çok
yakın. Tek tek bakınca önemsizler ama toplamları küçümsenmeyecek bir olasılık
oluşturuyor. Top-K bu saçma seçenekleri baştan eliyor.

### Zayıflığı

**K sabit, dağılım değil.** Sorun burada:

- Model **eminse** (bir token 0.95 olasılıklı), K=50 demek 49 tane alakasız tokenı
  yarışa sokmak demek.
- Model **kararsızsa** (50 token arasında olasılık dağılmışsa), K=50 makul.

Yani aynı K değeri farklı durumlarda farklı anlamlara geliyor. Bu zayıflık Top-P'nin
çıkış sebebi.

---

## 4. Top-P (Nucleus / Çekirdek Örnekleme)

### Ne yapıyor

Sabit sayıda token almak yerine, **kümülatif olasılığı P'ye ulaşana kadar** token
alıyor.

Örnek, P = 0.9 için:

| Token | Olasılık | Kümülatif | Alındı mı |
|---|---|---|---|
| Ankara | 0.89 | 0.89 | evet |
| İstanbul | 0.06 | 0.95 | evet (eşiği geçti, burada durdu) |
| burada | 0.02 | 0.97 | hayır |
| ... | ... | ... | hayır |

### Top-K'ya üstünlüğü

Havuz boyutu **duruma göre değişiyor**:

- Model eminse → 1-2 token yeter, havuz küçük kalır
- Model kararsızsa → havuz kendiliğinden büyür

Yani Top-P "modelin ne kadar emin olduğuna" uyum sağlıyor. Bu yüzden pratikte Top-K
yerine Top-P tercih ediliyor.

### Tipik değerler

| P | Etki |
|---|---|
| 0.1 | Çok dar, neredeyse deterministik |
| 0.9 | Yaygın varsayılan |
| 0.95 | Biraz daha çeşitli |
| 1.0 | Filtre yok, bütün dağılım |

### Birlikte kullanım

Üçü aynı anda uygulanabiliyor. Uygulama sırası genellikle şöyle:

```
logitler -> temperature ile ölçekle -> Top-K ile kes -> Top-P ile kes -> örnekle
```

Ama çoğu kılavuz **temperature ile top-p'den yalnızca birini ayarlamayı** öneriyor.
İkisini birden oynatmak etkilerin birbirine karışmasına ve neyin ne yaptığının
anlaşılamamasına yol açıyor.

---

## 5. Repetition Penalties (Tekrar Cezaları)

### Problem

Modeller kendini tekrarlamaya eğilimli. Özellikle düşük sıcaklıkta ve uzun
üretimlerde döngüye girip aynı cümleyi tekrar tekrar yazabiliyorlar.

Sebebi şu: model kendi ürettiği metni girdi olarak geri alıyor. Bir kalıp bir kez
oluştuğunda, o kalıbın devamı model için daha olası hale geliyor ve kendini
besleyen bir döngü kuruluyor.

### Yöntemler

**Repetition penalty (çarpımsal).**
Daha önce geçmiş tokenların logiti bir katsayıya bölünüyor. 1.0 ceza yok demek,
1.1-1.2 tipik, 1.5 üstü metni bozmaya başlıyor.

Dezavantajı: kaç kez geçtiğine bakmıyor, bir kez geçmiş de olsa cezalandırıyor.
Türkçede "ve", "bir", "bu" gibi doğal olarak sık geçen kelimeler haksız yere
cezalandırılıyor.

**Frequency penalty (sıklık cezası).**
Ceza, tokenın **kaç kez geçtiğiyle orantılı**. Çok tekrarlanan çok cezalanıyor, bir
kez geçen az. Genellikle -2.0 ile 2.0 arasında bir değer alıyor.

**Presence penalty (varlık cezası).**
Token **bir kez bile geçtiyse** sabit bir ceza uygulanıyor, sayısı önemli değil.
Amacı tekrarı engellemekten çok modeli yeni konulara itmek.

**No-repeat n-gram.**
Belirli uzunluktaki kelime dizilerinin (n-gram) tekrarını tamamen yasaklıyor. Kesin
çözüm ama sert; isim veya teknik terim tekrarı gerektiğinde metni bozuyor.

### Karşılaştırma

| Yöntem | Neye bakar | Etkisi |
|---|---|---|
| Repetition penalty | Geçti mi (çarpımsal) | Genel, kaba |
| Frequency penalty | Kaç kez geçti | Orantılı, hassas |
| Presence penalty | Geçti mi (sabit) | Konu çeşitliliği |
| No-repeat n-gram | Dizi tekrarı | Kesin ama sert |

### Dikkat

Bu cezalar RAG'de dikkatli kullanılmalı. Model bağlamdaki bir terimi tekrar etmek
zorunda olabilir (ürün adı, madde numarası). Yüksek ceza modeli eş anlamlı uydurmaya
itip halüsinasyona yol açabiliyor.

---

## 6. Karşılaştırma Tablosu

Görev bu tabloyu özellikle istiyor.

| Parametre | Ne yapar | Tipik aralık | Yaratıcılık | Doğruluk | Tekrar |
|---|---|---|---|---|---|
| **Context** | İşlenebilen maks. token | modele bağlı | etkisiz | dolaylı (bilgi görünürlüğü) | etkisiz |
| **Temperature** | Dağılımın keskinliği | 0 - 2 | ↑ artırır | ↓ düşürür | ↓ azaltır |
| **Top-K** | Sabit sayıda aday | 1 - 100 | K↑ artırır | K↑ düşürür | K↑ azaltır |
| **Top-P** | Kümülatif olasılık eşiği | 0.1 - 1.0 | P↑ artırır | P↑ düşürür | P↑ azaltır |
| **Repetition penalty** | Geçmiş tokenı cezalar | 1.0 - 1.3 | hafif artırır | ↓ (yüksekse) | ↓↓ azaltır |
| **Frequency penalty** | Sıklıkla orantılı ceza | -2.0 - 2.0 | hafif artırır | ↓ (yüksekse) | ↓↓ azaltır |
| **Presence penalty** | Varlığa sabit ceza | -2.0 - 2.0 | ↑ artırır | nötr | ↓ azaltır |

### Göreve göre önerilen ayarlar

| Kullanım | Temperature | Top-P | Ceza | Gerekçe |
|---|---|---|---|---|
| **RAG / soru-cevap** | 0.0 - 0.2 | 0.9 | yok/düşük | Sadakat esas, yaratıcılık zararlı |
| **Veri çıkarma, JSON** | 0.0 | 1.0 | yok | Biçim kesin olmalı |
| **Kod üretimi** | 0.1 - 0.3 | 0.95 | yok | Sözdizimi hata kaldırmıyor |
| **Özetleme** | 0.3 | 0.9 | hafif | Sadık ama akıcı |
| **Sohbet** | 0.7 | 0.9 | hafif | Doğal ama tutarlı |
| **Yaratıcı yazım** | 1.0 - 1.2 | 0.95 | orta | Çeşitlilik esas |

---

## Sonuç

Bu bölümde öğrendiğim en temel şey, bu parametrelerin modelin **bilgisini**
değil, ürettiği olasılık dağılımından **nasıl seçim yaptığını** değiştirmesi.
Sıcaklığı yükseltmek modeli yaratıcı yapmıyor; sadece daha az olası tokenları
seçme ihtimalini artırıyor. Bu ayrımı kavrayınca parametrelerin hepsi anlaşılır
hale geldi.

Top-K ile Top-P farkını da net gördüm: Top-K sabit sayıda aday alıyor ve modelin ne
kadar emin olduğuna bakmıyor. Top-P ise havuzu duruma göre büyütüp küçültüyor; model
eminse dar, kararsızsa geniş. Bu uyum yeteneği yüzünden pratikte Top-P tercih
ediliyor.

Tekrar cezalarında ise ayrımın "geçti mi" ile "kaç kez geçti" arasında olduğunu
öğrendim. Frequency penalty sıklıkla orantılı çalıştığı için doğal olarak sık geçen
kelimeleri haksız yere cezalandırmıyor.

Kendi projem açısından çıkarımım net: gün 15'te kuracağım RAG sisteminde sıcaklığı
sıfıra yakın tutacağım. Sebebi bugün yazdığım halüsinasyon önlemleriyle birebir
örtüşüyor — orada amaç modelin bağlama sadık kalması, ve düşük sıcaklık bunun
örnekleme tarafındaki karşılığı. Tekrar cezalarını da kullanmayacağım, çünkü modelin
bağlamdaki terimleri aynen tekrar etmesi tam olarak istediğim şey.

Bu parametrelerin etkisini yanındaki notebook'ta, gerçek bir model çağırmadan,
doğrudan olasılık dağılımı üzerinde hesaplayarak gösterdim.
