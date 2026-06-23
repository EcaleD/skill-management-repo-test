# Translation Rules

## Preserve Without Translation

Keep the following content unchanged unless the user explicitly asks otherwise:

- YAML frontmatter keys and structured metadata.
- Fenced code blocks, including language identifiers.
- Inline code enclosed in backticks.
- URLs, link targets, file paths, environment variable names, API field names, model IDs, error codes, and JSON keys.
- Raw HTML, HTML comments, and channel tags.
- `data:image/...` payloads and Base64 content.
- Shell commands and command flags.

## Translate

Translate the following visible content:

- Headings and paragraphs.
- Table headers and user-facing table cells.
- Markdown link labels, but not link destinations.
- Image alt text, but not image URLs.
- Admonition text and visible labels.
- Comments intended for documentation readers, unless they are a system directive.

## Markdown Examples

### Link

Source:

```md
请参考 [鉴权说明](https://example.com/auth)。
```

Translation:

```md
For authentication details, see [Authentication](https://example.com/auth).
```

### Inline Code

Source:

```md
设置 `ARK_API_KEY` 环境变量。
```

Translation:

```md
Set the `ARK_API_KEY` environment variable.
```

### Code Fence

Source:

````md
使用以下命令：

```bash
export ARK_API_KEY="your-api-key"
```
````

Translation:

````md
Run the following command:

```bash
export ARK_API_KEY="your-api-key"
```
````

## Terminology Rules

- Prefer concrete verbs: "create", "configure", "send", "retrieve", "validate".
- Use "request" and "response" consistently for API interactions.
- Use sentence case for headings unless the repository uses another style.
- Do not add explanations that do not appear in the source.
- Do not convert a warning into a recommendation or requirement unless the source does so.
