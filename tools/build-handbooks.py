#!/usr/bin/env python3
"""Build a separate Word file for each handbook page.

A handbook page is a section file whose front matter has `handbook: true`.
For each one, this renders the page on its own (outside the book) to Word
and saves it as _book/downloads/<Title>.docx, e.g. "1.10 Chapter 1
Handbook" -> Chapter-1-Handbook.docx. The handbook page links to that file.
Map text descriptions go in an appendix at the end, as in the book.

Run after `quarto render` (the GitHub workflow does this):
    python3 tools/build-handbooks.py
"""
import pathlib, re, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "_book" / "downloads"

CONFIG = """project:
  type: default
lang: en
handbook-file: true
number-sections: false
filters:
  - path: filters/map-outline.lua
    at: pre-quarto
  - path: filters/docx-figure-numbers.lua
    at: post-quarto
  - path: filters/docx-alt-text.lua
    at: post-quarto
format:
  docx:
    fig-align: center
"""

def main():
    pages = []
    for qmd in sorted((ROOT / "chapters").rglob("*.qmd")):
        text = qmd.read_text(encoding="utf-8")
        fm = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if fm and re.search(r"^handbook:\s*true\s*$", fm.group(1), re.M):
            pages.append((qmd, text))
    OUT.mkdir(parents=True, exist_ok=True)
    for qmd, text in pages:
        title = re.search(r"^# +(.+)$", text, re.M).group(1).strip()
        name = re.sub(r"^\d+\.\d+\s+", "", title)
        name = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-") + ".docx"
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            for d in ("filters", "images", "outlines"):
                shutil.copytree(ROOT / d, tmp / d)
            (tmp / "_quarto.yml").write_text(CONFIG, encoding="utf-8")
            # The file's own title drops the section number ("Chapter 1 Handbook").
            own = re.sub(r"^# +\d+\.\d+\s+", "# ", text, count=1, flags=re.M)
            (tmp / "handbook.qmd").write_text(own, encoding="utf-8")
            subprocess.run(["quarto", "render", "handbook.qmd", "--to", "docx"],
                           cwd=tmp, check=True)
            shutil.copy(tmp / "handbook.docx", OUT / name)
        print(f"build-handbooks: {qmd.relative_to(ROOT)} -> _book/downloads/{name}")
    if not pages:
        print("build-handbooks: no handbook pages")

if __name__ == "__main__":
    sys.exit(main())
