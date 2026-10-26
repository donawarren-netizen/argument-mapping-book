#!/usr/bin/env python3
"""
One command, every format.

For each .mup argument map, produces:
  - <name>_description.html  web version: nested lists inside a collapsible
                             details block, for a WordPress Custom HTML block
  - <name>_description.docx  Word version: one heading per claim/connector,
                             levels 1-9
  - <name>_list.md           plain Markdown bulleted list, no drop-down
And, when a PDF of the map with the same name sits next to the .mup
(e.g. Map.mup and Map.pdf):
  - <name>.png               the map image, trimmed, at 300 dpi
  - <name>_quarto.md         ready-to-paste Quarto block: the image at the
                             right display width, then the description

Usage:
    python3 convert_maps.py Map.mup                  one map
    python3 convert_maps.py Chapter6_maps/           every .mup in a folder
    python3 convert_maps.py Chapter6_maps/ out/      put results in "out/"
Optional:
    --name "Map 6.1"        summary text for the description (single map
                            only; default is just "(Text description)")
    --images images/ch06    folder the Quarto block points to for the
                            image (default: images)

Keep these files together in one folder:
    convert_maps.py, mup_to_outline.py, mup_to_html_list.py,
    pdf_to_image.py, build_docx.js
Requires Node.js with the "docx" package, and (for images)
pip install pypdfium2 pillow
"""
import json
import subprocess
import sys
from pathlib import Path

import mup_to_html_list  # also lifts the parser's depth cap for the web version

HERE = Path(__file__).parent


def make_docx(mup_path, docx_path):
    # The outline is parsed uncapped; build_docx.js clamps anything deeper
    # than level 9 to Heading 9.
    outline, title = mup_to_html_list.mup_to_outline.parse_mup(mup_path)
    tmp_json = Path(docx_path).with_suffix(".outline.json")
    tmp_json.write_text(json.dumps({"title": title, "outline": outline}, indent=1),
                        encoding="utf-8")
    try:
        subprocess.run(["node", str(HERE / "build_docx.js"), str(tmp_json), str(docx_path)],
                       check=True, stdout=subprocess.DEVNULL)
    finally:
        tmp_json.unlink(missing_ok=True)


def alt_text(outline):
    """Short alt text: what the map argues for, plus a pointer to the
    description. The claims themselves are in the description."""
    claims = [e["text"] for e in outline if e["type"] == "claim"]
    if claims and claims[0] != "(blank claim)":
        top = claims[0].replace(" (Stopping Point)", "").strip()
        if top[-1:] not in ".?!":
            top += "."
        text = f"Argument map concluding: {top} Text description follows."
    else:
        text = "Argument map. Text description follows."
    return text.replace('"', "'")  # keep the attribute's quotes intact


def make_quarto(mup, pdf, out_dir, image_folder, name):
    import pdf_to_image  # only needed when there's a PDF

    png_path = out_dir / (mup.stem + ".png")
    width, pages = pdf_to_image.pdf_to_png(pdf, png_path)
    snippet, outline = mup_to_html_list.make_snippet(mup, name)
    image_ref = f"{image_folder.rstrip('/')}/{png_path.name}"
    block = (
        f'![]({image_ref}){{width={width}px fig-alt="{alt_text(outline)}"}}\n'
        "\n"
        "```{=html}\n"
        f"{snippet}"
        "```\n"
    )
    (out_dir / (mup.stem + "_quarto.md")).write_text(block, encoding="utf-8")
    note = f" (warning: PDF has {pages} pages; only page 1 used)" if pages > 1 else ""
    return png_path.name, note


def convert_one(mup, out_dir, name=None, image_folder="images"):
    stem = mup.stem + "_description"
    html_path = out_dir / (stem + ".html")
    docx_path = out_dir / (stem + ".docx")
    n = mup_to_html_list.convert(mup, html_path, name)
    make_docx(mup, docx_path)
    md_path = out_dir / (mup.stem + "_list.md")
    mup_to_html_list.convert_markdown(mup, md_path)
    made = [html_path.name, docx_path.name, md_path.name]

    pdf = mup.with_suffix(".pdf")
    note = ""
    if pdf.exists():
        png_name, note = make_quarto(mup, pdf, out_dir, image_folder, name)
        made += [png_name, mup.stem + "_quarto.md"]
    else:
        note = " (no PDF found, so no image or Quarto block)"
    print(f"{mup.name}: {n} items -> {', '.join(made)}{note}")


def take_option(args, flag):
    if flag in args:
        i = args.index(flag)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return None


def main():
    args = sys.argv[1:]
    name = take_option(args, "--name")
    image_folder = take_option(args, "--images") or "images"
    if not args:
        print(__doc__)
        sys.exit(1)

    src = Path(args[0])
    if src.is_dir():
        maps = sorted(src.glob("*.mup"))
        out_dir = Path(args[1]) if len(args) > 1 else src
        name = None  # a single --name can't apply to a whole folder
    else:
        maps = [src]
        out_dir = Path(args[1]) if len(args) > 1 else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    if not maps:
        print(f"No .mup files found in {src}")
        sys.exit(1)

    failed = []
    for mup in maps:
        try:
            convert_one(mup, out_dir, name, image_folder)
        except Exception as e:  # keep going so one bad file doesn't stop a batch
            failed.append(mup.name)
            print(f"{mup.name}: FAILED ({e})")

    print(f"\nDone: {len(maps) - len(failed)} of {len(maps)} maps converted.")
    if failed:
        print("Failed: " + ", ".join(failed))


if __name__ == "__main__":
    main()
