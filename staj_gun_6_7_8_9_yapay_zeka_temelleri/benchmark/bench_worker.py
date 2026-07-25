"""
bench_worker.py — Tek bir konfigürasyonu (framework + cihaz) çalıştırıp
sonucu tek satır JSON olarak basar. Orkestratör (run_benchmark.py) bunu
subprocess olarak çağırır; böylece PyTorch ve TensorFlow birbirinin GPU/bellek
bağlamına karışmaz.

Ölçüm metodolojisi (arkadaşınkinden farkı):
  - CIFAR10 BOYUTUNDA (3x32x32) sentetik rastgele veri kullanılır. Amaç ham
    eğitim (compute) hızını ölçmek olduğu için indirme/veri yükleme gürültüsü
    devre dışı bırakılır ve kıyas tam tekrarlanabilir olur.
  - Warm-up adımları ölçüm DIŞI tutulur (cudnn algoritma seçimi + ısınma).
  - Sabit iş yükü: her konfigürasyon aynı sayıda adımı işler (adil kıyas).
  - GPU'da doğru süre için torch.cuda.synchronize() kullanılır.
  - Süre + throughput (görüntü/sn) + tepe VRAM raporlanır.
"""

import argparse
import json
import sys
import time

# --- Tüm konfigürasyonlar için ortak, adil ayarlar ---
BATCH_SIZE = 64
WARMUP_BATCHES = 30       # ölçüm dışı ısınma
TIMED_BATCHES = 200       # ölçülen iş yükü -> 200 * 64 = 12.800 görüntü
POOL = 64                 # farklı batch sayısı (döngüsel kullanılır)
NUM_CLASSES = 10


def run_pytorch(device_str):
    import torch
    import torch.nn as nn
    import torch.optim as optim

    device = torch.device(device_str)
    torch.manual_seed(0)

    class SimpleCNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
            self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
            self.pool = nn.MaxPool2d(2, 2)
            self.fc1 = nn.Linear(64 * 8 * 8, 64)
            self.fc2 = nn.Linear(64, 10)
            self.relu = nn.ReLU()

        def forward(self, x):
            x = self.pool(self.relu(self.conv1(x)))
            x = self.pool(self.relu(self.conv2(x)))
            x = x.view(x.size(0), -1)
            x = self.relu(self.fc1(x))
            return self.fc2(x)

    if device_str == "cuda":
        torch.backends.cudnn.benchmark = True

    # Sentetik veri havuzu (CIFAR10 boyutunda), doğrudan cihazda tutulur.
    X = torch.randn(POOL, BATCH_SIZE, 3, 32, 32, device=device)
    Y = torch.randint(0, NUM_CLASSES, (POOL, BATCH_SIZE), device=device)

    model = SimpleCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    model.train()

    def step(i):
        j = i % POOL
        optimizer.zero_grad()
        loss = criterion(model(X[j]), Y[j])
        loss.backward()
        optimizer.step()

    # --- Warm-up (ölçüm dışı) ---
    for i in range(WARMUP_BATCHES):
        step(i)
    if device_str == "cuda":
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()

    # --- Ölçülen kısım ---
    t0 = time.perf_counter()
    for i in range(TIMED_BATCHES):
        step(i)
    if device_str == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - t0

    images = TIMED_BATCHES * BATCH_SIZE
    res = {
        "framework": "PyTorch",
        "version": torch.__version__,
        "device": "GPU" if device_str == "cuda" else "CPU",
        "device_name": torch.cuda.get_device_name(0) if device_str == "cuda" else "CPU",
        "cuda": torch.version.cuda if device_str == "cuda" else None,
        "images": images,
        "elapsed_sec": elapsed,
        "throughput": images / elapsed,
    }
    if device_str == "cuda":
        p = torch.cuda.get_device_properties(0)
        res["vram_total_gb"] = round(p.total_memory / 1024 ** 3, 2)
        res["vram_peak_gb"] = round(torch.cuda.max_memory_allocated() / 1024 ** 3, 2)
    return res


def run_tensorflow(device_str):
    import os
    if device_str == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    import numpy as np
    import tensorflow as tf
    from tensorflow.keras import layers, models

    np.random.seed(0)
    gpus = tf.config.list_physical_devices("GPU")
    for g in gpus:
        try:
            tf.config.experimental.set_memory_growth(g, True)
        except Exception:
            pass
    device_used = "GPU" if gpus else "CPU"

    # Sentetik veri havuzu (CIFAR10 boyutunda, NHWC).
    X = np.random.randn(POOL, BATCH_SIZE, 32, 32, 3).astype("float32")
    Y = np.random.randint(0, NUM_CLASSES, (POOL, BATCH_SIZE)).astype("int64")

    model = models.Sequential([
        layers.Input((32, 32, 3)),
        layers.Conv2D(32, 3, activation="relu", padding="same"),
        layers.MaxPooling2D(2),
        layers.Conv2D(64, 3, activation="relu", padding="same"),
        layers.MaxPooling2D(2),
        layers.Flatten(),
        layers.Dense(64, activation="relu"),
        layers.Dense(10),  # logit -> from_logits=True
    ])
    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    )

    def step(i):
        j = i % POOL
        model.train_on_batch(X[j], Y[j])

    # Warm-up (ölçüm dışı)
    for i in range(WARMUP_BATCHES):
        step(i)

    # Ölçülen kısım
    t0 = time.perf_counter()
    for i in range(TIMED_BATCHES):
        step(i)
    elapsed = time.perf_counter() - t0

    images = TIMED_BATCHES * BATCH_SIZE
    return {
        "framework": "TensorFlow",
        "version": tf.__version__,
        "device": device_used,
        "device_name": gpus[0].name if device_used == "GPU" else "CPU",
        "cuda": None,
        "images": images,
        "elapsed_sec": elapsed,
        "throughput": images / elapsed,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--framework", required=True, choices=["pytorch", "tensorflow"])
    ap.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    args = ap.parse_args()

    try:
        if args.framework == "pytorch":
            result = run_pytorch(args.device)
        else:
            result = run_tensorflow(args.device)
        print("RESULT_JSON=" + json.dumps(result))
    except Exception as e:
        print("ERROR_JSON=" + json.dumps({
            "framework": args.framework, "device": args.device, "error": repr(e),
        }))
        sys.exit(0)  # orkestratörü düşürme
