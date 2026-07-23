# PyTorch vs. TensorFlow ve Diğer Framework'ler

## 1. Önce terimleri ayıralım: Framework, Library, SDK

Karıştırılan bu üç kavramı çok net ayırayım.

- **Library (Kütüphane)**: hazır fonksiyonlar topluluğu. Sen çağırırsın, o yapar. Kontrol sende. Örnek: NumPy, requests, pandas.
- **Framework**: iskeleti hazır bir yapı. Sen boşlukları doldurursun. Kontrol onda ("**Inversion of Control**"). Örnek: Django, PyTorch, TensorFlow.
- **SDK (Software Development Kit)**: bir platformda geliştirme yapmak için verilen paket. İçinde kütüphane, framework, örnek kod, doküman olabilir. Örnek: Android SDK, OpenAI SDK, Anthropic SDK.

PyTorch ve TensorFlow ikisi de framework — model eğitmenin akışını (autograd, optimizer, veri yükleyici) tanımlıyorlar, sen ağın yapısını içine yazıyorsun.

---

## 2. PyTorch

Meta (eski Facebook) tarafından çıkarıldı, şu anda Linux Foundation altında. Python öncelikli.

### 2.1 Öne çıkan özellikler

- **Dynamic Computational Graph (define-by-run)**: hesap grafiği kod çalışırken oluşur. Yani Python'da bir `if` yazarsan model her batch'te farklı yol izleyebilir. Debug'ı çok kolaylaştırıyor.
- **Pythonic**: gerçekten Python gibi hissediyor. NumPy bilenler için öğrenmesi çok kolay.
- **Otomatik türev (`autograd`)**: `.backward()` çağırınca gradyanlar otomatik hesaplanıyor.
- **Ekosistem**:
  - `torchvision` — görüntü işleme.
  - `torchaudio` — ses.
  - `torchtext` — metin (artık daha az güncelleniyor, HF baskın oldu).
  - `PyTorch Lightning` — training boilerplate'i azaltıyor.
  - **Hugging Face `transformers`** — pratikte PyTorch üstünde çalışıyor.
- **Deployment**: TorchScript, ONNX export, TorchServe.

### 2.2 Kime uygun?

- **Akademik araştırma**: yayınların büyük çoğunluğu PyTorch. Yeni bir paper okuduysanız, kodu %90 ihtimalle PyTorch'ta.
- **LLM eğitimi ve fine-tuning**: Hugging Face ekosistemi PyTorch üstünde.
- **Prototipleme ve hızlı deneme**.

### 2.3 Zayıf tarafları

- Mobil deployment TF'e göre daha az olgun (PyTorch Mobile var ama TFLite kadar yaygın değil).
- JavaScript / tarayıcı desteği daha zayıf (TF.js var).

---

## 3. TensorFlow

Google tarafından çıkarıldı. Uzun zaman DL'in tek büyük framework'üydü.

### 3.1 Öne çıkan özellikler

- **Static Computational Graph** (klasik TF 1.x). TF 2.x'te "eager execution" default oldu, dinamik graph da destekleniyor. Ama halâ istersen `@tf.function` decorator'ıyla statik graph'a alıyorsun.
- **Keras** artık TF'in resmi high-level API'si. Model tanımı Keras üstünden çok kısa oluyor.
- **Ecosystem for production**:
  - **TensorFlow Lite (TFLite)**: mobil, IoT, edge cihaz için optimize edilmiş sürüm.
  - **TensorFlow.js**: tarayıcıda çalışır.
  - **TensorFlow Serving**: production'da model sunmak için sunucu.
  - **TensorFlow Extended (TFX)**: ML pipeline'ları için.
- **Distributed training** için olgun araçlar.

### 3.2 Kime uygun?

- **Production odaklı ekipler** (özellikle mobil / edge).
- **Büyük kurumsal projeler** (Google'ın altyapı desteği).
- **Halihazırda TF ile başlamış** ekipler (geçiş maliyeti yüksek).

### 3.3 Zayıf tarafları

- Araştırma dünyası PyTorch'a kaydı, güncel makale kodları TF'de nadiren geliyor.
- TF 1.x → 2.x geçişi topluluk üzerinde travma etkisi yarattı, API kararsız algısı.
- Öğrenme eğrisi PyTorch'a göre daha dik.

---

## 4. Diğer önemli araçlar

### 4.1 JAX (Google)

- NumPy tarzı bir API + otomatik türev + otomatik paralel derleme (XLA).
- Google Research'ün gözde aracı. Gemini gibi büyük modeller JAX ile eğitiliyor.
- **Fonksiyonel** stil (mutasyon yok). Öğrenmesi daha farklı bir düşünüş gerektiriyor.
- TPU üstünde performansı çok iyi.

### 4.2 scikit-learn

- Klasik ML'in standardı. Karar ağaçları, SVM, k-means, PCA, cross-validation.
- Deep learning yok. Ama yapısal veri (tablo) için hâlâ en pratik araç.
- `fit / predict / transform` API'sini bütün ML dünyasına o kabul ettirdi.

### 4.3 Hugging Face `transformers`

- Bir framework değil, PyTorch/TF/JAX üstünde çalışan bir **model kütüphanesi**.
- Binlerce hazır model (BERT, GPT-2, Llama, Whisper, Stable Diffusion vs.) tek API'yle.
- LLM fine-tuning, tokenization, generation için standart. Yanında `datasets`, `accelerate`, `peft`, `trl` gibi kardeş kütüphaneler.
- Bugün NLP / LLM işi yapan neredeyse herkes bunu kullanıyor.

### 4.4 ONNX

- Framework'ler arası **model formatı**. PyTorch'ta eğit, ONNX'e export et, sonra C++/Java/mobil ortamda çalıştır.
- Deployment esnekliği için.

### 4.5 Ollama, llama.cpp

- Framework değil, LLM inference (çalıştırma) araçları.
- Yerel bilgisayarda LLM koşturmak için pratik.
- Fine-tuning için değil, çalıştırma / servis için.

---

## 5. Karşılaştırma tablosu

| Kriter | PyTorch | TensorFlow | JAX | scikit-learn |
|---|---|---|---|---|
| Çıkaran | Meta / Linux Fnd. | Google | Google | Topluluk |
| Ana kullanım | Araştırma, LLM | Production, mobil | Araştırma (Google) | Klasik ML |
| Graph türü | Dinamik | Dinamik + statik seçeneği | Statik (jit ile) | — |
| Öğrenme eğrisi | Kolay | Orta-zor | Zor | Çok kolay |
| Ekosistem büyüklüğü | Çok büyük | Büyük | Orta | Büyük |
| Mobil / edge | Zayıf | Güçlü (TFLite) | Zayıf | — |
| Tarayıcı | Zayıf | TF.js var | Zayıf | — |
| LLM / Transformers | Standart (HF) | Kısıtlı | Sınırlı | — |
| Akademik makaleler | Çoğunluk | Azalıyor | Google odaklı | Klasik ML |
| Distributed training | İyi | Çok iyi | Çok iyi (TPU) | Yok |
| TPU desteği | Sınırlı (XLA ile) | Yerli | Yerli | Yok |
| GPU desteği | Çok iyi | Çok iyi | Çok iyi | Yok |

### 5.1 Kod stili farkı — küçük örnek

**PyTorch:**
```python
import torch.nn as nn
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)
```

**TensorFlow (Keras):**
```python
from tensorflow.keras import layers, Sequential
model = Sequential([
    layers.Dense(128, activation="relu"),
    layers.Dense(10)
])
```

**JAX (Flax):**
```python
import flax.linen as nn
class MLP(nn.Module):
    @nn.compact
    def __call__(self, x):
        x = nn.Dense(128)(x)
        x = nn.relu(x)
        return nn.Dense(10)(x)
```

Görüldüğü gibi çoğu kavram aynı, sadece isimler ve stil farkı.

---

## 6. Benchmark ve performans — genel gözlem

Not: kesin sayı vermek zor, versiyon ve donanıma göre değişiyor. Ama genel eğilimler:

- **GPU üstünde saf hız**: Aşağı yukarı eşit. Aralarındaki fark %5-15 civarı, model türüne göre birinin bazı yerlerde önde olduğu oluyor.
- **TPU üstünde**: JAX ve TensorFlow açık ara önde (Google'ın kendi donanımı).
- **CPU üstünde**: PyTorch genelde biraz daha hızlı.
- **Mobil / edge**: TFLite (ve ONNX) domine ediyor. PyTorch Mobile geride.
- **Distributed / multi-GPU**: TensorFlow'un `tf.distribute` ve JAX'ın paralel API'si daha olgun. PyTorch'un `torch.distributed` + `FSDP` da yetişti.

Sonuç: performans genelde farkı yaratmıyor. Ekosistem, ekip alışkanlığı, hedef platform daha belirleyici.

---

## 7. Hangi projede hangisi? (Kendi tercih tablom)

- **LLM fine-tuning / eğitimi** → **PyTorch + Hugging Face**. Alternatif yok pratikte.
- **Yeni bir araştırma paper'ını reproduce** → **PyTorch**. Yazarın kodu büyük ihtimalle PyTorch.
- **Mobil uygulamaya model gömme (Android/iOS)** → **TensorFlow Lite** (veya PyTorch → ONNX → mobile).
- **Tarayıcıda ML çalıştırma** → **TensorFlow.js** (veya ONNX Runtime Web).
- **Google TPU üstünde büyük ölçekli eğitim** → **JAX** (veya TF).
- **Klasik ML (tablo, feature engineering, XGBoost tarzı)** → **scikit-learn** + **XGBoost / LightGBM**. Deep learning gereksiz.
- **Prototipleme, öğrenme, deney** → **PyTorch** (dinamik graph debug'ı kolaylaştırıyor).
- **Kurumsal büyük production ML pipeline** → **TensorFlow + TFX**. Ekosistem olgun.

### 7.1 "Ne öğrenmeliyim ilk?"

Ben olsam: **PyTorch**. Sebepler:
- Araştırma dünyasında baskın → yeni gelişmeleri takip etmek kolay.
- Hugging Face bu framework üstünde → LLM işine hızlı girersin.
- Debug etmek çok daha rahat (Python'un normal `print`, `pdb`'si çalışıyor).
- TF'e sonradan geçmek gerekirse kavramlar aynı, isimler farklı — çabuk oluyor.

---

## 8. Genel Değerlendirme

Bu çalışma sürecinde **PyTorch** temel araç olarak tercih ediliyor. Sebepleri:
- Klasik giriş kaynağı olan 60-Minute Blitz PyTorch üstünde yazılmış.
- Modern AI gündemi LLM ekseninde (Transformer, HuggingFace) ve bu ekosistem PyTorch üzerine kurulu.
- Genel deneme-yanılma / öğrenme sürecinde daha az sürtünme.

TensorFlow'u tanımak faydalı ama zamanı olduğunda ikinci sırada.

Klasik ML lazım olursa (küçük tablo veriler için) `scikit-learn` yeter, ayrı bir framework öğrenmeye gerek yok.

---

## 9. Sonraki başlıkla bağlantı

Bir sonraki konu: **PyTorch 60-Minute Blitz** (`06-pytorch-60-min-blitz/`).

Burada teorik olarak öne çıkan araç pratikte deneniyor. Blitz'in dört bölümü:
1. Tensor'lar (PyTorch'un temel veri tipi).
2. Autograd (otomatik türev, backprop'un kod hali).
3. Neural network kurma (`nn.Module`).
4. Bir görüntü sınıflandırıcının uçtan uca eğitilmesi (CIFAR10).

Böylece yukarıda anlatılan her şey (forward, loss, backward, optimizer, epoch) gerçek koda dönüşüyor.

---

**Durum:** Tamamlandı. Bir sonraki dosya: `06-pytorch-60-min-blitz/notlar.md` ve içindeki kod dosyaları.
