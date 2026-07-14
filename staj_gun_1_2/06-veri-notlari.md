# Veri Notları

Staj 1. hafta, veriyle ilgili araştırıp not aldığım sorular.

## Veriyi anlamak neden bu kadar önemli?

Yapay zeka aslında veriden öğrenen bir sistem. Yani modeli ne kadar iyi kurarsan kur,
verdiğin veri kötüyse sonuç da kötü oluyor. "Çöp girerse çöp çıkar" (garbage in, garbage out)
diye bir söz var, olayı güzel özetliyor. O yüzden amaç hep sistemi en tutarlı çalıştıracak
veriyle buluşturmak.

Okuduğum kadarıyla bir projede zamanın çoğu modeli kurmaya değil, veriyi toplamaya ve
temizlemeye gidiyormuş.

## Ne çeşit veriler var?

İki şekilde ayırabiliyoruz.

Yapısına göre:
- Yapılandırılmış (structured): Satır sütun düzenli, tabloya oturuyor. Örnek: Excel, SQL tabloları.
- Yarı yapılandırılmış (semi-structured): Düzeni var ama sabit tablo değil. Örnek: JSON, XML, loglar.
- Yapılandırılmamış (unstructured): Belirli bir şablonu yok. Örnek: metin, resim, ses, video.

İçeriğine göre:
- Sayısal: yaş, fiyat, sıcaklık gibi.
- Kategorik: renk, şehir, cinsiyet gibi sınıflar.
- Metin: serbest yazı.
- Görüntü / ses / video.
- Zaman serisi: zamana bağlı ölçümler (borsa, sensör).

Not: Dünyadaki verinin çoğu yapılandırılmamış (fotoğraf, video, yazı). Derin öğrenmenin
öne çıkmasının bir sebebi de bu tarz veriyle iyi çalışabilmesi.

## Yapay zeka eğitirken ne çeşit veri kullanılıyor?

Duruma göre değişiyor ama önemli bir ayrım şu:
- Etiketli veri (labeled): Her örneğin doğru cevabı belli. Buna gözetimli öğrenme
  (supervised) deniyor. Örnek: "bu mail spam mı değil mi".
- Etiketsiz veri (unlabeled): Cevap yok, model kendi bir yapı çıkarıyor. Buna gözetimsiz
  öğrenme (unsupervised) deniyor. Örnek: müşterileri benzerliğe göre gruplamak.

## Veri her zaman belirli bir formatta mı olmalı?

Anladığım kadarıyla: kaynakta olmak zorunda değil, ama modele girerken zorunlu.

Ham veri her yerden dağınık geliyor (JSON, CSV, resim, veritabanı, API). Ama model sonuçta
sayı anlıyor. O yüzden bir ön işleme (preprocessing) adımı gerekiyor:
- Metin sayıya çevriliyor (tokenization / embedding).
- Kategorik veri sayıya çevriliyor (one-hot encoding gibi).
- Sayılar ölçekleniyor / normalize ediliyor (mesela 0-1 arasına).
- Görüntü piksel matrisine dönüşüyor.

Yani "format" iki aşamalı: toplarken serbest, eğitirken standart (sayısal hale gelmiş olmalı).

## Veri kaynakları neler?

- Hazır veri setleri: Kaggle, Hugging Face Datasets, UCI, data.gov.
- API'ler: servislerden canlı veri çekme (genelde JSON döner).
- Web scraping: sayfalardan veri kazıma (yasal sınırlara dikkat).
- Veritabanları: kurumun kendi SQL/NoSQL verisi.
- Loglar: uygulamanın ürettiği kayıtlar.
- Sensör / IoT: cihazlardan gelen ölçümler.
- Elle üretim veya etiketleme.

## Kısa bir not (veri bölme)

Model eğitirken veri genelde üçe ayrılıyor: eğitim (train), doğrulama (validation), test.
Amaç modelin ezber yapmadığını (overfitting), görmediği veride de çalıştığını kontrol etmek.
