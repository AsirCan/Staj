# Gün 13 - Vektör Temsilleri, Vektör Veritabanları ve Eğitim/Çıkarım Farkı

Görevlendirmenin 2. bölümünün kalan iki başlığı. Bu iki konu bir sonraki günlerde
çalışacağım RAG'in doğrudan temeli: RAG'in "R" kısmı (retrieval) tamamen embedding
ve vektör araması üzerine kurulu.

---

## 1. Metin Nasıl Sayıya Dönüşüyor? (Embeddings)

### Problem

Model sayılarla çalışıyor, elimdeki veri ise metin. "Köpek" kelimesini modele nasıl
vereceğim?

### Çalışmayan ilk fikir: kelimeye numara vermek

köpek=1, kedi=2, otomobil=3 diye numaralasam, model bunları sayı sanıp
"köpek + kedi = otomobil" gibi anlamsız ilişkiler kurar. Sıralama uydurmuş olurum.

### İkinci fikir: one-hot kodlama

Her kelimeye, sadece kendi konumu 1 olan uzun bir vektör veririm. 50.000 kelimelik
sözlükte her kelime 50.000 uzunluğunda bir vektör olur.

İki sorunu var: vektörler devasa ve neredeyse tamamen sıfır (seyrek), ve daha
kötüsü **her kelime birbirine eşit uzaklıkta**. "Kedi" ile "köpek" arasındaki mesafe,
"kedi" ile "buzdolabı" arasındakiyle aynı. Anlam bilgisi sıfır.

### Çözüm: yoğun vektörler (embeddings)

Embedding, kelimeyi (ya da cümleyi, paragrafı) birkaç yüz ya da birkaç bin boyutlu,
**yoğun** ve **öğrenilmiş** bir vektörle temsil etmek.

Kritik nokta şu: bu sayılar elle atanmıyor, **eğitim sırasında öğreniliyor**. Ve
öğrenme şu ilkeye dayanıyor: *bir kelimenin anlamı, hangi kelimelerle birlikte
göründüğüyle belirlenir.* Benzer bağlamlarda geçen kelimeler benzer vektörler alıyor.

Sonuçta ortaya bir **anlam uzayı** çıkıyor. Bu uzayda yakınlık anlamsal yakınlık
demek. En bilinen örneği vektör aritmetiği:

```
kral - adam + kadın ≈ kraliçe
```

Yani "hükümdarlık" ve "cinsiyet" gibi kavramlar uzayda yönlere karşılık geliyor.
Bunu yanındaki notebook'ta elle kurduğum küçük bir uzayda deneyerek gösterdim.

### Gün 12'deki modelle bağlantısı

Aslında embedding'i zaten gördüm. `nn.Embedding` katmanı, içinde
`(sözlük_boyutu, embedding_boyutu)` şeklinde bir tablo tutan ve gelen kelime
numarasına karşılık gelen satırı döndüren bir katman. O tablo da diğer bütün
ağırlıklar gibi geri yayılımla öğreniliyor. Yani embedding sihirli bir şey değil,
sadece eğitilmiş bir arama tablosu.

### Statik embedding vs bağlamsal embedding

**Statik (Word2Vec, GloVe):** Her kelimenin tek bir sabit vektörü var. "Yüz"
kelimesi hem organ hem sayı anlamında aynı vektörü alıyor. Bağlamı göremiyor.

**Bağlamsal (BERT, modern embedding modelleri):** Vektör, kelimenin içinde bulunduğu
cümleye göre değişiyor. "Yüzünü yıkadı" ile "yüz lira" cümlelerindeki "yüz"
farklı vektörler alıyor. Transformer'ın attention mekanizması tam olarak bunu
sağlıyor: her token, cümledeki diğer tokenlara bakarak kendi temsilini güncelliyor.

RAG'de kullanılan modeller bağlamsal olanlar. Üstelik tek kelime değil, bütün bir
paragrafı tek vektöre indiriyorlar (sentence/document embedding).

### Boyut seçimi

Tipik değerler 384, 768, 1536, 3072. Ödünleşim şu:

- Büyük boyut → daha ince anlam ayrımı, ama daha çok bellek ve daha yavaş arama
- Küçük boyut → hızlı ve ucuz, ama benzer kavramlar birbirine karışabiliyor

Bazı modeller (Matryoshka tekniği) tek bir vektörü sondan kesip küçültmeye izin
veriyor, böylece aynı modelden hem büyük hem küçük boyut alınabiliyor.

---

## 2. Vektör Veritabanları ile Geleneksel Veritabanları

### Temel fark: ne sorduğun

Geleneksel veritabanına (PostgreSQL, MySQL) sorduğum soru **kesin eşleşme**:

```sql
SELECT * FROM urunler WHERE fiyat < 100 AND kategori = 'ayakkabi';
```

Cevap ya vardır ya yoktur. İki değer ya eşittir ya değildir.

Vektör veritabanına sorduğum soru **benzerlik**:

> Bu vektöre en yakın 5 vektörü getir.

Burada "eşit" diye bir şey yok, her kayıt için bir yakınlık skoru var ve en
yüksekleri isteniyor. Buna **k-en yakın komşu (k-NN)** araması deniyor.

| Konu | Geleneksel VT | Vektör VT |
|---|---|---|
| Sorgu tipi | Kesin eşleşme, aralık, birleştirme | Benzerlik (en yakın komşu) |
| Veri birimi | Satır ve sütunlar | Vektör + üstveri (metadata) |
| İndeks yapısı | B-tree, hash | HNSW, IVF, PQ |
| Sonuç | Kesin, tekrarlanabilir | Yaklaşık, skorlu, sıralı |
| "Yok" cevabı | Boş küme | Hep bir şey döner, skoru düşük olur |
| Tipik soru | "Fiyatı 100'den az ürünler" | "Bu açıklamaya benzeyen ürünler" |

Dikkat edilmesi gereken bir nokta: vektör veritabanı **her zaman bir cevap döndürür**.
Alakasız bir soru sorsam bile en yakın 5 parçayı getirir, sadece skorları düşük olur.
RAG'de halüsinasyonun önemli bir kaynağı bu; bu yüzden skor eşiği koymak gerekiyor.
Bunu gün 15'teki testlerde bizzat kullanacağım.

### Neden özel bir veritabanı gerekiyor?

Elimde 1 milyon parça olsun, her biri 1536 boyutlu. Soruyla hepsini tek tek
karşılaştırırsam 1 milyon çarpım işlemi yapmam gerekir. Bu "kaba kuvvet" (brute
force) araması küçük veride sorunsuz ama büyük veride çok yavaş.

Vektör veritabanları **yaklaşık en yakın komşu (ANN - Approximate Nearest Neighbor)**
algoritmaları kullanıyor. Kesin en yakını bulma garantisinden biraz feragat edip
aramayı yüzlerce kat hızlandırıyorlar.

**HNSW (Hierarchical Navigable Small World):** Vektörleri katmanlı bir grafik olarak
bağlıyor. Üst katmanlar seyrek ve uzun atlamalı, alt katmanlar yoğun. Arama üstten
başlayıp kabaca doğru bölgeye atlıyor, sonra aşağı inip inceliyor. Bugün en yaygın
kullanılan yöntem.

**IVF (Inverted File Index):** Vektör uzayını önce kümelere bölüyor. Arama sırasında
sadece soruya en yakın birkaç kümeye bakılıyor, diğerleri hiç taranmıyor.

**PQ (Product Quantization):** Vektörleri sıkıştırarak bellekte kapladıkları yeri
azaltıyor. Doğruluktan biraz kaybettirip çok daha fazla vektörü belleğe sığdırıyor.

### Öne çıkan araçlar

| Araç | Tipi | Notlar |
|---|---|---|
| **Pinecone** | Bulut servisi | Kurulum yok, ölçekleniyor, ücretli |
| **ChromaDB** | Gömülü / yerel | Python'da tek satırla başlıyor, prototip için ideal |
| **Qdrant** | Açık kaynak sunucu | Rust ile yazılmış, filtreleme desteği güçlü |
| **Weaviate** | Açık kaynak sunucu | Şema ve hibrit arama odaklı |
| **FAISS** | Kütüphane | Veritabanı değil, arama kütüphanesi; Meta geliştirdi |
| **pgvector** | PostgreSQL eklentisi | Mevcut ilişkisel veritabanına vektör araması ekliyor |

### Hibrit arama

Uygulamada yalnızca vektör araması genelde yetmiyor. Anlamsal arama "ürün iade
politikası" ile "malı geri gönderme kuralları"nı eşleştirebiliyor ama tam kelime
eşleşmesinde (ürün kodu, kanun maddesi numarası, özel isim) zayıf kalabiliyor.

Bu yüzden üretimde çoğunlukla **hibrit arama** kullanılıyor: anahtar kelime araması
(BM25) ile vektör araması birlikte çalıştırılıp sonuçlar birleştiriliyor.

---

## 3. Eğitim (Training) ile Çıkarım (Inference) Farkı

### İşlem farkı

**Eğitim** gün 11'de yazdığım döngünün ta kendisi: ileri geçiş, kayıp hesabı, geri
yayılım, parametre güncelleme. Kritik nokta şu: eğitimde model **değişiyor**.

**Çıkarım** ise sadece ileri geçiş. Ağırlıklar sabit, gradyan hesabı yok, güncelleme
yok. Gün 11 ve 12'de tahmin alırken kullandığım `torch.no_grad()` bloğu tam olarak
çıkarım modu demek.

| Konu | Eğitim | Çıkarım |
|---|---|---|
| Yapılan işlem | İleri + geri geçiş + güncelleme | Sadece ileri geçiş |
| Model durumu | Ağırlıklar değişiyor | Ağırlıklar sabit |
| Gradyan | Hesaplanıyor ve saklanıyor | Hiç hesaplanmıyor |
| Bellek ihtiyacı | Çok yüksek (ara aktivasyonlar saklanıyor) | Düşük (sadece ağırlıklar) |
| Veri akışı | Aynı veri onlarca kez (epoch) | Her istek bir kez |
| Süre | Günler, haftalar | Milisaniye, saniye |
| PyTorch karşılığı | `model.train()` + optimizer | `model.eval()` + `torch.no_grad()` |

### Donanım farkı

**Eğitim** yüksek bellekli GPU'lar ister. Sebebi sadece model boyutu değil: geri
yayılım için ileri geçişteki bütün ara aktivasyonların bellekte tutulması gerekiyor,
ayrıca optimizer da her parametre için ek durum saklıyor (Adam kullanılıyorsa
parametre başına iki ek değer). Pratikte eğitim, çıkarımın birkaç katı bellek
istiyor.

**Çıkarım** çok daha hafif. Küçük modeller CPU'da bile çalışabiliyor. Burada asıl
kısıt bellek miktarı ve bellek bant genişliği; her token üretiminde bütün ağırlıkların
okunması gerektiği için işlem gücünden çok bellek hızı sınırlıyor.

Kendi ortamımdan örnek: RTX 4050'nin 6 GB belleği gün 12'deki MiniBrain için fazlasıyla
yeterli, ama milyarlarca parametreli bir modeli eğitmeye kalksam anında yetmez.
Aynı modelin çıkarımı ise sıkıştırma (quantization) ile sığabilir.

### Maliyet farkı

Bu ayrım ekonomik olarak da kritik:

**Eğitim tek seferlik ve büyük.** Büyük bir modeli eğitmek milyonlarca dolar
tutabiliyor, ama bir kez ödeniyor.

**Çıkarım sürekli ve dağıtık.** Her kullanıcı isteği ayrı maliyet. Model popüler
olursa toplam çıkarım maliyeti eğitim maliyetini kolayca geçiyor.

Bu yüzden AI Mühendisliğinde optimizasyon çabasının çoğu çıkarım tarafında: model
sıkıştırma, önbellekleme (caching), toplu işleme (batching), istem kısaltma. Gün
13'te not ettiğim "token maliyeti bir ürün kararıdır" tespitinin teknik karşılığı bu.

### Ara durum: fine-tuning

İkisinin arasında duruyor. Eğitim gibi ağırlıkları değiştiriyor ama sıfırdan eğitime
göre çok daha kısa ve ucuz. LoRA gibi yöntemler yalnızca küçük bir ek parametre
kümesini eğiterek maliyeti daha da düşürüyor. Bu konu gün 14'ün başlığı.

---

## Sonuç

Bu bölümde RAG'in altyapısını öğrendim.

Embedding, metni anlamın korunduğu bir vektör uzayına taşıyan öğrenilmiş bir temsil.
One-hot'ın aksine benzer anlamlar birbirine yakın düşüyor, ve bu yakınlık ölçülebilir
bir sayı olduğu için arama yapılabiliyor.

Vektör veritabanları da bu yakınlık aramasını büyük ölçekte hızlı yapmak için var.
Geleneksel veritabanından farkı kesin eşleşme yerine benzerlik döndürmesi. Öğrendiğim
en önemli pratik detay, bu sistemlerin **her zaman bir cevap döndürmesi** — alakasız
soruda bile. Halüsinasyon riskinin kaynaklarından biri bu ve gün 15'te kuracağım
"Bilgi bulunamadı" mekanizmasının sebebi de bu.

Eğitim ile çıkarım arasındaki farkı ise aslında zaten uygulamıştım: `model.train()`
ile `torch.no_grad()` arasındaki fark tam olarak bu ayrım. Yeni öğrendiğim, bu
ayrımın donanım ve maliyet tarafındaki karşılığı; eğitim tek seferlik ve büyük,
çıkarım sürekli ve zamanla daha pahalı.
