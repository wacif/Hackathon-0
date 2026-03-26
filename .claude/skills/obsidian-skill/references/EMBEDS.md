# Embeds Reference

Embeds pull content from other notes, images, PDFs, audio, and video directly into a note.
When the source changes, the embedded view updates automatically (transclusion).

## Syntax

Embeds use the `!` prefix before a wikilink or markdown link. You can also drag and
drop supported files directly into a note on desktop to embed automatically.

## Note Embeds

```markdown
![[Note Name]]                       Full note content
![[Note Name#Heading]]               Everything under that heading
![[Note Name#^block-id]]             A specific block (paragraph, list, etc.)
```

### Heading Embeds

Embeds all content from the heading to the next heading of equal or higher level.

### Block Embeds

First, define a block ID in the source note by appending ` ^id` to a paragraph:

```markdown
The key insight is that simplicity wins. ^key-insight
```

Then embed it:

```markdown
![[Research Notes#^key-insight]]
```

For lists and blockquotes, place the block ID on a separate line with blank lines:

```markdown
- First item
- Second item
- Third item

^my-list

Next paragraph here.
```

## Embed a List

To embed a list from another note, add a block identifier to the list, then embed it:

```markdown
![[My note#^my-list-id]]
```

## Image Embeds

### Internal Images (from vault)

```markdown
![[photo.png]]                       Full size
![[photo.png|300]]                   Width only (aspect ratio maintained)
![[photo.png|640x480]]               Width × Height
![[diagram.svg]]                     SVG support
```

### External Images

```markdown
![Alt text](https://example.com/image.png)
![Alt text|300](https://example.com/image.png)
![250](https://publish-01.obsidian.md/access/.../image.jpg)
```

### Supported Image Formats

`avif`, `bmp`, `gif`, `jpeg`, `jpg`, `png`, `svg`, `webp`

## PDF Embeds

```markdown
![[document.pdf]]                    Full PDF viewer
![[document.pdf#page=3]]             Open at specific page
![[document.pdf#height=400]]         Custom viewer height (pixels)
```

## Audio Embeds

```markdown
![[recording.mp3]]                   Audio player
![[podcast.wav]]                     WAV format
![[voice.ogg]]                       OGG format
```

### Supported Audio Formats

`flac`, `m4a`, `mp3`, `ogg`, `wav`, `webm`, `3gp`

## Video Embeds

```markdown
![[lecture.mp4]]                     Video player
![[demo.webm]]                       WebM format
![[recording.mov]]                   MOV format
```

### Supported Video Formats

`mkv`, `mov`, `mp4`, `ogv`, `webm`

## YouTube Video Embed

You can embed YouTube videos using standard markdown image syntax:

```markdown
![](https://www.youtube.com/watch?v=NnTvZWp5Q7o)
```

## Tweet Embed

Embed tweets using the same markdown image syntax:

```markdown
![](https://twitter.com/obsdmd/status/1580548874246443010)
```

## Embed Search Results

Embed a live search query result using a `query` code block:

````markdown
```query
embed OR search
```
````

This renders a live search result panel within the note. Note: Obsidian Publish
does not support embedded search results.

## Iframe Embeds (Web Pages)

Embed external web pages using HTML iframe:

```html
<iframe src="https://example.com" width="100%" height="500"></iframe>
```

**Note:** Not all websites allow iframe embedding (they may block it via
`X-Frame-Options` or `Content-Security-Policy` headers). Search for the website
name followed by "embed iframe" to find embeddable URLs.

In Canvas, you can embed web pages directly in cards.

## Embed Behavior

- Embeds are **live** — changes to the source note reflect immediately
- Embeds are **read-only** in the embedded view; edit the source note to change content
- Embedded content inherits the current note's theme and CSS
- Deeply nested embeds (embed within embed) are supported but may impact performance
- In export (PDF/print), embeds are resolved and included inline

## Best Practices

1. **Use heading embeds** for reusable sections (e.g., shared action items, status blocks)
2. **Use block embeds** for specific paragraphs or data points
3. **Set image widths** to keep layouts consistent: `![[img.png|400]]`
4. **Avoid circular embeds** — Note A embedding Note B which embeds Note A
5. **Prefer vault images** over external URLs for reliability
6. **Use PDF page anchors** to point readers to relevant sections
7. **Use query code blocks** for dynamic, auto-updating lists of related notes
