# NLP'ye Giriş: Token ve Embedding

## NLP Nedir?

NLP (Natural Language Processing / Doğal Dil İşleme), bilgisayarın insan dilini işleyebilmesi için geliştirilmiş yöntemler bütünüdür. Ama bu tanım yeterince şey söylemiyor. Daha somut bir tanım:

> **NLP, dil üzerinden verilen bir görevi bilgisayara yaptırmak için gereken tüm tekniklerdir.**

Görevlerin bazıları şunlar:

- Metni sınıflandırma (spam mı değil mi, hangi konudan bahsediyor)
- Metin özetleme
- İki dil arasında çeviri
- Sorulan soruya cevap üretme
- Bir cümlenin duygu tonunu bulma (positive / negative / neutral)
- Metnin içindeki isim, yer, tarih gibi varlıkları çıkarma (NER — Named Entity Recognition)
- **Bir sonraki kelimeyi tahmin etmek** — bu görev şu an tüm modern LLM'lerin kalbi

Son madde çok önemli çünkü ChatGPT, Claude, Gemini gibi sistemler aslında yalnızca "bir sonraki tokeni tahmin etmek" üzerine eğitilmişler. Sohbet edebilmeleri, kod yazabilmeleri, matematik problemi çözebilmeleri hep bu tek görevin tekrar tekrar uygulanmasından çıkıyor. Bir yerde okumuştum: "yeterince iyi bir 'sonraki kelime tahmini' modeli, aslında dünyayı anlamak zorundadır." Şu an bunun ne demek olduğunu daha iyi kavrıyorum.

---

## Klasik NLP ile Modern NLP Arasındaki Fark

Bu iki dönem arasındaki fark önemli. Aynı problemi çözmenin iki tamamen farklı yolu var.

### Klasik NLP (yaklaşık 2010'lardan önce)

Yaklaşım büyük ölçüde **kural tabanlı** ve **istatistiksel özellik çıkarımına dayalı**. Örnekler:

- **Bag-of-Words (BoW):** Cümledeki kelimeleri say, sırayı umursama. "Kedi köpeği kovaladı" ve "köpek kediyi kovaladı" bu yöntemde neredeyse aynı vektör olurdu.
- **TF-IDF:** BoW'un geliştirilmiş hali. Bir belgede geçen kelimenin, tüm koleksiyonda ne kadar seyrek olduğunu da hesaba katıyor. Arama motorlarının klasik alt yapısı.
- **n-gram modelleri:** "Şu 3 kelime yan yana geliyor mu?" gibi kısa örüntüleri sayıp bir sonraki kelimenin olasılığını tahmin ediyor. Cep telefonlarındaki eski otomatik tamamlama böyle çalışıyordu.
- **POS tagging, dependency parsing:** Cümlenin gramerini elle programlanmış kurallarla analiz etme.

Bu yaklaşımların avantajı: hızlı, açıklanabilir, az veri yeter. Dezavantajı: her dil için ayrı ayrı özellik mühendisliği (feature engineering) yapman lazım ve **anlamı** yakalayamıyorlar. "Doktor" ile "hekim" iki farklı stringtir, aralarında sıfır ilişki görürler.

### Modern NLP (2018 sonrası)

Yaklaşım: **yeterince büyük bir sinir ağını, yeterince fazla veriyle, uygun bir hedefle eğit; gerisini o çözer.**

- Kelimeleri stringlerle değil, **öğrenilmiş vektör temsilleriyle** (embedding) ifade et.
- Sırayı, bağlamı, hatta uzun mesafedeki bağımlılıkları modelin kendisinin keşfetmesine izin ver.
- Grammer kurallarını, sözlükleri, dilbilim uzmanlığını dışarıdan verme — model bunları verinin içinden çıkarsın.

Bu ikinci yaklaşımın çıkardığı sonuçlar bir önceki neslin çok üstünde. Tek model 100'den fazla dili öğrenebiliyor, hiç görmediği bir görevi (few-shot / zero-shot) yapabiliyor.

### Karşılaştırma

| Özellik | Klasik NLP | Modern NLP |
|---------|-----------|------------|
| Yaklaşım | Kural + istatistik | Uçtan uca sinir ağı |
| Kelime temsili | Bag-of-Words, TF-IDF, n-gram sayaçları | Öğrenilmiş embedding vektörleri |
| Bağlam kavrayışı | Sınırlı (n-gram penceresi) | Uzun (attention mekanizması) |
| Grammer bilgisi | Elle çıkarılan özellikler | Model kendi keşfediyor |
| Genelleme | Zayıf, dile özgü | Güçlü, çok dilli |
| Veri ihtiyacı | Az veri yeter | Milyarlarca cümle şart |
| Hesap ihtiyacı | Düşük | Çok yüksek (GPU zorunlu) |
| Yorumlanabilirlik | Yüksek (kural okunabilir) | Düşük (kara kutu) |

**Ortak yönleri:** İkisi de sonuçta metnin dağılımını modelleyerek çalışıyor. Klasik NLP açıkça olasılık dağılımı sayıyor, modern NLP bu dağılımı sinir ağının parametrelerinde saklıyor. Yani felsefe aynı: "dilde hangi örüntü daha olası" sorusuna cevap üretmek. Sadece bu cevabı üretme yolları birbirinden çok farklı.

---

## Token Nedir?

Model harflerle mi çalışsın, kelimelerle mi? İki uçtaki cevap da probleme yol açıyor. Modern NLP bunun için üçüncü bir yol geliştirdi: **token**.

**Token = modelin girdi olarak gördüğü en küçük anlamlı metin parçası.**

Üç ana yaklaşım var. Karar vermeden önce üçünün de artılarını, eksilerini görmek lazım.

### 1) Karakter Tabanlı Tokenizasyon

Her karakter bir token. "merhaba" → `['m', 'e', 'r', 'h', 'a', 'b', 'a']` yani 7 token.

- **Artı:** Kelime dağarcığı (vocabulary) çok küçük. Türkçe için sadece ~30 karakter yeter. Yeni kelime görsen bile sorun olmuyor, hepsi zaten mevcut karakterlerden oluşuyor (OOV — Out of Vocabulary — problemi yok).
- **Eksi:** Dizi uzunluğu çok fazla oluyor. 20 kelimelik bir cümle 150+ token olabiliyor. Modelin dikkatinin çok bölünmesi ve "merhaba" kelimesinin tek bir kavram olduğunu her seferinde sıfırdan öğrenmek zorunda kalması demek bu.

Sonuç: Genelde yaygın kullanılmıyor. Bazı özel görevlerde (ör. dil tanımlama, yazım hatası düzeltme) hâlâ tercih edilir.

### 2) Kelime Tabanlı Tokenizasyon

Boşluklardan böl. "Bugün hava güzel" → `['Bugün', 'hava', 'güzel']`.

- **Artı:** Dizi kısa, insan sezgisine yakın.
- **Eksi:** İki büyük dert var:
  1. **Kelime dağarcığı patlar.** Türkçe gibi çekimli dillerde her fiilin onlarca çekim biçimi var: "gel", "geldi", "geliyorum", "gelmeliyim", "gelemeyeceğimi"... Her biri ayrı bir token olarak tutulmak zorunda. Türkçe için 500K+ farklı token gerekir. Bellek katliamı.
  2. **OOV problemi.** Model eğitim sırasında hiç görmediği bir kelimeyle karşılaştığında bunu ya `[UNK]` (unknown) sabit tokeniyle temsil eder ya da hiç halledemez. Sözlük dışı isimler, teknik terimler, argo — hepsi çuvallar.

### 3) Subword (Alt-Kelime) Tabanlı Tokenizasyon — Modern LLM Standardı

Fikir: **sık geçen bütün kelimeleri bütün tut, nadir olanları parçala.** Yani ideal orta yol.

Örnek: "unbelievable" → `['un', 'believ', 'able']`. "un-" ve "-able" ekleri o kadar sık geçiyor ki ayrı token olarak öğrenilmesi mantıklı.

Türkçe örnek: "yapabileceklerimiz" → `['yap', 'abilecek', 'lerimiz']` gibi bir bölünme olabilir. Kesin bölünme kullanılan tokenizer'a göre değişir.

Bu yaklaşımın üç popüler algoritması var:

- **BPE (Byte Pair Encoding):** GPT ailesinin kullandığı. En sık geçen bitişik karakter çiftini birleştirerek dağarcık oluşturuyor. İteratif olarak çalışıyor.
- **WordPiece:** BERT'in kullandığı. BPE'ye çok benzer ama birleştirme kriteri farklı (olabilirlik tabanlı).
- **SentencePiece:** Llama, T5 ve daha birçok modelin kullandığı. Dilden bağımsız çalışıyor, boşluğu bile bir karakter gibi işliyor. Bu Çince, Japonca gibi boşluksuz dillerde ayrıca faydalı.

**Neden subword bu kadar iyi?**

- **OOV yok.** En kötü durumda karakter seviyesine iner, hep bir çözüm bulur.
- **Sık kelimeler tek parça.** "Merhaba", "the", "and" gibi kelimeler zaten tek token, verimli.
- **Dağarcık makul.** 30.000-100.000 token yeter, milyonlarca değil.
- **Yeni kelimeleri makul parçalayabilir.** Hiç görmediği "quantumdynamics" kelimesini "quantum" + "dynamics" olarak bölmesi mantıklı.

### Kendi Denemem — tiktoken ile Türkçe

`tiktoken` kütüphanesiyle GPT'nin tokenizer'ını test ettim:

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")   # GPT-4'ün tokenizer'ı

metin = "Merhaba dünya, nasılsın?"
tokenler = enc.encode(metin)
print(tokenler)
# → [65947, 27070, 90154, 11, 92610, 21636, 91201, 30] gibi 8 token

for t in tokenler:
    print(enc.decode([t]))
# → "Mer", "haba", " dünya", ",", " nas", "ıls", "ın", "?"
```

"Merhaba" kelimesi bile 2 parçaya bölündü ("Mer" + "haba"). Çünkü GPT'nin dağarcığı ağırlıklı olarak İngilizce üzerine eğitilmiş, Türkçe için verimli parçalanmalar öğrenmemiş. Aynı cümlenin İngilizcesi "Hello world, how are you?" muhtemelen 5-6 tokendır.

**Sonuç:** Türkçe metin, aynı anlamlı İngilizce metinden yaklaşık %30-50 daha fazla token üretiyor. Bu bir API kullanılırken doğrudan maliyete yansıyor (OpenAI, Anthropic vs. token başına fiyatlandırıyor).

**Genel kural:** İngilizcede 1 token ≈ 4 karakter ≈ 0.75 kelime. Türkçede bu oran daha kötü.

---

## Embedding Nedir?

Tokenizer bize bir tam sayı ID verdi (mesela `65947` = "Mer"). Ama bu sayının kendisi bir anlam taşımıyor. `65947 - 65946 = 1` diye "bu ikisi birbirine bir birim yakın kelimeler" diyemeyiz. Token ID'ler sadece etiket — anlam katmanına henüz geçmedik.

**Embedding = her token ID'sini `d` boyutlu, öğrenilebilir bir vektöre çevirmek.**

Formal olarak `nn.Embedding(vocab_size, d_model)` katmanı sadece bir tablodur: `V × d` boyutlu bir matris. Bir token ID geldiğinde o satırı çekiyor. Bu kadar basit bir "lookup" işlemi. Ama iki büyük sihiri var:

1. Bu tablo **eğitim sırasında güncelleniyor.** Model her cümleyi tahmin etmeye çalıştıkça embedding'lerini "daha iyi" yönde ayarlıyor.
2. Bu vektörler, eğitim bittiğinde, **kelimelerin anlamlarını yakınlık ilişkileriyle kodluyor.**

### Meşhur Örnek: Vektör Aritmetiği

Word2Vec (2013) makalesinden çıkan bu örnek hâlâ etkileyici:

```
vec("kral") - vec("erkek") + vec("kadın") ≈ vec("kraliçe")
```

Bu, model kelimeleri sadece etiket olarak değil, **anlamlı boyutları olan bir uzayda** temsil ediyor demek. Bir eksen "cinsiyet" gibi bir kavramı, başka bir eksen "hükümdarlık" gibi bir kavramı kodluyor olabiliyor. Kimse modele "kral bir hükümdardır" demedi; model bunu milyonlarca cümleye bakarak istatistiksel olarak buldu.

Benzer örnekler:

```
vec("Paris") - vec("Fransa") + vec("Türkiye") ≈ vec("Ankara")
vec("koştu") - vec("koşmak") + vec("yürümek") ≈ vec("yürüdü")
```

Bu bir sihir gibi görünse de aslında istatistiksel bir sonuç: aynı bağlamlarda geçen kelimeler benzer vektörlere sahip olacak şekilde eğitiliyorlar (dağılımsal varsayım — "kelimeyi arkadaşlarından tanı").

### Cosine Similarity — İki Vektör Ne Kadar Yakın?

İki vektörün ne kadar benzer olduğunu ölçmek için genellikle **cosine similarity** kullanılır:

```
cos(θ) = (A · B) / (||A|| · ||B||)
```

Sonuç [-1, 1] arasında bir sayı:
- **+1** → aynı yön, tam benzer
- **0** → dik açı, ilgisiz
- **-1** → tam ters yönlü, zıt anlamlı

Örnek beklenti (önceden eğitilmiş bir modelde):

```
cos(vec("doktor"), vec("hekim"))     ≈ 0.85   (eş anlamlı)
cos(vec("doktor"), vec("hastane"))   ≈ 0.60   (ilgili ama farklı)
cos(vec("doktor"), vec("muz"))       ≈ 0.05   (alakasız)
```

### Statik vs Kontekstüel Embedding

Klasik Word2Vec, GloVe gibi yöntemlerde her kelimenin **tek bir sabit** embedding'i var. Yani "bank" kelimesi hem "para koyulan bank" (banka) hem "nehir kenarı" için aynı vektöre sahip. Bu, aynı yazımlı iki farklı anlamı ayırt edememek demek.

Transformer mimarisi bunu köklü şekilde değiştirdi. Artık her kelimenin embedding'i **içinde bulunduğu cümleye göre değişiyor**. Bu **kontekstüel embedding** deniyor. Aynı "bank" kelimesi:

- "I deposited money in the bank" → bir vektör (finans anlamı)
- "We sat by the river bank" → başka bir vektör (nehir kenarı anlamı)

Bu değişiklik büyük bir sıçrama. Attention mekanizması sayesinde kelime her cümleye özel bir temsil kazanıyor.

### Embedding'in Boyutu Ne Olmalı?

Modele göre değişir ama tipik değerler:

- Küçük modeller: `d = 128`, `d = 256`
- Orta modeller: `d = 512`, `d = 768` (BERT-base için 768)
- Büyük modeller: `d = 1024`, `d = 2048`
- Çok büyük LLM'ler: `d = 4096`, `d = 8192`, `d = 12288` (GPT-3'ün 12288'i)

Daha büyük embedding, daha çok anlam kapasitesi ama daha çok bellek ve hesap. Praktikte problem karmaşıklığına göre denenerek seçiliyor.

---

## Tüm Boru Hattı

Bu iki kavramı (token + embedding) modelin giriş kapısı olarak düşünüyorum:

```
ham metin: "Merhaba dünya"
    ↓  tokenize (BPE / WordPiece / SentencePiece)
token ID'leri: [65947, 27070, 90154]
    ↓  embedding lookup
vektörler: 3 tane d-boyutlu vektör (öğrenilmiş anlam)
    ↓  positional encoding eklenir (pozisyon bilgisi)
    ↓  N tane Transformer bloğu
kontekstüel vektörler
    ↓  çıktı katmanı + softmax
sonraki token için olasılık dağılımı
```

Yani ham metnin "sayı" haline gelmesi ve modelin "anlam çıkarımı" yapabilir hale gelmesi bu iki adımla başlıyor. Bunlar olmadan ne kadar güçlü bir Transformer inşa edersen et, model bir şey öğrenemez — çünkü onun konuşabildiği tek dil vektörlerin dili.

Embedding'ler eğitim sonucunda öyle iyi yerlere yerleşiyor ki, hatta modelin sınıflandırıcı çıkışı olmadan bile embedding'leri kullanarak arama, benzer belge bulma, öneri sistemi gibi işler yapılabiliyor. Modern **RAG (Retrieval-Augmented Generation)** sistemleri de tam olarak bu prensibi kullanıyor: sorguyu embed et, en yakın belgeleri getir, sonra bunları LLM'e ver.
