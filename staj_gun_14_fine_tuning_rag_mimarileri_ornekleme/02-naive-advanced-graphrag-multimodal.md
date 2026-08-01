# Gün 14 - RAG Mimarileri (1): Naive'den Advanced'e, GraphRAG ve Multimodal

Görevlendirmenin 4. bölümü en büyük bölüm, o yüzden ikiye ayırdım. Bugün RAG'in
temel hattını, gelişmiş versiyonunu ve veri yapısına göre değişen türlerini
inceliyorum. Akış ve mantık odaklı RAG'ler (CRAG, Self-RAG, Agentic) sonraki dosyaya kaldı.

---

## 0. RAG Nedir, Neden Var?

Gün 13'te AGI engellerini yazarken şunu not etmiştim: modelin kalıcı belleği ve
güncel bilgiye erişimi yok. RAG (Retrieval-Augmented Generation) tam olarak bu
kısıta verilen mühendislik cevabı.

Fikir basit: modele soruyu doğrudan sormak yerine, önce soruyla alakalı belgeleri
bul, onları soruyla birlikte modele ver, model cevabı **o belgelere dayanarak**
üretsin.

Kazandırdıkları:

- Model eğitim verisinde olmayan bilgiyi kullanabiliyor
- Bilgi güncellendiğinde modeli yeniden eğitmek gerekmiyor
- Cevabın kaynağı gösterilebiliyor
- Halüsinasyon azalıyor (bitmiyor, azalıyor)

---

## 1. Naive (Standart) RAG

### Hat

En temel kurulum dört adımdan oluşuyor:

```
Belgeler -> Parçalama -> Vektörleştirme -> [Vektör DB]
                                               |
Soru -> Vektörleştirme -> Arama --------------→|
                             |
                        En yakın k parça
                             |
                     Soru + parçalar -> LLM -> Cevap
```

İki ayrı zaman var: **indeksleme** (belgeler bir kez işlenip veritabanına konur) ve
**sorgu** (kullanıcı soru sorunca çalışır).

Gün 15'te sıfırdan yazacağım hat tam olarak bu.

### Tıkanıklıklar

Görev "standart RAG hattındaki tıkanıklıklar nelerdir" diye soruyor. Araştırdığım
kadarıyla her adımın kendi zayıf noktası var:

**Parçalama adımında:**
- Sabit boyutlu bölme cümleyi ortadan kesebiliyor, anlam kopuyor.
- Parça çok küçükse bağlam eksik kalıyor; çok büyükse içinde alakasız bilgi de
  taşıyor ve embedding'i bulanıklaşıyor.
- Bir tablonun ya da listenin ortasından bölünmesi bilgiyi anlamsızlaştırıyor.

**Vektörleştirme adımında:**
- Tek bir vektör, uzun bir parçanın bütün anlamını taşımak zorunda; parça çok konulu
  ise vektör bunların ortalamasına kayıyor ve hiçbirine tam benzemiyor.
- Embedding modeli hangi dilde/alanda eğitildiyse orada iyi; alan dışında zayıflıyor.

**Arama adımında (en kritik):**
- **Soru ile cevap farklı biçimde yazılır.** Kullanıcı "iade edebilir miyim" diye
  sorar, belgede "iade süreci 14 gündür" yazar. İkisinin vektörleri her zaman yakın
  olmayabiliyor.
- **Kısa ve belirsiz sorular** iyi vektör üretmiyor. "Peki ya fiyat?" gibi bir soru
  tek başına anlamsız.
- **Kesin terim aramada zayıf.** Ürün kodu, kanun maddesi, özel isim gibi şeylerde
  anlamsal arama tutturamıyor.
- **Her zaman sonuç dönüyor.** Gün 13'te not ettiğim gibi, alakasız soruda bile en
  yakın k parça geliyor. Bu doğrudan halüsinasyon kaynağı.

**Üretim adımında:**
- Getirilen parçalar alakasızsa model yine de onlardan cevap uydurmaya çalışıyor.
- Bağlamın ortasındaki bilgi gözden kaçabiliyor (lost in the middle).
- Model bazen bağlamı bırakıp kendi ezberinden cevap veriyor.

### Ortak sonuç

Naive RAG'in temel sorunu şu: **hat tek yönlü ve sorgulamasız.** Hiçbir adım kendi
çıktısının kalitesini kontrol etmiyor. Arama kötü sonuç getirse bile üretim adımı
onu sorgusuz kabul ediyor.

---

## 2. Advanced RAG

Advanced RAG, aynı hattın etrafına **arama öncesi** ve **arama sonrası** katmanlar
ekliyor. Hat hâlâ tek yönlü, ama her adım güçlendirilmiş.

### Arama öncesi (pre-retrieval)

**Soru yeniden yazma (Query Rewriting).**
Kullanıcının sorusu arama için uygun olmayabiliyor. LLM'e soruyu önce arama dostu
hale getirtiyoruz. Özellikle çok turlu konuşmalarda kritik: "peki ya fiyatı?"
sorusunu "X ürününün fiyatı nedir" haline getirmek gerekiyor, yoksa arama boşa
gidiyor.

**Soru genişletme / çoklu sorgu (Multi-Query).**
Tek sorudan birkaç farklı ifade üretip hepsiyle ayrı ayrı arama yapmak, sonuçları
birleştirmek. Farklı ifadeler farklı parçaları yakalıyor, kapsama artıyor.

**HyDE (Hypothetical Document Embeddings).**
En ilginç bulduğum teknik. Yukarıda "soru ile cevap farklı biçimde yazılır" diye bir
tıkanıklık yazmıştım; HyDE bunu şöyle çözüyor: önce LLM'den soruya **uydurma bir
cevap** yazmasını istiyoruz. Bu cevap olgusal olarak yanlış olabilir, önemli değil.
Sonra soruyu değil, bu uydurma cevabı vektörleştirip arama yapıyoruz.

Mantığı şu: uydurma cevap, biçim olarak gerçek cevaba benziyor. Belgedeki gerçek
cevaba, sorunun kendisinden daha yakın düşüyor. Yani soru-cevap uyumsuzluğunu, soruyu
cevap biçimine çevirerek aşıyor.

**Yönlendirme (Routing).**
Sorunun hangi veri kaynağına gitmesi gerektiğine karar vermek. Muhasebe sorusu
muhasebe koleksiyonuna, teknik soru dokümantasyona.

### Arama sonrası (post-retrieval)

**Yeniden sıralama (Re-ranking).**
Bence en yüksek getirili iyileştirme. İki aşamalı çalışıyor:

1. Vektör aramasıyla geniş bir aday kümesi çek (mesela 50 parça). Bu adım hızlı ama
   kaba.
2. Bu 50 parçayı, soruyla birlikte tek tek inceleyen daha güçlü bir modele (cross-
   encoder) ver, gerçek alaka skoruna göre sırala, ilk 5'ini al.

Neden iki aşama? Çünkü cross-encoder her parçayı soruyla birlikte işlediği için çok
daha doğru ama çok daha yavaş; 100 bin parçaya uygulanamaz, 50 parçaya uygulanır.
Vektör araması ise hızlı ama kaba. İkisi birleşince hem hızlı hem doğru oluyor.

**Bağlam sıkıştırma (Contextual Compression).**
Getirilen parçalardan soruyla alakasız cümleleri atmak. Hem token maliyeti düşüyor
hem de modelin dikkati dağılmıyor. Bugün istem/bağlam bölümünde not ettiğim "daha çok bağlam her zaman
daha iyi değil" tespitinin uygulaması.

**Yeniden sıralama-konumlandırma.**
"Lost in the middle" sorununa karşı en alakalı parçaları bağlamın başına ve sonuna
yerleştirmek.

### Naive ile Advanced farkı

| Adım | Naive | Advanced |
|---|---|---|
| Soru | Doğrudan kullanılır | Yeniden yazılır, genişletilir, HyDE uygulanır |
| Arama | Tek sorgu, tek kaynak | Çoklu sorgu, hibrit arama, yönlendirme |
| Sonuç | İlk k parça doğrudan kullanılır | Yeniden sıralanır, sıkıştırılır |
| Kalite kontrolü | Yok | Kısmi (sıralama skoru) |
| Maliyet | Düşük | Orta-yüksek (ek LLM çağrıları) |
| Gecikme | Düşük | Yüksek |

**Sistemde ne değişiyor:** Alaka oranı ve cevap doğruluğu belirgin artıyor,
halüsinasyon azalıyor. Karşılığında gecikme ve maliyet artıyor, sistem karmaşıklaşıyor.
Yani her uygulamaya bütün katmanları eklemek doğru değil; hangi tıkanıklık varsa ona
karşılık gelen katman ekleniyor.

---

## 3. Vector-based RAG ile GraphRAG

### Vector-based RAG'in kör noktası

Standart RAG belgeleri birbirinden bağımsız parçalara bölüyor. Her parça kendi
vektörüyle duruyor, aralarında bağ yok. Bu şu tür sorularda çöküyor:

> "A projesinde çalışan kişilerin daha önce birlikte çalıştığı yöneticiler kimler?"

Bu sorunun cevabı tek bir parçada yazmıyor. Birden fazla belgeden gelen bilgilerin
**ilişkilendirilmesi** gerekiyor. Vektör araması "en benzeyen 5 parça"yı getirir, ama
o parçalar arasında bağlantı kuramaz.

Aynı şekilde "bu belgenin ana temaları neler" gibi **bütünsel (global) sorular** da
çalışmıyor, çünkü cevap belgenin tamamında dağılmış durumda.

### GraphRAG nasıl çalışıyor?

GraphRAG, metni parçalara bölmek yerine bir **bilgi grafiğine (knowledge graph)**
dönüştürüyor.

**İndeksleme aşaması:**
1. Metin parçalanır.
2. Her parçadan LLM ile **varlıklar** (kişi, kurum, ürün, kavram) ve **ilişkiler**
   çıkarılır. Örnek: `(Ahmet) -[yönetiyor]-> (A Projesi)`.
3. Aynı varlığın farklı parçalardaki geçişleri birleştirilir.
4. Grafik üzerinde topluluk tespiti yapılır; birbirine sıkı bağlı varlık grupları
   bulunur ve her topluluk için özet üretilir.

**Sorgu aşaması** iki modda çalışıyor:
- **Yerel (local) arama:** Soruda geçen varlıkları bul, grafikte komşularına yayıl,
  o bölgeyi bağlam olarak ver.
- **Bütünsel (global) arama:** Topluluk özetlerini kullanarak belgenin geneline dair
  soruları cevapla.

### Karşılaştırma

| Konu | Vector RAG | GraphRAG |
|---|---|---|
| Veri temsili | Bağımsız metin parçaları | Varlıklar ve aralarındaki ilişkiler |
| İyi olduğu soru | "X nedir", "X nasıl yapılır" | "X ile Y arasındaki ilişki", "kimler nerede" |
| Çok adımlı akıl yürütme | Zayıf | Güçlü |
| Bütünsel sorular | Yapamaz | Topluluk özetleriyle yapar |
| İndeksleme maliyeti | Düşük | **Çok yüksek** (her parça için LLM çağrısı) |
| Güncelleme | Kolay (yeni parça ekle) | Zor (grafiği yeniden düzenlemek gerekebilir) |
| Kurulum karmaşıklığı | Düşük | Yüksek |

### GraphRAG ne zaman avantajlı?

- Veride **doğal ilişkiler** varsa: organizasyon şemaları, tıbbi kayıtlar (hasta-
  ilaç-yan etki), hukuki atıflar (madde-karar-içtihat), tedarik zincirleri,
  akademik atıf ağları, dolandırıcılık tespiti.
- Sorular **çok adımlı** ise.
- Belge kümesi görece **durağan** ise (sık güncellenmiyorsa).

Avantajlı olmadığı yer: sık değişen, ilişkisi zayıf, düz metinden oluşan içerikler.
Blog yazıları veya SSS dokümanı için GraphRAG kurmak gereksiz maliyet.

Uygulamada sık görülen çözüm **hibrit**: vektör araması ana hat, grafik ise ilişki
gerektiren sorular için ek katman.

---

## 4. Multimodal RAG

### Problem

Gerçek belgeler sadece düz metin değil. Bir teknik doküman içinde tablolar, şemalar,
grafikler ve fotoğraflar var. Standart RAG bunları ya atlıyor ya da bozuyor.

Somut örnek: bir finansal raporun asıl bilgisi tablodadır. PDF'ten düz metin
çıkarınca tablo satır sonlarıyla parçalanmış anlamsız bir sayı yığınına dönüşüyor;
vektörleştirilse bile arama işe yaramıyor.

### Yaklaşımlar

**1. Her şeyi metne çevir.**
Görselleri ve tabloları LLM'e verip metin açıklamalarını üret, o açıklamaları
vektörleştir. Basit ve mevcut hatla uyumlu. Dezavantajı: açıklama üretilirken bilgi
kaybı oluyor, ve cevap üretilirken görselin kendisi elde olmuyor.

**2. Ortak gömme uzayı (unified embedding).**
Metni ve görseli **aynı** vektör uzayına gömen modeller (CLIP tarzı) kullanmak.
Böylece metinle görsel doğrudan karşılaştırılabiliyor. Avantajı tek hat; dezavantajı
bu modellerin ince detayda (tablodaki bir sayı) zayıf kalması.

**3. Çoklu vektör / özet üzerinden arama.**
En yaygın pratik çözüm. Her görsel veya tablo için bir metin özeti üretilip **özet
vektörleştiriliyor**, ama veritabanında **orijinal görselin kendisi** saklanıyor.
Arama özet üzerinden yapılıyor, üretim aşamasında modele orijinal görsel veriliyor.
Böylece hem arama kalitesi hem de detay korunuyor.

### Hattın değişen yerleri

| Adım | Metin RAG | Multimodal RAG |
|---|---|---|
| Yükleme | Metin çıkarma | Düzen analizi: metin/tablo/görsel ayrıştırma |
| Parçalama | Karakter/cümle bazlı | Öğe bazlı; tablo ve görsel bölünmez |
| Vektörleştirme | Tek model | Tip başına farklı işlem |
| Depolama | Parça + vektör | Vektör + orijinal öğeye referans |
| Üretim | Metin LLM | Görme yeteneği olan LLM |

### Zorluklar

- **Düzen analizi (layout parsing)** hattın en kırılgan adımı. PDF'ten tabloyu doğru
  çıkarmak hâlâ zor bir problem.
- Grafiklerdeki bilgi (bir çizginin eğimi) metne çevrilirken kaybolabiliyor.
- Maliyet artıyor: görsel işleyen modeller daha pahalı, görseller daha çok token
  tüketiyor.

---

## Sonuç

Bugün RAG'in tek bir kalıp olmadığını, çözülmek istenen probleme göre değiştiğini
gördüm.

Naive RAG'in temel zaafı hattın **sorgusuz** olması: hiçbir adım kendi çıktısını
kontrol etmiyor, arama kötü sonuç getirse bile üretim onu kabul ediyor. Advanced RAG
bu hattın önüne ve arkasına katmanlar ekliyor. Bunlar arasında en çok HyDE ilgimi
çekti; soru ile cevabın farklı biçimde yazılması problemini, soruyu sahte bir cevaba
çevirerek çözmesi zekice geldi. En yüksek getirili iyileştirmenin ise yeniden
sıralama olduğunu öğrendim: hızlı ve kaba bir aramayla geniş aday çek, yavaş ve
doğru bir modelle bunları ele.

GraphRAG'in vektör RAG'e üstünlüğü, parçalar arasında **ilişki** kurabilmesi.
"Kim kiminle çalıştı" tarzı çok adımlı sorularda vektör araması yetersiz kalıyor.
Bedeli ise çok yüksek indeksleme maliyeti; her parça için LLM çağrısı gerekiyor.

Multimodal RAG'de öğrendiğim en pratik kalıp, **özet üzerinden arayıp orijinali
saklamak**. Arama metinle yapılıyor ama modele asıl görsel veriliyor, böylece hem
arama kalitesi hem detay korunuyor.

Ortak çıkarım: her katmanın bir bedeli var (gecikme, maliyet, karmaşıklık). Doğru
yaklaşım bütün teknikleri eklemek değil, hangi tıkanıklık varsa ona karşılık gelen
katmanı eklemek.
