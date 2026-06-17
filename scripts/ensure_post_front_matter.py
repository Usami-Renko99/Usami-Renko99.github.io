from __future__ import annotations

import argparse
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path


POST_EXTENSIONS = {".md", ".markdown"}
DATE_SLUG_PATTERN = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})(?:-(?P<slug>.+))?$")
H1_PATTERN = re.compile(r"^\s*#\s+(.+?)\s*#*\s*$", re.MULTILINE)
ASCII_WORD_PATTERN = re.compile(r"[A-Za-z]")


def has_front_matter(text: str) -> bool:
    text = text.lstrip("\ufeff")
    return text.startswith("---\n") or text.startswith("---\r\n")


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def title_from_heading(text: str) -> str | None:
    match = H1_PATTERN.search(text)
    if not match:
        return None
    title = match.group(1).strip()
    title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)
    title = title.strip("`*_ ")
    return title or None


def split_date_and_slug(path: Path) -> tuple[str | None, str]:
    match = DATE_SLUG_PATTERN.match(path.stem)
    if match:
        return match.group("date"), match.group("slug") or path.stem
    return None, path.stem


def humanize_slug(slug: str) -> str:
    title = slug.replace("-", " ").replace("_", " ").strip()
    if ASCII_WORD_PATTERN.search(title):
        title = " ".join(word[:1].upper() + word[1:] for word in title.split())
    return title or "Untitled"


def default_date(date_prefix: str | None) -> str:
    if date_prefix:
        return f"{date_prefix} 00:00:00 +0800"
    china_time = datetime.now(timezone(timedelta(hours=8)))
    return china_time.strftime("%Y-%m-%d %H:%M:%S +0800")


def build_front_matter(path: Path, body: str) -> str:
    date_prefix, slug = split_date_and_slug(path)
    title = title_from_heading(body) or humanize_slug(slug)
    date = default_date(date_prefix)
    cover = f"/assets/images/blog/{slug}.jpg"

    return "\n".join(
        [
            "---",
            "layout: post",
            f"title: {yaml_quote(title)}",
            f"date: {yaml_quote(date)}",
            f"cover: {cover}",
            'cover_alt: "" # 可选的封面说明',
            'cover_caption: "" # 可选的封面题注',
            "---",
            "",
        ]
    )


def iter_post_files(posts_dir: Path) -> list[Path]:
    if not posts_dir.exists():
        return []
    return sorted(
        path
        for path in posts_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in POST_EXTENSIONS
    )


def ensure_front_matter(path: Path, dry_run: bool = False) -> bool:
    text = path.read_text(encoding="utf-8")
    if has_front_matter(text):
        return False

    body = text.lstrip("\ufeff\r\n")
    newline = "\r\n" if "\r\n" in text else "\n"
    front_matter = build_front_matter(path, body)
    updated = front_matter.replace("\n", newline) + body

    if not dry_run:
        path.write_text(updated, encoding="utf-8", newline="")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add default Jekyll front matter to _posts Markdown files that do not have it."
    )
    parser.add_argument(
        "--posts-dir",
        default="_posts",
        help="Directory containing blog posts. Defaults to _posts.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print files that would be changed without editing them.",
    )
    args = parser.parse_args()

    posts_dir = Path(args.posts_dir)
    changed: list[Path] = []

    for path in iter_post_files(posts_dir):
        if ensure_front_matter(path, dry_run=args.dry_run):
            changed.append(path)

    action = "Would update" if args.dry_run else "Updated"
    if changed:
        for path in changed:
            print(f"{action}: {path}")
    else:
        print("All post Markdown files already have front matter.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
