---
name: markdown-translation-change-review
description: Review changes to Chinese Markdown documentation and decide whether the English translation should be updated. Use when comparing baseline and updated Markdown, evaluating translation triggers, or distinguishing substantive content changes from frontmatter, whitespace, and channel-tag changes.
license: MIT
compatibility: Requires Python 3.9+ for the bundled comparison script and read access to source and English Markdown files.
metadata:
  com.example.owner: docs-team
  com.example.product-line: docs-platform
  com.example.status: example
  com.example.version: "0.1.0"
---

# Markdown Translation Change Review

## Purpose

Determine whether a changed Chinese Markdown document should trigger a translation update.

This example follows a conservative documentation workflow:

1. A new Chinese source document requires translation.
2. An existing Chinese document with no matching English file does not automatically trigger translation.
3. Changes limited to frontmatter, whitespace, or standalone channel tags do not trigger translation.
4. Other content changes require translation.

## Required Input

Collect:

- The baseline Chinese Markdown file, if the document already existed.
- The updated Chinese Markdown file.
- The matching English Markdown file, if it exists.
- The repository's actual channel-tag syntax, if it differs from the bundled example.

## Workflow

1. Determine whether the updated source file is new.
2. Determine whether a matching English document exists.
3. Run the bundled script:

   ```bash
   python3 scripts/check_translation_trigger.py \
     --baseline /path/to/baseline.md \
     --updated /path/to/updated.md \
     --english /path/to/docs_en/file.md
   ```

4. Read the JSON result.
5. If `translation_required` is `true`, summarize the substantive changed lines and recommend translation.
6. If it is `false`, state the reason and do not modify translation files unless the user asks.

## Important Limits

- The bundled script is a lightweight example, not a full semantic Markdown parser.
- Customize `CHANNEL_TAG_PATTERN` in the script to match the repository's channel labels.
- Do not delete or overwrite source, baseline, or English files.
- Do not automatically invoke translation; only report the decision unless the user explicitly asks to translate.

## Output Format

Return:

```text
Decision: translation required / not required
Reason: <machine-readable reason>
Evidence: <short summary of substantive changes>
Next action: <translate / no action / request review>
```
