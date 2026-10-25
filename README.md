# Argument Mapping

Source for the Argument Mapping textbook, built with [Quarto](https://quarto.org)
into a website and a single Word file.

## Where things are

| Path | What it is |
|---|---|
| `_quarto.yml` | Book settings, including the list of chapters and sections |
| `chapters/ch05/05-01-introduction.qmd` | One file per section (text + figures) |
| `images/ch05/` | Map images and illustrations for Chapter 5 |
| `outlines/ch05/` | The converter's `_list.md` outlines, one per map |
| `filters/` | Build helpers: collapsible text descriptions, Word alt text |
| `styles.css` | Look of the description boxes, phone layout, contrast fix |

## Editing on GitHub

Open a section file, click the pencil icon, edit, and click **Commit changes**.
The book rebuilds automatically (see the **Actions** tab). To get the built
book, open the latest run and download it under **Artifacts**: it contains the
website files and `Argument-Mapping.docx`.

## Adding an argument map to a section

1. Upload the image to `images/chNN/` and its `_list.md` outline to `outlines/chNN/`,
   with matching names.
2. In the section file, add:

```markdown
![Caption for the map.](/images/ch05/Map_name.png){#fig-short-name width=100% fig-alt="Argument map concluding: (1) .... A full text description is provided."}

::: {.map-outline fig="fig-short-name"}
{{< include /outlines/ch05/Map_name_list.md >}}
:::
```

Refer to it in the text as `@fig-short-name`; it becomes "Figure 3" etc.
Figures are numbered within each section page.
