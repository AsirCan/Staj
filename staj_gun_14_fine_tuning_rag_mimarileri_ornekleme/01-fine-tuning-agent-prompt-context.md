# Gün 14 - Fine-tuning, Yapay Zeka Ajanları ve İstem/Bağlam Mühendisliği

Görevlendirmenin 3. bölümü. Üç başlık da "hazır modeli nasıl kendi işime uydururum"
sorusunun farklı cevapları.

---

## 1. İnce Ayar (Fine-tuning)

### Ne işe yarıyor?

Fine-tuning, önceden eğitilmiş bir modeli alıp kendi dar alanımdaki veriyle bir süre
daha eğitmek. Sıfırdan eğitim değil; modelin genel dil yeteneği duruyor, üstüne
uzmanlık ekleniyor.

Teknik olarak gün 11'de yazdığım eğitim döngüsünün aynısı çalışıyor: ileri geçiş,
kayıp, geri yayılım, güncelleme. Tek fark başlangıç noktasının rastgele ağırlıklar
değil, zaten eğitilmiş ağırlıklar olması.

### Ne zaman gerçekten işe yarıyor?

Araştırırken en çok karşılaştığım yanılgı şuydu: "modele yeni bilgi öğretmek için
fine-tuning yapılır". Doğrusu bu değil. Fine-tuning **bilgi öğretmekten çok davranış
öğretiyor**.

İyi çalıştığı yerler:

- **Biçim ve üslup:** Modelin hep belirli bir formatta (JSON şeması, resmi dil, kurum
  üslubu) cevap vermesi.
- **Alan diline uyum:** Tıp, hukuk, finans gibi kendine has terminolojisi olan
  alanlarda dilin oturması.
- **Görev uzmanlaşması:** Dar ve tekrar eden bir iş (belge sınıflandırma, etiketleme)
  için küçük bir modeli büyük modelin seviyesine çıkarmak.
- **Maliyet düşürme:** Uzun sistem istemleriyle büyük modele yaptırdığın işi, kısa
  istemle küçük bir modele yaptırmak.

Kötü çalıştığı yer: **sık değişen olgusal bilgi.** Şirketin fiyat listesini
fine-tuning ile öğretirsen, fiyat değiştiğinde modeli yeniden eğitmen gerekir.
Üstelik model bilgiyi ezberlemek yerine "o tarz cümleler kurmayı" öğrenebilir, yani
yanlış fiyatı kendinden emin bir şekilde söyler.

### Maliyet

Tam fine-tuning'de bütün ağırlıklar güncelleniyor. Bu, gün 13'te not ettiğim eğitim
maliyetinin tamamını getiriyor: ağırlıklar + gradyanlar + optimizer durumu bellekte.
Büyük modellerde tek bir GPU'ya sığmıyor.

**LoRA (Low-Rank Adaptation)** bu sorunu çözüyor. Fikir şu: orijinal ağırlıkları
dondur, yanına küçük bir "ek matris" tak ve sadece onu eğit. Eğitilen parametre sayısı
toplamın yüzde biri civarına düşüyor. **QLoRA** ise ana modeli sıkıştırılmış (4-bit)
halde tutarak bellek ihtiyacını daha da azaltıyor; tek bir tüketici GPU'sunda bile
fine-tuning yapılabiliyor.

Ek avantajı: LoRA adaptörleri küçük dosyalar olduğu için aynı ana modele farklı
görevler için farklı adaptörler takılabiliyor.

### Fine-tuning ile RAG karşılaştırması

Görev bu karşılaştırmayı özellikle istiyor. Araştırdığım kadarıyla ayrım şu cümleyle
özetleniyor:

> **Fine-tuning modelin nasıl davranacağını, RAG neyi bileceğini belirler.**

| Konu | Fine-tuning | RAG |
|---|---|---|
| Neyi değiştiriyor | Model ağırlıklarını | Modele verilen bağlamı |
| Bilgi güncelleme | Yeniden eğitim gerekir | Veritabanına yeni belge eklemek yeterli |
| Kurulum maliyeti | Yüksek (GPU, veri hazırlama) | Düşük |
| İstek başı maliyet | Düşük (kısa istem) | Yüksek (bağlam token'ları eklenir) |
| Gecikme | Düşük | Arama adımı ek gecikme getirir |
| Kaynak gösterme | Yapamaz | Yapabilir, hangi belgeden geldiği bellidir |
| Veri ihtiyacı | Binlerce örnek | Sadece belgelerin kendisi |
| Halüsinasyon | Azaltmaz, hatta artırabilir | Bağlama sadık kalma kuralıyla azaltır |
| İyi olduğu yer | Biçim, üslup, dar görev | Olgusal, değişken, kaynaklı bilgi |

**Ne zaman hangisi:**

- Model *nasıl konuşacağını* bilmiyorsa → fine-tuning
- Model *neyi konuşacağını* bilmiyorsa → RAG
- İkisi de eksikse → ikisi birden (yaygın kurulum: RAG ile bilgi, fine-tuning ile
  biçim)

Pratikte önerilen sıra: önce istem mühendisliği dene, yetmezse RAG ekle, yine
yetmezse fine-tuning'e geç. Çünkü maliyet ve karmaşıklık bu sırayla artıyor.

---

## 2. Yapay Zeka Ajanları (AI Agents)

### Soru-cevap sistemi ile ajan arasındaki fark

**Soru-cevap (reaktif) sistem:** Girdi gelir, model cevap üretir, biter. Tek yönlü ve
tek adımlı. Modelin dış dünyaya erişimi yok, sadece eğitim verisinden ve verilen
bağlamdan bildiğini söyler.

**Ajan:** Model bir **döngünün** içinde çalışır. Hedefi alır, ne yapması gerektiğine
kendi karar verir, araç (tool) çağırır, sonucu görür, gerekirse tekrar dener, hedefe
ulaştığına kanaat getirince durur.

Aradaki fark tek kelimeyle **karar**. Reaktif sistemde akışı geliştirici belirler,
ajanda modelin kendisi.

### Ajanın bileşenleri

1. **Akıl yürütme döngüsü:** Düşün → araç seç → çağır → sonucu değerlendir → tekrar
   veya bitir. En bilinen kalıbı ReAct (Reasoning + Acting).
2. **Araçlar (tools):** Modelin dış dünyayla temas noktası. Web araması, veritabanı
   sorgusu, kod çalıştırma, dosya okuma, API çağrısı. Modele araçların ne işe
   yaradığı tarif edilir, model hangisini ne zaman çağıracağına kendi karar verir.
3. **Bellek:** Kısa vadeli (o anki konuşma) ve uzun vadeli (kalıcı depo, genellikle
   vektör veritabanı).
4. **Planlama:** Büyük hedefi alt adımlara bölme.

### Reaktif ajandan otonom ajana geçiş

Araştırırken bunun keskin bir sınır değil, bir **özerklik merdiveni** olduğunu gördüm:

| Seviye | Ne yapıyor | Kararı kim veriyor |
|---|---|---|
| 0 - Basit üretim | Soruya cevap üretir | Geliştirici (akış sabit) |
| 1 - Araçlı model | Tanımlı araçları çağırabilir | Model (hangi araç), geliştirici (sıra) |
| 2 - Yönlendirici (router) | Gelen isteği doğru akışa yönlendirir | Model (dallanma) |
| 3 - Döngülü ajan | Sonucu değerlendirip tekrar dener | Model (adım sayısı ve sıra) |
| 4 - Planlayan ajan | Hedefi kendi alt görevlere böler | Model (planın tamamı) |
| 5 - Çoklu ajan | Ajanlar birbirine görev dağıtır | Ajanlar arası |

Yukarı çıktıkça yetenek artıyor ama **öngörülebilirlik düşüyor**. Seviye 0'da ne
olacağını biliyorum, seviye 4'te modelin ne yapacağını önceden bilemiyorum.

### Riskler

- **Hata birikmesi:** Her adımda küçük bir hata olasılığı varsa, 10 adımlık bir
  zincirde toplam başarı olasılığı hızla düşüyor.
- **Sonsuz döngü:** Ajan aynı aracı tekrar tekrar çağırıp ilerleyemeyebiliyor. Adım
  sınırı koymak şart.
- **Maliyet öngörülemezliği:** Kaç model çağrısı yapılacağı baştan belli değil.
- **Geri alınamaz işlemler:** Araçlar dış dünyayı değiştiriyorsa (e-posta gönderme,
  kayıt silme) yanlış karar geri alınamıyor. Bu tür araçlarda insan onayı isteniyor.

Bu yüzden pratikte önerilen yaklaşım: **işi çözen en düşük özerklik seviyesini
seç.** Sabit bir akış yetiyorsa ajan kurma.

---

## 3. İstem Mühendisliği ile Bağlam Mühendisliği

Bu ikisi sık karıştırılıyor. Ayrımı şöyle anladım:

> **İstem mühendisliği modele ne söylediğinle, bağlam mühendisliği modelin
> penceresinde ne bulunduğuyla ilgilenir.**

### İstem Mühendisliği (Prompt Engineering)

Amaç: modelden istenen çıktıyı almak için talimatı doğru kurmak.

Başlıca teknikler:

- **Sıfır atışlı (zero-shot):** Sadece talimat. "Bu metni özetle."
- **Az atışlı (few-shot):** Talimatla birlikte birkaç örnek vermek. Model istenen
  biçimi örneklerden çıkarıyor. Biçim tutturmada çok etkili.
- **Düşünce zinciri (chain-of-thought):** Modelden adım adım düşünmesini istemek.
  Aritmetik ve mantık sorularında doğruluğu belirgin artırıyor. Sebebi şu: model
  her token'ı üretirken sadece bir ileri geçiş yapıyor; ara adımları yazdırmak ona
  daha fazla hesaplama alanı veriyor.
- **Rol verme:** "Sen bir hukuk danışmanısın" gibi. Üslup ve terminolojiyi
  yönlendiriyor.
- **Çıktı biçimi dayatma:** JSON şeması vermek, kod bloğu istemek.
- **Kısıt koyma:** "Sadece verilen metne dayan", "bilmiyorsan bilmiyorum de". Gün
  20'de kuracağım halüsinasyon engeli tam olarak bu.

Sınırı: istem tek başına modelin bilmediği bir bilgiyi ona veremez.

### Bağlam Mühendisliği (Context Engineering)

Amaç: sınırlı bağlam penceresine **doğru bilgiyi, doğru miktarda, doğru sırada**
yerleştirmek.

Bağlam penceresi modelin bir seferde işleyebildiği maksimum token sayısı. Pencereler
büyüdü ama sorun bitmedi, çünkü:

- **Maliyet:** Her token para ve gecikme demek.
- **"Ortada kaybolma" (lost in the middle):** Model bağlamın başındaki ve sonundaki
  bilgiye, ortasındakinden daha çok dikkat ediyor. Uzun bağlamın ortasına gömülen
  kritik bilgi gözden kaçabiliyor.
- **Dikkat dağılması:** Alakasız bilgi eklemek doğruluğu düşürüyor. Daha çok bağlam
  her zaman daha iyi değil.

Başlıca teknikler:

- **Getirme (retrieval):** Her şeyi değil, soruyla alakalı parçaları koymak. RAG'in
  kendisi bir bağlam mühendisliği tekniği.
- **Sıkıştırma:** Getirilen parçaları özetleyip kısaltmak.
- **Yeniden sıralama (re-ranking):** En alakalı parçayı en görünür konuma koymak.
- **Konuşma özetleme:** Uzayan sohbetlerde eski turları özete indirgemek.
- **Bölümleme:** Sistem talimatı, belgeler, konuşma geçmişi ve soruyu ayrı ve
  etiketli tutmak.

### Karşılaştırma

| Konu | İstem Mühendisliği | Bağlam Mühendisliği |
|---|---|---|
| Soru | Modelden ne istiyorum, nasıl söylüyorum | Modele hangi bilgi girsin |
| Odak | Talimatın ifadesi | Pencerenin içeriği ve yönetimi |
| Ölçek | Tek istek | Oturum, belge kümesi, sistem geneli |
| Tipik sorun | Model formatı tutturamıyor | Model doğru bilgiyi görmüyor / bağlam taşıyor |
| Araçlar | Örnekler, roller, kısıtlar | Getirme, sıkıştırma, sıralama, özetleme |
| Maliyet etkisi | Az | Doğrudan ve büyük |

İkisi rakip değil, katman. Bağlam mühendisliği malzemeyi hazırlıyor, istem
mühendisliği o malzemeyle ne yapılacağını söylüyor. RAG hattında ikisi de var:
parçaları seçmek bağlam mühendisliği, "sadece bu parçalara dayanarak cevap ver"
demek istem mühendisliği.

---

## Sonuç

Bu bölümde hazır bir modeli kendi işime uydurmanın üç yolunu öğrendim ve bunların
birbirinin alternatifi değil, farklı problemlerin cevabı olduğunu gördüm.

Fine-tuning modelin **davranışını** değiştiriyor; biçim, üslup ve dar görev
uzmanlaşmasında güçlü, ama sık değişen olgusal bilgi için yanlış araç. LoRA ve QLoRA
sayesinde maliyeti eskisi kadar caydırıcı değil.

Ajanlar, modeli tek atışlık cevap üreticisinden karar veren bir döngüye taşıyor.
Özerkliğin bir merdiven olduğunu ve yukarı çıktıkça öngörülebilirliğin düştüğünü
öğrendim; doğru yaklaşımın "işi çözen en düşük seviyeyi seçmek" olduğunu not ettim.

İstem ve bağlam mühendisliği ayrımı ise bana en çok şunu kazandırdı: modelin yanlış
cevap vermesinin iki farklı sebebi olabiliyor. Ya doğru bilgiyi görmüyordur (bağlam
problemi) ya da gördüğü bilgiyle ne yapacağını anlamamıştır (istem problemi). Bu
ikisini ayırt etmek, hatayı nerede arayacağımı belirliyor.

Üç konu da bir sonraki bölüme çıkıyor: RAG hem bir bağlam mühendisliği tekniği, hem
fine-tuning'in alternatifi, hem de ajanların en sık kullandığı araç.
