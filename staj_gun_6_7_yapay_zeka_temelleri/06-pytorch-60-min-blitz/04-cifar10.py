"""
Bölüm 4 — Uçtan Uca CIFAR10 Sınıflandırıcı
============================================

Bu Blitz serisinin final dosyası. Önceki üç bölümde tensor, autograd ve
nn.Module gördük. Şimdi hepsini birleştirip küçük bir CNN (convolutional
neural network) ile 10 sınıflı bir görüntü sınıflandırıcı eğiteceğiz.

CIFAR10 nedir:
    - 32x32 renkli görüntülerden oluşan bir veri seti
    - 10 sınıf: uçak, araba, kuş, kedi, geyik, köpek, kurbağa, at, gemi, kamyon
    - 50.000 eğitim + 10.000 test görüntüsü
    - PyTorch'un `torchvision` paketinde hazır

Bu betik ilk çalıştırıldığında ~170 MB veri indirir. Sonrasında yerelde saklı
kalır.

Eğitim CPU'da yaklaşık 3-5 dakika, GPU'da 30 saniye civarı sürer.
"""

# %%
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.transforms as T
import matplotlib.pyplot as plt
import numpy as np

torch.manual_seed(42)     # tekrarlanabilirlik için

# %% [markdown]
# ## 1. Cihaz Seçimi

# %%
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Kullanılacak cihaz:", device)

# %% [markdown]
# ## 2. Veriyi Yükleme
#
# `torchvision.datasets` bize CIFAR10'u getirebiliyor. `transform` ile de
# her görüntüyü tensor'a çeviriyor ve normalize ediyoruz.
#
# Normalizasyon: (x - 0.5) / 0.5 → pikselleri -1..1 aralığına çekiyor.

# %%
transform = T.Compose([
    T.ToTensor(),                                          # PIL → tensor
    T.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),         # -1..1
])

train_set = torchvision.datasets.CIFAR10(
    root="./data", train=True, download=True, transform=transform,
)
test_set = torchvision.datasets.CIFAR10(
    root="./data", train=False, download=True, transform=transform,
)

# DataLoader: batch'leme + karıştırma + paralel yükleme
BATCH = 64
train_loader = torch.utils.data.DataLoader(
    train_set, batch_size=BATCH, shuffle=True, num_workers=0
)
test_loader = torch.utils.data.DataLoader(
    test_set, batch_size=BATCH, shuffle=False, num_workers=0
)

siniflar = ("plane", "car", "bird", "cat", "deer",
            "dog", "frog", "horse", "ship", "truck")

print("Eğitim örneği sayısı:", len(train_set))
print("Test örneği sayısı:", len(test_set))
print("Batch başına örnek:", BATCH)

# %% [markdown]
# ## 3. Birkaç Görüntüye Bakalım (kontrol)

# %%
def imshow(img):
    img = img / 2 + 0.5     # normalize'ı geri al
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.axis("off")

dataiter = iter(train_loader)
images, labels = next(dataiter)

fig, axs = plt.subplots(1, 8, figsize=(16, 3))
for i in range(8):
    axs[i].imshow(np.transpose(images[i].numpy() / 2 + 0.5, (1, 2, 0)))
    axs[i].set_title(siniflar[labels[i]])
    axs[i].axis("off")
# plt.show()    # interactive'de aç, batch modunda kapalı bırak

# %% [markdown]
# ## 4. Model — Küçük Bir CNN
#
# Katmanlar:
#   Conv2d(3 → 32, 3x3) → ReLU → MaxPool
#   Conv2d(32 → 64, 3x3) → ReLU → MaxPool
#   Flatten
#   Linear(64*6*6 → 128) → ReLU
#   Linear(128 → 10)
#
# CNN detayı Deep Learning bölümünde derinlemesine yok — burada sadece
# "matris çarpımlarının görüntüye uyarlanmış hali" olarak düşün. Conv katman
# bir filtreyi görüntü üzerinde kaydırıp öznitelik çıkarıyor.

# %%
class KucukCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3)
        self.pool = nn.MaxPool2d(2, 2)     # 2x2 max pooling
        # 32x32 → conv1 (30x30) → pool (15x15) → conv2 (13x13) → pool (6x6)
        self.fc1 = nn.Linear(64 * 6 * 6, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)             # (B, 64, 6, 6) → (B, 64*6*6)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)                     # ham logits — softmax loss içinde
        return x


model = KucukCNN().to(device)
print(model)

toplam = sum(p.numel() for p in model.parameters())
print(f"Toplam parametre: {toplam:,}")

# %% [markdown]
# ## 5. Loss ve Optimizer

# %%
loss_fn = nn.CrossEntropyLoss()           # softmax + NLL birleşik
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# %% [markdown]
# ## 6. Eğitim Döngüsü
#
# `03-nn-module.py`'daki şablonun aynısı, sadece:
#   - Veriyi cihaza taşıyoruz
#   - Batch'ler DataLoader'dan geliyor
#   - Epoch başına ortalama loss'u raporluyoruz

# %%
EPOCH = 3          # kısa tutuldu; daha iyi sonuç için 10-20 denenebilir

for epoch in range(EPOCH):
    model.train()
    epoch_loss = 0.0
    dogru = 0
    toplam_ornek = 0

    for i, (images, labels) in enumerate(train_loader):
        images, labels = images.to(device), labels.to(device)

        # Forward
        outputs = model(images)
        loss = loss_fn(outputs, labels)

        # Backward + step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # İstatistik
        epoch_loss += loss.item()
        _, tahmin = outputs.max(1)          # en yüksek olasılıklı sınıf
        dogru += (tahmin == labels).sum().item()
        toplam_ornek += labels.size(0)

    train_acc = 100 * dogru / toplam_ornek

    # Validation (test set üstünde — kolay olsun diye ayrı val setine bölünmedi)
    model.eval()
    val_dogru = 0
    val_toplam = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, tahmin = outputs.max(1)
            val_dogru += (tahmin == labels).sum().item()
            val_toplam += labels.size(0)
    val_acc = 100 * val_dogru / val_toplam

    print(f"Epoch {epoch+1}/{EPOCH} | "
          f"loss = {epoch_loss/len(train_loader):.4f} | "
          f"train acc = {train_acc:.2f}% | "
          f"test acc = {val_acc:.2f}%")

# %% [markdown]
# ## 7. Sınıf Bazında Doğruluk
#
# Model her sınıfta ne kadar başarılı? Genel doğruluk gizleyebilir.

# %%
sinif_dogru = [0] * 10
sinif_toplam = [0] * 10

model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, tahmin = outputs.max(1)
        for i in range(labels.size(0)):
            label = labels[i].item()
            sinif_toplam[label] += 1
            if tahmin[i].item() == label:
                sinif_dogru[label] += 1

for i, isim in enumerate(siniflar):
    oran = 100 * sinif_dogru[i] / sinif_toplam[i] if sinif_toplam[i] else 0
    print(f"{isim:8s}: {oran:.1f}%")

# %% [markdown]
# ## 8. Model Kaydet

# %%
torch.save(model.state_dict(), "cifar10_cnn.pt")
print("Model kaydedildi → cifar10_cnn.pt")

# %% [markdown]
# ## 9. Yorum / Gözlem
#
# 3 epoch'ta ~60-65% doğruluk normal. Bunun üstüne çıkmak için:
#   - Daha fazla epoch
#   - Data augmentation (RandomCrop, HorizontalFlip)
#   - Daha derin bir CNN
#   - BatchNorm katmanları
#   - Learning rate scheduler
#
# CIFAR10'un state-of-the-art'ı >%99. Ama küçük bir modelle burada
# eğitim döngüsünün nasıl çalıştığını **görmek** önemli, kazanan model
# yapmak değil.
#
# Bu betik koşturulunca (özellikle test acc'nin train acc'yi geride bırakıp
# bırakmadığı, loss eğrisinin nasıl indiği) `04-deep-learning-temelleri.md`
# dosyasındaki overfitting ve eğitim dinamiği gözlemleri elle
# doğrulanmış oluyor.

# %% [markdown]
# ## Öz — Blitz Tamamlandı
#
# 4 dosyanın kapsadıkları:
#   1. `01-tensor.py`  → PyTorch'un temel veri tipi.
#   2. `02-autograd.py` → Otomatik türevin nasıl çalıştığı.
#   3. `03-nn-module.py` → `nn.Module` + optimizer + loss şablonu.
#   4. `04-cifar10.py` → Şablonun gerçek bir problemde uçtan uca kullanımı.
#
# Bu şablon sayesinde PyTorch'la yeni bir probleme yaklaşmanın standart yolu şu:
#   - Model'i `nn.Module`'dan miras alarak yaz
#   - Uygun loss ve optimizer seç
#   - DataLoader'la batch'leri hazırla
#   - Eğitim döngüsünü koştur
#
# Bir sonraki adım NLP → Transformer → LLM ekosistemi. Hugging Face'in
# `transformers` kütüphanesi işte bu PyTorch temelinin üstünde çalışıyor.
"""
Not: Bu betik çalıştırılınca `./data` klasörü oluşur (CIFAR10) ve
`cifar10_cnn.pt` model dosyası kaydedilir. Git'e girmesin diye `.gitignore`
kontrol edilmeli.
"""
