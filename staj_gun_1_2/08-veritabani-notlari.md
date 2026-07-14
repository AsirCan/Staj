# Veritabanı Notları

Staj 1. hafta, veritabanlarıyla ilgili araştırma notlarım. Kod tarafını
`04-sql-denemeleri.sql` ve `05-mongodb-denemeleri.js` dosyalarında denedim.

## Veritabanı nedir, nasıl ve nerede kullanılır?

Veritabanı, verinin düzenli bir şekilde saklandığı, güncellendiği ve sorgulandığı sistem.
Veriyi bir dosyaya elle yazmak yerine veritabanı kullanmanın sebebi: çok fazla veriyi hızlı
sorgulamak, aynı anda birçok kullanıcıya hizmet vermek, veri bütünlüğünü ve güvenliğini korumak.

Veritabanını yöneten yazılıma DBMS deniyor (mesela PostgreSQL, MongoDB).

Nerede kullanılıyor: neredeyse her uygulamada. Web ve mobil uygulamalar, e-ticaret, bankalar,
sosyal medya. Yapay zeka tarafında da eğitim verisini saklamak, kullanıcı geçmişini tutmak,
model çıktısını kaydetmek için kullanılıyor.

## SQL ve NoSQL neden ikiye ayrılıyor?

Temel sebep şu: verinin şekli her zaman düzenli tablo değil. Bazı veriler tabloya güzel oturuyor,
bazıları oturmuyor. Bu yüzden iki farklı yaklaşım çıkmış.

### SQL (ilişkisel)
- Veri tablolarda tutuluyor (satır = kayıt, sütun = alan).
- Önceden tanımlı bir şema var, her satır aynı sütunlara uyuyor.
- Tablolar birbirine ilişkilerle bağlanıyor (mesela musteri_id ile).
- Ortak dili SQL (Structured Query Language).
- Güçlü yanı tutarlılık ve ilişkisel sorgular (JOIN). Banka gibi kesinlik isteyen yerler için ideal.
- Örnekler: PostgreSQL, MySQL, SQLite, Oracle, SQL Server.

### NoSQL (ilişkisel olmayan)
- Sabit şema zorunlu değil, esnek yapı. Farklı kayıtlar farklı alanlara sahip olabiliyor.
- Çok büyük veri ve yoğun trafik için sunucu ekleyerek büyümeye (yatay ölçeklenme) daha uygun.
- Alt türleri var:
  - Doküman (JSON benzeri): MongoDB
  - Anahtar-değer: Redis
  - Sütun ailesi: Cassandra
  - Graf: Neo4j

## Hangisini nerede kullanmalıyız?

Araştırdıktan sonra kendime çıkardığım basit kural:

- Veri düzenliyse ve ilişkiler önemliyse (sipariş, müşteri, ürün): SQL.
- Para/işlem var, kesin tutarlılık şart (banka): SQL.
- Yapı esnek/değişkense, hızlı geliştirme ve büyük ölçek gerekiyorsa: NoSQL.
- JSON gibi doküman saklanacaksa: MongoDB.
- Çok hızlı geçici veri, önbellek, sayaç gerekiyorsa: Redis.

Önemli nokta: biri diğerinden mutlak iyi değil, işe göre araç seçiliyor. Hatta gerçek
projelerde ikisi birlikte kullanılıyor (ana veri PostgreSQL'de, önbellek Redis'te gibi).

## Temel seviyede: SQL / PostgreSQL / MongoDB / Redis

### Standart SQL
Neredeyse tüm ilişkisel veritabanlarında mantık aynı. Temel komutlar:

```sql
CREATE TABLE kullanicilar (id INT PRIMARY KEY, ad VARCHAR(50), yas INT);
INSERT INTO kullanicilar VALUES (1, 'Asir', 22);
SELECT * FROM kullanicilar WHERE yas > 18 ORDER BY yas DESC;
UPDATE kullanicilar SET yas = 23 WHERE id = 1;
DELETE FROM kullanicilar WHERE id = 1;
```

Komutlar kategorilere ayrılıyor: DDL (CREATE, ALTER, DROP - yapı), DML (INSERT, UPDATE, DELETE
- veri), DQL (SELECT - sorgu).

### PostgreSQL
Açık kaynak, güçlü ve güvenilir bir ilişkisel veritabanı. Standart SQL'i iyi destekliyor,
ayrıca JSON alanları, coğrafi veri, tam metin arama gibi ekstraları var. pgvector eklentisiyle
vektör de saklayabildiği için yapay zeka projelerinde popüler.

### MongoDB (NoSQL, doküman)
Veriyi doküman olarak tutuyor ve doküman neredeyse birebir JSON. Tablo yerine collection,
satır yerine document, sütun yerine field var.

```javascript
db.kullanicilar.insertOne({ ad: "Asir", yas: 22 })
db.kullanicilar.find({ yas: { $gt: 18 } })
db.kullanicilar.updateOne({ ad: "Asir" }, { $set: { yas: 23 } })
db.kullanicilar.deleteOne({ ad: "Asir" })
```

### Redis (NoSQL, anahtar-değer)
Veriyi bellekte (RAM) tuttuğu için çok hızlı. Ama RAM sınırlı, o yüzden her şeyi değil, hızlı
erişilmesi gereken şeyi tutuyorsun. Bir anahtar (key) verip bir değer (value) koyup alıyorsun.

```
SET kullanici:1:ad "Asir"
GET kullanici:1:ad
EXPIRE kullanici:1:ad 60
INCR sayfa:ziyaret
```

En sık kullanımı: önbellek (cache), oturum (session) saklama, sayaç, kuyruk.

## Karşılaştırma

| Özellik | PostgreSQL (SQL) | MongoDB (NoSQL) | Redis (NoSQL) |
|---------|------------------|-----------------|---------------|
| Model | İlişkisel tablo | Doküman (JSON) | Anahtar-değer |
| Şema | Sabit | Esnek | Esnek |
| Nerede tutar | Disk | Disk | Bellek (RAM) |
| Güçlü yanı | Tutarlılık, JOIN | Esneklik, ölçek | Hız, önbellek |
| Tipik kullanım | Ana iş verisi | Değişken/JSON veri | Cache, session |

## SQL ve MongoDB kavram karşılığı

| SQL | MongoDB |
|-----|---------|
| Tablo | Collection |
| Satır | Document |
| Sütun | Field |
| JOIN | $lookup (veya gömülü doküman) |
