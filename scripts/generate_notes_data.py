#!/usr/bin/env python3
"""Generate _data/notes.json from uploaded note files.

PDF-first convention, recommended:
  assets/pdf/<category>/<slug>.pdf

Optional TeX source convention:
  assets/tex/<category>/<slug>.tex

Backward compatibility with the older template is kept:
  assets/notes/<category>/<slug>.pdf
  assets/notes/<category>/<slug>.tex

A PDF alone is enough for a note to appear on the website.  If a TeX file with
the same category and slug also exists, the note card will show an additional
TeX/source link.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "_data"
OUT_FILE = DATA_DIR / "notes.json"
CATEGORIES_FILE = DATA_DIR / "categories.yml"

# Preferred modern locations. The old assets/notes location is still scanned so
# existing files keep working after this update.
PDF_ROOTS = [ROOT / "assets" / "notes", ROOT / "assets" / "pdf"]
TEX_ROOTS = [ROOT / "assets" / "notes", ROOT / "assets" / "tex"]


def read_categories() -> dict[str, dict[str, str]]:
    """Read the small categories.yml file without requiring PyYAML."""
    categories: dict[str, dict[str, str]] = {}
    current: dict[str, str] = {}

    if not CATEGORIES_FILE.exists():
        return categories

    for raw in CATEGORIES_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
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
    """Turn algebraic-geometry/sheaves-v2 style slugs into readable titles."""
    name = Path(slug).name
    words = name.replace("_", "-").split("-")
    return " ".join(w.capitalize() if w else w for w in words)


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return "/" + quote(rel)


def git_last_date(path: Path | None) -> str | None:
    if path is None or not path.exists():
        return None
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


def mtime_date(path: Path | None) -> str | None:
    if path is None or not path.exists():
        return None
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


def scan_files(roots: list[Path], suffix: str) -> dict[tuple[str, str], Path]:
    """Return {(category, slug): path}. Later roots override earlier roots."""
    found: dict[tuple[str, str], Path] = {}
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob(f"*{suffix}")):
            if not path.is_file():
                continue
            rel = path.relative_to(root)
            parts = rel.parts
            if len(parts) < 2:
                # Require <root>/<category>/<file>
                continue
            category = parts[0]
            slug = Path(*parts[1:]).with_suffix("").as_posix()
            found[(category, slug)] = path
    return found


def normalized_lookup(files: dict[tuple[str, str], Path]) -> dict[tuple[str, str], Path]:
    """Return a case-insensitive lookup for matching sibling PDF/TeX files."""
    return {(category.casefold(), slug.casefold()): path for (category, slug), path in files.items()}


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    categories = read_categories()

    pdfs = scan_files(PDF_ROOTS, ".pdf")
    texs = scan_files(TEX_ROOTS, ".tex")
    texs_normalized = normalized_lookup(texs)

    # PDF-first: a note is published only when a PDF exists. TeX is optional and
    # attached only if it shares the same category and slug.
    notes = []
    for category, slug in sorted(pdfs.keys()):
        pdf = pdfs[(category, slug)]
        tex = texs.get((category, slug)) or texs_normalized.get((category.casefold(), slug.casefold()))
        cat = categories.get(category, {})
        category_title = cat.get("title", category.replace("-", " ").title())
        updated = git_last_date(pdf) or mtime_date(pdf)

        notes.append(
            {
                "title": title_from_slug(slug),
                "slug": slug,
                "category": category,
                "category_title": category_title,
                "updated": updated,
                "pdf_url": url_for(pdf),
                "tex_url": url_for(tex) if tex else None,
                "pdf_size": human_size(pdf),
            }
        )

    notes.sort(key=lambda n: (n["category"], n["title"].lower()))
    OUT_FILE.write_text(json.dumps(notes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {OUT_FILE.relative_to(ROOT)} with {len(notes)} PDF notes.")


if __name__ == "__main__":
    main()
