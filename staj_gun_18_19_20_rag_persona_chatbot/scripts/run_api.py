"""Yerel FastAPI sunucusunu proje kokunden calistiran yardimci komut."""

from __future__ import annotations

import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOCAL_PACKAGES = PROJECT_ROOT / ".python-packages"
if LOCAL_PACKAGES.exists() and sys.version_info[:2] == (3, 12):
    sys.path.insert(0, str(LOCAL_PACKAGES))
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("HF_HOME", str(PROJECT_ROOT / ".model-cache"))

import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=int(os.getenv("API_PORT", "8000")), reload=False)
