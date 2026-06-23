#!/usr/bin/env python3
"""Validate the basic Agent Skills structure in ./skills.

Usage:
    python3 scripts/validate_skills.py
    python3 scripts/validate_skills.py skills
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024


def parse_frontmatter(skill_file: Path) -> dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("Missing opening YAML frontmatter delimiter '---'.")

    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("Missing closing YAML frontmatter delimiter '---'.")

    frontmatter = text[4:end].splitlines()
    data: dict[str, str] = {}
    for line in frontmatter:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        if not line.startswith((" ", "\t")):
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def main() -> int:
    skills_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("skills")
    if not skills_root.is_dir():
        print(f"ERROR: Skills directory not found: {skills_root}", file=sys.stderr)
        return 1

    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    if not skill_files:
        print(f"ERROR: No SKILL.md files found directly under {skills_root}/<skill-name>/", file=sys.stderr)
        return 1

    errors: list[str] = []
    for skill_file in skill_files:
        directory_name = skill_file.parent.name
        try:
            metadata = parse_frontmatter(skill_file)
        except ValueError as exc:
            errors.append(f"{skill_file}: {exc}")
            continue

        name = metadata.get("name", "")
        description = metadata.get("description", "")

        if not name:
            errors.append(f"{skill_file}: Missing required frontmatter field 'name'.")
        elif name != directory_name:
            errors.append(f"{skill_file}: name '{name}' must match directory name '{directory_name}'.")
        elif len(name) > MAX_NAME_LENGTH or not NAME_PATTERN.fullmatch(name):
            errors.append(f"{skill_file}: name '{name}' must use lowercase letters, numbers, and single hyphens only.")

        if not description:
            errors.append(f"{skill_file}: Missing required frontmatter field 'description'.")
        elif len(description) > MAX_DESCRIPTION_LENGTH:
            errors.append(f"{skill_file}: description exceeds {MAX_DESCRIPTION_LENGTH} characters.")

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_files)} skill(s) under {skills_root}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
