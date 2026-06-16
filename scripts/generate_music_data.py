#!/usr/bin/env python3
"""Generate _data/music.json from uploaded audio files.

Put music files in:
  assets/music/<filename>

Nested folders are supported too:
  assets/music/<album>/<filename>
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "_data"
OUT_FILE = DATA_DIR / "music.json"
MUSIC_ROOT = ROOT / "assets" / "music"

SUPPORTED_EXTENSIONS = {
    ".aac",
    ".flac",
    ".m4a",
    ".mp3",
    ".oga",
    ".ogg",
    ".opus",
    ".wav",
    ".webm",
}


def title_from_path(path: Path) -> str:
    words = path.stem.replace("_", "-").split("-")
    return " ".join(word.capitalize() if word else word for word in words)


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return "/" + quote(rel)


def human_size(path: Path) -> str:
    size = path.stat().st_size
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{size} B"


def mtime_date(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")


def scan_music() -> list[dict[str, str]]:
    if not MUSIC_ROOT.exists():
        return []

    tracks = []
    for path in sorted(MUSIC_ROOT.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        if path.suffix.casefold() not in SUPPORTED_EXTENSIONS:
            continue

        rel = path.relative_to(MUSIC_ROOT).with_suffix("").as_posix()
        tracks.append(
            {
                "title": title_from_path(path),
                "slug": rel,
                "url": url_for(path),
                "size": human_size(path),
                "updated": mtime_date(path),
            }
        )

    return tracks


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tracks = scan_music()
    OUT_FILE.write_text(json.dumps(tracks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {OUT_FILE.relative_to(ROOT)} with {len(tracks)} music tracks.")


if __name__ == "__main__":
    main()
