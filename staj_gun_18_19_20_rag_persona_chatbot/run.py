"""API ve Streamlit arayuzunu tek komutla baslatir.

Kullanim:
    python run.py
    python run.py --no-browser
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


def is_reachable(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return 200 <= response.status < 300
    except (urllib.error.URLError, TimeoutError):
        return False


def wait_for_api(url: str, timeout_seconds: int = 20) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if is_reachable(url):
            return True
        time.sleep(0.5)
    return False


def terminate(process: subprocess.Popen[object] | None) -> None:
    if process is not None and process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def main() -> int:
    parser = argparse.ArgumentParser(description="Kanye West RAG chatbot baslaticisi")
    parser.add_argument("--api-port", type=int, default=8000)
    parser.add_argument("--ui-port", type=int, default=8501)
    parser.add_argument("--no-browser", action="store_true", help="Tarayiciyi otomatik acmaz.")
    args = parser.parse_args()

    # 0. .env ve ChromaDB indeks otomatik kontrolü
    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        example_file = PROJECT_ROOT / ".env.example"
        if example_file.exists():
            env_file.write_text(example_file.read_text(encoding="utf-8"), encoding="utf-8")

    chroma_dir = PROJECT_ROOT / "data" / "chroma"
    if not chroma_dir.exists() or not any(chroma_dir.iterdir()):
        print("Vektor veritabani (ChromaDB) bulunamadi. Indeks otomatik olusturuluyor...")
        subprocess.run([sys.executable, str(PROJECT_ROOT / "scripts" / "collect_lyrics.py"), "--confirm-permission", "--delay", "1.0"], check=False)
        subprocess.run([sys.executable, str(PROJECT_ROOT / "scripts" / "build_index.py"), "--reset"], check=False)

    if not is_reachable("http://127.0.0.1:11434/api/tags"):
        print("Ollama acik degil. Ollama uygulamasini veya `ollama serve` komutunu baslatin.")
        return 1

    api_env = os.environ.copy()
    api_env["API_PORT"] = str(args.api_port)
    api_process = subprocess.Popen(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "run_api.py")],
        cwd=PROJECT_ROOT,
        env=api_env,
    )

    ui_process: subprocess.Popen[object] | None = None
    try:
        if not wait_for_api(f"{api_url}/api/v1/health"):
            print("API 20 saniye icinde baslayamadi.")
            return 1

        ui_env = os.environ.copy()
        ui_env["API_BASE_URL"] = api_url
        ui_env["STREAMLIT_PORT"] = str(args.ui_port)
        ui_process = subprocess.Popen(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "run_ui.py")],
            cwd=PROJECT_ROOT,
            env=ui_env,
        )

        print(f"API / Swagger: {api_url}/docs")
        print(f"Chat arayuzu: {ui_url}")
        print("Durdurmak için Ctrl+C tuşlarına basın.")
        if not args.no_browser:
            webbrowser.open(ui_url)
        return ui_process.wait()
    except KeyboardInterrupt:
        print("\nSunucular kapatiliyor...")
        return 0
    finally:
        terminate(ui_process)
        terminate(api_process)


if __name__ == "__main__":
    raise SystemExit(main())
