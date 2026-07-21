# PyTorch 60-Minute Blitz — Notlar

PyTorch'un resmi **60 Minute Blitz** tutorial'ının dört bölümü Python dosyalarına döküldü, her adım açıklamalı biçimde.

Resmi kaynak: https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html

Klasördeki dosyalar:

1. **`01-tensor.py`** — Tensor nedir, nasıl oluşturulur, NumPy ile farkı.
2. **`02-autograd.py`** — Otomatik türev, `.backward()`'ın kod hali.
3. **`03-nn-module.py`** — `nn.Module` ile sinir ağı tanımlama.
4. **`04-cifar10.py`** — Bir görüntü sınıflandırıcının uçtan uca eğitilmesi.

Dosyalar `.py` formatında (`# %%` işaretleriyle hücrelere bölünmüş). Böylece:
- VS Code'da "interactive window" ile hücre hücre çalıştırılabilir.
- Aynı zamanda normal Python betiği olarak da çalışır.
- Git'te temiz görünür (`.ipynb`'nin JSON çıktı diff'i problemi yok).

`jupyter nbconvert --to notebook --execute` veya VS Code notebook desteği ile `.ipynb`'ye çevrilebilir.

---

## Nasıl çalıştırırım?

### Kurulum (bir kere)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install torch torchvision matplotlib numpy
```

CUDA'lı GPU (NVIDIA) varsa, PyTorch resmi sitesinden GPU'lu wheel URL'si alınmalı:
https://pytorch.org/get-started/locally/

### Çalıştırma

```bash
python 01-tensor.py
python 02-autograd.py
python 03-nn-module.py
python 04-cifar10.py         # bu biraz zaman alır, CIFAR10 indirir
```

VS Code'da açıp `# %%` ile hücre hücre koşturmak, deneme yaparak öğrenmek için daha uygun.

---

## Blitz'in Ana Dersleri

1. **Tensor = GPU'lu NumPy + autograd.** Neredeyse aynı API.
2. **`.backward()`** arkasında forward pass boyunca oluşturulmuş bir "hesap grafiği" işletir.
3. **`nn.Module`** modelleri sınıf olarak yazmanın standart yolu. `__init__`'te katmanlar tanımlanır, `forward()`'ta birleştirilir.
4. **Eğitim döngüsü hep aynı**: forward → loss → `backward()` → `optimizer.step()` → `optimizer.zero_grad()`.
5. **GPU'ya taşımak** için hem model hem veri `.to(device)` yapılmalı. Aksi halde cihaz uyuşmazlığı hatası alınır.
