"""
run_benchmark.py — PyTorch vs TensorFlow benchmark orkestratörü.

Her konfigürasyonu ayrı bir subprocess'te (bench_worker.py) çalıştırır,
sonuçları toplar, ekrana düzgün bir RAPOR basar ve `benchmark_raporu.txt`
dosyasına kaydeder.

Kullanım:
    python run_benchmark.py

Not: TensorFlow, Windows'ta GPU'yu native göremez (TF 2.11+). Bu yüzden TF
büyük ihtimalle CPU'da çalışır ve raporda bu AÇIKÇA belirtilir.
"""

import subprocess
import sys
import os
import json
import datetime

# Windows konsolu cp1254 (Türkçe) olduğunda '→' gibi karakterler çökertiyor;
# çıktıyı UTF-8'e sabitliyoruz.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
WORKER = os.path.join(HERE, "bench_worker.py")
PY = sys.executable
REPORT_FILE = os.path.join(HERE, "benchmark_raporu.txt")


def probe(code):
    """Küçük bir kod parçasını çalıştırıp stdout'unu döndürür (yoksa None)."""
    try:
        out = subprocess.run([PY, "-c", code], capture_output=True, text=True, timeout=120)
        return out.stdout.strip()
    except Exception:
        return None


def run_worker(framework, device, label):
    print(f"  → Çalışıyor: {label} ...", flush=True)
    cmd = [PY, WORKER, "--framework", framework, "--device", device]
    proc = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    for line in output.splitlines():
        if line.startswith("RESULT_JSON="):
            r = json.loads(line[len("RESULT_JSON="):])
            print(f"     bitti: {r['elapsed_sec']:.2f} s, {r['throughput']:.0f} görüntü/sn", flush=True)
            return r
        if line.startswith("ERROR_JSON="):
            e = json.loads(line[len("ERROR_JSON="):])
            print(f"     atlandı ({label}): {e['error']}", flush=True)
            return None
    print(f"     atlandı ({label}): sonuç alınamadı", flush=True)
    return None


def build_report(results):
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

    # Ortam bilgisi (GPU'lu PyTorch sonucundan)
    gpu_line = "GPU           : (bulunamadı)"
    cuda_ver = "-"
    torch_ver = tf_ver = "-"
    for r in results:
        if r["framework"] == "PyTorch" and r["device"] == "GPU":
            vram = r.get("vram_total_gb", "?")
            gpu_line = f"GPU           : {r['device_name']} ({vram} GB VRAM)"
            cuda_ver = r.get("cuda", "-")
            torch_ver = r["version"]
        elif r["framework"] == "PyTorch":
            torch_ver = r["version"]
        elif r["framework"] == "TensorFlow":
            tf_ver = r["version"]

    tf_note = ""
    for r in results:
        if r["framework"] == "TensorFlow" and r["device"] == "CPU":
            tf_note = "  (CPU — Windows'ta GPU desteklenmiyor)"

    # Hızlanma için taban: en düşük throughput
    base = min((r["throughput"] for r in results), default=1.0)

    L = []
    L.append("=" * 66)
    L.append("      PyTorch vs TensorFlow  —  BENCHMARK RAPORU")
    L.append("=" * 66)
    L.append(f" Tarih         : {now}")
    L.append(f" {gpu_line}")
    L.append(f" CUDA (torch)  : {cuda_ver}")
    L.append(f" PyTorch       : {torch_ver}")
    L.append(f" TensorFlow    : {tf_ver}{tf_note}")
    L.append(" İş yükü       : Sentetik veri (3x32x32), aynı CNN, batch=64,")
    L.append("                 200 ölçülen adım (12.800 görüntü), 30 adım warm-up dışı")
    L.append("-" * 66)
    L.append(f" {'Konfigürasyon':<26}{'Süre(s)':>9}{'Görüntü/sn':>13}{'Hızlanma':>11}")
    L.append("-" * 66)
    for r in results:
        name = f"{r['framework']} — {r['device']}"
        if r["framework"] == "PyTorch" and r["device"] == "GPU":
            name = f"PyTorch — GPU (4050)"
        speed = r["throughput"] / base
        L.append(f" {name:<26}{r['elapsed_sec']:>9.2f}{r['throughput']:>13.0f}{speed:>10.1f}x")
    L.append("-" * 66)

    # Sonuç cümlesi
    best = max(results, key=lambda r: r["throughput"])
    worst = min(results, key=lambda r: r["throughput"])
    if best is not worst:
        factor = best["throughput"] / worst["throughput"]
        L.append(f" Sonuç: En hızlı '{best['framework']} — {best['device']}',")
        L.append(f"        en yavaş '{worst['framework']} — {worst['device']}' konfigürasyonuna")
        L.append(f"        göre ~{factor:.1f}x daha hızlı.")
        gpu_res = next((r for r in results if r["framework"] == "PyTorch" and r["device"] == "GPU"), None)
        if gpu_res:
            L.append(f"        RTX 4050 (PyTorch GPU) tepe VRAM kullanımı: "
                     f"{gpu_res.get('vram_peak_gb', '?')} GB")
    L.append("=" * 66)
    L.append(" Not: Bu bir HAM EĞİTİM HIZI (throughput) kıyasıdır. Sentetik veri")
    L.append(" kullanılır; amaç iki framework'ün compute hızını izole ölçmektir.")
    L.append("=" * 66)
    return "\n".join(L)


def main():
    print("PyTorch vs TensorFlow benchmark başlıyor...\n", flush=True)

    has_torch = probe("import torch;print('ok')") == "ok"
    has_cuda = probe("import torch;print(torch.cuda.is_available())") == "True"
    has_tf = probe("import tensorflow;print('ok')") == "ok"

    print(f"Ortam: torch={'var' if has_torch else 'YOK'}, "
          f"CUDA={'var' if has_cuda else 'YOK'}, "
          f"tensorflow={'var' if has_tf else 'YOK'}\n", flush=True)

    plan = []
    if has_torch and has_cuda:
        plan.append(("pytorch", "cuda", "PyTorch — GPU (4050)"))
    if has_torch:
        plan.append(("pytorch", "cpu", "PyTorch — CPU"))
    if has_tf:
        plan.append(("tensorflow", "cuda", "TensorFlow (otomatik cihaz)"))

    if not plan:
        print("Çalıştırılacak hiçbir framework bulunamadı. torch/tensorflow kurulu mu?")
        return

    results = []
    for framework, device, label in plan:
        r = run_worker(framework, device, label)
        if r:
            results.append(r)

    if not results:
        print("\nHiçbir konfigürasyon başarıyla tamamlanamadı.")
        return

    report = build_report(results)
    print("\n" + report)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report + "\n")
    print(f"\nRapor kaydedildi: {REPORT_FILE}")


if __name__ == "__main__":
    main()
