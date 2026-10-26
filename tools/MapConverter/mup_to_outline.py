#!/usr/bin/env python3
"""
Parse a .mup argument map into a flat, ordered list of {level, text} heading
entries, following the pattern established in Test_3_long_description.docx:

- Every claim AND every connector (group) gets its own heading level.
- A claim with nothing at all rendered beneath it -- no support AND no
  objection -- has " (Stopping Point)" appended directly to its heading
  text, e.g. "Claim 4" -> "Claim 4 (Stopping Point)". A claim that has
  only an objection beneath it (no support) is NOT tagged, since there is
  more to see -- just not support. Word draws a (non-functional) collapse
  arrow next to every heading regardless of whether it has nested
  content, which is misleading on its own; this gives an explicit signal
  instead. Since it's part of the heading text itself, it's heard via
  pure heading-jump navigation, and costs nothing toward the 9-level
  heading budget (it's not a separate heading of its own).
- The root claim is level 1; each step down (claim -> connector, or
  connector -> claim) increases the level by 1.
- Claim heading text is the claim's raw title, with the Role 2 marker
  stripped and replaced by a spelled-out "Role 2:" prefix placed before
  the claim text, e.g. "5 (r2). Dogs require a lot of work." -> "Role 2:
  5. Dogs require a lot of work." The marker is now typed directly into
  the map itself as "(r2)" (case-insensitive) rather than an asterisk --
  a bare "*" is still recognized too, for older maps, but "(r2)" is the
  current convention since it reads reliably regardless of a screen
  reader's punctuation-verbosity setting.
- Connector heading text is the connector's parentConnector.label with
  abbreviations expanded: "Inf." -> "Inference", "Outf." -> "Outference"
  (checking the longer "Not So Outf." / "So What Outf." forms first). If a
  group has no parentConnector.label at all (missing or empty), the
  heading text is "(unlabeled)" rather than blank, so an unlabeled
  connector is still announced as a distinct heading rather than
  disappearing silently. A "Not So"/"So What" qualifier is moved after the
  instance letter so every connector heading leads with "Inference" or
  "Outference" consistently, e.g. "Not So Outference D" -> "Outference D -
  Not So". This makes heading-by-heading navigation more predictable: the
  first word always tells you the connector type.
- Empty groups (no children) are skipped entirely.
- A "group" node nested inside another group's ideas (alongside a claim,
  rather than under an intervening claim) is a data-tree artifact of the
  mapping tool -- it is logically attached to the MOST RECENTLY EMITTED
  claim sibling, one level below that claim, not to the outer group's own
  level. (Confirmed against Test_3.mup / Test_3_long_description.docx:
  "So What Outf. B" is nested this way and renders as a child of claim 5,
  not as a sibling of "Not So Outf. A".)
- Heading levels are capped at 9 (Word's full set of built-in heading
  styles); anything deeper continues at level 9.
"""
import json
from pathlib import Path

MAX_LEVEL = 9


import re


def expand_connector_label(label):
    if not label:
        return label
    replacements = [
        ("Not So Outf.", "Not So Outference"),
        ("So What Outf.", "So What Outference"),
        ("Outf.", "Outference"),
        ("Inf.", "Inference"),
    ]
    for old, new in replacements:
        if old in label:
            label = label.replace(old, new)
            break

    # Lead with "Outference" (or "Inference") for consistent, predictable
    # heading navigation -- every connector heading then starts with the
    # same word, with any "Not So"/"So What" qualifier moved after the
    # instance letter, e.g. "Not So Outference D" -> "Outference D - Not So".
    m = re.match(r"^(Not So|So What)\s+Outference\s+(.+)$", label, re.IGNORECASE)
    if m:
        qualifier, letter = m.group(1), m.group(2)
        label = f"Outference {letter} - {qualifier}"

    return label


def cap(level):
    return min(level, MAX_LEVEL)


ROLE2_PATTERN = re.compile(r"\s*\(r2\)\s*", re.IGNORECASE)


def clean_claim_title(title):
    """Detect the Role 2 marker in a claim title and replace it with a
    spelled-out "Role 2:" prefix placed before the claim text.

    Two marker forms are recognized, for backward compatibility with older
    maps: a literal "(r2)" (case-insensitive) -- the current convention,
    typed directly into the map -- or a bare asterisk "*" (the original
    convention, before it was replaced because NVDA's default punctuation
    verbosity setting skips asterisks silently)."""
    is_role2 = False

    if ROLE2_PATTERN.search(title):
        is_role2 = True
        title = ROLE2_PATTERN.sub(" ", title)

    if "*" in title:
        is_role2 = True
        title = title.replace("*", "")

    clean = title.strip()
    clean = re.sub(r"\s{2,}", " ", clean)  # collapse any doubled-up spaces
    clean = re.sub(r"\s+([.,;:!?])", r"\1", clean)  # drop space before punctuation
    if is_role2:
        clean = f"Role 2: {clean}"
    return clean


def render_claim(idea, level, out, extra_groups=None):
    """Render a claim's heading, then everything logically attached to it:
    both its own direct connector groups (idea["ideas"]) and any
    extra_groups passed in by the caller -- nested connectors that live in
    the .mup data as a sibling one level up (see render_group) but that
    logically belong to this claim.

    If none of those groups produced any content at all -- no support AND
    no objection -- "(Stopping Point)" is appended to the heading text:
    this is a genuine dead end, nothing further follows it. (A claim that
    has only an objection beneath it, no support, is NOT tagged -- there
    IS more to see, just not support.)"""
    title = clean_claim_title(idea.get("title", ""))
    # A box with no letters or digits (blank, or just "." used as a layout
    # spacer) isn't a real claim. If nothing hangs from it, skip it; if
    # something does, keep its place in the tree as "(blank claim)".
    is_blank = not re.search(r"\w", title)
    entry = {"level": cap(level), "text": "(blank claim)" if is_blank else title,
             "type": "claim"}
    out.append(entry)

    own_groups = [c for c in idea.get("ideas", {}).values() if c.get("title") == "group"]
    all_groups = own_groups + (extra_groups or [])

    before = len(out)
    for g in all_groups:
        render_group(g, level + 1, out)

    if len(out) == before:
        if is_blank:
            out.pop()
            return
        entry["text"] = f"{entry['text']} (Stopping Point)"


def render_group(group, level, out):
    children = group.get("ideas", {})
    if not children:
        return

    entries = list(children.values())
    claim_entries = [c for c in entries if c.get("title") != "group"]

    if claim_entries:
        attr = group.get("attr", {})
        label = attr.get("parentConnector", {}).get("label", "")
        expanded = expand_connector_label(label) if label else "(unlabeled)"
        out.append({"level": cap(level), "text": expanded, "type": "connector"})

    # Bundle each claim with any "group" entries immediately following it
    # in this same ideas dict -- those are nested connectors that are a
    # data-tree artifact of the mapping tool (see module docstring) but
    # logically belong to the preceding claim, one level below it.
    i = 0
    # Rare fallback: a nested group appearing before any claim has been
    # seen yet in this dict. Attach it at this group's own level + 1,
    # matching the level a first claim would have been rendered at.
    while i < len(entries) and entries[i].get("title") == "group":
        render_group(entries[i], level + 1, out)
        i += 1

    while i < len(entries):
        claim = entries[i]
        i += 1
        trailing = []
        while i < len(entries) and entries[i].get("title") == "group":
            trailing.append(entries[i])
            i += 1
        render_claim(claim, level + 1, out, extra_groups=trailing)


def parse_mup(mup_path):
    data = json.loads(Path(mup_path).read_text(encoding="utf-8"))
    top_ideas = data.get("ideas", {})
    out = []
    for idea in top_ideas.values():
        render_claim(idea, 1, out)
    return out, (data.get("title") or "Argument Map")


if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/uploads/Test_3.mup"
    out_json = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/outline.json"
    outline, title = parse_mup(src)
    Path(out_json).write_text(
        json.dumps({"title": title, "outline": outline}, indent=1), encoding="utf-8"
    )
    print(f"Wrote {out_json} ({len(outline)} headings)")
