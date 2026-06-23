#!/usr/bin/env python3
"""Decide whether a Markdown source change should trigger translation.

This is intentionally dependency-free. It is a starter heuristic for documentation
repositories, not a full Markdown semantic-diff engine.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path
from typing import Iterable


# Adjust this expression to match your repository's standalone channel-tag syntax.
# Examples recognized by default:
#   <!-- ve -->
#   <!-- ive -->
#   <!-- note -->
#   <ve>
#   <ive>
#   <note>
CHANNEL_TAG_PATTERN = re.compile(
    r"^\s*(?:<!--\s*(?:ve|ive|note|ve&ive|ve\|ive)\s*-->|<(?:ve|ive|note|ve&ive|ve\|ive)>)\s*$",
    re.IGNORECASE,
)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    except UnicodeDecodeError as exc:
        raise SystemExit(f"Cannot decode UTF-8 Markdown file: {path}: {exc}") from exc


def strip_frontmatter(lines: list[str]) -> list[str]:
    """Remove one leading YAML frontmatter block if present."""
    if not lines or lines[0].strip() != "---":
        return lines

    for index in range(1, len(lines)):
        if lines[index].strip() in {"---", "..."}:
            return lines[index + 1 :]

    # Unclosed frontmatter is treated as normal content to avoid hiding a real change.
    return lines


def is_ignored_line(line: str) -> bool:
    stripped = line.strip()
    return not stripped or bool(CHANNEL_TAG_PATTERN.fullmatch(stripped))


def normalized_lines(path: Path) -> list[str]:
    lines = strip_frontmatter(read_text(path).splitlines())
    return [line.strip() for line in lines if not is_ignored_line(line)]


def changed_preview(baseline: Iterable[str], updated: Iterable[str], limit: int = 10) -> list[str]:
    matcher = difflib.SequenceMatcher(a=list(baseline), b=list(updated), autojunk=False)
    preview: list[str] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue

        if tag in {"replace", "delete"}:
            preview.extend(f"- {line}" for line in matcher.a[i1:i2])
        if tag in {"replace", "insert"}:
            preview.extend(f"+ {line}" for line in matcher.b[j1:j2])

        if len(preview) >= limit:
            break

    return preview[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline",
        type=Path,
        help="Path to the previous Chinese Markdown file. Omit for a new document.",
    )
    parser.add_argument("--updated", type=Path, required=True, help="Path to the updated Chinese Markdown file.")
    parser.add_argument(
        "--english",
        type=Path,
        help="Path to the matching English Markdown file. If omitted or missing, no automatic translation is requested for existing documents.",
    )
    args = parser.parse_args()

    if not args.updated.exists():
        parser.error(f"Updated file does not exist: {args.updated}")

    if args.baseline is None or not args.baseline.exists():
        result = {
            "translation_required": True,
            "reason": "new_source_document",
            "details": "No baseline source file was provided or found.",
            "changed_lines_preview": [f"+ {line}" for line in normalized_lines(args.updated)[:10]],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.english is None or not args.english.exists():
        result = {
            "translation_required": False,
            "reason": "no_matching_english_document",
            "details": "The source document exists, but the matching English file is absent.",
            "changed_lines_preview": [],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    baseline = normalized_lines(args.baseline)
    updated = normalized_lines(args.updated)

    if baseline == updated:
        result = {
            "translation_required": False,
            "reason": "only_frontmatter_whitespace_or_channel_tag_changes",
            "details": "No substantive Markdown content changed after normalization.",
            "changed_lines_preview": [],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    result = {
        "translation_required": True,
        "reason": "substantive_markdown_content_changed",
        "details": "Meaningful Markdown content changed after excluding frontmatter, whitespace, and standalone channel tags.",
        "changed_lines_preview": changed_preview(baseline, updated),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
