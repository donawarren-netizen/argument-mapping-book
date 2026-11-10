# Notes for converting sections into this book

Owner: Dona (philosophy professor). She uploads one textbook section at a time,
all at once: the section's Word document, its .mup files and their PDFs (same
base name), and any other images (e.g. flattened illustrations).

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
- Word: map descriptions go in one "Appendix to Chapter N" after each chapter's
  last section (map-outline.lua finds chapters from the `# N.S` titles). Each map
  is labelled in bold ("Section 5.1, Figure 3"); its top claim is Heading 2, so
  maps get Heading 2–9. Word contents list shows Heading 1 only.
- Word: each chapter starts on a new page with its title from the `part:` entry
  (large, centered Heading 1; added by map-outline.lua). Part names must start
  "Chapter N:" for this to find them.
- Inserting a chapter or section between existing ones means renumbering
  everything after it: section titles, part names, figure ids, folder/file
  names, and any "Chapter N"/"Section N.S" mentions in the text — check with Dona.
- Word figure numbers restart at each section, matching the web: Quarto would
  number straight through the book, so filters/docx-figure-numbers.lua replaces
  Quarto's Word figures with its own captions and fixes `@fig-...` link text.

## Converting a section
- Convert the maps with the converter in `tools/MapConverter/` (the current
  version always lives here; Dona no longer uploads it):
  `pip install pypdfium2 pillow --break-system-packages`, then
  `python3 tools/MapConverter/convert_maps.py <folder of .mup+.pdf> <out>`.
  (`npm install docx` only if Dona wants the Word description files too.)
  Copy `<name>.png` to `images/chNN/` and `<name>_list.md` to `outlines/chNN/`.
  The other outputs aren't used in the book; send them to Dona if she asks.
- Use the display width from the converter's `_quarto.md` (`width=NNNpx`) as the
  figure width, so map text is the same size across maps; take a starting point
  for `fig-alt` from it too, changing "Text description follows." to
  "A full text description is provided."
- Convert the .docx with pandoc to Markdown, then clean up: drop Word style
  classes on headings, move figures out of block quotes, remove Word image sizes.
  Delete empty bold lines (`** **`, `****`): invisible in Word, but `****` on its
  own line renders as a horizontal rule.
- Illustrations built from stacked image fragments in Word: use the flattened
  image files Dona supplies, with `fig-alt` and no caption (`.illustration`, px width).
- Callouts: Dona marks boxed text in her Word documents with plain-text markers,
  `[CALLOUT: Title]` ... `[END CALLOUT]`, optionally with a type and/or
  "collapsed" (`[CALLOUT tip: Title]`, `[CALLOUT, collapsed: Answer]`). Turn each
  into a Quarto callout (`::: {.callout-TYPE}` + `## Title`; default type note;
  `collapse="true"` if collapsed). If a document uses Word text boxes instead,
  convert them too and tell Dona what became of each. The first time callouts
  appear, check their colors with axe in light and dark mode.
- Argument maps: figure with caption + `#fig-` id + `fig-alt`, then a
  `::: {.map-outline fig="..."}` div including the map's `_list.md`.
  Only `_list.md` is used; `_quarto.md` (raw HTML) and `_description.docx` are not.
- Figure ids MUST start with the section number (`fig-5-1-full`): in Word all
  sections become one document, so ids must be unique book-wide.
- Match each map image to its outline by file name.
- Capital C when the text refers to a specific claim in an argument ("Claim 2",
  "Claims 2 and 3"), in body text, captions and alt text (Dona, Nov 4).
- Flag (don't silently fix) wording differences between the text and the maps,
  and anything Claude invented (captions, alt text, titles).

## Checks before committing
- Local rendering: `pip install --break-system-packages quarto-cli==1.10.19`
  (the version pinned in the workflow; downloading from GitHub may be blocked).
  `soffice --headless --convert-to pdf` shows the Word output.
- `quarto render` with no warnings. map-outline.lua warns if a map needs more
  than 9 Word heading levels (map root sits at H2) — report it to Dona.
- axe-core WCAG 2.x A/AA on the rendered pages, light and dark: 0 violations.
  Test dark mode by calling `window.quartoToggleColorScheme()` — Quarto ignores
  the browser's prefers-color-scheme, so emulating it still shows light mode.
- The university checks pages with the Silktide toolbar (WCAG 2.1 AA) and wants
  a screenshot of a clean result before launch. Silktide flags things axe
  doesn't: search-field contrast (1.4.11; it compares the field's background
  with what's right around it and ignores borders, hence the dark frame around
  the white field), and duplicate ids (4.1.1). styles.css and
  tools/fix-duplicate-ids.py (post-render) handle those; search-label.html
  renames the search field from Quarto's "Submit" to "Search" for screen readers.
- Look at the page at phone width (no sideways scrolling) and the Word file.

## Handbook pages (one per chapter, its last section)
- Front matter `handbook: true` (first: 1.10 Chapter 1 Handbook). Under the
  title, an HTML-only box links `/downloads/Chapter-N-Handbook.docx`.
- Structure (rebuilt Nov 10 from Dona's new handbooks): kinds of claims and
  connections are headings (Ultimate Conclusion, Premise, Inference…), with
  bulleted explanations; key terms in definitions italic. Word heading levels
  shift down one under the page title.
- New material (handbooks after Chapter 1; Dona's Word files, Nov 10): marked
  with a bold "NEW:" label only (`**NEW:** text`); the rest of the item is not
  bold. In headings, plain "NEW: " in the heading text. Her Word highlight on
  "NEW" is dropped (not announced; contrast). A note under the title says so.
  (Replaces the Nov 6 "whole item bold, New:" convention.)
- Wording Dona wants in all handbooks (Nov 10): Constructing step 2 is
  "Research answers."; claim order is "Lead with the conclusion unless it would
  alienate your reader, in which case start with a claim that your reader would
  accept." Order under "Communicating an Argument" (Dona, Nov 10), numbered
  from 1) with only the topics a chapter has covered: Decide what claims you
  want to state (from Chapter 3) → Decide in what order you want to state the
  claims (from Chapter 2) → Make the connections clear (Chapter 1). So Ch1:
  1) Make the connections clear; Ch2: 1) Decide in what order…, 2) Make the
  connections clear.
- Extra blank line where Dona asks for one (e.g. 2.10's Analyzing section): wrap
  the block in `::: {.blank-line-before}` (styles.css pads it on web/print) and
  put an empty raw-openxml paragraph before it for Word:
  ```` ```{=openxml} ```` / `<w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr></w:p>`.
- `tools/build-handbooks.py` (run after `quarto render`; the workflow does it)
  renders each handbook on its own to Word, title without the section number,
  map descriptions in a plain "Appendix" at the end, saved in `_book/downloads/`.
- Printing (styles.css `@media print`, all pages): only the page content, black
  on white; collapsible descriptions left out. On handbook pages,
  map-outline.lua adds a print-only appendix of the descriptions and a
  print-only "see the appendix, Figure N" line under each map. Check by
  printing to PDF (Playwright `page.pdf`), from dark mode too.
