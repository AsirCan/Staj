// MongoDB denemeleri - staj 1. hafta
// Ayni magaza senaryosu, bu sefer NoSQL (doküman) tarafinda.
// Calistir: mongosh < 05-mongodb-denemeleri.js
// veya mongosh acip komutlari tek tek yapistir.

// magaza veritabanina gec (yoksa ilk yazimda olusur)
use magaza

// temiz baslamak icin eski koleksiyonlari sil
db.musteriler.drop()
db.urunler.drop()
db.siparisler.drop()

// veri ekle (SQL'deki INSERT karsiligi)
db.musteriler.insertMany([
  { _id: 1, ad: "Ali", sehir: "Istanbul", kayit_yili: 2021 },
  { _id: 2, ad: "Ayse", sehir: "Ankara", kayit_yili: 2022 },
  { _id: 3, ad: "Mehmet", sehir: "Izmir", kayit_yili: 2021 },
  { _id: 4, ad: "Zeynep", sehir: "Istanbul", kayit_yili: 2023 }
])

db.urunler.insertMany([
  { _id: 1, urun_adi: "Klavye", kategori: "Elektronik", fiyat: 450 },
  { _id: 2, urun_adi: "Mouse", kategori: "Elektronik", fiyat: 250 },
  { _id: 3, urun_adi: "Defter", kategori: "Kirtasiye", fiyat: 40 },
  { _id: 4, urun_adi: "Kalem", kategori: "Kirtasiye", fiyat: 15 },
  { _id: 5, urun_adi: "Monitor", kategori: "Elektronik", fiyat: 3200 }
])

db.siparisler.insertMany([
  { _id: 1, musteri_id: 1, urun_id: 1, adet: 1 },
  { _id: 2, musteri_id: 1, urun_id: 2, adet: 2 },
  { _id: 3, musteri_id: 2, urun_id: 5, adet: 1 },
  { _id: 4, musteri_id: 3, urun_id: 3, adet: 5 },
  { _id: 5, musteri_id: 4, urun_id: 4, adet: 10 }
])

// butun musteriler (SELECT * FROM)
db.musteriler.find()

// fiyati 200'den yuksek urunler ($gt = greater than)
db.urunler.find({ fiyat: { $gt: 200 } })

// adi A ile baslayanlar (regex, SQL'deki LIKE 'A%')
db.musteriler.find({ ad: /^A/ })

// sadece belirli alanlari getir (projection)
db.urunler.find({ kategori: "Elektronik" }, { _id: 0, urun_adi: 1, fiyat: 1 })

// bir urunun fiyatini guncelle (UPDATE)
db.urunler.updateOne({ _id: 1 }, { $set: { fiyat: 500 } })

// adeti 1 olan siparisleri sil (DELETE)
db.siparisler.deleteMany({ adet: 1 })

// urunleri pahalidan ucuza sirala, ilk 3 (ORDER BY DESC + LIMIT)
db.urunler.find().sort({ fiyat: -1 }).limit(3)

// kategoriye gore ortalama fiyat (aggregate = SQL'deki GROUP BY)
db.urunler.aggregate([
  { $group: { _id: "$kategori", ortalama: { $avg: "$fiyat" }, adet: { $sum: 1 } } }
])

// siparisleri urun bilgisiyle birlestir ($lookup = SQL'deki JOIN)
db.siparisler.aggregate([
  { $lookup: { from: "urunler", localField: "urun_id", foreignField: "_id", as: "urun" } },
  { $unwind: "$urun" },
  { $project: { _id: 0, musteri_id: 1, urun: "$urun.urun_adi", adet: 1 } }
])
