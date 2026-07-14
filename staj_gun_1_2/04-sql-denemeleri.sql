-- SQL denemeleri - staj 1. hafta
-- Basit bir magaza veritabani: musteriler, urunler, siparisler
-- SQLite ile denedim. SQL Server icin basa sunu ekle:
--   CREATE DATABASE MagazaDB; GO; USE MagazaDB; GO


-- tablolar
CREATE TABLE Musteriler (
    id INT PRIMARY KEY,
    ad VARCHAR(50) NOT NULL,
    sehir VARCHAR(50),
    kayit_yili INT
);

CREATE TABLE Urunler (
    id INT PRIMARY KEY,
    urun_adi VARCHAR(50) NOT NULL,
    kategori VARCHAR(30),
    fiyat DECIMAL(8,2)
);

CREATE TABLE Siparisler (
    id INT PRIMARY KEY,
    musteri_id INT,
    urun_id INT,
    adet INT,
    FOREIGN KEY (musteri_id) REFERENCES Musteriler(id),
    FOREIGN KEY (urun_id) REFERENCES Urunler(id)
);


-- veri ekle
INSERT INTO Musteriler (id, ad, sehir, kayit_yili) VALUES
(1, 'Ali', 'Istanbul', 2021),
(2, 'Ayse', 'Ankara', 2022),
(3, 'Mehmet', 'Izmir', 2021),
(4, 'Zeynep', 'Istanbul', 2023);

INSERT INTO Urunler (id, urun_adi, kategori, fiyat) VALUES
(1, 'Klavye', 'Elektronik', 450.00),
(2, 'Mouse', 'Elektronik', 250.00),
(3, 'Defter', 'Kirtasiye', 40.00),
(4, 'Kalem', 'Kirtasiye', 15.00),
(5, 'Monitor', 'Elektronik', 3200.00);

INSERT INTO Siparisler (id, musteri_id, urun_id, adet) VALUES
(1, 1, 1, 1),
(2, 1, 2, 2),
(3, 2, 5, 1),
(4, 3, 3, 5),
(5, 4, 4, 10),
(6, 2, 2, 1);


-- butun musteriler
SELECT * FROM Musteriler;

-- fiyati 200'den yuksek urunler
SELECT urun_adi, fiyat FROM Urunler WHERE fiyat > 200;

-- adi A ile baslayan musteriler
SELECT ad FROM Musteriler WHERE ad LIKE 'A%';

-- kac farkli sehir var
SELECT DISTINCT sehir FROM Musteriler;

-- kim ne siparis etmis (3 tablo JOIN)
SELECT m.ad, u.urun_adi, s.adet
FROM Siparisler s
JOIN Musteriler m ON s.musteri_id = m.id
JOIN Urunler u ON s.urun_id = u.id;

-- her musterinin toplam harcamasi
SELECT m.ad, SUM(u.fiyat * s.adet) AS toplam
FROM Siparisler s
JOIN Musteriler m ON s.musteri_id = m.id
JOIN Urunler u ON s.urun_id = u.id
GROUP BY m.ad;

-- kategoriye gore ozet
SELECT kategori, COUNT(*) AS urun_sayisi, AVG(fiyat) AS ortalama,
       MIN(fiyat) AS en_ucuz, MAX(fiyat) AS en_pahali
FROM Urunler
GROUP BY kategori;

-- sehir basina musteri sayisi
SELECT sehir, COUNT(*) AS musteri_sayisi
FROM Musteriler
GROUP BY sehir;

-- bir urunun fiyatini guncelle
UPDATE Urunler SET fiyat = 500.00 WHERE id = 1;

-- adeti 1 olan siparisleri sil
DELETE FROM Siparisler WHERE adet = 1;

-- urunleri pahalidan ucuza sirala
SELECT urun_adi, fiyat FROM Urunler ORDER BY fiyat DESC;

-- en pahali 3 urun (SQL Server'da LIMIT yerine TOP 3 kullanilir)
SELECT urun_adi, fiyat FROM Urunler ORDER BY fiyat DESC LIMIT 3;
