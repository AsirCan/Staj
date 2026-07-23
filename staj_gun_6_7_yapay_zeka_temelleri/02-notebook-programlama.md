# Hücre / Notebook Tabanlı Programlama

## 1. Notebook nedir? (En basit anlatım)

Klasik programlamada bir `.py` dosyası yazarsın, çalıştırırsın, en son çıktı gelir. Ortada bir şey kırılırsa baştan çalıştırırsın.

**Notebook** ise dosyayı **hücrelere** böler. Her hücre kendi başına çalışan küçük bir kod bloğu. Bir hücreyi çalıştırırsın, çıktısı hemen altında görünür. Diğer hücreye geçersin, oradan devam edersin. Değişkenler hafızada kalır.

Yani bir Python **oturumu** var, sen ona hücre hücre kod yediriyorsun. Klasik betikten farkı: **her adımı ayrı ayrı görme ve değiştirme özgürlüğü**.

### Bir hücre neye benziyor?

```python
# Hücre 1
import pandas as pd
df = pd.read_csv("veri.csv")
df.head()
```

Bu hücreyi çalıştırınca `df.head()` çıktısı (tablo) hemen altında görünür. Sonra:

```python
# Hücre 2
df["yas"].mean()
```

Bunu çalıştırınca yaşın ortalamasını verir. `df` tekrar okunmadı, hafızada duruyor.

---

## 2. Nerede çalışıyoruz? (Ortamlar)

### 2.1 Jupyter Notebook / JupyterLab

Klasik. Yerel bilgisayarında pip ile kurup tarayıcıdan açıyorsun.
- **Jupyter Notebook**: eski, daha sade arayüz.
- **JupyterLab**: yeni, IDE'ye daha yakın. Sekme, dosya gezgini, terminal içeride.
- Dosya uzantısı `.ipynb` (JSON formatında — hücreler ve çıktılar birlikte saklanıyor).

### 2.2 Google Colab

Bulutta Jupyter. Google hesabıyla açıyorsun, kurulum yok. En büyük avantajı **ücretsiz GPU / TPU** (belirli limitle).
- ML/DL eğitmek için mükemmel.
- Notebook'ları Drive'a kaydediyor, paylaşmak kolay.
- Uzun süre kullanmazsan runtime kapanıyor, o yüzden uzun eğitim işleri için Colab Pro (ücretli) daha uygun.

### 2.3 Kaggle Notebooks

Kaggle sitesinin kendi notebook ortamı. Colab'a çok benziyor.
- Yarışmalar için birebir.
- Veri setleri hazır olarak takılı.
- Ücretsiz GPU var.

### 2.4 VS Code / Cursor / Antigravity içindeki Notebook desteği

Modern IDE'lerin çoğunda `.ipynb` desteği var. Sağda değişken izleyici, aşağıda çıktı — Jupyter deneyimini IDE içinde veriyor. Avantajı, aynı ekranda `.py` dosyalarıyla birlikte çalışabilmek.

### 2.5 "Interactive Window" (VS Code'da `# %%`)

Bir de düz `.py` dosyasında `# %%` yorumuyla hücre işaretlemek var. Böylece dosya `.py` kalıyor (git'e temiz düşüyor) ama VS Code hücre hücre çalıştırabiliyor. Küçük deneyler için pratik bir yol.

---

## 3. Neden bu kadar sevilir? (Avantajlar)

### 3.1 Adım adım çalıştırma (incremental execution)

Notebook'un en büyük özelliklerinden biri bu. Bir veri işleme betiğinde 10 adım varsa, klasik yolda hepsini baştan koşarsın. Notebook'ta:
1. Veriyi okursun (hücre 1) — 30 saniye sürer.
2. Temizleme hücrelerini deneyip deneyip değiştirirsin. **Veriyi tekrar okumazsın**, sadece o hücreyi tekrar koşarsın.
3. Model kısmına gelince, veri hâlâ hazır.

Özellikle **büyük veri yüklemesi** veya **uzun süren hesap** olduğunda inanılmaz zaman kazandırıyor.

### 3.2 Kod + çıktı + metin bir arada

Bir hücrede kodu yazarsın, altında çıktısı (tablo, grafik, sayı) durur. Aralara **Markdown hücreleri** koyarak açıklama yazarsın:

```markdown
## Veri Keşfi
Aşağıda yaş kolonunun dağılımına bakıyoruz.
```

Böylece dosya hem kod hem rapor oluyor. Ders anlatmak, sonuç sunmak, kendine not almak için mükemmel.

### 3.3 Grafik ve görselleştirme direkt gömülü

Matplotlib ile grafik çizince direkt hücrenin altında görünür. Pandas tabloları güzel render ediliyor. Resim çıktısı gömülü. Bir sürü ML kütüphanesi (scikit-learn, TensorBoard, Plotly) notebook'ta özel widget'lar sunuyor.

### 3.4 Deneme-yanılma kolaylığı

ML çalışmasının doğası buymuş: bir hiperparametre değiştir, dene, bak. Notebook bu döngüye uygun. Model eğitildikten sonra farklı analiz hücreleri koşup sonucu incelersin, tekrar eğitmen gerekmez.

### 3.5 Magic komutlar

Jupyter'a özel `%` ve `%%` başlangıçlı komutlar var, çok işe yarıyor:

```python
%timeit sum(range(1000000))     # Bir satırın hızını ölçer
%%time                           # Bütün hücrenin süresini verir
%matplotlib inline               # Grafiklerin hücre içinde çıkmasını sağlar
%load_ext autoreload             # Değişen modülleri otomatik yeniden yükler
%autoreload 2
!pip install pandas              # ! ile shell komutu çalıştırılır
!ls
```

Özellikle `%timeit` ve `%%time` performans ölçmek için, `%autoreload` da dışarıda değiştirdiğin `.py` dosyalarının notebook'a otomatik yansıması için hayat kurtarıyor.

---

## 4. Ne zaman **kullanmamalı**? (Dezavantajlar)

Notebook her şeye uygun değil. Aksine bazı yerlerde tam olarak yanlış araç.

### 4.1 Prodüksiyona kod yazarken

Bir web servisi, arka plan işi, ya da uzun ömürlü uygulama yazacaksan, notebook değil klasik `.py` (veya paket yapısı) tercih edilir.
- Test yazmak zor.
- Sürüm kontrolü (git diff) zor — çünkü `.ipynb` altındaki JSON'da çıktılar da var, satır satır diff okunmuyor.
- Kod tekrar kullanılabilirliği düşük — hücrelerdeki her şey global scope'ta.
- Import yapıları dağınık.

### 4.2 Uzun otomasyon işleri

Cron ile her gece çalışacak bir iş için notebook kullanılmaz. `.py` betik + zamanlama daha temiz.

### 4.3 Ekip çalışmasında büyük projeler

Aynı notebook üstünde birden fazla kişi çalışması zor (çakışma, çıktı farkları). Ekip projelerinde notebook genelde "keşif ve rapor" için, asıl kod için `.py` modülleri kullanılır.

### 4.4 Sıra bağımlılığı (silent state)

En sinsi problem bu. Diyelim ki notebook'ta 20 hücre var. Sırayla çalıştırdın, sonuç güzel. Sonra 5. hücreyi silmeyi unuttun ama tanımladığı değişken hâlâ hafızada. Notebook'u tekrar açıp baştan çalıştırdığında hata veriyor, çünkü o değişken yok.

Buna **"hidden state"** problemi deniyor. Çözüm: bitince mutlaka **"Restart & Run All"** ile baştan koşarak dosyanın gerçekten tutarlı olduğunu doğrulamak.

---

## 5. Ne zaman **kullanmalı**? (Uygun alanlar)

Yukarıdakinin tersi hepsi:

- **Exploratory Data Analysis (EDA)** — veriyi ilk kez görüyorsun, dağılımına bakıyorsun, kolonları anlıyorsun.
- **Veri temizleme prototipleme** — aynı veriyi 20 farklı transform ile deniyorsun.
- **Model prototipleme** — küçük bir model eğit, sonuca bak, hiperparametre değiştir.
- **Eğitim / öğrenme materyali** — PyTorch Blitz gibi kod + açıklama iç içe olan öğreticiler.
- **Sonuç raporlama** — paydaşlara sunulacak analiz (grafiği, açıklaması, kodu bir arada).
- **Araştırma makalesi kodu** — çoğu ML paper'ının reproduce kodu notebook olarak paylaşılıyor.
- **Bir API'yi keşfetme** — yeni bir kütüphaneyi öğrenirken hücre hücre denemek çok hızlı.

### Genel kural

> **Not defterinde keşfet, `.py` dosyasında ürün yap.**

Notebook'ta bir şey oturduysa, kodu `.py` dosyasına taşıyıp fonksiyona sar. Notebook'u da rapor / demo dosyası olarak sakla.

---

## 6. Küçük bir örnek akış

Diyelim ki bir CSV üzerinde EDA yapılıyor. Sırayla:

```python
# Hücre 1 — kütüphaneler
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# Hücre 2 — veri
df = pd.read_csv("musteriler.csv")
df.shape

# Hücre 3 — ilk bakış
df.head()

# Hücre 4 — istatistiksel özet
df.describe()

# Hücre 5 — eksik değerler
df.isna().sum()

# Hücre 6 — yaş dağılımı
df["yas"].hist(bins=30)
plt.title("Yaş Dağılımı")
plt.show()

# Hücre 7 — kategori sayımı
df["sehir"].value_counts().head(10)
```

Her hücre tek bir iş yapıyor, çıktısı görülüp bir sonrakine karar veriliyor. Bir hata çıkarsa sadece o hücre düzeltiliyor.

**Aynı iş `.py` betiğinde yapılsa** her seferinde tüm verinin baştan okunması, tüm hesabın baştan yapılması gerekirdi. Küçük veride problem değil ama 5 GB CSV'de zaman öldürücü.

---

## 7. Notebook + Git — küçük bir püf noktası

`.ipynb` dosyaları çıktıları da içerdiği için Git diff'i berbat oluyor. Ekipte çalışılıyorsa şunları öneriyorlar:

- **Commit öncesi çıktıları temizleme.** Jupyter'da "Kernel → Restart & Clear Output" sonrası commit.
- **`nbstripout`** aracı: git hook olarak takılıp otomatik çıktı temizliyor.
- **`jupytext`**: notebook'u aynı anda `.py` olarak da tutan bir araç. Git'e `.py` gidiyor, notebook otomatik senkron.

Küçük kişisel projelerde bu adımlar atlanabilir ama takım projesinde şart.

---

## 8. AI / ML dünyasındaki yeri

Notebook'un özellikle ML projelerinde neden bu kadar sık kullanıldığı şöyle özetlenebilir:

1. **Veri her seferinde yüklenmiyor.** Büyük veri setlerini bir kere yükleyip üstünde çalışmak.
2. **Deneme-yanılma yoğun.** Hiperparametreyi değiştir, tek hücreyi tekrar koş, sonucu gör.
3. **Görselleştirme kritik.** Loss eğrisi, confusion matrix, veri dağılımı — hepsi gömülü olarak akıyor.
4. **Ekosistem uyumlu.** pandas, numpy, matplotlib, scikit-learn, PyTorch, TensorFlow, Hugging Face — hepsinin dokümantasyonu notebook örnekleriyle dolu.
5. **Colab / Kaggle GPU'ları.** Kendi bilgisayarında GPU yoksa bile bulutta ücretsiz GPU üstünde model eğitebiliyorsun.

Kısacası **notebook, AI dünyasının "laboratuvarı"**. Deney yapılan yer.

---

## 9. Sonraki başlıkla bağlantı

Bir sonraki konu: **ML temelleri** (`03-ml-temelleri.md`).

Bağlantısı basit: ML temellerindeki eğitim döngüsünü (veri → model → tahmin → loss → güncelleme) küçük ölçekte adım adım görmek için notebook en uygun ortam. Yani "teori orada, deney burada" ilişkisi var.

---

**Durum:** Tamamlandı. Bir sonraki dosya: `03-ml-temelleri.md`.
