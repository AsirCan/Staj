# Gün 14 - RAG Mimarileri (2): Akış Odaklı RAG'ler ve Temel Teknik Bileşenler

4. bölümün ikinci yarısı. Önceki dosyada hattın **yapısını** güçlendiren yaklaşımları
inceledim; burada hattın **kendini denetlemesini** sağlayan yaklaşımlara ve RAG'in
temel teknik bileşenlerine bakıyorum.

---

## 1. Corrective RAG (CRAG)

### Çözdüğü problem

Önceki dosyada Naive RAG'in temel zaafını "hat sorgusuz" diye özetlemiştim. Arama alakasız
parçalar getirse bile üretim adımı bunları sorgusuz kabul ediyor ve model
alakasız bağlamdan cevap uydurmaya çalışıyor.

CRAG bu boşluğa bir **kalite kontrol adımı** koyuyor.

### Nasıl çalışıyor?

Arama ile üretim arasına bir **değerlendirici (retrieval evaluator)** giriyor.
Getirilen her parçaya "bu soruyla gerçekten alakalı mı" diye puan veriyor. Sonuca
göre üç yoldan biri seçiliyor:

| Değerlendirme | Yapılan işlem |
|---|---|
| **Doğru** (parçalar alakalı) | Parçalar temizlenir, gereksiz cümleler atılır, üretime gider |
| **Yanlış** (parçalar alakasız) | Yerel sonuçlar atılır, **web araması** yapılır |
| **Belirsiz** (kararsız) | Her ikisi birleştirilir |

Buradaki kritik fikir: **sistem "bilmiyorum" diyebilecek bir noktaya sahip.**
Yerel veritabanı yetersizse dışarı çıkabiliyor.

Ek bir mekanizması da parçaları daha küçük "bilgi şeritlerine" ayırıp alakasız
olanları ayıklamak. Yani sadece parça seçimini değil, parçanın içeriğini de
süzüyor.

**Maliyeti:** Her sorguda ek değerlendirme çağrısı, bazen ek web araması. Gecikme
artıyor.

---

## 2. Self-RAG

### Farkı

CRAG dışarıdan bir değerlendirici ekliyordu. Self-RAG ise **modelin kendisini**
değerlendirici hale getiriyor. Model, özel "yansıma jetonları" (reflection tokens)
üretecek şekilde eğitiliyor ve bu jetonlarla kendi sürecini yönetiyor.

### Yansıma jetonları

| Jeton | Sorusu | Ne zaman |
|---|---|---|
| **Retrieve** | Arama yapmam gerekiyor mu? | Üretimden önce |
| **IsRel** | Getirilen parça alakalı mı? | Arama sonrası |
| **IsSup** | Ürettiğim cümle bu parçayla destekleniyor mu? | Üretim sırasında |
| **IsUse** | Cevabım soruya gerçekten faydalı mı? | Üretim sonrası |

### En önemli farkı: isteğe bağlı arama

Self-RAG'in en dikkat çekici tarafı, **her soruda arama yapmaması**. "Merhaba nasılsın"
sorusu için veritabanına gitmenin anlamı yok. Model önce "bu soru için arama gerekli
mi" diye karar veriyor.

İkinci önemli tarafı, ürettiği her cümle için "bu, getirdiğim kaynakta gerçekten
yazıyor mu" kontrolü yapması. Halüsinasyona doğrudan müdahale eden nokta burası.

### CRAG ile Self-RAG karşılaştırması

| Konu | CRAG | Self-RAG |
|---|---|---|
| Denetleyen | Ayrı bir değerlendirici model | Modelin kendisi |
| Kurulum | Mevcut modelle çalışır | Özel eğitim (fine-tuning) gerekir |
| Arama | Her zaman yapılır | Gerekirse yapılır |
| Düzeltme yöntemi | Web araması ile telafi | Yeniden arama / kendini düzeltme |
| Denetim noktası | Arama sonrası | Hem arama hem üretim sırasında |
| Uygulama kolaylığı | Yüksek | Düşük (eğitim gerekli) |

---

## 3. Agentic RAG

### Fikir

Şimdiye kadar incelediğim bütün RAG türlerinde hattı **geliştirici** kurmuştu.
Advanced RAG'de hangi katmanların ekleneceğine ben karar veriyordum; CRAG'de
değerlendirme kuralını ben yazıyordum.

Agentic RAG bu kararları **ajana** bırakıyor. Bugün ajanlar bölümünde öğrendiğim ajan mantığı
burada RAG hattına uygulanıyor: RAG artık sabit bir boru hattı değil, ajanın
kullanabileceği **araçlardan biri**.

### Ajanın verdiği kararlar

- Arama yapayım mı, yoksa doğrudan cevaplayabilir miyim?
- Hangi kaynağa bakayım? (ürün dokümanı, mevzuat, web, SQL veritabanı)
- Soru karmaşık mı, alt sorulara bölmeli miyim?
- Getirdiğim sonuç yeterli mi, farklı bir sorguyla tekrar arayayım mı?
- Cevabı yazmadan önce doğrulama yapayım mı?

### Avantajları

- **Çok adımlı sorular çözülebiliyor.** "X ürünü ile Y ürününün garanti sürelerini
  karşılaştır" sorusu için ajan iki ayrı arama yapıp sonuçları birleştirebiliyor.
  Tek atışlı RAG bunu yapamıyor.
- **Çoklu kaynak.** Farklı veritabanları, API'ler ve web aynı akışta kullanılabiliyor.
- **Uyarlanabilirlik.** Basit soruda tek arama, zor soruda birkaç tur.
- **Kendini düzeltme.** İlk arama boş gelirse sorguyu değiştirip tekrar deniyor.

### Riskleri

Bugün ajanlar için not ettiğim riskler burada da geçerli:

- **Öngörülemezlik:** Aynı soru iki farklı yolla cevaplanabiliyor. Hata ayıklamak
  zorlaşıyor.
- **Maliyet kontrolsüzlüğü:** Kaç arama ve kaç LLM çağrısı yapılacağı belli değil.
- **Gecikme:** Turlar arttıkça cevap süresi uzuyor.
- **Döngüye girme:** Ajan aynı aramayı tekrarlayıp ilerleyemeyebiliyor; adım sınırı
  şart.
- **Hata birikmesi:** Her turda küçük bir sapma varsa zincir sonunda konudan
  uzaklaşılıyor.

### Değerlendirmem

Agentic RAG en yetenekli yaklaşım ama **en az öngörülebilir** olanı. Bugün ajanlar için vardığım
sonucun aynısı burada da geçerli: işi çözen en basit yapı tercih edilmeli. Sabit bir
hat yetiyorsa ajan kurmanın getirisi yok.

### RAG türlerinin özeti

| Tür | Ana fikri | Kararı veren |
|---|---|---|
| Naive | Bul, ver, üret | Sabit hat |
| Advanced | Öncesine ve sonrasına katman ekle | Geliştirici |
| GraphRAG | Parçalar yerine ilişkiler | Geliştirici |
| Multimodal | Metin dışı veriyi de işle | Geliştirici |
| CRAG | Getirilen veriyi denetle, gerekirse dışarı çık | Değerlendirici model |
| Self-RAG | Model kendi sürecini denetlesin | Modelin kendisi |
| Agentic | Bütün akışı ajan yönetsin | Ajan |

---

## 4. Metin Bölme (Chunking)

Görevin B kısmına geçiyorum. Chunking, RAG'in en çok küçümsenen ama sonucu en çok
etkileyen adımı.

### Neden bölüyoruz?

Üç sebep var:

1. Embedding modellerinin girdi sınırı var; tüm belge tek seferde vektörleştirilemiyor.
2. Tek bir vektör çok uzun metnin anlamını taşıyamıyor, ortalamaya kayıyor.
3. Modele bütün belgeyi vermek hem pahalı hem de dikkat dağıtıcı.

### Yöntemler

**Sabit boyutlu (fixed-size).**
Metni N karakter/token'da bir kes. Basit, hızlı, öngörülebilir. Sorunu: cümlenin
veya kelimenin ortasından kesebiliyor, anlam kopuyor.

**Cümle / paragraf tabanlı.**
Doğal sınırlardan böl. Anlam bütünlüğü korunuyor ama parça boyutları çok değişken
oluyor; bazı paragraflar tek cümle, bazıları bir sayfa.

**Özyinelemeli (recursive).**
Pratikte en yaygın kullanılan yöntem. Bir ayraç önceliği listesi tanımlanıyor:
önce paragraf (`\n\n`), sığmazsa satır (`\n`), sığmazsa cümle (`. `), sığmazsa
kelime, en son karakter. Yani "mümkün olan en doğal yerden böl, olmazsa bir alt
seviyeye in". Hem boyut kontrolü hem anlam bütünlüğü sağlıyor.

**Anlamsal (semantic) parçalama.**
Cümleleri tek tek vektörleştir, ardışık cümleler arasındaki benzerliğe bak.
Benzerlik aniden düştüğü yer konu değişimidir, oradan böl. En kaliteli sonucu
veriyor ama indeksleme sırasında her cümle için embedding gerektiği için pahalı.

**Yapıya duyarlı (structure-aware).**
Markdown başlıkları, HTML etiketleri, kod fonksiyonları gibi belgenin kendi
yapısını kullanmak. Teknik dokümanlarda çok etkili.

### Örtüşme (overlap) neden gerekli?

Bu, chunking'in en kritik ayrıntısı. Parçalar arasında bir miktar tekrar bırakılıyor.

Sebebi şu: bir bilgi tam kesme noktasına denk gelirse ikiye bölünüyor ve her iki
parça da eksik kalıyor. Örnek:

```
... İade süresi ürün teslim tarihinden itibaren   | PARÇA 1 SONU
14 gündür ve kargo ücreti müşteriye aittir. ...   | PARÇA 2 BAŞI
```

"İade süresi ne kadar?" diye sorulduğunda parça 1 soruyu içeriyor ama cevabı
içermiyor; parça 2 cevabı içeriyor ama neyin cevabı olduğu belli değil. Örtüşme
sayesinde bilgi en az bir parçada bütün kalıyor.

**Örtüşme ne kadar olmalı?** Genel kabul parça boyutunun yüzde 10-20'si.

Ödünleşim:
- Az örtüşme → sınırda bilgi kaybı riski
- Çok örtüşme → depolama ve maliyet artıyor, aynı içerik birden çok parçada
  çıktığı için arama sonuçları tekrar ediyor

### Parça boyutu ödünleşimi

| Boyut | Artısı | Eksisi |
|---|---|---|
| Küçük (100-200 token) | Keskin ve odaklı vektör, isabetli arama | Bağlam eksik, cevap yarım kalıyor |
| Orta (300-600 token) | Dengeli, en yaygın tercih | — |
| Büyük (1000+ token) | Bağlam bol | Vektör bulanıklaşıyor, alakasız bilgi taşınıyor, maliyet artıyor |

Bir de şu kalıp var: **küçük parçayla ara, büyük parçayı ver.** Arama küçük ve keskin
parçalar üzerinden yapılıp, bulunan parçanın çevresindeki daha geniş metin modele
veriliyor. Böylece hem isabet hem bağlam elde ediliyor.

---

## 5. Benzerlik Metrikleri

Gün 13'te kosinüs benzerliğini uygulamıştım. Şimdi üç metriğin mantıksal farkına
bakıyorum.

### Kosinüs Benzerliği (Cosine Similarity)

```
cos(a, b) = (a · b) / (|a| × |b|)
```

Sadece **yöne** bakıyor, uzunluğu yok sayıyor. Sonuç -1 ile 1 arasında.

Metin aramasında varsayılan tercih. Sebebi: vektörün uzunluğu çoğunlukla metnin
uzunluğuyla ilgili, anlamıyla değil. Aynı konuyu anlatan kısa cümle ile uzun
paragrafın benzer sayılması isteniyor.

### İç Çarpım (Dot Product)

```
a · b = Σ (aᵢ × bᵢ)
```

Hem yöne hem **büyüklüğe** duyarlı. Uzun vektörler daha yüksek skor alıyor.

Ne zaman kullanılıyor:
- Vektörler zaten normalize edilmişse **kosinüsle matematiksel olarak aynı** hale
  geliyor (gün 13'te bunu deneyerek gösterdim). Bu durumda iç çarpım tercih ediliyor
  çünkü tek matris çarpımıyla hesaplanıyor, daha hızlı.
- Büyüklüğün anlamlı olduğu durumlarda (öneri sistemlerinde popülerlik gibi) bilerek
  seçiliyor.

### Öklid Uzaklığı (Euclidean / L2)

```
d(a, b) = sqrt(Σ (aᵢ - bᵢ)²)
```

Uzaydaki düz çizgi mesafesi. **Uzaklık** ölçüyor, yani küçük olması iyi (diğer ikisi
benzerlik ölçüyordu, büyük olması iyiydi).

Hem yön hem büyüklük farkına duyarlı. Gün 13'teki demoda gördüğüm gibi, aynı yöndeki
bir vektörün üç katını "farklı" sayabiliyor. Metin aramasında bu istenmiyor.

Kümeleme (k-means) gibi işlerde ve büyüklüğün gerçekten anlam taşıdığı sayısal
verilerde tercih ediliyor.

### Karşılaştırma

| Metrik | Neye duyarlı | Aralık | İyi olan | Metin RAG'de |
|---|---|---|---|---|
| Kosinüs | Yön | -1 … 1 | Büyük | Varsayılan |
| İç çarpım | Yön + büyüklük | Sınırsız | Büyük | Normalize vektörlerde (hızlı) |
| Öklid | Yön + büyüklük | 0 … ∞ | **Küçük** | Nadiren |

**Kritik ilişki:** Vektörler normalize edilmişse üçü de aynı sıralamayı veriyor.
Normalize edilmiş vektörlerde Öklid uzaklığı ile kosinüs benzerliği arasında şu bağ
var:

```
d² = 2 × (1 - cos)
```

Yani kosinüs arttıkça Öklid uzaklığı azalıyor. Sıralama aynı, sadece skorun ölçeği
farklı. Bunu yanındaki notebook'ta sayısal olarak doğruladım.

---

## 6. Halüsinasyon Engelleme

RAG halüsinasyonu azaltıyor ama bitirmiyor. Sebebi gün 13'te not ettiğim gerçek:
**vektör veritabanı her zaman bir sonuç döndürür.** Alakasız soruda bile en yakın k
parça gelir ve model onlardan cevap üretmeye çalışır.

### İstem seviyesinde önlemler

**1. Bağlama sadakat kuralı.**
Modele açıkça söylemek: "Yalnızca aşağıdaki bağlamı kullan. Bağlamda yoksa
'Bilgi bulunamadı' de." Gün 15'te kuracağım kural bu.

**2. Kaçış yolu vermek.**
En önemli maddelerden biri. Modele "bilmiyorum" diyebileceği bir çıkış tanımlanmazsa
model bir şey uydurmak zorunda hissediyor. Açıkça izin vermek gerekiyor.

**3. Bağlamı sınırlarla ayırmak.**
Bağlamı `<baglam>...</baglam>` gibi etiketlerle çevrelemek, modelin talimat ile veriyi
karıştırmasını önlüyor.

**4. Kaynak göstermeyi zorunlu kılmak.**
"Her cümlenin hangi parçadan geldiğini belirt." Model kaynak göstermek zorunda
kalınca uydurma cümle kurması zorlaşıyor, ayrıca kullanıcı doğrulayabiliyor.

**5. Emin olmadığında belirtmesini istemek.**
Kısmi bilgi varsa "bağlamda sadece şu kadarı var" demesini istemek.

### Hat seviyesinde önlemler

**1. Benzerlik eşiği.**
En yüksek skor bile belirli bir değerin altındaysa aramayı başarısız say, modele hiç
gitme, doğrudan "Bilgi bulunamadı" döndür. Vektör veritabanının her zaman sonuç
döndürmesi sorununa doğrudan çare.

**2. Alaka denetimi.**
CRAG'de gördüğüm değerlendirme adımı.

**3. Üretim sonrası doğrulama.**
Üretilen cevabın her iddiasını bağlamla karşılaştırmak (Self-RAG'in IsSup jetonunun
yaptığı iş).

**4. Düşük sıcaklık.**
Bugünün son bölümünün konusu: temperature değerini düşürmek modelin daha kararlı ve bağlama sadık
kalmasını sağlıyor.

### Neyi tamamen çözemiyoruz

- Bağlamdaki bilgi yanlışsa model de yanlış cevap veriyor. RAG kaynağın doğruluğunu
  denetlemiyor.
- Parçalar çelişiyorsa model birini seçiyor ve seçiminin gerekçesi belirsiz kalıyor.
- Model bazen bağlamı bırakıp eğitim verisindeki bilgiye dönüyor.

---

## Sonuç

Bugün RAG'in **kendini denetleyen** türlerini ve temel bileşenlerini inceledim.

CRAG, Self-RAG ve Agentic RAG'in ortak yanı, önceki dosyada "Naive RAG sorgusuz bir hat" diye
tespit ettiğim boşluğu doldurmaları. Farkları denetimi kimin yaptığı: CRAG'de ayrı
bir değerlendirici, Self-RAG'de modelin kendisi, Agentic RAG'de bütün akışı yöneten
bir ajan. Yetenek arttıkça öngörülebilirlik ve maliyet kontrolü kötüleşiyor.

Chunking'in sonucu ne kadar etkilediğini görmek şaşırtıcı oldu. Örtüşmenin sebebini
somut bir örnekle anladım: bilgi kesme noktasına denk gelirse iki parça da eksik
kalıyor. Bugün öğrendiğim en pratik kalıp ise "küçük parçayla ara, büyük parçayı ver".

Benzerlik metriklerinde ise en önemli çıkarım şu oldu: vektörler normalize edilmişse
üç metrik de aynı sıralamayı veriyor, sadece hesap maliyetleri farklı. O yüzden metin
aramasında tartışma "hangi metrik daha doğru" değil, "normalize ediyor muyuz"
sorusuna indirgeniyor.

Halüsinasyon engellemede ise en çok şu madde dikkatimi çekti: modele "bilmiyorum"
diyebileceği bir kaçış yolu tanımlamazsam, model uydurmak zorunda hissediyor. Gün
20'de bunu bizzat test edeceğim.
