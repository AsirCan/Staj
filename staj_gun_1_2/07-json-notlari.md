# JSON Notları

Staj 1. hafta, JSON ile ilgili araştırma notlarım.

## JSON nedir?

JSON (JavaScript Object Notation), verinin metin olarak yazılıp taşınma biçimi. Adında
JavaScript geçiyor ama artık her dilde kullanılıyor, dile bağlı değil. En güzel tarafı
hem insanın hem makinenin kolay okuyabilmesi.

Python'daki dict (sözlük) yapısına neredeyse birebir benziyor. Anahtar-değer mantığıyla
çalışıyor. Küçük bir örnek:

```json
{
  "ad": "Asir",
  "yas": 22,
  "aktif": true,
  "diller": ["Python", "JavaScript"],
  "adres": null
}
```

Temel tipleri: metin (string), sayı (number), true/false, null, dizi ([]) ve nesne ({}).
Nesneler ve diziler iç içe girebiliyor, yani karmaşık veriyi de rahat tutuyor.

## Neden önemli?

- Ortak dil gibi: Farklı sistemler (mesela bir web sitesi ile bir sunucu) veriyi JSON ile
  konuşuyor. Herkes anlıyor.
- Basit ve hafif: XML'e göre daha az yer kaplıyor, okuması daha kolay.
- Dilden bağımsız: Python, JavaScript, Java, C# hepsi JSON okuyup yazabiliyor.
- Esnek: Sabit bir şema zorunlu değil, veriyi olduğu gibi taşıyabiliyorsun.

## Yapay zekada nerede kullanılıyor?

Araştırınca gördüm ki gerçekten her yerde:

- API istek/cevapları: Model servislerine (OpenAI, Hugging Face gibi) istek atarken ve cevap
  alırken veri JSON formatında gidip geliyor.
- Ayar / config dosyaları: Eğitim ayarları, hiperparametreler genelde JSON'da tutuluyor.
- Veri setleri: Özellikle JSONL formatı (her satır ayrı bir JSON) eğitim verilerinde çok yaygın.
- Etiketleme: Görüntü veya metin etiketleri (label) çoğunlukla JSON ile saklanıyor.

### JSONL nedir?

Normal JSON tek bir büyük yapıdır. JSONL'de ise her satır ayrı bir JSON kaydıdır:

```
{"soru": "nasilsin", "cevap": "iyiyim"}
{"soru": "hava nasil", "cevap": "gunesli"}
```

Bu format büyük veri setlerinde işe yarıyor çünkü dosyanın tamamını belleğe almadan
satır satır okuyabiliyorsun.

## Kısa not

Bu konunun kod tarafını `03-json-denemeleri.py` dosyasında denedim (dict ile JSON arasında
dönüşüm, dosyaya yazıp okuma, iç içe JSON ve JSONL).
