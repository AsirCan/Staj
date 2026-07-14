# JSON denemeleri - staj 1. hafta
# json modulu python ile hazir gelir, kurulum yok.
# Calistir: python 03-json-denemeleri.py
import json
import os

# dict <-> json metni
kisi = {"ad": "Asir", "yas": 22, "aktif": True, "diller": ["Python", "JS"], "adres": None}
metin = json.dumps(kisi, ensure_ascii=False, indent=2)   # dict -> json metni
print(metin)
geri = json.loads(metin)                                 # json metni -> dict
print(geri["ad"], geri["diller"])

# dosyaya yaz / dosyadan oku
veri = {"proje": "MailAssistant", "surum": 1, "etiketler": ["ai", "mail"]}
with open("gecici.json", "w", encoding="utf-8") as f:
    json.dump(veri, f, ensure_ascii=False, indent=2)
with open("gecici.json", "r", encoding="utf-8") as f:
    print(json.load(f))
os.remove("gecici.json")

# ic ice json (bir api cevabi gibi)
cevap = {
    "durum": "ok",
    "sonuc": {
        "toplam": 2,
        "kayitlar": [
            {"id": 1, "baslik": "Merhaba", "okundu": False},
            {"id": 2, "baslik": "Toplanti", "okundu": True},
        ],
    },
}
print(cevap["sonuc"]["toplam"])
for k in cevap["sonuc"]["kayitlar"]:
    if not k["okundu"]:
        print("okunmadi:", k["baslik"])

# jsonl - her satir ayri bir json (ai veri setlerinde cok kullanilir)
ornekler = [
    {"soru": "nasilsin", "cevap": "iyiyim"},
    {"soru": "hava nasil", "cevap": "gunesli"},
]
with open("gecici.jsonl", "w", encoding="utf-8") as f:
    for o in ornekler:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")
with open("gecici.jsonl", "r", encoding="utf-8") as f:
    for satir in f:
        print(json.loads(satir)["soru"])
os.remove("gecici.jsonl")
