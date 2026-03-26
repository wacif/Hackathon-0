# Callouts Reference

Callouts are styled blockquote blocks that highlight information with colors and icons.
Callouts are also supported natively on Obsidian Publish.

## Basic Syntax

```markdown
> [!info] Here's a callout title
> Here's a callout block.
> It supports **Markdown**, [[Internal link|Wikilinks]], and [[Embed files|embeds]]!
> ![[Engelbart.jpg]]
```

You can insert a default `[!note]` callout using the **Insert callout** command
from the Command Palette. To wrap existing content in a callout, select text
and run the **Insert callout** command.

In Live Preview, right-click the callout name to change the callout type.

## Custom Titles

Replace the default title (the type name in title case) with custom text:

```markdown
> [!tip] Callouts can have custom titles
> Like this one.
```

Title-only callouts (no body):

```markdown
> [!tip] Title-only callout
```

Titles can contain formatting, emojis, and wikilinks:
`> [!tip] **Important** tip about [[links]]`

## Foldable Callouts

Append `-` or `+` directly after the type (no space) to make foldable:

```markdown
> [!faq]- Are callouts foldable?
> Yes! In a foldable callout, the contents are hidden when the callout is collapsed.

> [!faq]+ Expanded by default
> This content is visible but can be collapsed.
```

- `-` = starts collapsed (folded)
- `+` = starts expanded (open)
- No suffix = not foldable (always visible)

Both markers make the callout foldable. Users click the triangle icon to
expand/collapse in Reading and Live Preview modes.

## Nested Callouts

Add an extra `>` per nesting level:

```markdown
> [!question] Can callouts be nested?
>> [!todo] Yes!, they can.
>>> [!example] You can even use multiple layers of nesting.
```

## Built-in Callout Types

Each type has a unique background color and icon. Type identifiers are
**case-insensitive**. Any unsupported type defaults to `note` styling.

### note
Default callout. General information.
```markdown
> [!note]
> General information or remarks.
```

### abstract
**Aliases:** `summary`, `tldr`
```markdown
> [!abstract]
> Brief summary of the content.
```

### info
**Aliases:** `todo`
```markdown
> [!info]
> Informational content.
```

### tip
**Aliases:** `hint`, `important`
```markdown
> [!tip]
> Helpful advice or best practices.
```

### success
**Aliases:** `check`, `done`
```markdown
> [!success]
> Task completed or positive outcome.
```

### question
**Aliases:** `help`, `faq`
```markdown
> [!question]
> Something to think about or investigate.
```

### warning
**Aliases:** `caution`, `attention`
```markdown
> [!warning]
> Proceed with caution.
```

### failure
**Aliases:** `fail`, `missing`
```markdown
> [!failure]
> Something went wrong or is missing.
```

### danger
**Alias:** `error`
```markdown
> [!danger]
> Critical issue or error.
```

### bug
```markdown
> [!bug]
> Known bug or unexpected behavior.
```

### example
```markdown
> [!example]
> An illustrative example.
```

### quote
**Alias:** `cite`
```markdown
> [!quote]
> Quoted text or citation.
```

## Content Inside Callouts

All Markdown formatting works inside callouts, including bold, italic, highlights,
strikethrough, wikilinks, embeds, task items, code blocks, and math.

## Customize Callouts (CSS Snippets)

Create custom callout types by adding CSS to `.obsidian/snippets/`:

```css
/* File: .obsidian/snippets/custom-callouts.css */

.callout[data-callout="goal"] {
    --callout-color: 0, 200, 100;
    --callout-icon: lucide-target;
}

.callout[data-callout="brain"] {
    --callout-color: 200, 100, 255;
    --callout-icon: lucide-brain;
}
```

Then use in notes:

```markdown
> [!goal] Sprint Objective
> Complete the API migration by Friday.
```

**CSS variables:**
- `--callout-color`: RGB values as comma-separated integers (0–255)
- `--callout-icon`: Lucide icon ID from https://lucide.dev/icons/

Obsidian uses Lucide version **0.446.0** (ISC License).

### SVG Icons

You can also use a custom SVG element instead of a Lucide icon:

```css
--callout-icon: '<svg>...custom svg...</svg>';
```

## Best Practices

1. **Use semantic types** — pick the type that matches the content's purpose
2. **Foldable for long content** — use `-` to keep notes scannable
3. **Don't over-nest** — 2 levels deep is usually the practical maximum
4. **Consistent titles** — use a consistent naming convention across your vault
5. **Custom callouts** for recurring categories (e.g., `[!review]`, `[!decision]`)
6. **Alias awareness** — `[!caution]` renders identically to `[!warning]`
