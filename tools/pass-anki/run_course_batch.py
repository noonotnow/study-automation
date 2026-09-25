#!/usr/bin/env python3
"""Generate Anki cards for a predefined group of PASS course decks."""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "tools/pass-anki/pass_anki_generator.py"
DECKS = {
    "1": ROOT / "inputs/pass/Ch. 1 The Low Energy State Sept 2022.ppt",
    "2": ROOT / "inputs/pass/Ch. 2 Vitamins, Minerals, and Trace Elements Jun 2022.ppt",
    "3": ROOT / "inputs/pass/Ch. 3 Biochemistry Jun 2022.ppt",
    "4": ROOT / "inputs/pass/Ch. 4 Protein Structure Jun 2022.ppt",
    "5": ROOT / "inputs/pass/Ch. 5 Enzymes Jun 2022.ppt",
    "6": ROOT / "inputs/pass/Ch. 6 Anabolic Pathways Jun 2022.pptx",
    "7": ROOT / "inputs/pass/Ch. 7 Anemias Jun 2022.ppt",
    "8": ROOT / "inputs/pass/ch-08-clotting-system-jun-2022.ppt",
    "9": ROOT / "inputs/pass/ch-09-catabolic-pathways-jun-2022.ppt",
}
BATCHES = {
    "1-3": ("1", "2", "3"),
    **{chapter: (chapter,) for chapter in "456789"},
}


def prefix_media_files(output: Path, chapter: str) -> None:
    media = output / "media"
    if not media.is_dir():
        return

    replacements = {}
    for source in media.iterdir():
        if source.is_file():
            target_name = f"ch{int(chapter):02d}_{source.name}"
            source.rename(media / target_name)
            replacements[source.name] = target_name

    for filename in ("cards.tsv", "cards.txt"):
        path = output / filename
        if path.exists():
            content = path.read_text(encoding="utf-8")
            for old, new in replacements.items():
                content = content.replace(f'src="{old}"', f'src="{new}"')
            path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("selection", choices=(*BATCHES, "custom"))
    parser.add_argument("--output", type=Path, default=Path(".run/output"))
    parser.add_argument("--deck-path", type=Path, help="Repo-relative .ppt/.pptx path for a custom deck")
    args = parser.parse_args()

    if args.selection == "custom":
        if args.deck_path is None:
            parser.error("Choose a .ppt or .pptx path when selection is custom")
        deck = (ROOT / args.deck_path).resolve()
        if not deck.is_relative_to(ROOT) or not deck.is_file():
            parser.error("Custom deck path must name a file inside this repository")
        if deck.suffix.lower() not in {".ppt", ".pptx"}:
            parser.error("Custom deck path must end in .ppt or .pptx")
        selected = [(None, deck)]
    else:
        if args.deck_path is not None:
            parser.error("--deck-path is only used with the custom selection")
        selected = [(chapter, DECKS[chapter]) for chapter in BATCHES[args.selection]]

    output_root = args.output if args.output.is_absolute() else ROOT / args.output
    output_root.mkdir(parents=True, exist_ok=True)
    for chapter, deck in selected:
        if not deck.is_file():
            raise SystemExit(f"Deck not found: {deck.relative_to(ROOT)}")
        label = f"custom-{re.sub(r'[^A-Za-z0-9_-]+', '-', deck.stem).strip('-')}" if chapter is None else f"chapter-{int(chapter):02d}"
        chapter_output = output_root / label
        print(f"Generating {deck.relative_to(ROOT)} → {chapter_output.relative_to(ROOT)}", flush=True)
        subprocess.run(
            [sys.executable, str(GENERATOR), str(deck), "--output", str(chapter_output)],
            cwd=ROOT,
            check=True,
        )
        if chapter is not None:
            prefix_media_files(chapter_output, chapter)
        shutil.rmtree(chapter_output / "_work", ignore_errors=True)


if __name__ == "__main__":
    main()