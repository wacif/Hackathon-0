# Properties Reference

Properties store structured metadata in YAML frontmatter at the top of a note.

## Frontmatter Format

Properties **must** appear at the very first line of the file, before any content.
Delimited by `---` on their own lines. Each property name must be unique within a note.

```yaml
---
title: A New Hope
date: 2020-08-21
tags:
  - movies
  - sci-fi
aliases:
  - Episode IV
  - Star Wars 4
cssclasses:
  - wide-page
publish: true
link: "[[Episode IV]]"
url: https://www.example.com
favorite: true
year: 1977
---
```

## Property Types

Obsidian supports these property value types. Once a type is assigned to a property
name, all properties with that name across the vault use the same type.

### Text

Single line of text. Markdown formatting is **not** rendered. Hashtags do **not**
create tags. Internal links must be quoted:

```yaml
title: A New Hope
link: "[[Episode IV]]"
url: https://www.example.com
```

### List

Multiple values, each on its own line preceded by `-`. Internal links must be quoted:

```yaml
cast:
  - Mark Hamill
  - Harrison Ford
  - Carrie Fisher
links:
  - "[[Link]]"
  - "[[Link2]]"
```

### Number

Literal numbers only (no expressions). Integers and decimals allowed:

```yaml
year: 1977
pie: 3.14
```

### Checkbox

Boolean values — `true` or `false`. Displays as a checkbox in Live Preview:

```yaml
favorite: true
reply: false
```

### Date

ISO 8601 format (`YYYY-MM-DD`). With the Daily Notes plugin enabled, date properties
function as internal links to the corresponding daily note:

```yaml
date: 2020-08-21
```

### Date & Time

Includes both date and time:

```yaml
time: 2020-08-21T10:30:00
```

### Tags

Special type used exclusively by the `tags` property. Cannot be assigned to other properties:

```yaml
tags:
  - journal
  - personal
  - draft
```

## JSON Properties

Properties can also be defined as JSON. Obsidian reads, interprets, and saves as YAML:

```yaml
---
{
  "tags": ["journal"],
  "publish": false
}
---
```

## Default Properties

| Property     | Type | Description                                           |
|--------------|------|-------------------------------------------------------|
| `tags`       | List | Searchable labels. See Tags.                          |
| `aliases`    | List | Alternative note names for link suggestions.          |
| `cssclasses` | List | CSS classes applied to individual notes via snippets. |

### Obsidian Publish Properties

| Property      | Description                              |
|---------------|------------------------------------------|
| `publish`     | Controls whether note is published.      |
| `permalink`   | Custom URL path for the published note.  |
| `description` | Page description for SEO.                |
| `image`       | Social media preview image.              |
| `cover`       | Alternative to `image` for preview.      |

### Deprecated Properties (since Obsidian 1.4, removed in 1.9)

| Deprecated   | Use Instead  |
|--------------|--------------|
| `tag`        | `tags`       |
| `alias`      | `aliases`    |
| `cssclass`   | `cssclasses` |

Use the Format Converter plugin to bulk-convert deprecated properties.

## Searching Properties

Use `[property:value]` search syntax:

```
[tags:project]              Exact match
[status:draft]              Text property match
[priority:>2]               Number comparison
[date:2024-01-01]           Date match
[reviewed:true]             Checkbox match
[tags:project/active]       Nested tag match
```

## Display Modes

Settings → Editor → Properties in document:

- **Visible** (default) — shows the property editor UI
- **Hidden** — hides properties, can still be displayed in sidebar via Properties view
- **Source** — shows raw YAML (needed for viewing nested/complex properties)

## Not Supported

- **Nested properties** — use Source mode to view
- **Bulk-editing properties** — use VSCode, scripts, or community plugins
- **Markdown in properties** — intentional limitation; properties are for small, atomic data

## Hotkeys

| Action                | Hotkey               |
|-----------------------|----------------------|
| Add new property      | `Cmd/Ctrl + ;`       |
| Focus next property   | `Down arrow` or `Tab`|
| Focus previous        | `Up arrow` or `Shift+Tab` |
| Jump to editor        | `Alt+Down arrow`     |
| Edit property name    | `Left arrow`         |
| Edit property value   | `Right arrow`        |
| Delete property       | `Cmd/Ctrl+Backspace` |
| Select all            | `Cmd/Ctrl+A`         |
| Undo                  | `Cmd/Ctrl+Z`         |
| Redo                  | `Cmd/Ctrl+Shift+Z`   |

Vim keybindings also supported: `j` (down), `k` (up), `h` (key), `l` (value),
`A` (value end), `i` (value start), `o` (new property).

## Best Practices

1. **Consistent naming** — use the same property keys across notes (Obsidian suggests existing keys)
2. **Correct types** — use Date for dates, Number for numbers (enables sorting/filtering)
3. **Quote internal links** — always wrap `[[links]]` in quotes within properties
4. **No duplicate keys** — each property key should appear only once in frontmatter
5. **Quote special strings** — quote values containing colons, brackets, or special YAML characters
