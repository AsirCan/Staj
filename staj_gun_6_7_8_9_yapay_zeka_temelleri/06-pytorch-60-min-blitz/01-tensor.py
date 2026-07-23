"""
Bölüm 1 — Tensor'lar
=====================

Tensor, PyTorch'un temel veri tipi. Kabaca "GPU'da çalışabilen NumPy dizisi"
diye düşünebiliriz. Modelin girdileri, çıktıları, parametreleri — hepsi tensor.

Bu dosya, tensor kavramını sıfırdan sindirmek için hazırlanmış bir alıştırma.
VS Code'da açıp `# %%` işaretli hücreleri tek tek çalıştırabilirsin, ya da
düz `python 01-tensor.py` diye koşturursun.

Konular:
    - Tensor oluşturma yolları
    - Tensor'un attribute'ları (shape, dtype, device)
    - Aritmetik işlemler
    - NumPy ile geçiş
    - CPU / GPU aktarımı
    - Reshape / view / squeeze
"""

# %% [markdown]
# ## 1. Kütüphaneler

# %%
import torch
import numpy as np

print("PyTorch sürümü:", torch.__version__)
print("CUDA (GPU) kullanılabilir mi?", torch.cuda.is_available())

# %% [markdown]
# ## 2. Tensor Oluşturma
#
# Bir tensor'u dolduracak birkaç yol var:
# - Doğrudan bir liste / numpy dizisi ile
# - Sıfırlar / birler / rastgele ile
# - Başka bir tensor'un şeklinden ("like" fonksiyonları)

# %%
# Doğrudan listeden
t1 = torch.tensor([[1, 2, 3], [4, 5, 6]])
print("t1:")
print(t1)
print("Şekli (shape):", t1.shape)
print("Veri tipi (dtype):", t1.dtype)   # int64
print("Cihaz (device):", t1.device)     # cpu

# %%
# Sıfırlar ve birler
zeros = torch.zeros(3, 4)          # 3x4 sıfır matrisi
ones = torch.ones(2, 2)            # 2x2 birler matrisi
print("zeros:", zeros)
print("ones:", ones)

# %%
# Rastgele değerler (0-1 arası uniform)
rnd = torch.rand(2, 3)
print("Rastgele tensor:", rnd)

# Rastgele değerler (normal dağılım, ortalama 0, std 1)
rnd_normal = torch.randn(2, 3)
print("Normal dağılımdan:", rnd_normal)

# %%
# Başka bir tensor'un şeklinde
same_shape = torch.zeros_like(t1)     # t1 ile aynı şekilde ama sıfırlarla
print("zeros_like:", same_shape)

# %% [markdown]
# ## 3. Tensor Nitelikleri (Attributes)

# %%
tensor = torch.rand(3, 4)
print("Şekil:", tensor.shape)            # torch.Size([3, 4])
print("Veri tipi:", tensor.dtype)        # torch.float32
print("Cihaz:", tensor.device)           # cpu (veya cuda:0)
print("Toplam eleman sayısı:", tensor.numel())   # 12

# %% [markdown]
# ## 4. Aritmetik İşlemler
#
# NumPy'ye benziyor. Broadcasting kuralları da benzer.

# %%
a = torch.tensor([[1., 2.], [3., 4.]])
b = torch.tensor([[10., 20.], [30., 40.]])

print("Toplama:", a + b)               # veya torch.add(a, b)
print("Çarpma (elementwise):", a * b)  # eleman-eleman
print("Matris çarpımı:", a @ b)        # veya torch.matmul(a, b)
print("Transpoz:", a.T)
print("Ortalama:", a.mean())
print("Toplam:", a.sum())

# %%
# In-place işlemler — sonuna `_` gelir, tensor'u yerinde değiştirir.
# Autograd ile ihtiyatlı kullanmak gerekir.
c = torch.ones(2, 2)
c.add_(5)     # c artık 6'larla dolu
print("In-place ekleme sonrası c:", c)

# %% [markdown]
# ## 5. NumPy ile Geçiş
#
# Aynı bellek paylaşılabilir. Yani birinde değişiklik ötekini de etkileyebilir!
# (CPU üstündeyken — GPU'da paylaşım yok.)

# %%
np_array = np.array([1, 2, 3, 4])
t_from_np = torch.from_numpy(np_array)
print("NumPy'den tensor:", t_from_np)

# Ters yön
t = torch.ones(3)
np_from_t = t.numpy()
print("Tensor'dan numpy:", np_from_t)

# Bellek paylaşımı örneği
t.add_(10)               # tensor'u değiştir
print("Tensor değişti:", t)
print("Numpy de değişti mi? :", np_from_t)   # evet, çünkü aynı bellek

# %% [markdown]
# ## 6. Reshape / View / Squeeze
#
# Sinir ağları çok fazla şekil değiştirme yapıyor. En sık kullanacaklarım.

# %%
x = torch.arange(12)     # 0..11 arası tensor, şekli (12,)
print("Orjinal:", x, "şekil:", x.shape)

# Yeniden şekillendirme (3x4)
x_reshaped = x.reshape(3, 4)
print("3x4:", x_reshaped)

# view aynı işi yapıyor ama bellek sürekli olmalı, aksi halde hata
x_view = x.view(4, 3)
print("4x3:", x_view)

# -1 kullanımı: "kalanı sen hesapla"
x_flat = x_reshaped.reshape(-1)     # şekli (12,)
x_auto = x.reshape(2, -1)           # (2, 6)
print("2, -1:", x_auto)

# %%
# Boyut ekleme / çıkarma
y = torch.rand(1, 3, 1, 4)
print("Orjinal:", y.shape)          # (1, 3, 1, 4)

y_squeezed = y.squeeze()            # 1 boyutlarını kaldır
print("Squeeze:", y_squeezed.shape) # (3, 4)

y_unsq = y_squeezed.unsqueeze(0)    # başa 1 boyut ekle
print("Unsqueeze:", y_unsq.shape)   # (1, 3, 4)

# %% [markdown]
# ## 7. Cihaz Aktarımı (CPU ↔ GPU)
#
# Modeli GPU'da eğitmek istiyorsak, veri de GPU'ya taşınmalı.

# %%
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Kullanılacak cihaz:", device)

t_cpu = torch.rand(3, 3)
print("CPU'daki tensor:", t_cpu.device)

t_gpu = t_cpu.to(device)             # GPU varsa GPU'ya taşır
print("Taşındıktan sonra:", t_gpu.device)

# Geri CPU'ya
t_back = t_gpu.to("cpu")
print("Geri CPU'ya:", t_back.device)

# %% [markdown]
# ## 8. İndeksleme
#
# NumPy gibi çalışıyor.

# %%
x = torch.arange(20).reshape(4, 5)
print("x:", x)

print("İlk satır:", x[0])
print("Son sütun:", x[:, -1])
print("Alt matris (2x2):", x[:2, :2])
print("Şart ile:", x[x > 10])        # 10'dan büyük elemanlar

# %% [markdown]
# ## 9. Küçük Bir Alıştırma
#
# Bir sinir ağının içindeki "linear katman" işlemini elle yapalım:
# y = x @ W.T + b

# %%
# Girdi: 2 örnek, her biri 4 boyutlu
x = torch.rand(2, 4)
print("Girdi x:", x, "\nşekil:", x.shape)

# Katman parametreleri: 4 boyuttan 3 boyuta gidiyoruz
W = torch.rand(3, 4)      # (n_out, n_in)
b = torch.rand(3)         # (n_out,)

# Forward
y = x @ W.T + b
print("Çıktı y:", y, "\nşekil:", y.shape)      # (2, 3)

# İşte bu, `nn.Linear(4, 3)` katmanının içinde tam olarak yaptığı iş.

# %% [markdown]
# ## Öz
#
# Bu bölümden çıkarılması gereken temel noktalar:
# - Tensor bir n-boyutlu dizi. shape, dtype, device üçlüsü kritik.
# - `+, *, @, .mean()` gibi işlemler NumPy'ye benziyor.
# - `.reshape() / .view()` sık kullanılıyor, sinir ağları arasında akıştaki
#   şekiller sürekli değişiyor.
# - GPU'ya `.to(device)` ile taşıyoruz. Hem veri hem model taşınmalı.
#
# Sonraki dosya: `02-autograd.py` — otomatik türev.
