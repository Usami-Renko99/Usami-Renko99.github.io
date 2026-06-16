#!/usr/bin/env bash
set -euo pipefail
python3 scripts/generate_notes_data.py
python3 scripts/generate_music_data.py
bundle exec jekyll serve
