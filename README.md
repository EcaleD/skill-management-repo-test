# Agent Skills Catalog

[English](README.md) | [简体中文](README.zh-CN.md)

A small public catalog of reusable Agent Skills for technical documentation workflows. The repository stores Skill source files in Git and lets users discover and install them with the [`npx skills`](https://github.com/vercel-labs/skills) CLI.

## About

Coding agents benefit from repository-specific instructions, reliable workflows, and current domain guidance. This repository packages that context as reusable Agent Skills: each Skill is a directory containing a `SKILL.md` file and optional references, scripts, or assets.

The repository is a test catalog for learning how to create, review, publish, install, and update Skills through GitHub or GitLab.

## Skills in this repository

| Product line | Skill | Description |
| :--- | :--- | :--- |
| `docs-platform` | [`technical-doc-translation`](skills/docs-platform/technical-doc-translation/) | Translates or proofreads Chinese Markdown technical documentation while preserving code blocks, URLs, frontmatter, HTML, API identifiers, and Markdown structure. |
| `docs-platform` | [`markdown-translation-change-review`](skills/docs-platform/markdown-translation-change-review/) | Determines whether a change to Chinese Markdown documentation should trigger an English translation update. |

## Installation

The examples below use [TRAE](https://www.trae.ai/) as the target agent. Replace `trae` with another supported agent name when appropriate.

### Browse available Skills

```bash
npx skills add EcaleD/skill-management-repo-test --list
```

### Install a Skill into the current TRAE project

```bash
npx skills add EcaleD/skill-management-repo-test \
  --skill technical-doc-translation \
  --agent trae \
  --yes
```

### Install a Skill globally for TRAE

```bash
npx skills add EcaleD/skill-management-repo-test \
  --skill technical-doc-translation \
  --agent trae \
  --global \
  --yes
```

### Update installed Skills

```bash
# Update all project-level Skills.
npx skills update --project --yes

# Update one project-level Skill.
npx skills update technical-doc-translation --project --yes
```

For a new Skill added to this repository, run `npx skills add <repo> --skill <skill-name>` explicitly. `update` refreshes Skills that are already installed; it does not automatically install newly added Skills.

## Local development

Clone the repository, then validate the catalog before opening a pull request:

```bash
git clone https://github.com/EcaleD/skill-management-repo-test.git
cd skill-management-repo-test

# Validate the catalog layout and required frontmatter.
python3 scripts/validate_skills.py

# Discover local Skills without installing them.
npx skills add . --list
```

For a persistent local TRAE test, install a copied project-level Skill:

```bash
npx skills add . \
  --skill technical-doc-translation \
  --agent trae \
  --copy \
  --yes
```

Edit source files under `skills/`, not the installed copy. Remove the test installation when finished:

```bash
npx skills remove technical-doc-translation --agent trae
```

## Repository layout

```text
skills/
└── <product-line>/
    └── <skill-name>/
        ├── SKILL.md
        ├── references/  # Optional long-form guidance
        ├── scripts/     # Optional deterministic helpers
        └── assets/      # Optional templates and sample files
```

The catalog uses this required layout:

```text
skills/<category>/<skill-name>/SKILL.md
```

- `category` identifies a product line or shared capability area, such as `docs-platform`, `modelark`, `seedance`, or `common`.
- `skill-name` is globally unique and uses lowercase letters, numbers, and hyphens.
- The `name` field in `SKILL.md` must exactly match the `skill-name` directory.
- Keep references, scripts, and assets inside the owning Skill directory.

Do not use `.trae/skills/` as the repository source directory. It is an installation target for TRAE; publishable source files belong under `skills/`.

## Add a new Skill

1. Create a directory such as `skills/modelark/ark-api-integration/`.
2. Add a `SKILL.md` file with required `name` and `description` frontmatter.
3. Add optional `references/`, `scripts/`, or `assets/` only when the Skill needs them.
4. Run `python3 scripts/validate_skills.py` and `npx skills add . --list`.
5. Update this English README, the Chinese README, and `MANIFEST.json`.
6. Open a pull request with the Skill purpose, trigger scenarios, risk notes, and validation result.

## Governance and releases

Use pull requests and CI to review every catalog change. Create Git tags and GitHub or GitLab Releases when you need stable, auditable catalog snapshots. For the complete author, repository-manager, and consumer workflow, see [SKILLS_MANAGEMENT.md](SKILLS_MANAGEMENT.md).

## More information

- [Skills CLI](https://github.com/vercel-labs/skills)
- [Agent Skills specification](https://agentskills.io/specification)
- [Repository management guide](SKILLS_MANAGEMENT.md)

## Disclaimer

This is a test repository for demonstrating Agent Skills catalog management. It does not provide production support or a compatibility guarantee.
