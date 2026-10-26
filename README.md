# Argument Mapping

Source for the Argument Mapping textbook, built with [Quarto](https://quarto.org)
into a website and a single Word file.

**Read it:** https://donawarren-netizen.github.io/argument-mapping-book/

Licensed under CC BY-NC-SA 4.0 — see [LICENSE.md](LICENSE.md).

## Where things are

| Path | What it is |
|---|---|
| `_quarto.yml` | Book settings, including the list of chapters and sections |
| `chapters/ch05/05-01-introduction.qmd` | One file per section (text + figures) |
| `images/ch05/` | Map images and illustrations for Chapter 5 |
| `outlines/ch05/` | The converter's `_list.md` outlines, one per map |
| `filters/` | Build helpers: collapsible text descriptions, Word appendices, Word figure numbers and alt text |
| `styles.css` | Look of the description boxes, phone layout, contrast fix |
| `tools/MapConverter/` | The converter that turns Because maps (.mup + PDF) into map images and text descriptions; see its README.txt |

## Editing on GitHub

Open a section file, click the pencil icon, edit, and click **Commit changes**.
The book rebuilds and republishes automatically within a few minutes (see the
**Actions** tab). The Word version can be downloaded from the website's sidebar.

## Adding an argument map to a section

1. Upload the image to `images/chNN/` and its `_list.md` outline to `outlines/chNN/`,
   with matching names.
2. In the section file, add:

```markdown
![Caption for the map.](/images/ch05/Map_name.png){#fig-5-1-short-name width=100% fig-alt="Argument map concluding: (1) .... A full text description is provided."}

::: {.map-outline fig="fig-5-1-short-name"}
{{< include /outlines/ch05/Map_name_list.md >}}
:::
```

Start every figure id with its section number (`fig-5-1-...`), so ids never
repeat across the book. Refer to it in the text as `@fig-5-1-short-name`; it
becomes "Figure 3" etc. Figures are numbered within each section, on the web
and in Word.

In Word, each map's text description goes in an appendix at the end of its
chapter, automatically.
