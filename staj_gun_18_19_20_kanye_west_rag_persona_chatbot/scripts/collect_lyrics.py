"""Izin verilen bir kaynaktan lyrics manifest'indeki sarki sozlerini toplar.

Bu betik varsayilan olarak ag istegi yapmaz. Calistirmak icin kaynak kosullarini
kontrol ettikten sonra --confirm-permission verilmelidir.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = PROJECT_ROOT / "data" / "song_manifest.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "songs.jsonl"
USER_AGENT = "AcademicRAGBot/1.0 (personal coursework; contact: local-user)"


def lyrics_ovh_url(title: str) -> str:
    """Anahtarsiz Lyrics.ovh endpoint'ini guvenli URL biciminde uretir."""
    return f"https://api.lyrics.ovh/v1/{quote('Kanye West', safe='')}/{quote(title, safe='')}"


def extract_lyrics(html: str) -> str:
    """Genius-benzeri sayfalardaki modern ve eski lyrics kapsayicilarini okur."""
    soup = BeautifulSoup(html, "html.parser")
    containers = soup.select("[data-lyrics-container]")
    if not containers:
        containers = soup.select(".lyrics, div.lyrics")
    for container in containers:
        for br in container.select("br"):
            br.replace_with("\n")
    text = "\n".join(container.get_text("\n", strip=True) for container in containers)
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def load_existing(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    return {
        item["title"]: item
        for item in (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    }


def collect(delay_seconds: float, provider: str) -> tuple[int, list[str]]:
    existing = load_existing(OUTPUT_PATH)
    errors: list[str] = []
    with MANIFEST_PATH.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    for row in rows:
        title = row["title"]
        if title in existing:
            continue
        try:
            request_url = lyrics_ovh_url(title) if provider == "lyrics-ovh" else row["source_url"]
            response = requests.get(
                request_url,
                headers={"User-Agent": USER_AGENT},
                timeout=20,
            )
            response.raise_for_status()
            if provider == "lyrics-ovh":
                lyrics = str(response.json().get("lyrics", "")).strip()
            else:
                lyrics = extract_lyrics(response.text)
            if len(lyrics) < 100:
                raise ValueError("Lyrics kapsayicisi bulunamadi veya veri cok kisa.")
            existing[title] = {
                "artist": "Kanye West",
                "title": title,
                "album": row["album"],
                "year": int(row["year"]),
                "lyrics": lyrics,
                "source_url": request_url,
            }
            time.sleep(delay_seconds)
        except (requests.RequestException, ValueError) as exc:
            errors.append(f"{title}: {exc}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False) for item in existing.values()) + "\n",
        encoding="utf-8",
    )
    return len(existing), errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Kanye West lyrics collector")
    parser.add_argument("--confirm-permission", action="store_true", help="Kaynak erisim kosullarini kontrol ettiginizi onaylar.")
    parser.add_argument("--delay", type=float, default=1.5, help="Iki istek arasindaki saniye (varsayilan: 1.5).")
    parser.add_argument(
        "--provider",
        choices=["lyrics-ovh", "html"],
        default="lyrics-ovh",
        help="lyrics-ovh hazir API'yi, html ise manifest'teki BeautifulSoup kaynaklarini kullanir.",
    )
    args = parser.parse_args()
    if not args.confirm_permission:
        parser.error("Ag istegi icin --confirm-permission zorunludur.")
    if args.delay < 1:
        parser.error("Kaynaklari zorlamamak icin --delay en az 1 saniye olmali.")

    collected, errors = collect(args.delay, args.provider)
    print(f"Saglayici: {args.provider}")
    print(f"Kaydedilen sarki sayisi: {collected}")
    if errors:
        print("Atlanan sarkilar:")
        print("\n".join(f"- {error}" for error in errors))


if __name__ == "__main__":
    main()
