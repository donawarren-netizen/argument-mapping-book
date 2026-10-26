#!/usr/bin/env python3
"""
Convert .mup argument maps into nested-list HTML long descriptions,
ready to paste into a WordPress Custom HTML block.

Uses the same parser as the Word toolkit (mup_to_outline.py), so every
established convention carries over unchanged: expanded connector labels,
"Outference D - Not So" ordering, "Role 2:" prefixes, "(Stopping Point)"
tags, "(unlabeled)" connectors, skipped empty groups, and the unfolding of
nested independent groups. Connectors keep their own list items.

Differences from the Word output:
- Structure is a nested <ul> list instead of headings, so there is no
  depth limit (the parser's 9-level cap is lifted here).
- Each description is wrapped in a <details> element, collapsed by default,
  with the summary "(Text description)", or "(Text description of <name>)"
  when --name is given.

Usage:
    python3 mup_to_html_list.py Map.mup               -> Map_description.html
    python3 mup_to_html_list.py Map.mup out.html
    python3 mup_to_html_list.py some_folder/          -> one file per .mup,
                                                         written into that folder
Optional:  --name "Map 6.1"   text used in the summary line
           (default: none -- the summary is just "(Text description)")

Keep this file in the same folder as mup_to_outline.py.
"""
import html
import re
import sys
from pathlib import Path

import mup_to_outline

# Lists have no depth limit, so lift the Word heading cap.
mup_to_outline.MAX_LEVEL = 10**6


def outline_to_list(outline, indent="  "):
    """Turn the flat [{level, text}] outline into nested <ul> markup."""
    # Build a tree: each node is (text, children).
    root = []
    stack = [(0, root)]  # (level, children list)
    for entry in outline:
        node = (entry["text"], [])
        while stack[-1][0] >= entry["level"]:
            stack.pop()
        stack[-1][1].append(node)
        stack.append((entry["level"], node[1]))

    lines = []

    def render(nodes, depth):
        pad = indent * depth
        lines.append(pad + "<ul>")
        for text, children in nodes:
            if children:
                lines.append(pad + indent + "<li>" + html.escape(text))
                render(children, depth + 2)
                lines.append(pad + indent + "</li>")
            else:
                lines.append(pad + indent + "<li>" + html.escape(text) + "</li>")
        lines.append(pad + "</ul>")

    if root:
        render(root, 0)
    return "\n".join(lines)


MD_SPECIAL = re.compile(r"([\\`*_\[\]<>#|])")


def outline_to_markdown(outline):
    """Plain Markdown nested bullet list, 4 spaces per level (works in
    Quarto/Pandoc and other Markdown readers alike)."""
    lines = []
    for entry in outline:
        text = MD_SPECIAL.sub(r"\\\1", entry["text"])
        # "(1) ..." or "1. ..." at the start would be read as list numbering
        # and the claim number dropped, so escape it.
        if text.startswith("("):
            text = "\\" + text
        else:
            text = re.sub(r"^(\d+)([.)])", r"\1\\\2", text)
        lines.append("    " * (entry["level"] - 1) + "- " + text)
    return "\n".join(lines) + "\n"


def convert_markdown(mup_path, out_path):
    outline, _ = mup_to_outline.parse_mup(mup_path)
    Path(out_path).write_text(outline_to_markdown(outline), encoding="utf-8")


def convert(mup_path, out_path, name=None):
    snippet, outline = make_snippet(mup_path, name)
    Path(out_path).write_text(snippet, encoding="utf-8")
    return len(outline)


def make_snippet(mup_path, name=None):
    """Return (details-block HTML, outline) for one map."""
    outline, _ = mup_to_outline.parse_mup(mup_path)
    body = outline_to_list(outline)
    label = f"Text description of {html.escape(name)}" if name else "Text description"
    snippet = (
        "<details>\n"
        f"<summary>({label})</summary>\n"
        f"{body}\n"
        "</details>\n"
    )
    return snippet, outline


def main():
    args = sys.argv[1:]
    name = None
    if "--name" in args:
        i = args.index("--name")
        name = args[i + 1]
        del args[i:i + 2]
    if not args:
        print(__doc__)
        sys.exit(1)

    src = Path(args[0])
    if src.is_dir():
        for mup in sorted(src.glob("*.mup")):
            out = mup.with_name(mup.stem + "_description.html")
            n = convert(mup, out)
            print(f"Wrote {out} ({n} items)")
    else:
        out = Path(args[1]) if len(args) > 1 else src.with_name(src.stem + "_description.html")
        n = convert(src, out, name)
        print(f"Wrote {out} ({n} items)")


if __name__ == "__main__":
    main()
