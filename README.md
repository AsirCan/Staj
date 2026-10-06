# Staj Çalışmaları

Yapay zeka odaklı stajım boyunca gün gün yaptığım çalışmaların, notların ve projelerin toplandığı repo.

## Günlere Göre İçerik

| Gün | Klasör | Konu |
|-----|--------|------|
| 1–2 | `staj_gun_1_2` | Python temelleri, NumPy, JSON, SQL ve MongoDB denemeleri |
| 4–5 | `staj_gun_4_5(3 tatil)` | Web scraping (BeautifulSoup, Selenium, Scrapy, API reverse engineering), AI kodlama araçları araştırması ve benchmark karşılaştırması |
| 6–9 | `staj_gun_6_7_8_9_yapay_zeka_temelleri` | Olasılık/istatistik, ML ve deep learning temelleri, PyTorch 60 dk Blitz, NLP, Transformer mimarisi, *Attention Is All You Need*, Hugging Face |
| 10 | `staj_gun_10_pytorch_tensor_manipulasyonu` | PyTorch tensor boyut manipülasyonu |
| 11 | `staj_gun_11_pytorch_training_loop` | Sıfırdan training loop ile gizli formülü öğrenme |
| 12 | `staj_gun_12_nn_module_mini_brain` | `nn.Module` ile küçük bir sinir ağı ("mini brain") |
| 13 | `staj_gun_13_ai_muhendisligi_ve_embeddings` | AI mühendisliği, embedding'ler, vektör veritabanları, benzerlik demosu |
| 14 | `staj_gun_14_fine_tuning_rag_mimarileri_ornekleme` | Fine-tuning, RAG mimarileri (Naive, Advanced, GraphRAG, CRAG, Self-RAG, Agentic), chunking ve sampling parametreleri |
| 15 | `staj_gun_15_native_rag_projesi` | Kütüphanesiz (native) RAG: chunking, embedding, arama ve cevap üretimi |
| 16–17 | `staj_gun_16_17_fastapi_ve_agent_temelleri` | FastAPI, HTTP routing, Pydantic, Swagger, CORS ve agent temelleri |
| 18–20 | `staj_gun_18_19_20_rag_persona_chatbot` | **Proje:** Şarkı sözleri üzerinde tema analizi yapan RAG chatbot (ChromaDB + Ollama + FastAPI + Web UI) |

> 3. gün tatil olduğu için ayrı bir klasör yok.

## Kurulum

Python 3.13 ile:

```bash
uv venv --python 3.13 .venv
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
```

GPU'lu PyTorch kurulumu için `requirements.txt` içindeki notlara bakın. Gün 18–20 projesinin kendi kurulum adımları [kendi README dosyasında](staj_gun_18_19_20_rag_persona_chatbot/README.md) yer alıyor.

## Lisans

[MIT](LICENSE)
