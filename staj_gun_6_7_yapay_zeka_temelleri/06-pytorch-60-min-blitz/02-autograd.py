"""
Bölüm 2 — Autograd (Otomatik Türev)
====================================

Bir önceki dosyada tensor'lerle oynadık. Şimdi PyTorch'un asıl sihrine geliyoruz:
her tensor işleminin türevini otomatik hesaplayabilmesi.

Neden önemli? Sinir ağını eğitmek için milyonlarca parametrenin gradyanını
hesaplamamız lazım. Elle yapmak imkansız. PyTorch bunu şöyle yapıyor:
    1. Forward pass sırasında yaptığın her işlemi bir "hesap grafiği"nde
       kaydediyor.
    2. Sonuç tensor'una `.backward()` çağırınca, bu grafik boyunca zincir
       kuralıyla geri gidip her parametrenin gradyanını hesaplıyor.

Bu dosyada:
    - `requires_grad=True` ile gradyan takibi
    - Basit bir örnekle `.backward()` çağrısı
    - `.grad` attribute'u
    - Zincir kuralı örneği
    - Gradyanları sıfırlama
    - `no_grad()` bloğu (inference için)
"""

# %%
import torch

# %% [markdown]
# ## 1. `requires_grad=True` — "Bu tensor'u takip et"
#
# Varsayılan olarak tensor'lar için gradyan takibi kapalı. Bir parametreyi
# öğrenilebilir yapmak için `requires_grad=True` diyoruz.

# %%
x = torch.tensor(3.0, requires_grad=True)
print("x:", x)
print("requires_grad:", x.requires_grad)

# Basit bir fonksiyon: y = x^2
y = x ** 2
print("y = x^2:", y)
print("y.grad_fn:", y.grad_fn)     # PowBackward — PyTorch nasıl geri gideceğini biliyor

# %% [markdown]
# ## 2. `.backward()` ile Türev
#
# `dy/dx = 2x` olması lazım. `x = 3` iken sonuç 6 çıkmalı.

# %%
y.backward()      # geriye doğru türev hesapla
print("dy/dx (x=3):", x.grad)    # 6.0 çıkmalı

# %% [markdown]
# ## 3. Biraz Daha Karmaşık: İki Değişkenli Fonksiyon
#
# f(a, b) = a^2 + 3ab + b^3
#
# ∂f/∂a = 2a + 3b
# ∂f/∂b = 3a + 3b^2

# %%
a = torch.tensor(2.0, requires_grad=True)
b = torch.tensor(4.0, requires_grad=True)

f = a**2 + 3*a*b + b**3
print("f =", f.item())

f.backward()
print("df/da (beklenen 2*2 + 3*4 = 16):", a.grad.item())
print("df/db (beklenen 3*2 + 3*16 = 54):", b.grad.item())

# %% [markdown]
# ## 4. Zincir Kuralı Örneği
#
# İç içe fonksiyonlarda PyTorch zincir kuralını kendisi uyguluyor.
#
# u = x^2
# v = 3u + 1
# w = sin(v)
#
# dw/dx = cos(v) * 3 * 2x

# %%
import math

x = torch.tensor(1.0, requires_grad=True)
u = x**2
v = 3*u + 1
w = torch.sin(v)

w.backward()

expected = math.cos(4.0) * 3 * 2 * 1
print("PyTorch'un cevabı:", x.grad.item())
print("Elle hesap:", expected)
# İkisi eşit olmalı

# %% [markdown]
# ## 5. Vektörel Gradyan — Bir Sinir Ağının Küçük Hali
#
# Şimdi biraz "sinir ağı"na benzer bir örnek:
# y = (W · x + b)^2 toplamı
#
# Amacımız: W ve b'nin gradyanını bulmak (gerçek eğitimde olduğu gibi).

# %%
x = torch.tensor([1.0, 2.0, 3.0])           # girdi, öğrenilebilir DEĞİL
W = torch.rand(3, requires_grad=True)       # ağırlıklar, öğrenilebilir
b = torch.rand(1, requires_grad=True)       # bias, öğrenilebilir

y = (W @ x + b) ** 2                        # skaler çıktı
print("y =", y.item())

y.backward()
print("W.grad:", W.grad)          # dy/dW
print("b.grad:", b.grad)          # dy/db

# %% [markdown]
# ## 6. Gradyanları Sıfırlama
#
# `.grad` her `.backward()` çağrısında **toplanır**, üzerine yazılmaz.
# Yani eğer eğitimde her adımda sıfırlamazsak, önceki gradyanlar birikir.

# %%
p = torch.tensor(1.0, requires_grad=True)

for i in range(3):
    q = p ** 2
    q.backward()
    print(f"Adım {i+1}: p.grad = {p.grad.item()}")
    # Her seferinde 2 çıkması gerekirken, 2, 4, 6 çıkıyor — toplandı!

# %%
# Doğru kullanım: her adımda grad'ı sıfırla
p.grad.zero_()
for i in range(3):
    q = p ** 2
    q.backward()
    print(f"Doğru — Adım {i+1}: p.grad = {p.grad.item()}")
    p.grad.zero_()      # optimizer.zero_grad() bunu tüm parametreler için yapar

# %% [markdown]
# ## 7. `torch.no_grad()` — Inference için gradyan hesaplamayı kapat
#
# Eğitim bittikten sonra modeli sadece tahmin için kullanacaksak, gradyan
# hesabına gerek yok. Hem hızlı hem hafıza tasarrufu.

# %%
x = torch.tensor(3.0, requires_grad=True)
print("Eğitim modu — grad var:")
y = x ** 2
print("y.requires_grad:", y.requires_grad)

print("\nInference modu — grad yok:")
with torch.no_grad():
    y2 = x ** 2
    print("y2.requires_grad:", y2.requires_grad)   # False

# Alternatif: model.eval() + torch.no_grad() birlikte kullanılır inference'ta.

# %% [markdown]
# ## 8. `.detach()` — Bir tensor'u grafikten koparmak
#
# Bir hesap sonucunu artık takip etmek istemiyorsak `.detach()` diyoruz.
# Değeri aynı kalıyor, ama gradyan hesabı için kullanılmıyor.

# %%
x = torch.tensor(2.0, requires_grad=True)
y = x ** 3
y_detached = y.detach()

print("y.requires_grad:", y.requires_grad)                 # True
print("y_detached.requires_grad:", y_detached.requires_grad)   # False

# %% [markdown]
# ## 9. Küçük Bir Gradient Descent Örneği
#
# Amaç: y = 3x + 1 doğrusuna uyacak parametreleri bulmak.
# Sadece autograd + manuel adımlarla, `nn.Module` veya optimizer kullanmadan.

# %%
# Sahte veri
x_data = torch.linspace(0, 10, 100)
y_data = 3 * x_data + 1 + torch.randn(100) * 0.5   # gerçek + gürültü

# Öğrenilecek parametreler — rastgele başla
w = torch.rand(1, requires_grad=True)
b = torch.rand(1, requires_grad=True)

lr = 0.01
for step in range(200):
    # Forward
    y_pred = w * x_data + b
    loss = ((y_pred - y_data) ** 2).mean()

    # Backward
    loss.backward()

    # Elle güncelleme — optimizer'ın yaptığı iş
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
        w.grad.zero_()
        b.grad.zero_()

    if step % 20 == 0:
        print(f"Adım {step:3d} | loss = {loss.item():.4f} | w = {w.item():.3f} | b = {b.item():.3f}")

print("\nSon değerler (gerçek: w=3, b=1):")
print(f"w = {w.item():.3f}")
print(f"b = {b.item():.3f}")

# %% [markdown]
# ## Öz
#
# Bu bölümde şunları oturttum:
# - `requires_grad=True` diyerek bir tensor'u "takip edilebilir" yaptım.
# - `.backward()` ile PyTorch zincir kuralını uygulayıp gradyanları hesapladı.
# - `.grad` attribute'unda gradyanlar birikiyor — her adımda sıfırlamak lazım.
# - `torch.no_grad()` inference'ta hem hız hem hafıza kazandırıyor.
# - Manuel bir gradient descent örneğiyle "eğitim döngüsünün özünü" gördüm.
#
# Bir sonraki dosya (`03-nn-module.py`) bu döngüyü `nn.Module`, `optimizer`
# ve `loss` sınıflarıyla profesyonel hale getirecek.
