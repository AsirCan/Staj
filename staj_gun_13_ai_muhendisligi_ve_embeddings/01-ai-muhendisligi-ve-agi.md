# Gün 13 - AI Mühendisliğine Giriş, Rol Tanımları ve AGI

Bu rapor görevlendirmenin 1. bölümünü ve 2. bölümün "Yapay Zeka Türleri" başlığını
kapsıyor. İki soruya cevap arıyorum: AI Mühendisi ile ML Mühendisi arasındaki fark
nedir, ve bugünkü dar yapay zeka ile AGI arasında ne var.

---

## 1. AI Mühendisi ile ML Mühendisi Arasındaki Fark

İlk başta bu ikisi bana aynı iş gibi geldi. Araştırınca farkın **modelin hangi
tarafında durduğunla** ilgili olduğunu anladım.

En kısa özeti şu: **ML Mühendisi modeli üretir, AI Mühendisi modeli üründe
kullanılır hale getirir.**

### Temel Ayrım

ML Mühendisi bir problemi alır, veri toplar, model eğitir. Elinde eğitim verisi,
kayıp fonksiyonu ve GPU vardır. Başarı ölçütü doğruluk, F1 skoru, kayıp değeri gibi
metriklerdir. Yani gün 11 ve 12'de yaptığım şey (veri üret, model kur, eğit) ML
mühendisliğinin çekirdeği.

AI Mühendisi ise genellikle **modeli eğitmez**. Hazır bir temel modeli (GPT, Claude,
Gemini, Llama) alır ve onun etrafına bir sistem kurar: hangi veriye bakacak, istem
nasıl kurulacak, cevap doğru mu, maliyet ne olacak, hata verirse ne olacak. Başarı
ölçütü kullanıcının aldığı cevabın kalitesi, gecikme süresi ve maliyettir.

### Karşılaştırma Tablosu

| Konu | ML Mühendisi | AI Mühendisi |
|---|---|---|
| Çıkış noktası | Ham veri | Hazır temel model (foundation model) |
| Ana faaliyet | Model eğitmek, hiperparametre ayarlamak | Model etrafında sistem kurmak |
| Tipik araçlar | PyTorch, TensorFlow, scikit-learn, MLflow | LLM API'leri, vektör veritabanları, RAG, ajan çerçeveleri |
| Veri ihtiyacı | Büyük, etiketli eğitim verisi | Az; genelde şirket dokümanları ve örnek istemler |
| Donanım | GPU kümesi, uzun eğitim süreleri | Çoğunlukla CPU yeterli; ağır iş API tarafında |
| Başarı ölçütü | Doğruluk, F1, kayıp | Cevap kalitesi, gecikme, token maliyeti, halüsinasyon oranı |
| Zaman ölçeği | Günler-haftalar süren eğitim döngüleri | Saatler süren istem/mimari döngüleri |
| Tipik problem | "Bu görüntüde kedi var mı?" | "Şirketin 4000 sayfalık dokümanına soru soran bir asistan" |
| Matematik ağırlığı | Yüksek (gradyan, optimizasyon, istatistik) | Orta (vektör benzerliği, olasılık örnekleme) |

### Yetkinlik Farkı

ML Mühendisinden beklenen: doğrusal cebir, olasılık, optimizasyon, model mimarileri,
veri temizliği, deney takibi.

AI Mühendisinden beklenen: yazılım mühendisliği (asıl ağırlık burada), API tasarımı,
istem mühendisliği, RAG mimarileri, vektör veritabanları, maliyet ve gecikme yönetimi,
değerlendirme (evaluation) kurgusu.

Dikkatimi çeken nokta: AI Mühendisliği aslında **backend mühendisliğine ML
mühendisliğinden daha yakın**. İşin büyük kısmı model değil, modelin etrafındaki
sistem.

### Kesişim Alanı

İkisi keskin çizgiyle ayrılmıyor. Fine-tuning, model değerlendirme ve gömme
(embedding) modeli seçimi gibi konular her ikisinin de alanına giriyor. Küçük
şirketlerde zaten tek kişi ikisini birden yapıyor. Ayrım daha çok büyük ekiplerde
netleşiyor.

---

## 2. AI Mühendisinin Ürün Geliştirmedeki Kritik Rolü

Görev "bir yazılım ürününün geliştirilmesinde AI Mühendisinin kapladığı kritik rolü
örneklerle açıklayın" diyor. Araştırdığım kadarıyla bu rolün kritik olmasının sebebi
şu: **yapay zeka ürünleri klasik yazılımın kırıldığı yerde başlıyor.**

Klasik yazılımda aynı girdi hep aynı çıktıyı verir. LLM tabanlı üründe vermez.
Bu tek fark, ürün geliştirmenin neredeyse her aşamasını değiştiriyor ve AI
Mühendisinin varlık sebebi bu boşluğu doldurmak.

### Örnek 1 - Belirsizliğin ürün tasarımına etkisi

Bir bankanın müşteri destek asistanını düşünelim. Klasik yazılımcı "kullanıcı X
yazarsa Y ekranı açılır" diye tasarlar. LLM'de böyle bir garanti yok; model bazen
mevzuatta olmayan bir şey uydurabilir (halüsinasyon).

AI Mühendisi burada devreye girip şunları kurar: cevap yalnızca doğrulanmış
dokümanlardan üretilsin (RAG), doküman bulunamazsa model "bilmiyorum" desin,
riskli konularda insana aktarılsın. Yani ürünün **güvenilirlik sınırlarını** çizen
kişi o.

### Örnek 2 - Maliyetin bir ürün kararı olması

Klasik yazılımda bir fonksiyonu çağırmanın maliyeti sıfıra yakındır. LLM'de her
çağrı token başına para. Bağlam penceresini gereksiz doldurmak faturayı katlar.

AI Mühendisi burada "hangi modeli nerede kullanacağız" kararını verir: basit
sınıflandırma için küçük ve ucuz model, karmaşık akıl yürütme için büyük model.
Bu doğrudan ürünün birim ekonomisini belirleyen bir mühendislik kararı.

### Örnek 3 - Değerlendirmenin (evaluation) kurulması

Klasik yazılımda test ya geçer ya kalır. LLM çıktısında "doğru cevap" tek bir string
değil. Ürünün her sürümünde kalitenin düşüp düşmediğini ölçmek için ayrı bir
değerlendirme altyapısı gerekiyor: örnek soru-cevap kümeleri, otomatik puanlama,
regresyon takibi.

Bu altyapı olmadan ekip istemde bir kelime değiştirip farkında olmadan ürünü
bozabilir. AI Mühendisi bunu kurmazsa kimse kurmuyor.

### Örnek 4 - Ürün ekibiyle model arasındaki tercüme

Ürün yöneticisi "asistan daha yaratıcı cevaplar versin" der. Bunun teknik karşılığı
temperature değerini yükseltmek, top-p'yi gevşetmek, istemi değiştirmek olabilir; ama
aynı hamle halüsinasyonu da artırır. AI Mühendisi bu ödünleşimi (trade-off) görüp
ürün ekibine "yaratıcılık artarsa doğruluk düşer, hangisini istiyorsun" diye
sorabilen kişi.

### Özet

AI Mühendisi ürüne şunu katıyor: **olasılıksal bir bileşeni, deterministik bir ürünün
içinde güvenle çalıştırmak.** Model zaten hazır ve herkese açık; rekabet avantajı
modelde değil, onun etrafına kurulan bu sistemde oluşuyor.

---

## 3. Dar Yapay Zeka (ANI) ile Yapay Genel Zeka (AGI) Arasındaki Sınır

### Tanımlar

**Dar AI (ANI - Artificial Narrow Intelligence):** Belirli bir görev kümesi için
eğitilmiş, o kümenin dışına çıkamayan sistemler. Bugün var olan **her** yapay zeka
bu sınıfta. Satranç motoru, görüntü sınıflandırıcı, ve evet, ChatGPT dahil bütün
LLM'ler.

**AGI (Artificial General Intelligence):** İnsanın yapabildiği bilişsel işlerin
büyük çoğunluğunu, yeniden eğitilmeye ihtiyaç duymadan, öğrenerek ve genelleyerek
yapabilen sistem.

### LLM'ler neden hâlâ dar AI?

Burası araştırırken en çok kafa yorduğum kısım oldu, çünkü LLM'ler çok "genel"
görünüyor. Şiir de yazıyor, kod da yazıyor, çeviri de yapıyor. Buna rağmen dar AI
sayılmalarının sebepleri:

**Eğitim ile kullanım ayrı.** Model eğitim bittikten sonra öğrenmeyi durduruyor.
Bugün ona öğrettiğim bir şeyi yarın hatırlamıyor; bağlam penceresine sığdırdığım
kadarı geçici olarak duruyor, o kadar. İnsan ise sürekli öğreniyor.

**Genelleme değil, kapsama.** Model çok geniş bir veri dağılımını kapsıyor, bu yüzden
genel görünüyor. Ama eğitim dağılımının gerçekten dışına çıkan bir problemde
performansı hızla düşüyor. Genellik ile "çok şey ezberlemiş olmak" farklı şeyler.

**Dünya modeli zayıf.** Metinden öğrendiği için fizik, nedensellik ve zaman
konularında tutarsız olabiliyor. Gün 9'da not ettiğim çıkarım burada da geçerli:
model düşünmüyor, çok iyi öğrenilmiş bir olasılık dağılımından tahmin üretiyor.

**Hedef ve amaç yok.** LLM kendine hedef koymuyor, sadece verilen istemi yanıtlıyor.
Ajan (agent) mimarileri bunu dışarıdan bir döngüyle taklit ediyor ama modelin
kendisinde böyle bir yeti yok.

### AGI için aşılması gereken teknik engeller

Araştırmada tekrar tekrar karşıma çıkan başlıklar şunlar:

**1. Sürekli öğrenme (continual learning).** Modelin çalışırken öğrenmesi gerekiyor.
Bunun önündeki engel "felaket unutma" (catastrophic forgetting): yeni bilgi
öğretildiğinde eski bilginin bozulması. Gün 11-12'de gördüğüm gradyan tabanlı
güncellemenin doğal bir sonucu bu; ağırlıklar yeni veriye göre kayınca eskisi
siliniyor.

**2. Uzun vadeli bellek.** Bugünkü çözüm bağlam penceresi ve RAG. İkisi de dışarıdan
takılan protez; modelin kendi kalıcı belleği değil. Kalıcı, güncellenebilir ve
çelişkileri çözebilen bir bellek yapısı henüz yok.

**3. Nedensellik ve akıl yürütme.** Model korelasyon öğreniyor, nedensellik değil.
Çok adımlı akıl yürütmede zincirin ortasında kopabiliyor. Düşünce zinciri
(chain-of-thought) ve akıl yürütme modelleri bu konuda ilerleme sağladı ama sorunu
çözmedi.

**4. Örneklem verimliliği.** İnsan bir kavramı birkaç örnekle öğreniyor, model
milyonlarca örnek istiyor. Bu fark sadece ölçek meselesi değil, öğrenme yönteminin
farklı olduğunun işareti.

**5. Çok kipli ve bedenli deneyim.** Metinle öğrenilen dünya eksik. Görme, işitme ve
fiziksel etkileşimin birleştiği bir öğrenme henüz olgun değil.

**6. Değerlendirme problemi.** AGI'ye ulaşıldığını nasıl anlayacağız sorusunun kabul
görmüş bir cevabı yok. Turing testi yetersiz kaldı, mevcut kıyaslama testleri ise
eğitim verisine sızdığı için güvenilirliğini yitiriyor.

**7. Hizalama (alignment) ve güvenlik.** Teknik bir engel olmasa da AGI tartışmasının
ayrılmaz parçası: genel yetenekli bir sistemin hedeflerinin insan değerleriyle
uyumlu kalmasını garanti etmenin bilinen bir yöntemi yok.

### Ölçek yeterli mi?

Alanda iki görüş var. Birincisi, modelleri ve veriyi büyütmeye devam edersek genel
yeteneklerin kendiliğinden ortaya çıkacağını savunuyor (ölçek hipotezi). İkincisi,
sürekli öğrenme ve nedensellik gibi eksiklerin mimari kaynaklı olduğunu, sadece
büyütmekle çözülmeyeceğini söylüyor.

Benim anladığım kadarıyla son dönemde ikinci görüş güç kazandı; artık sadece
büyütmek yerine akıl yürütme, araç kullanımı ve bellek gibi ek yapılar üzerinde
çalışılıyor. Bugünkü ajan mimarilerinin popülerliği de bunun bir işareti.

---

## Sonuç

Bu bölümde iki şey öğrendim.

Birincisi, AI Mühendisi ile ML Mühendisi arasındaki fark unvan farkı değil, **işin
odağının farkı**. ML Mühendisi modeli üretiyor, AI Mühendisi hazır modeli güvenilir
bir ürüne dönüştürüyor. Staj boyunca gün 10-12'de yaptığım tensör ve eğitim döngüsü
çalışmaları ML tarafına, bundan sonra gireceğim RAG konusu ise AI Mühendisliği
tarafına ait.

İkincisi, bugünkü LLM'ler ne kadar genel görünürse görünsün hâlâ dar yapay zeka
sınıfında. AGI'ye giden yolda ölçek büyütmenin tek başına yetmediği, sürekli öğrenme,
kalıcı bellek ve nedensellik gibi mimari eksiklerin çözülmesi gerektiği anlaşılıyor.
İlginç olan şu: bu eksiklerden en az ikisi (bellek ve güncel bilgiye erişim) bugün
RAG ile dışarıdan telafi ediliyor. Yani bir sonraki günlerde çalışacağım konu,
aslında modelin bu temel kısıtına verilen mühendislik cevabı.
