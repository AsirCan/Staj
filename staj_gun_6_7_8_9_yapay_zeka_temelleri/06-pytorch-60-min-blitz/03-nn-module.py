"""
Bölüm 3 — nn.Module ile Sinir Ağı
==================================

Bir önceki dosyada gradient descent'i "elle" yaptık. Bu dosyada aynı işi
PyTorch'un standart araçlarıyla yapacağız:

    - `torch.nn.Module`  → modelin sınıf olarak tanımlanması
    - `torch.nn.Linear`, `torch.nn.ReLU`  → hazır katmanlar
    - `torch.nn.MSELoss`, `torch.nn.CrossEntropyLoss`  → hazır loss'lar
    - `torch.optim.SGD`, `torch.optim.Adam`  → hazır optimizer'lar

Bu blokları öğrenince artık her sinir ağını aynı şablonla yazabiliyorsun.
"""

# %%
import torch
import torch.nn as nn
import torch.optim as optim

# %% [markdown]
# ## 1. nn.Module — Kendi Modelini Sınıf Olarak Yaz
#
# Her modeli `nn.Module`'dan miras alan bir sınıf olarak yazmak standart.
# İki şey lazım:
#   - `__init__`: katmanları tanımla
#   - `forward`: girişin katmanlar arasında nasıl aktığını söyle
#
# `backward`'ı YAZMIYORUZ; autograd bunu forward'dan otomatik türetiyor.

# %%
class KucukAg(nn.Module):
    def __init__(self):
        super().__init__()
        # 3 girişten 8 nörona, oradan 8'e, oradan 1'e
        self.katman1 = nn.Linear(3, 8)
        self.katman2 = nn.Linear(8, 8)
        self.katman3 = nn.Linear(8, 1)
        self.aktivasyon = nn.ReLU()

    def forward(self, x):
        x = self.aktivasyon(self.katman1(x))
        x = self.aktivasyon(self.katman2(x))
        x = self.katman3(x)
        return x


model = KucukAg()
print(model)

# %% [markdown]
# ## 2. Parametreleri Sorgulama

# %%
for isim, param in model.named_parameters():
    print(f"{isim:20s} | şekil: {tuple(param.shape)} | eleman sayısı: {param.numel()}")

# Toplam parametre
toplam = sum(p.numel() for p in model.parameters())
print(f"\nToplam parametre: {toplam}")

# %% [markdown]
# ## 3. Forward Pass

# %%
# Rastgele bir batch (5 örnek, her biri 3 boyutlu)
x = torch.rand(5, 3)
y_pred = model(x)              # `model(x)` çağrısı forward()'u tetikliyor
print("Girdi şekli:", x.shape)
print("Çıktı şekli:", y_pred.shape)
print("Çıktı:", y_pred)

# %% [markdown]
# ## 4. Loss ve Optimizer

# %%
# Loss fonksiyonu — regresyon için MSE
loss_fn = nn.MSELoss()

# Optimizer — hangi parametreler öğrenilecek, öğrenme oranı ne?
optimizer = optim.Adam(model.parameters(), lr=0.01)

# %% [markdown]
# ## 5. Eğitim Döngüsü Şablonu
#
# Neredeyse tüm PyTorch eğitimleri bu 5 satırlık kalıba dayanıyor.
# Ezberle:
#     y_pred = model(x)
#     loss = loss_fn(y_pred, y)
#     optimizer.zero_grad()
#     loss.backward()
#     optimizer.step()

# %%
# Sahte veri: y = x[0] + 2*x[1] - x[2]
def sahte_veri(n=200):
    x = torch.rand(n, 3) * 10
    y = (x[:, 0] + 2 * x[:, 1] - x[:, 2]).unsqueeze(1)
    y += torch.randn_like(y) * 0.1     # biraz gürültü
    return x, y

x_train, y_train = sahte_veri(1000)
x_test, y_test = sahte_veri(200)

# Modeli sıfırdan başlat (üsttekiyle karışmasın)
model = KucukAg()
loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Eğitim
epoch_sayisi = 200
for epoch in range(epoch_sayisi):
    # Forward
    y_pred = model(x_train)
    loss = loss_fn(y_pred, y_train)

    # Backward + adım
    optimizer.zero_grad()          # geçen adımın gradyanlarını temizle
    loss.backward()                # yeni gradyanları hesapla
    optimizer.step()               # parametreleri güncelle

    if epoch % 20 == 0:
        # Validation loss'u da hesapla
        with torch.no_grad():
            val_pred = model(x_test)
            val_loss = loss_fn(val_pred, y_test)
        print(f"Epoch {epoch:3d} | train loss = {loss.item():.4f} | val loss = {val_loss.item():.4f}")

# %% [markdown]
# ## 6. Model Değerlendirme (Inference)
#
# `model.eval()` — dropout/batchnorm gibi katmanlar davranışını değiştirir.
# `torch.no_grad()` — gradyan hesabını kapatır.

# %%
model.eval()
with torch.no_grad():
    ornekler = torch.tensor([
        [1.0, 2.0, 3.0],
        [5.0, 1.0, 0.0],
        [0.0, 0.0, 10.0],
    ])
    tahminler = model(ornekler)
    for x, y in zip(ornekler, tahminler):
        beklenen = x[0] + 2 * x[1] - x[2]
        print(f"x = {x.tolist()} | beklenen = {beklenen.item():.2f} | tahmin = {y.item():.2f}")

# %% [markdown]
# ## 7. Sequential — Kısa Yol
#
# Küçük modeller için ayrı bir sınıf yazmaya gerek yok. `nn.Sequential` ile
# katmanları sırayla yığmak yeterli.

# %%
model_seq = nn.Sequential(
    nn.Linear(3, 8),
    nn.ReLU(),
    nn.Linear(8, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
)
print(model_seq)

# Kullanımı aynı — model_seq(x)

# %% [markdown]
# ## 8. Farklı Loss ve Optimizer Örnekleri

# %%
# Sınıflandırma için
sınıflandırma_loss = nn.CrossEntropyLoss()   # softmax'ı içinde yapıyor!
binary_loss = nn.BCEWithLogitsLoss()         # sigmoid + BCE birleşik

# Farklı optimizer'lar
sgd = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
adam = optim.Adam(model.parameters(), lr=0.001)
adamw = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

# Hepsinin arayüzü aynı:
#   optimizer.zero_grad()
#   loss.backward()
#   optimizer.step()

# %% [markdown]
# ## 9. Modeli Kaydetme / Yükleme

# %%
# Kaydet — sadece parametreleri (tavsiye edilen yol)
torch.save(model.state_dict(), "kucuk_ag.pt")

# Yükle — model şablonu lazım, sonra parametreler
yeni_model = KucukAg()
yeni_model.load_state_dict(torch.load("kucuk_ag.pt"))
yeni_model.eval()

# Test edelim
with torch.no_grad():
    orijinal = model(x_test[:5])
    kopya = yeni_model(x_test[:5])
    print("Orijinal:", orijinal.squeeze().tolist())
    print("Yüklenen:", kopya.squeeze().tolist())
    # Aynı olmalı

# %% [markdown]
# ## 10. GPU'ya Taşıma

# %%
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Cihaz:", device)

# Modeli taşı
model.to(device)

# Veriyi de her batch'te taşımak lazım — GPU üstündeyken:
x_gpu = x_train.to(device)
y_gpu = y_train.to(device)

# Not: kayıp fonksiyonu genelde otomatik taşınıyor, ama modeli ve veriyi
# aynı cihazda tutmayı unutma.

# %% [markdown]
# ## Öz
#
# Bu bölümde artık standart PyTorch şablonu kullanılıyor:
#     model = MyModel()
#     loss_fn = nn.XxxLoss()
#     optimizer = optim.Adam(model.parameters(), lr=...)
#
#     for epoch:
#         for batch:
#             y_hat = model(x)
#             loss = loss_fn(y_hat, y)
#             optimizer.zero_grad()
#             loss.backward()
#             optimizer.step()
#
# Bu 8 satır, PyTorch'la yazılan her eğitim döngüsünün özü.
#
# Sonraki dosya (`04-cifar10.py`): bu şablon gerçek bir problemde
# (CIFAR10 görüntü sınıflandırma) kullanılıyor.
"""
Bölüm 4 için not: modelin adı kalabalık olabilir diye ayrı bir dosyada.
Şimdilik `.pt` dosyasını da silmeyeyim, sonra silerim.
"""
