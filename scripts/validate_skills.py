#!/usr/bin/env python3
"""Validate the Agent Skills catalog under ./skills.

Expected layout:
    skills/<category>/<skill-name>/SKILL.md

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
EXPECTED_PARTS = 3  # <category>/<skill-name>/SKILL.md


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

    all_skill_files = sorted(skills_root.rglob("SKILL.md"))
    if not all_skill_files:
        print(
            f"ERROR: No SKILL.md files found under "
            f"{skills_root}/<category>/<skill-name>/.",
            file=sys.stderr,
        )
        return 1

    errors: list[str] = []
    discovered_names: set[str] = set()
    validated_categories: set[str] = set()

    for skill_file in all_skill_files:
        relative_path = skill_file.relative_to(skills_root)
        if len(relative_path.parts) != EXPECTED_PARTS:
            errors.append(
                f"{skill_file}: expected path "
                f"{skills_root}/<category>/<skill-name>/SKILL.md."
            )
            continue

        category_name, directory_name, filename = relative_path.parts
        if filename != "SKILL.md":
            errors.append(f"{skill_file}: expected filename 'SKILL.md'.")
            continue

        if not NAME_PATTERN.fullmatch(category_name):
            errors.append(
                f"{skill_file}: category '{category_name}' must use lowercase "
                "letters, numbers, and single hyphens only."
            )

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
            errors.append(
                f"{skill_file}: name '{name}' must match directory name "
                f"'{directory_name}'."
            )
        elif len(name) > MAX_NAME_LENGTH or not NAME_PATTERN.fullmatch(name):
            errors.append(
                f"{skill_file}: name '{name}' must use lowercase letters, "
                "numbers, and single hyphens only."
            )
        elif name in discovered_names:
            errors.append(f"{skill_file}: duplicate skill name '{name}'.")
        else:
            discovered_names.add(name)

        if not description:
            errors.append(f"{skill_file}: Missing required frontmatter field 'description'.")
        elif len(description) > MAX_DESCRIPTION_LENGTH:
            errors.append(
                f"{skill_file}: description exceeds "
                f"{MAX_DESCRIPTION_LENGTH} characters."
            )

        validated_categories.add(category_name)

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(all_skill_files)} skill(s) in "
        f"{len(validated_categories)} category/categories under {skills_root}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
