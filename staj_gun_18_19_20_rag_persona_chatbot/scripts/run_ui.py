"""Basit HTTP sunucusu ile statik UI dosyalarini sunar."""

import argparse
import http.server
import os
import socketserver
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
UI_DIR = PROJECT_ROOT / "ui"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI_DIR), **kwargs)
        
    def log_message(self, format, *args):
        # Sadece hata mesajlarini logla, HTTP erisim loglarini gizle
        pass

def main():
    parser = argparse.ArgumentParser(description="Static UI server")
    parser.add_argument("--port", type=int, default=8501)
    args = parser.parse_args()

    port = int(os.environ.get("STREAMLIT_PORT", args.port))

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"UI Sunucusu baslatildi. Port: {port}")
        print(f"Dizin: {UI_DIR}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nUI Sunucusu kapaniyor...")

if __name__ == "__main__":
    main()
