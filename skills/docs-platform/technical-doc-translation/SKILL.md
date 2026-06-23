---
name: technical-doc-translation
description: Translate Chinese Markdown technical documentation into accurate, natural English while preserving Markdown structure, code, URLs, API identifiers, frontmatter, HTML, and channel tags. Use when translating or proofreading Chinese developer documentation, API guides, release notes, code samples, or Markdown content.
license: MIT
compatibility: Requires read access to the source Markdown files. No network access is required.
metadata:
  com.example.owner: docs-team
  com.example.product-line: docs-platform
  com.example.status: example
  com.example.version: "0.1.0"
---

# Technical Documentation Translation

## Purpose

Translate Chinese Markdown technical documentation into clear English for developers. Prioritize technical accuracy, stable terminology, and preservation of machine-readable content.

Read [the translation rules](references/translation-rules.md) before translating. Use [the output template](assets/translation-output-template.md) only when the user asks for a standalone translated document.

## Required Input

Before translating, identify:

1. The source Markdown file or pasted content.
2. The expected English output location, if a file update is requested.
3. Whether a glossary, previous English version, or product terminology is available.
4. Whether the request is a full translation, an incremental update, or proofreading.

If no glossary is provided, use consistent, natural developer-documentation terminology and record assumptions briefly.

## Workflow

1. Read the complete source context before translating individual lines.
2. Preserve YAML frontmatter unless the user explicitly asks to localize its values.
3. Preserve fenced code blocks, inline code, URLs, file paths, API names, JSON keys, CLI commands, and HTML tags.
4. Translate visible Markdown text, including headings, paragraphs, table cells, link labels, image alt text, and callout content.
5. Preserve Markdown hierarchy, list nesting, tables, anchors, and links.
6. For Markdown links, translate the label but keep the URL unchanged.
7. Return complete Markdown unless the user explicitly requests a diff or selected section.
8. When the user requests proofreading, improve fluency without changing product behavior or technical meaning.

## Quality Checklist

Before finishing, verify:

- Code blocks and JSON/YAML syntax are unchanged.
- URLs, link targets, file paths, and API identifiers are unchanged.
- Tables still have the same number of columns.
- Channel tags and pure HTML lines are unchanged.
- Product terms are translated consistently.
- The result reads like original English technical documentation, not literal translation.

## Default Tone

Use concise, professional developer-documentation English.

When the user asks for alternatives, provide:

- **Recommended**: Natural documentation English.
- **Formal**: More formal enterprise wording.
- **Concise**: Shorter UI or release-note wording.
