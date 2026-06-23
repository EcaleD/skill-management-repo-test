# Test Repository: Agent Skills Management Guide

This package is designed for the test repository:

```text
/Users/bytedance/Documents/github/translation-agent
```

If your active test repository has moved, replace that path in the commands below.

## 1. Package Layout

```text
translation-agent/
├── skills/                                      # Source of truth: commit these files
│   ├── technical-doc-translation/
│   │   ├── SKILL.md
│   │   ├── references/translation-rules.md
│   │   └── assets/translation-output-template.md
│   └── markdown-translation-change-review/
│       ├── SKILL.md
│       └── scripts/check_translation_trigger.py
├── scripts/
│   └── validate_skills.py
├── examples/
│   └── translation-trigger/
├── .github/workflows/
│   └── validate-agent-skills.yml
└── SKILLS_MANAGEMENT.md
```

Keep author-maintained Skill source files under `skills/`.

Do **not** use `.agents/skills/` as the source directory for this repository package. `npx skills` installs project-level Skills into an agent-facing location such as `./.agents/skills/`; keeping your published source under `skills/` avoids source/installation overlap during local tests.

## 2. Add the Files to the Test Repository

After downloading and extracting this starter package:

```bash
cd /Users/bytedance/Documents/github/translation-agent

# Extract the archive content into the repository root.
unzip -o ~/Downloads/translation-agent-skills-starter.zip

# Review the files before committing.
git status
git diff -- skills scripts examples .github SKILLS_MANAGEMENT.md
```

If your repository already has a workflow with the same name, merge the `validate-agent-skills.yml` job manually instead of overwriting it.

Add generated local agent-install directories to your existing `.gitignore`:

```gitignore
# Local copies or symlinks created while testing with npx skills
/.agents/skills/
/.codex/skills/
/.claude/skills/
/.cursor/skills/
```

## 3. Validate the Two Source Skills

From the repository root:

```bash
python3 scripts/validate_skills.py
npx skills add . --list
```

Expected discovered Skills:

```text
technical-doc-translation
markdown-translation-change-review
```

The first command validates basic frontmatter and naming. The second asks the Skills CLI to discover Skills in this repository without installing them.

## 4. Test Without Installing

Use `skills use` to provide the Skill to a supported coding agent only for the current task:

```bash
npx skills use .   --skill technical-doc-translation   --agent codex
```

For the second Skill:

```bash
npx skills use .   --skill markdown-translation-change-review   --agent codex
```

This is the safest author workflow when you are iterating rapidly because it does not create a persistent project installation.

## 5. Install a Local Copy for Persistent Project Testing

When you want a persistent local copy for a specific agent:

```bash
npx skills add .   --skill technical-doc-translation   --agent codex   --copy   --yes

npx skills add .   --skill markdown-translation-change-review   --agent codex   --copy   --yes
```

`--copy` creates an independent local copy. Do not edit that installed copy; edit the source under `skills/`, then rerun the install command after changes.

Inspect installed Skills:

```bash
npx skills list
npx skills ls -a codex
```

Remove local test installations:

```bash
npx skills remove technical-doc-translation --agent codex
npx skills remove markdown-translation-change-review --agent codex
```

## 6. Run the Change-Review Example

A substantive body-content change should require translation:

```bash
python3 skills/markdown-translation-change-review/scripts/check_translation_trigger.py   --baseline examples/translation-trigger/baseline.md   --updated examples/translation-trigger/updated-content-change.md   --english examples/translation-trigger/english.md
```

A frontmatter-only change should not require translation:

```bash
python3 skills/markdown-translation-change-review/scripts/check_translation_trigger.py   --baseline examples/translation-trigger/baseline.md   --updated examples/translation-trigger/updated-frontmatter-only.md   --english examples/translation-trigger/english.md
```

A new source document requires translation:

```bash
python3 skills/markdown-translation-change-review/scripts/check_translation_trigger.py   --updated examples/translation-trigger/updated-content-change.md
```

The script emits a JSON decision with `translation_required`, a machine-readable `reason`, and a short changed-lines preview.

## 7. Day-to-Day Author Workflow

```bash
cd /Users/bytedance/Documents/github/translation-agent

# 1. Edit the source-of-truth files.
code skills/technical-doc-translation/SKILL.md
code skills/markdown-translation-change-review/SKILL.md

# 2. Validate the package.
python3 scripts/validate_skills.py
npx skills add . --list

# 3. Try one Skill without a persistent installation.
npx skills use . --skill technical-doc-translation --agent codex

# 4. Commit only source and supporting files.
git add skills scripts examples .github/workflows/validate-agent-skills.yml SKILLS_MANAGEMENT.md
git commit -m "feat(skills): refine translation workflow skills"
git push
```

## 8. Publish the Repository for Other Users

After pushing the repository to GitHub or GitLab, users can install by repository URL or GitHub shorthand.

GitHub:

```bash
npx skills add YOUR_GITHUB_OWNER/translation-agent   --skill technical-doc-translation   --agent codex   --yes
```

GitLab:

```bash
npx skills add https://gitlab.com/YOUR_NAMESPACE/translation-agent   --skill markdown-translation-change-review   --agent codex   --yes
```

Install both Skills in one command:

```bash
npx skills add YOUR_GITHUB_OWNER/translation-agent   --skill technical-doc-translation   --skill markdown-translation-change-review   --agent codex   --yes
```

## 9. Use `npx skills` as a Consumer

```bash
# Discover installable Skills in this repository.
npx skills add YOUR_GITHUB_OWNER/translation-agent --list

# Install a project-level Skill. Project scope is the default.
npx skills add YOUR_GITHUB_OWNER/translation-agent   --skill technical-doc-translation   --agent codex   --yes

# Install a global personal Skill.
npx skills add YOUR_GITHUB_OWNER/translation-agent   --skill technical-doc-translation   --agent codex   --global   --yes

# List project and global installs.
npx skills list
npx skills ls -g

# Check for updates.
npx skills check

# Update a single installed Skill in the current project.
npx skills update technical-doc-translation --project --yes

# Update all project-level installed Skills.
npx skills update --project --yes

# Remove a project-level Skill.
npx skills remove technical-doc-translation --agent codex
```

For published consumers, use `npx skills update` to refresh Skills already installed from your repository. When you add a **new** Skill to the repository, consumers should rerun `npx skills add <repo> --skill <new-skill>` because an update refreshes installed items rather than necessarily installing newly added Skills.

## 10. Release Procedure

Use Git tags to make a published version easy to identify:

```bash
git checkout main
git pull --ff-only

python3 scripts/validate_skills.py
npx skills add . --list

git tag -a v0.1.0 -m "Initial Agent Skills release"
git push origin v0.1.0
```

Create a GitHub Release or GitLab Release from the tag. Keep a short changelog in the release notes:

- Added or changed Skills.
- Changes to triggering conditions.
- Script behavior changes.
- Any compatibility requirements.

## 11. Official References

- Skills CLI: https://github.com/vercel-labs/skills
- Agent Skills specification: https://agentskills.io/specification
- Agent Skills quickstart: https://agentskills.io/skill-creation/quickstart
