#!/usr/bin/env python3
"""Generate _data/notes.json from assets/notes/**.{pdf,tex}.

Convention:
  assets/notes/<category>/<slug>.pdf
  assets/notes/<category>/<slug>.tex

The same basename is treated as one note. Markdown pages are not required.
"""

from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "assets" / "notes"
DATA_DIR = ROOT / "_data"
OUT_FILE = DATA_DIR / "notes.json"
CATEGORIES_FILE = DATA_DIR / "categories.yml"


def read_categories() -> dict[str, dict[str, str]]:
    categories: dict[str, dict[str, str]] = {}
    current: dict[str, str] = {}

    if not CATEGORIES_FILE.exists():
        return categories

    for raw in CATEGORIES_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("-"):
            if current.get("key"):
                categories[current["key"]] = current
            current = {}
            line = line[1:].strip()
            if line and ":" in line:
                k, v = line.split(":", 1)
                current[k.strip()] = v.strip().strip('"').strip("'")
        elif ":" in line:
            k, v = line.split(":", 1)
            current[k.strip()] = v.strip().strip('"').strip("'")

    if current.get("key"):
        categories[current["key"]] = current
    return categories


def title_from_slug(slug: str) -> str:
    name = Path(slug).name
    words = name.replace("_", "-").split("-")
    return " ".join(w.capitalize() if w else w for w in words)


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return "/" + quote(rel)


def git_last_date(path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path.relative_to(ROOT))],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        value = result.stdout.strip()
        return value or None
    except Exception:
        return None


def mtime_date(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")


def human_size(path: Path | None) -> str | None:
    if path is None or not path.exists():
        return None
    size = path.stat().st_size
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return None


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    categories = read_categories()
    paired: dict[tuple[str, str], dict[str, Path]] = {}

    if NOTES_DIR.exists():
        for path in sorted(NOTES_DIR.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".pdf", ".tex"}:
                continue
            rel = path.relative_to(NOTES_DIR)
            parts = rel.parts
            if len(parts) < 2:
                # Require assets/notes/<category>/<file>
                continue
            category = parts[0]
            slug = Path(*parts[1:]).with_suffix("").as_posix()
            key = (category, slug)
            paired.setdefault(key, {})[path.suffix.lower()[1:]] = path

    notes = []
    for (category, slug), files in paired.items():
        pdf = files.get("pdf")
        tex = files.get("tex")
        date_source = pdf or tex
        cat = categories.get(category, {})
        category_title = cat.get("title", category.replace("-", " ").title())
        title = title_from_slug(slug)

        notes.append(
            {
                "title": title,
                "slug": slug,
                "category": category,
                "category_title": category_title,
                "updated": git_last_date(date_source) or mtime_date(date_source),
                "pdf_url": url_for(pdf) if pdf else None,
                "tex_url": url_for(tex) if tex else None,
                "pdf_size": human_size(pdf),
            }
        )

    notes.sort(key=lambda n: (n["category"], n["title"].lower()))
    OUT_FILE.write_text(json.dumps(notes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {OUT_FILE.relative_to(ROOT)} with {len(notes)} notes.")


if __name__ == "__main__":
    main()
