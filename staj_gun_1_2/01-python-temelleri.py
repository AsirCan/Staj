# Python temelleri - staj 1. hafta
# Degiskenlerden OOP'ye kadar kisa tekrar.
# Calistir: python 01-python-temelleri.py

# --- degiskenler ve tipler ---
sayi = 42
ondalik = 3.14
metin = "merhaba"
dogru = True
print(sayi, ondalik, metin, dogru)
print(type(sayi), type(metin))

# tip donusumu
print(str(sayi) + " kere")
print(int("100") + 1)

# --- operatorler ---
a, b = 7, 2
print(a + b, a - b, a * b, a / b, a // b, a % b, a ** b)
print(a > b, a == b, a != b)
print(a > 0 and b > 0, a > 10 or b > 0, not (a > b))

# --- stringler ---
ad = "Asir Can"
print(ad.upper(), ad.lower(), len(ad))
print(ad.replace("Can", "CAN"))
print(ad.split(" "))
print(ad[0:4])
yas = 22
print(f"{ad}, {yas} yasinda")

# --- listeler, tuple, set, dict ---
liste = [3, 1, 2]
liste.append(5)
liste.sort()
print(liste)

nokta = (10, 20)          # tuple - degistirilemez
print(nokta[0])

kume = {1, 2, 2, 3}       # set - tekrar tutmaz
print(kume)

kisi = {"ad": "Asir", "yas": 22}
kisi["sehir"] = "Istanbul"
print(kisi, kisi["ad"])

# --- kosullar ve donguler ---
for i in range(1, 6):
    if i % 2 == 0:
        print(i, "cift")
    else:
        print(i, "tek")

sayac = 3
while sayac > 0:
    print("geri sayim", sayac)
    sayac -= 1

kareler = [x * x for x in range(1, 6)]   # list comprehension
print(kareler)

# match/case (python 3.10+)
for gun in ["Pazartesi", "Cumartesi"]:
    match gun:
        case "Cumartesi" | "Pazar":
            print(gun, "hafta sonu")
        case _:
            print(gun, "hafta ici")

# --- fonksiyonlar ---
def kare(n):
    return n * n

def selamla(ad, selam="Merhaba"):        # varsayilan parametre
    return f"{selam}, {ad}!"

def topla(*sayilar):                     # *args
    return sum(sayilar)

print(kare(5))
print(selamla("Asir"))
print(selamla("Ali", "Gunaydin"))
print(topla(1, 2, 3, 4))

# --- hata yakalama ---
try:
    print(10 / 0)
except ZeroDivisionError:
    print("sifira bolme hatasi yakalandi")
finally:
    print("finally her durumda calisir")

# --- OOP ---
class Hayvan:
    def __init__(self, ad, ses):
        self.ad = ad
        self.ses = ses

    def konus(self):
        return f"{self.ad}: {self.ses}"

class Kedi(Hayvan):          # kalitim
    def __init__(self, ad):
        super().__init__(ad, "Miyav")

    def konus(self):         # override
        return f"{self.ad}: {self.ses}~"

class Kopek(Hayvan):
    def __init__(self, ad):
        super().__init__(ad, "Hav")

    def konus(self):
        return f"{self.ad}: {self.ses}! {self.ses}!"

# polymorphism - ayni konus() cagrisi neseneye gore farkli davraniyor
for h in [Kedi("Tekir"), Kopek("Karabas")]:
    print(h.konus())

class Hesap:                 # encapsulation - bakiyeye sadece metotla erisilir
    def __init__(self, sahip):
        self.sahip = sahip
        self.__bakiye = 0

    def yatir(self, miktar):
        if miktar > 0:
            self.__bakiye += miktar

    def bakiye(self):
        return self.__bakiye

hesap = Hesap("Asir")
hesap.yatir(500)
hesap.yatir(250)
print(hesap.sahip, hesap.bakiye())
