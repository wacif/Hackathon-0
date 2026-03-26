# HTML in Obsidian Reference

Obsidian supports HTML to allow you to display your notes the way you want, or even
embed web pages. To prevent malicious code from doing harm, Obsidian sanitizes any
HTML in your notes.

## HTML Limitations

### No Markdown Inside HTML

Obsidian does **not** render Markdown syntax inside HTML elements. This is an
intentional design choice for performance optimization and parser complexity.

This will **not** work as expected:

```html
<div>
This **will not** be bold and this `will not` be code.
</div>
```

### HTML Blocks Must Be Self-Contained

HTML blocks must be complete and **cannot contain blank lines** within them.

This will work:

```html
<table>
<tr>
<td>Content here</td>
</tr>
</table>
```

This will **not** work correctly:

```html
<table>

<tr>

<td>Content here</td>

</tr>

</table>
```

### When Markdown Appears to Work in HTML

Some inline HTML tags like `<span>` or `<a>` have limited functionality and may
appear to render Markdown, but the Markdown is being processed outside of the
HTML context, not within it.

### Sanitized Tags

Obsidian strips potentially dangerous HTML for security:

- `<script>` — JavaScript execution
- `<style>` — CSS injection
- `<form>`, `<input>` — form elements
- `<object>`, `<embed>` — plugin content
- Event handlers (`onclick`, `onerror`, etc.)

## Common HTML Usage

### Comments

```html
<!-- This is an HTML comment -->
<!--
Multi-line
HTML comment
-->
```

Use HTML comments when exporting notes via Pandoc (which has limited support
for Obsidian's `%%` comment syntax). For normal vault use, prefer `%%` comments.

### Underline

```html
<u>Underlined text</u>
```

### Strikethrough (HTML alternative)

```html
<s>Strikethrough text</s>
```

### Subscript and Superscript

```html
H<sub>2</sub>O
E = mc<sup>2</sup>
```

### Span and Div Styling

Span and div tags apply custom classes from CSS snippets or inline styling:

```html
<span style="font-family: cursive">Cursive text</span>
<span style="color: red">Red text</span>
<span style="font-size: 1.5em">Larger text</span>
<span class="my-custom-class">Styled via CSS snippet</span>

<div style="text-align: center">
Centered block of content
</div>

<div class="custom-container">
Content styled by CSS snippet
</div>
```

### Highlighted Text (Custom Color)

```html
<mark style="background: #ffd700">Custom color highlight</mark>
```

### Keyboard Keys

```html
<kbd>Ctrl</kbd> + <kbd>C</kbd>
```

### Collapsible Sections

```html
<details>
<summary>Click to expand</summary>
Content hidden by default.
</details>

<details open>
<summary>Expanded by default</summary>
This content is visible initially.
</details>
```

**Note:** For collapsible content with full Markdown rendering, prefer
Obsidian's foldable callouts (`> [!type]-`) over HTML `<details>`.

### Tables (Advanced)

For complex tables beyond Markdown's capabilities (colspan, rowspan):

```html
<table>
<tr>
<th>Header 1</th>
<th colspan="2">Spanning Header</th>
</tr>
<tr>
<td rowspan="2">Merged rows</td>
<td>Cell A</td>
<td>Cell B</td>
</tr>
<tr>
<td>Cell C</td>
<td>Cell D</td>
</tr>
</table>
```

### Iframes (Embed Web Pages)

```html
<iframe src="https://www.youtube.com/embed/VIDEO_ID"
        width="560" height="315"
        frameborder="0" allowfullscreen>
</iframe>

<iframe src="https://example.com"
        width="100%" height="500">
</iframe>
```

Not all websites allow iframe embedding — sites may block it via
`X-Frame-Options` or `Content-Security-Policy` headers.

**Tip:** Search for the website name followed by "embed iframe" to find
embeddable URLs. YouTube and tweets can also be embedded using markdown
image syntax: `![](https://www.youtube.com/watch?v=VIDEO_ID)`

## Using cssclasses as Alternative

Instead of inline HTML styles, use the `cssclasses` property to apply vault-wide
styling to specific notes:

```yaml
---
cssclasses:
  - wide-page
  - serif-font
---
```

Then define in `.obsidian/snippets/custom.css`:

```css
.wide-page .markdown-preview-view {
    max-width: 900px;
}
.serif-font .markdown-preview-view {
    font-family: Georgia, serif;
}
```

## Portability Note

HTML reduces note portability to other Markdown editors. Prefer Markdown syntax
when possible. Use HTML only for features Markdown doesn't support natively
(underline, subscript/superscript, custom styling, complex tables).
