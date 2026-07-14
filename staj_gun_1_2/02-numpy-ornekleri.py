# NumPy denemeleri - staj 1. hafta
# Kurulum: pip install numpy
# Calistir: python 02-numpy-ornekleri.py
import numpy as np

# dizi olusturma
a = np.array([1, 2, 3, 4])
print(a, a.dtype, a.shape)
print(np.zeros(3))
print(np.ones((2, 2)))
print(np.arange(0, 10, 2))
print(np.linspace(0, 1, 5))

# neden numpy: dongu yazmadan tum diziye tek islem
liste = [1, 2, 3]
print([x * 2 for x in liste])      # listede dongu gerekiyor
dizi = np.array([1, 2, 3])
print(dizi * 2)                    # numpy'da tek satir
print(dizi ** 2)
print(np.array([1, 2, 3]) + np.array([10, 20, 30]))

# indeksleme ve dilimleme
a = np.array([10, 20, 30, 40, 50])
print(a[0], a[-1], a[1:4])
print(a[a > 30])                   # kosullu filtre

m = np.array([[1, 2, 3], [4, 5, 6]])
print(m[1, 2])                     # 2. satir 3. sutun
print(m[0, :])                     # ilk satir
print(m[:, 0])                     # ilk sutun

# istatistik
veri = np.array([[5, 10, 15], [20, 25, 30]])
print(veri.sum(), veri.mean(), round(float(veri.std()), 2))
print(veri.min(), veri.max())
print(veri.mean(axis=0))           # sutun bazinda ortalama
print(veri.sum(axis=1))            # satir bazinda toplam

# reshape ve matris
a = np.arange(1, 7)
print(a.reshape(2, 3))
print(a.reshape(2, 3).T)           # transpoz
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(A @ B)                       # matris carpimi

# rastgele + normalize (veriyi 0-1 arasina cekme)
np.random.seed(42)                 # ayni sonuc gelsin diye
print(np.round(np.random.rand(3), 3))
ham = np.array([50, 100, 150, 200])
print((ham - ham.min()) / (ham.max() - ham.min()))
