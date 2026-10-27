"""Post-render step: remove Quarto's duplicate IDs from every HTML page.

Quarto's light/dark theme switch writes three <link> elements that share
id="quarto-bootstrap" and three that share id="quarto-text-highlighting-styles".
Accessibility checkers (e.g. Silktide) report these under WCAG 4.1.1.

This script moves those two names from `id` to a class on the <link> elements
and updates Quarto's inline theme-switching script to match, so the light/dark
toggle keeps working. If a future Quarto version changes this markup, the script
warns in the build log instead of guessing.
"""

import os
import pathlib
import re
import sys

OUT = pathlib.Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_book"))

NAMES = {
    "quarto-bootstrap": "quarto-bootstrap-sheet",
    "quarto-text-highlighting-styles": "quarto-highlighting-sheet",
}

LINK = re.compile(r"<link\b[^>]*>")


def fix_link(tag: str) -> str:
    for old, new in NAMES.items():
        if f'id="{old}"' not in tag:
            continue
        tag = tag.replace(f' id="{old}"', "")
        if 'class="' in tag:
            tag = tag.replace('class="', f'class="{new} ', 1)
        else:
            tag = tag.replace("<link", f'<link class="{new}"', 1)
    return tag


def fix_page(html: str) -> str:
    html = LINK.sub(lambda m: fix_link(m.group(0)), html)
    for old, new in NAMES.items():
        html = html.replace(f"link#{old}", f"link.{new}")
    html = html.replace(
        'sheetNode.id === "quarto-bootstrap"',
        'sheetNode.classList.contains("quarto-bootstrap-sheet")',
    )
    return html


warnings = 0
for page in sorted(OUT.rglob("*.html")):
    text = page.read_text(encoding="utf-8")
    fixed = fix_page(text)
    leftover = [n for n in NAMES if n in fixed.replace(NAMES[n], "")]
    if leftover:
        warnings += 1
        print(f"WARNING fix-duplicate-ids: {page} still mentions {leftover}; "
              "Quarto's theme markup may have changed.", file=sys.stderr)
    if fixed != text:
        page.write_text(fixed, encoding="utf-8")

print(f"fix-duplicate-ids: checked HTML pages in {OUT} ({warnings} warnings)")
