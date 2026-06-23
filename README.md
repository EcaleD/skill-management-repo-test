# Agent Skills Catalog Test Repository

This repository is a test catalog for publishing and managing reusable Agent Skills from GitHub or GitLab. It uses the `npx skills` CLI for discovery and installation.

## Catalog layout

```text
skill-management-repo-test/
├── skills/                                      # Published Skill source of truth
│   └── docs-platform/                            # Product line / category
│       ├── technical-doc-translation/            # Concrete Skill
│       │   ├── SKILL.md
│       │   ├── references/
│       │   │   └── translation-rules.md
│       │   └── assets/
│       │       └── translation-output-template.md
│       └── markdown-translation-change-review/  # Concrete Skill
│           ├── SKILL.md
│           └── scripts/
│               └── check_translation_trigger.py
├── scripts/
│   └── validate_skills.py
├── examples/
│   └── translation-trigger/
├── .github/workflows/
│   └── validate-agent-skills.yml
├── MANIFEST.json
└── SKILLS_MANAGEMENT.md
```

The catalog follows this required structure:

```text
skills/<category>/<skill-name>/SKILL.md
```

- `category` is a product line or shared capability area, such as `docs-platform`, `modelark`, `seedance`, or `common`.
- `skill-name` is a globally unique, lowercase, hyphenated Skill identifier.
- The `name` field in each `SKILL.md` must exactly match the `skill-name` directory.
- Keep reusable references, scripts, and assets inside the owning Skill directory.

Do not use `.trae/skills/` as this repository's source directory. That directory is an agent installation target; publishable source files belong under `skills/`.

## Included Skills

| Product line | Skill | Purpose |
|---|---|---|
| `docs-platform` | `technical-doc-translation` | Translate or proofread Chinese Markdown technical documentation while preserving code, URLs, frontmatter, and Markdown structure. |
| `docs-platform` | `markdown-translation-change-review` | Decide whether a Chinese Markdown change should trigger an English translation update. |

## Repository author quick start

Run these commands from the repository root:

```bash
# Validate the catalog's folder structure and frontmatter.
python3 scripts/validate_skills.py

# Ask Skills CLI to discover Skills without installing them.
npx skills add . --list
```

Expected discovered Skills:

```text
technical-doc-translation
markdown-translation-change-review
```

Test a persistent project-level installation for TRAE:

```bash
npx skills add . \
  --skill technical-doc-translation \
  --agent trae \
  --copy \
  --yes
```

`--copy` is recommended for testing because it creates a project-local installed copy. Edit files under `skills/`, not the installed copy.

Remove the local test installation when finished:

```bash
npx skills remove technical-doc-translation --agent trae
```

## Run the change-review example

A substantive content change should require translation:

```bash
python3 skills/docs-platform/markdown-translation-change-review/scripts/check_translation_trigger.py \
  --baseline examples/translation-trigger/baseline.md \
  --updated examples/translation-trigger/updated-content-change.md \
  --english examples/translation-trigger/english.md
```

A frontmatter-only change should not require translation:

```bash
python3 skills/docs-platform/markdown-translation-change-review/scripts/check_translation_trigger.py \
  --baseline examples/translation-trigger/baseline.md \
  --updated examples/translation-trigger/updated-frontmatter-only.md \
  --english examples/translation-trigger/english.md
```

## Install from GitHub

Discover the published catalog:

```bash
npx skills add EcaleD/skill-management-repo-test --list
```

Install one Skill into the current TRAE project:

```bash
npx skills add EcaleD/skill-management-repo-test \
  --skill technical-doc-translation \
  --agent trae \
  --yes
```

Install the translation-change review Skill:

```bash
npx skills add EcaleD/skill-management-repo-test \
  --skill markdown-translation-change-review \
  --agent trae \
  --yes
```

For a personal global TRAE installation, add `--global`:

```bash
npx skills add EcaleD/skill-management-repo-test \
  --skill technical-doc-translation \
  --agent trae \
  --global \
  --yes
```

## Add a new product line or Skill

For a new ModelArk Skill, create:

```text
skills/modelark/ark-api-integration/SKILL.md
```

Then ensure:

1. `name: ark-api-integration` appears in the YAML frontmatter.
2. The `description` explains both the capability and when an agent should use it.
3. `python3 scripts/validate_skills.py` and `npx skills add . --list` succeed.
4. You update this README and `MANIFEST.json`.

See [SKILLS_MANAGEMENT.md](SKILLS_MANAGEMENT.md) for the author, repository-manager, and consumer workflow.

## References

- [Skills CLI](https://github.com/vercel-labs/skills)
- [Agent Skills specification](https://agentskills.io/specification)
