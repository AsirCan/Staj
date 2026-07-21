# Hugging Face Ekosistemi

Modern AI dünyasında Hugging Face (HF), açık kaynak modellerin ve veri setlerinin merkezi haline gelmiş bir platform. "AI'nin GitHub'ı" nitelemesi çok yerinde.

---

## Hugging Face Nedir?

Kısa cevap: Hugging Face, açık model ve veri seti paylaşımı için bir platform + üzerinde kurulu kütüphane ekosistemi + aktif bir topluluk.

Uzun cevap: 2016'da chatbot şirketi olarak kurulmuştu. 2018'de `pytorch-pretrained-bert` adında bir kütüphane yayınladılar — BERT'i PyTorch'ta yeniden implement edip kolayca yüklenebilir hale getirdiler. Bu kütüphane sonra `transformers` adını aldı ve NLP camiasının fiilen standardı haline geldi. Bu andan itibaren HF bir platform şirketine dönüştü.

Bugün platformda yaklaşık:

- **500.000+ model**
- **200.000+ veri seti**
- **200.000+ interaktif demo (Space)**
- **Milyonlarca aktif kullanıcı**

Ücretsiz. Hem indirmek hem yüklemek. Bazı büyük dosyalar ve profesyonel bulut GPU'lar için ödemeli katman var ama temel kullanım tamamen ücretsiz.

---

## Neden Bu Kadar Merkezi?

Birkaç sebep:

**Standartlaştırma.** `transformers` kütüphanesi sayesinde her model aynı API ile kullanılıyor:
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")
```
Ne Llama, ne Qwen, ne DeepSeek — hepsi aynı üç satırla yüklenir. Model iç yapısı değişse bile kullanıcı arayüzü sabit.

**Depolama ve dağıtım.** Multi-gigabyte model dosyalarını hostlamak ve indirmek için altyapı sağlıyor. Version control, LFS (Large File Storage) desteği, hızlı CDN.

**Topluluk etkisi.** Yeni bir model yayınlandığında HF'ye yükleniyor. Modelin popülerliği ve kullanım kolaylığı da HF üzerinden ölçülüyor. Bu döngü kendini besliyor.

**Multimodal genişleme.** Sadece NLP değil, artık görüntü (Vision), ses (Audio), video, çok modlu — tüm alanlarda merkez.

---

## Ana Bölümler

### 1) Models (`huggingface.co/models`)

Platformun kalbi. Filtrelenebilir arayüz:

- **Görev:** text-generation, image-classification, translation, ASR (speech-to-text), TTS (text-to-speech), embeddings, image-to-text, visual-question-answering, ...
- **Kütüphane:** PyTorch, TensorFlow, JAX, ONNX, GGUF, safetensors
- **Dil, boyut, lisans, popülerlik, güncelleme tarihi**

Her modelin bir **model card**'ı (README) var. İyi bir card şunları içerir:

- Model açıklaması, mimari detayları
- Eğitim verisi (hangi datasetler)
- Kullanım örneği (çalışan kod snippet)
- Benchmark sonuçları
- Limitasyonlar, bias uyarıları
- Lisans

**Lisans önemi.** Bu genelde göz ardı edilen bir nokta. Örnekler:

- **MIT, Apache 2.0:** tam serbest, ticari kullanım dahil (DeepSeek modelleri MIT).
- **Llama Community License:** Meta'nın lisansı. Ticari kullanımda 700 milyon aylık aktif kullanıcı limiti var.
- **Non-commercial:** Sadece araştırma. Bazı Gemma sürümleri, bazı akademik modeller.
- **OpenRAIL, CreativeML OpenRAIL-M:** Sorumlu kullanım şartlarıyla açık lisans. Stable Diffusion modelleri kullanıyor.

Bir projeyi ürüne çevirirken lisans okumak şart.

### 2) Datasets (`huggingface.co/datasets`)

Aynı mantık, veri setleri için. Klasik NLP datasetleri (SQuAD, GLUE, SuperGLUE, WikiText, C4, Common Crawl), görüntü (ImageNet, CIFAR, LAION), ses (Common Voice, LibriSpeech), video, çok modlu — hepsi orada.

Tek satırda yüklenir:

```python
from datasets import load_dataset
ds = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")
print(ds[0])
```

Streaming desteği var — çok büyük datasetleri (terabyte'larca) diske indirmeden batch batch okuyabiliyor.

Uyarı: bazı büyük datasetler devasa (LAION-5B, RedPajama-Data-v2 gibi). İndirmeden önce boyutu görmek şart.

### 3) Spaces (`huggingface.co/spaces`)

İnteraktif demo hostlama. Genelde Gradio veya Streamlit ile yazılmış web uygulamaları. Bir modelin ne yaptığını kod yazmadan denemek için ideal.

- **Ücretsiz katman:** CPU-only, yavaş ama çalışır.
- **Ücretli katman:** GPU (T4, A10G, A100) — hızlı, ama saatlik fiyatlandırılıyor.

Örnekler: Stable Diffusion demolar, LLM chat arayüzleri, kod düzenleyicileri, ses tanıma, otomatik altyazı — binlerce.

Kendi projemi yayınlamak için de kullanışlı. Bir Gradio uygulaması yazıp GitHub gibi HF'e push edince otomatik deploy oluyor.

### 4) Papers (`huggingface.co/papers`)

Günlük öne çıkan arxiv makaleleri. Yorumlar, ilişkili modeller, tartışma. Alanın nabzını tutmak için pratik. Her makalenin altında topluluk ne düşünüyor görebiliyorsun.

### 5) Leaderboards

İki tanesi kritik:

- **Open LLM Leaderboard.** Açık modeller çeşitli otomatik benchmark'larda (MMLU, ARC, HellaSwag, TruthfulQA, GSM8K, MATH, IFEval, MMLU-Pro, GPQA...). Otomatik ölçüm, ama modellerin bu benchmark'lara overfit olma riski var.
- **LMSYS Chatbot Arena.** İnsanlar iki modelin cevabını kör görüp oy veriyor. Sonuçlar Elo skoruna dönüşüyor. Otomatik benchmark'lardan yavaş güncelleniyor ama daha "gerçekçi" bir kalite sinyali.

Kişisel gözlemim: Open LLM Leaderboard'un tepesindeki modeller çoğunlukla MMLU'ya overfit oluyor. LMSYS Arena Elo daha güvenilir bir metrik.

### 6) Docs

Kütüphane dokümantasyonu. Aşağıdaki kütüphanelerin her birinin ayrı, detaylı, örneklerle dolu dokümantasyonu var.

---

## Ana Kütüphaneler

Hugging Face'in en güçlü yanlarından biri: birbirini tamamlayan bir kütüphane ekosistemi.

### `transformers`

Merkez kütüphane. Modelleri yükleme, ince ayar, inference — hepsi burada. `AutoModel`, `AutoTokenizer`, `pipeline` gibi soyutlamalar sayesinde model tipini bilmeye gerek kalmadan çalıştırılabiliyor.

```python
from transformers import pipeline
generator = pipeline("text-generation", model="gpt2")
print(generator("Merhaba, ben"))
```

Model tipleri: `AutoModelForCausalLM` (metin üretme), `AutoModelForSequenceClassification` (sınıflandırma), `AutoModelForQuestionAnswering`, `AutoModelForMaskedLM`, `AutoModelForImageClassification`, `AutoModelForSpeechSeq2Seq` — düzinelerce.

### `datasets`

Veri seti yükleme, ön işleme, formatlama. Hızlı, streaming destekli, HF Hub ile entegre.

```python
from datasets import load_dataset
ds = load_dataset("imdb")
ds_tokenized = ds.map(lambda x: tokenizer(x["text"]), batched=True)
```

### `tokenizers`

Rust'ta yazılmış çok hızlı tokenizer. Bir dakikada milyonlarca cümle tokenize edebiliyor. `transformers` içinden şeffaf olarak kullanılıyor.

### `accelerate`

Kodunu tek GPU / çoklu GPU / TPU / karışık precision arasında değiştirmeden çalıştırabilmeni sağlayan katman. `torch.distributed` katmanının üstünde bir kolay-kullanım katmanı.

```python
from accelerate import Accelerator
accelerator = Accelerator()
model, optimizer, loader = accelerator.prepare(model, optimizer, loader)
```

Sonrasında `loss.backward()` yerine `accelerator.backward(loss)` diyorsun ve kodun aynı hem tek GPU'da hem 8 GPU'lu dağıtık ortamda çalışıyor.

### `peft` (Parameter-Efficient Fine-Tuning)

LoRA, QLoRA, prefix tuning, prompt tuning gibi teknikler. Modelin tümünü ince ayar etmek yerine sadece küçük bir alt kümesini eğitiyor.

Neden önemli: 7B modeli tamamen ince ayar etmek 100+ GB VRAM istiyor. LoRA ile 7B modelin sadece ~4M parametresi (yani %0.06'sı) eğitiliyor, 12 GB VRAM'e sığıyor. Sonuç kalitesi çoğu zaman full fine-tune ile karşılaştırılabilir. Küçük laboratuvarların ve bireysel kullanıcıların açık modelleri kendine göre uyarlamasının anahtarı.

### `trl` (Transformer Reinforcement Learning)

RLHF, DPO, KTO, PPO — insana hizalama algoritmaları. `SFTTrainer`, `DPOTrainer` gibi hazır sınıflarla açık kaynak modelleri "sohbet modu"na getirmenin standart yolu.

### `diffusers`

Diffusion modelleri için (Stable Diffusion, SDXL, Flux). `transformers`'ın diffusion tarafındaki karşılığı.

```python
from diffusers import StableDiffusionPipeline
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
image = pipe("a cat riding a bicycle").images[0]
```

### `optimum`

Modelleri farklı runtime'larda (ONNX, TensorRT, OpenVINO, Intel Neural Compressor) hızlı çalıştırmak için köprü kütüphane.

### `evaluate`

Metrikler (BLEU, ROUGE, accuracy, F1, perplexity vs.) tek arayüzden.

---

## Model Seçim İpuçları

Kendi donanımına göre hangi modeli seçebileceğine dair genel rehber:

**Boyut vs VRAM ilişkisi (fp16):**

- **1B parametre** → ~2 GB VRAM. 6 GB GPU rahatça, hatta 4 GB da yeter.
- **3B parametre** → ~6 GB. 6 GB GPU'da tam kıvamında.
- **7B parametre** → ~14 GB. 12 GB GPU'da fp16 zor, 4-bit quantize (~4 GB) ile 6-8 GB GPU'da çalışır.
- **13B parametre** → ~26 GB. 24 GB GPU (RTX 3090/4090) veya 4-bit quantize.
- **34B, 70B** → 40+ GB. Multi-GPU veya server-grade donanım gerekli.

**Quantization**  büyük modelleri küçük donanıma sığdırmanın en pratik yolu. GGUF formatı (llama.cpp uyumlu) 8-bit, 6-bit, 5-bit, 4-bit, hatta 2-bit sürümlerini içeriyor. `TheBloke`, `bartowski`, `Qwen`, `LM Studio Community` gibi kullanıcılar/organizasyonlar birçok popüler modelin GGUF sürümlerini yükleyip paylaşıyorlar.

**Base vs Instruct/Chat farkı:** `-base` modeller sadece next-token tahmini yapabiliyor, sohbet formatı bilmiyor. `-Instruct`, `-Chat` sonekli sürümler ise SFT + RLHF geçmiş, sohbet formatı öğrenmiş. Bir chatbot yapmak istiyorsan mutlaka Instruct/Chat sürümünü seçmek lazım.

---

## Küçük "Hello World" Örneği

Küçük bir modeli lokal GPU'da (RTX 4050 Laptop, 6 GB VRAM) çalıştırmak için pratik bir şablon:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Kişisel GPU'ya rahatça sığan bir model — 0.5B, fp16 modda ~1 GB
model_id = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="cuda",       # doğrudan GPU'ya yükle
)

# Sohbet formatında mesajları hazırla
messages = [
    {"role": "system", "content": "Sen yardımsever bir asistansın."},
    {"role": "user", "content": "Merhaba, kısaca kendini tanıtır mısın?"},
]

# Modelin beklediği formata (chat template) dönüştür
prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)

# Tokenize et, GPU'ya taşı
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

# Üret
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=True,
        top_p=0.9,
        temperature=0.7,
    )

# Decode et — sadece üretilen kısmı al (prompt'u atlayarak)
generated = outputs[0][inputs.input_ids.shape[1]:]
print(tokenizer.decode(generated, skip_special_tokens=True))
```

İlk çalıştırma modeli indirir (~1 GB). Sonraki çalıştırmalar disk cache'ten yükler (birkaç saniye).

Kurulum:
```bash
pip install transformers accelerate torch
```

---

## Şu Anki Trend Modeller

Genel gözlemim (2026 ortası itibariyle):

**Genel LLM'ler:**
- **DeepSeek V3 / R1** — açık kaynağın en güçlüsü, GPT-4 sınıfı.
- **Qwen 3** (72B, 32B) — Alibaba'nın yeni sürümü, çok dilli, güçlü.
- **Llama 3.3 70B** — Meta'nın açık sürümü, agent yeteneklerinde iyi.
- **Mistral Large 2** — Mistral'ın kapalı ama API'li amiral gemisi.

**Küçük ölçekli (SLM — Small Language Model):**
- **Phi-3, Phi-4** (Microsoft) — 3-14B, veri kalitesine yatırım.
- **Qwen 2.5 (0.5B - 3B)** — küçük ama kapasiteli.
- **Gemma 2 (2B, 9B)** (Google) — geniş bağlam, açık kaynak.
- **SmolLM (HuggingFace)** — 135M, 360M, 1.7B — edge deployment için.

**Kod:**
- **DeepSeek Coder V2, V3**
- **Qwen 2.5-Coder**
- **Codestral (Mistral)**

**Multimodal:**
- **Qwen 2.5-VL** — vision-language
- **Llama 3.2 Vision**
- **Phi-3.5 Vision**

**Ses:**
- **Whisper-large-v3** (OpenAI, açık) — ASR
- **Distil-Whisper** — hızlı ASR
- **Piper, Kokoro, XTTS-v2** — TTS

**Embedding:**
- **BAAI/bge-m3** — çok dilli, çok fonksiyonlu (dense + sparse + colbert)
- **intfloat/multilingual-e5-large**
- **jinaai/jina-embeddings-v3**

**Görüntü üretimi:**
- **Stable Diffusion 3, SDXL, FLUX.1** — açık kaynak
- **Midjourney, DALL-E 3, Ideogram** — kapalı

---

## Genel İzlenim

Hugging Face'in ekosistemdeki yerini bir cümlede özetlemem gerekirse: **açık AI'nin altyapısı**. Model geliştiricileri modellerini oraya yayınlıyor, uygulama geliştiricileri oradan indirip kullanıyor, araştırmacılar makalelerini oraya bağlıyor, meraklılar oradan öğreniyor.

Kapalı kaynaklı modeller (GPT, Claude, Gemini) bir API ile erişilebiliyor ama tam kontrol ve maliyet-verimliliği için HF üzerinden erişilen açık modeller çok değerli. Özellikle:

- **Prototipleme** — hızlı test için küçük modeller
- **Domain-specific ince ayar** — kendi verine göre model eğitmek
- **Offline / on-premise deployment** — veri gizliliği önemli olduğunda
- **Maliyet kontrolü** — API başına para vermek yerine kendi GPU'nda çalıştırmak
- **Öğrenme** — modelin içine bakabilmek, deneyler yapabilmek

Bir AI mühendisliği kariyeri düşünen için Hugging Face'i etkin kullanmayı öğrenmek neredeyse zorunlu bir beceri.
