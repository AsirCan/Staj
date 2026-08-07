# Gün 18–20 Proje Raporu: Kanye West RAG Persona Chatbot

## Amaç

Bu çalışma, Kanye West'in seçilmiş 30 şarkısından alınan sözleri RAG mimarisinde kullanarak kullanıcının sorularına tema ve duygu odaklı yanıt üreten yerel bir chatbot geliştirir. Sistem, sanatçı gibi davranmaz; kaynak alınan söz parçalarına dayanarak yorum yapar.

## Veri hattı

1. `song_manifest.csv` şarkı adı, albüm, yıl ve kaynak URL'sini tutar.
2. Collector izin onayından sonra hız sınırıyla JSONL üretir. Varsayılan sağlayıcı Lyrics.ovh API'sidir; BeautifulSoup HTML sağlayıcısı, erişim koşulları uygun bir sayfa için alternatif olarak bulunur.
3. Metin temizlenir; satır bütünlüğü korunarak 200–400 karakterlik chunk'lara bölünür.
4. `multilingual-e5-small` her chunk için embedding üretir; metadata ile ChromaDB'ye yazar.

## Retrieval ve persona

Kullanıcı sorusu `query:` ön ekiyle embed edilir. Kosinüs benzerliğine göre ilk üç chunk seçilir. Bu bağlam ve kullanıcı mesajı Ollama'daki `qwen2.5:7b-instruct` modeline verilir. Sistem promptu, yanıtın kullanıcı dilinde olmasını, uydurmamasını, sanatçı kimliğine bürünmemesini ve uzun söz kopyalamamasını ister.

## API sözleşmesi

`POST /api/v1/chat`

```json
{"user_id":"ogrenci_01", "message":"Hangi şarkılarda başarı baskısı öne çıkıyor?"}
```

Yanıt `status`, `persona`, `reply`, `retrieved_context` ve `sources` alanlarını içerir. Vektör veritabanı boşsa 409, Ollama ulaşılamazsa 503 döner. Swagger arayüzü `/docs` yolundadır.

## Web Arayüzü (Dark Monolith Architecture)

Uygulama için özel olarak tasarlanmış koyu tema (**#0a0a0a**) ve cam efekti (`glassmorphism`) içeren yeni bir web arayüzü (`ui/index.html`) geliştirilmiştir:

- **Near-Black Taban (#0a0a0a) & Dot-Grid Dokusu:** %3 opaklıkta noktasal ızgara deseni ve katmanlı derinlik.
- **Canlı Durum Göstergesi:** Yanıp sönen yeşil durum ışığı ile canlı ChromaDB bağlantı durum takibi (`CHROMADB ONLINE • 14ms`).
- **İkon-Odaklı Gezinti Çubuğu:** Aktif gösterge çizgili sol navigasyon rayı.
- **ChromaDB İndeks Gezgini (Modal):** Vektör veritabanı parça sayısını, 384-D boyut bilgisini ve şarkı dağılım şemasını gösteren modal arayüz.
- **Persona & Tema İlişki Grafiği (Modal):** İnanç, Kırılganlık, Aile Sorumluluğu ve Ego temalarını haritalandıran interaktif bilgi grafiği.
- **Komut Paleti Girdisi & Çeviri:** Odaklanma ışımalı arama çubuğu ve tek tıkla `Türkçe'ye Çevir` dinamik çeviri butonu.

## Demo senaryoları

1. **Tema analizi:** `Runaway şarkısında öz eleştiri nasıl işleniyor?`
2. **Şarkı bulma:** `Yalnızlık ve şöhret çatışmasını hangi şarkılar ele alıyor?`
3. **Güvenli sınır:** Veri setinde kanıt bulunmayan bir sanatçı/konu sorusu sorulup modelin belirsizliği belirtmesi gözlemlenir.

## Doğrulama sonuçları

- Lyrics.ovh sağlayıcısıyla 28 şarkılık corpus oluşturuldu; iki başlık sağlayıcıda bulunamadığı için atlandı. Bu sayı hedeflenen 25–40 aralığındadır.
- Corpus, 202 adet 200–400 karakterlik ChromaDB parçasına indekslendi.
- `qwen2.5:7b-instruct` ile Swagger ve Web UI üzerinden gerçek `POST /api/v1/chat` istekleri 200 döndü; yanıt, kaynak şarkı adlarını, renk kodlu benzerlik skorlarını (🟢 yüksek, 🟡 orta, 🔵 düşük) ve çeviri desteğini içerdi.
- Bağlam dışı kontrolünde `Fransa'nın başkenti nedir?` sorusu `insufficient_context` döndü ve kaynak göstermedi.
- Birim/API testleri: `14 passed`.

Ekran görüntüleri `docs/screenshots/` altında hazırdır:

1. `swagger-docs.png` — Swagger üzerinden başarılı canlı API yanıtı.
2. `scenario-1-theme.png` — Tema analizi.
3. `scenario-2-song-search.png` — Şarkı/tema araması.
4. `scenario-3-no-context.png` — Bağlam dışı güvenli geri dönüş.
