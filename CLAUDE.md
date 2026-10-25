# Notes for converting sections into this book

Owner: Dona (philosophy professor). She uploads one textbook section at a time:
a Word document, the map images, and the .mup converter's outputs.

## Structure
- One Quarto book. Each chapter is a `part:` in `_quarto.yml`; each section is its
  own .qmd file: `chapters/chNN/NN-SS-short-name.qmd`, title `# N.S Title`.
  (Quarto drops part titles from Word, so the section number in the title is
  what identifies the chapter there.)
- Images in `images/chNN/`, outlines in `outlines/chNN/`. Use root-relative
  paths (`/images/...`, `{{< include /outlines/... >}}`).
- `number-sections: false`, `crossref: chapters: false` → figures are
  Figure 1, 2, 3 per section page. Dona only cross-references within a section.
- One book-wide Word file (`Argument-Mapping.docx`) is the student download.

## Converting a section
- Convert the .docx with pandoc to Markdown, then clean up: drop Word style
  classes on headings, move figures out of block quotes, remove Word image sizes.
- Illustrations built from stacked image fragments in Word: use the flattened
  image files Dona supplies, with `fig-alt` and no caption (`.illustration`, px width).
- Argument maps: figure with caption + `#fig-` id + `fig-alt`, then a
  `::: {.map-outline fig="..."}` div including the map's `_list.md`.
  Only `_list.md` is used; `_quarto.md` (raw HTML) and `_description.docx` are not.
- Match each map image to its outline by file name.
- Flag (don't silently fix) wording differences between the text and the maps,
  and anything Claude invented (captions, alt text, titles).

## Checks before committing
- `quarto render` with no warnings. map-outline.lua warns if a map needs more
  than 9 Word heading levels (map root sits at H3) — report it to Dona.
- axe-core WCAG 2.x A/AA on the rendered pages, light and dark: 0 violations.
- Look at the page at phone width (no sideways scrolling) and the Word file.
