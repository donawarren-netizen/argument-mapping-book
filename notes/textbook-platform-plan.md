# Textbook platform plan (as of Nov 5, 2026)

> Recovered Nov 22, 2026 from earlier session transcripts. The copy in Dona's Claude Project was last
> updated Nov 5; this is that version, unchanged, plus "Later changes" at the end. Status, Accessibility
> findings and Next describe Nov 5. Chapter 3 is logged in `chapter-3-notes.md`; standing conventions are in
> `CLAUDE.md`.

## Status
The book is **published** at https://donawarren-netizen.github.io/argument-mapping-book/ from the **public** repository github.com/donawarren-netizen/argument-mapping-book (Claude GitHub app installed on that repo only). Every commit rebuilds and republishes the site and the Word file within a few minutes (GitHub Actions → GitHub Pages). Contains sections 1.1, 1.2 (Example 1), 1.3 (Example 2), 1.4 (Example 3), 1.5 (Example 4), 1.6 (Example 5), 1.7 (Example 6), 1.8 (Example 7), 1.9 (Constructing Arguments), 1.10 (Chapter 1 Handbook), 2.1 (Introduction), 2.2 (Example 1), 2.3 (Example 2), 2.4 (Example 3), 2.5 (Example 4), 2.6 (Example 5), 2.7 (Example 6), 2.8 (Example 7), 2.9 (Constructing Arguments), 2.10 (Chapter 2 Handbook) and 5.1 so far; the book grows section by section, in any order. Chapters 1 and 2 are complete (Chapter 2 finished Nov 5 with 2.10, its handbook). In Chapter 1, 1.9 ends the teaching ("In Chapter 2, we'll continue…") and 1.10, the chapter handbook, is the last section.

## University sign-off (IT, Oct 27)
- No technology-alignment concerns as long as sign-in uses "Continue with Microsoft" or "Continue with Google".
- Public/student-facing, so it must meet WCAG 2.1 AA (ADA Title II). Before going live: run the Silktide Toolbar on each page, send IT a screenshot of the score plus the URL.
- First Silktide run (Oct 27) flagged: form control contrast ×1 (the search field, 1.4.11) and duplicate IDs ×2 (Quarto's light/dark stylesheet links, 4.1.1). All fixed the same day; **Silktide came back clean on Oct 27.** Silktide ignores a field's border and compares its background with its surroundings, so the white search field now sits in a dark gray frame. Also fixed: dark-mode breadcrumb/next-page text contrast, and the search field's screen-reader name ("Submit" → "Search").

## Per-section workflow
1. Dona attaches, all at once: the section's Word document, its .mup files with matching PDFs, and any other images (e.g. flattened illustrations). Some sections have no maps (1.4, 1.7).
2. Claude converts the maps with the converter in the repo (`tools/MapConverter/`), assembles the section, adds it to the book settings, checks it, and commits. Existing sections aren't touched.
3. Dona makes small text edits herself on GitHub (she has done several successfully). If she sends a revised Word document for a section already converted, Claude compares it with the earlier one and applies only the differences.
4. Dona runs Silktide on the new page and keeps the screenshot for IT.
- Always compare each _Eval .mup with its PDF: evaluation notes have been missing from the .mup four times (1.3, 1.5, 1.6, 1.8) — the PDF is right; fix the outline by hand and ask Dona to re-save the .mup. Pattern: Dona seems to save the _I_Eval PDF after adding the inference note but before re-saving the .mup. (2.3's, 2.5's, 2.6's, 2.7's and 2.8's were complete.)
- Also compare the Word document's map images with the PDFs: 1.9's Word file had an older version of one map (no numbers/labels); the current PDF was used.
- Stray leftovers in Dona's Word documents happen (e.g. the sad face in 1.6, which she'd meant to delete): if an image or element looks out of place, ask rather than keep it.
- Empty bold lines in Dona's Word documents are invisible in Word but became horizontal lines on the web (1.4, 1.5; removed Oct 31 at Dona's request). Delete them when converting (now in CLAUDE.md). Lines holding only a non-breaking space also show up; drop them too.
- Repo gotcha: `tools/MapConverter/__pycache__/*.pyc` are tracked, and running the converter modifies them. Discard those changes (`git checkout -- tools/MapConverter/__pycache__`) before committing; untracking them would be a sensible cleanup.
- Session setup: Quarto isn't preinstalled in the workspace; download the version pinned in `.github/workflows/build.yml` (1.10.19) to render locally. Pushing may first need the repo added to the session (add_repo, push access).
- axe in dark mode: wait ~1.5 s after `quartoToggleColorScheme()` before running axe, or it catches the color transition and reports false contrast failures.

## Revising later
- The GitHub version is the most recent copy (some revisions are made directly there).
- For a bigger revision of a section or chapter, Dona asks Claude for a Word file of just that part: Claude renders it from a temporary copy of the book whose contents list only that part (plus the required preface). The published book isn't touched. Dona edits in Word and sends it back; Claude applies only the differences.
- Maps are revised in Because: send the new .mup + PDF with the same file name.
- New chapters/sections can go anywhere; anything inserted before existing material means renumbering what follows (titles, part names, figure ids, folders, and "Chapter N"/"Section N.S"/"Example N" mentions in the text — e.g. 5.1 says "as we saw in Chapter 2"; 1.8 refers to Examples 1 and 2; 1.9 mentions Chapters 2 and 3; 2.3 mentions Chapters 1 and 4; 2.4 mentions Chapter 3; 2.5 refers to Example 2 twice; 2.6 mentions Chapter 1; 2.8 mentions Example 2 and Chapter 1; 2.9 mentions Chapter 1 and "the next chapter"). Claude lists every such mention for Dona to check.

## Decisions
- Each chapter is a part in the sidebar; each section is its own page (`chapters/chNN/NN-SS-name.qmd`), titled with its number ("5.1 Introduction").
- Word: each chapter starts on a new page with its chapter title from the part name (large, centered Heading 1; added by map-outline.lua). It shares Heading 1 with section titles, so the contents list shows chapters and sections at one level; indenting sections would cost the maps a heading level (7 instead of 8).
- Figures numbered within each section (Figure 1, 2, 3…) on the web and in Word. Figure ids start with the section number (`fig-5-1-full`) so they're unique in the combined Word file.
- A map shown more than once in a section is a separate figure each time (own number, own text description), e.g. 1.2 has 4 maps but 10 figures.
- Summaries: each section's summary ("Summary of Example 1", "Summary of Introduction") is a level-2 heading at the end of the section page, not a separate page; Step headings inside a summary are level 3. 1.1 and 5.1 got summaries on Oct 29.
- One book-wide Word file, downloadable from the sidebar, containing every section in the book settings; section pages are linked from Canvas modules (External URL items) in place of uploaded Word documents.
- Word: map descriptions in one "Appendix to Chapter N" after each chapter's last section; maps labelled "Section 5.1, Figure 3"; map top claim at Heading 2 (8 levels available for a map).
- Right-hand contents list on each page (Nov 3, Dona): headings down to level 4, always expanded (`toc-depth: 4`, `toc-expand: true` in `_quarto.yml`). Was level 3, with deeper levels collapsed.
- Evaluation notes on an inference go in the connector line of the outline ("Inference A [Evaluation: This inference is bad.]"), matching the map.
- Strikethrough: Dona asked (Oct 30); it isn't announced by screen readers, so she'll show "we'll ignore this sentence" in words instead.
- Boulder pictures (Nov 1, Dona): the wooden connectors are bridges, not ladders; all alt text says "bridge" (the horizontal joiner in 5.1's dependent-reason pictures is called a "plank").
- Terminology (Nov 5, Dona): "subconclusion", one word, no hyphen.
- Terminology (Oct 30, Dona): always "Gully Test" (not "Gully Method"). "I.Q." with periods, plural "I.Q.'s" (Claude's choice, delegated by Dona; matches the maps and passages, so no map changes needed).
- Capital C when referring to a specific claim ("Claim 2"), book-wide (Nov 4, Dona).
- License: CC BY-NC-SA 4.0, © 2026 Dona Warren, for the book and the converter (preface, web footer, LICENSE.md, tools/MapConverter/LICENSE.md).
- The converter lives in the repo, so Dona no longer uploads MapConverter.zip; the repo copy is the current version.

## What's in the repo
- `_quarto.yml`, `index.qmd` (preface: how to read text descriptions + license), section files under `chapters/`.
- `images/chNN/`, `outlines/chNN/` (converter `_list.md` files only).
- `filters/map-outline.lua` (collapsible description on web; Word appendix per chapter and chapter title pages), `filters/docx-figure-numbers.lua` (per-section numbering in Word), `filters/docx-alt-text.lua` (alt text in Word).
- `styles.css`: description boxes, phone layout, contrast fixes (quotes/captions, search field in a dark gray frame, dark-mode breadcrumbs and next-page text), 24px targets for sidebar icons, the search button and (since Oct 29) the phone-width breadcrumb links. Since Nov 3: long chapter names wrap in the slide-out section menu on phones/tablets (under 992px wide; they used to run off the screen, hiding the fold arrows).
- `search-label.html`: renames the search field "Search" for screen readers.
- `tools/fix-duplicate-ids.py`: post-render step that removes Quarto's duplicate stylesheet ids while keeping the light/dark toggle working.
- `tools/MapConverter/`: the .mup/PDF converter. Since Nov 5 it strips HTML tags (e.g. `<b>…</b>`, which Because sometimes saves inside claim text) and unescapes entities in claim titles; before, the tags came out as literal text.
- `.github/workflows/build.yml`: render + publish to Pages; built files also saved as a run artifact.
- `CLAUDE.md` (conventions for future sessions), `README.md`, `LICENSE.md`.

## Accessibility findings
- Silktide (WCAG 2.1 AA): clean on the preface and 5.1 (Oct 27). Not yet run on 1.1–1.10 or 2.1–2.10.
- axe (WCAG 2.0–2.2 A/AA): 0 violations on the preface, 1.1–1.10, 2.1–2.10 and 5.1, light and dark (dark tested via the site's toggle), desktop and phone width.
- Keyboard opens the boxes; no sideways scrolling on phones; tap-to-enlarge on maps.
- Remaining limit: Word's 9 heading levels — a map deeper than 8 levels won't fit in the appendix; the build warns.

## 1.1 edits (Oct 27)
- Corrected Soda map ("nutritious") swapped in; four text typos fixed from Dona's revised Word document; "the" removed from "included in the school lunches"; "Applying the Four Big Steps…" made a main heading alongside "Argument Maps to the Rescue!".

## 1.2 Example 1 (Oct 29)
- Maps: Reason_Conclusion, Advertisement1, 1_A_2, Advertisement1_P_Eval. Captions and alt text written by Claude (Dona to check).
- Small fixes made while converting: Step headings' dashes made consistent; summary's second "Step 2 – Evaluating" renumbered Step 3; "That's why [conclusion]" spacing (×2); stray doubled closing quote; "instead of a bridge"; "an argument is a unit of reasoning"; "I shudder" (author alone).

## 1.3 Example 2 (Oct 29)
- Maps: Advertisement2, Advertisement2_P_Eval, Elixir. Captions and alt text written by Claude.
- Advertisement2_P_Eval.mup was identical to Advertisement2.mup (no evaluation note), though its PDF shows "[Evaluation: Assumes the Conclusion]". Claude added the note to the outline by hand; if the map is re-saved from Because, the .mup needs the note too.
- Fixes made while converting: "After all [conclusion]" → "After all [reason]" (×3, in every reason-indicator list); "That's why [conclusion]" spacing; Step heading dashes; "a bad premise"; "the reason indicator is placed"; "have true conclusions"; "worked through"; missing period after "reason indicator expressions".
- Left for Dona: "the Elixir" / "the elixir" capitalization varies between passages.

## 1.4 Example 3 (Oct 30)
- No maps or images; text only (fact vs. opinion, disagreement).
- Changes while converting: the bold lines "1) Disagreement" and "2) "Fact" vs. "Opinion"" became real level-4 headings under "Two Common Mistakes…" (screen-reader navigation; since Nov 3 they also show in the page's contents list); Step heading dash; "prove that the ultimate conclusion is true" (added "the"). The closing "Let's summarize…" and "Now let's take a look at another passage." lines kept as in the Word document.
- Oct 31: stray horizontal line (from an empty bold line in Word) removed at Dona's request.

## 1.5 Example 4 (Oct 30)
- Maps: Advertisement4, Advertisement4_P_Eval, Advertisement4_I_Eval (7 figures). Illustrations (flattened, supplied by Dona): ladder_good, ladder_cracked_boulder, ladder_broken. Captions and alt text written by Claude.
- Advertisement4_I_Eval: the first .mup lacked the inference note and both files lacked the "]" after "This premise is good."; Dona sent corrected .mup + PDF the same day. The new image is in, and the converter's outline now matches the hand-fixed one exactly.
- Fixes made while converting: "Cool and Fresh soap" → "Cool and Fresh soap must be the best" (as the conclusion); "therefore"; (semicolon outside quotes); "If I asked you" and "I think so" (author alone); "We'll call an objection that asserts that an inference is weak a…"; "this argument is bad"; "Just because..." (3 dots); "We will, instead, want"; "'Gully' for short" (missing quote, summary); summary bullets: comma after "[state the reason here]", capital "If"; "Communicating Our Evaluation" capitalized as in 1.3; underlined "Evaluating Inferences and the Map Analogy" made a level-3 heading (renamed "Evaluating Inferences vs. Evaluating Premises" by Dona, Nov 1); Step heading dashes; "Note:" lines moved out of the quotations.
- Oct 31: the same kind of stray horizontal line (before "(Will we always be ignoring questions?…") removed along with 1.4's.

## 1.6 Example 5 (Oct 30)
- Maps: Advertisement5, Advertisement5_P_Eval, Advertisement5_I_Eval, Lee1, Lee1_I_Eval, Lee2, Lee2_I_Eval, Lee3, Lee3_I_Eval (13 figures). Captions and alt text written by Claude.
- Lee3_I_Eval.mup first came without the inference note its PDF showed; Dona re-saved it the same day. The outline was already hand-fixed and matches; the image didn't change.
- Sad-face picture removed at Dona's request (a leftover she'd meant to delete).
- Fixes made while converting: "Degress" → "Degrees of Goodness"; "bad as a whole" (summary); missing period on the summary's Note; "-as is the case here" → em dash; "*most likely*" (one italic span); "…claimed?" and "Is this claim…" ("And" → "and", ×2); "if I said… obey me… my order or request" (author alone); Step heading dashes and bold removed from the Step 1 heading; "Note:" lines moved out of the quotations. Follow-up (Dona): "Gully Method" → "Gully Test"; "IQ" → "I.Q."; "I.Q.s" → "I.Q.'s".

## 1.7 Example 6 (Oct 31)
- No maps or images; text only (a passage that isn't an argument).
- Changes while converting: Step heading dashes; the summary's "Step 1 – Recognizing an Argument" made a level-3 heading under the summary (as in 1.4); an empty bold line from Word dropped.
- Revised the same day after Claude raised two points ("relaying facts" when one claim is an opinion; "Don't you agree?" might look like persuasion): Dona's new wording says "telling us things", adds a paragraph addressing "Don't you agree?", and uses "establish" instead of "prove". Claude removed a stray "to" ("saying anything to that might get us to agree").

## 1.8 Example 7 (Oct 31)
- Maps: Advertisement7, Advertisement7_P_Eval, Advertisement7_I_Eval (8 figures). Captions and alt text written by Claude.
- Advertisement7_I_Eval.mup first came without the inference note its PDF shows; outline fixed by hand. Dona re-saved the .mup the same day; the converter's outline now matches the hand-fixed one exactly (image unchanged).
- Structure: the six bold objections under "Swallowing the Bitter Pill" became level-4 headings (navigable), and the indented replies under them became ordinary paragraphs (they aren't quotations). The two indicator-list intro lines un-indented as in 1.3. "Summary of Example 7" demoted from Heading 1 to level 2, its Steps to level 3. Figures and "Note:" lines moved out of the quotations. Empty bold lines dropped.
- Fixes made while converting: "(… like "because")?" (question mark); "and **"Is this claim…"** (×2); "a form of deception" (stray "a"); "'it follows that' introduces a conclusion" (was "introduces a conclusion indicator expression"); "and I think that they're designed to make money" (was "we think"; author alone); comma removed before "could believe this premise"; "premise, so I think"; "*perfect*,"; "decide that the argument is *good*?" (was "map"); "more likely than not" (was "that"); "In short," (bold comma); "Its Ultimate Conclusion" (heading caps); missing opening quote and "..." on the second objection; "a perfect island must exist"; "the conclusion is false"; "what I've written … why I evaluated … as I did" (author alone); "Because arguments lie on a continuum between good and bad," (semicolon → comma); "suspend judgment" (spelling consistent); summary: "we decided", no comma after "It follows that", "its conclusion"; "constructing arguments—the last" (em dash).
- Follow-up (Dona): "the claim in back of" → "the claim after"; truth 2 now says "ultimate conclusion is probably true".

## 1.9 Constructing Arguments (Nov 1)
- Maps: Ultimate_Conclusion, Reason, Revised_Reason (4 figures; Revised_Reason appears twice). All three .mup files matched their PDFs. Captions and alt text written by Claude.
- The Word document's last map (under "Communicating Arguments") was an older image with no claim numbers or "Inference A" label; replaced with Revised_Reason (same claims). Flagged for Dona.
- Structure: Word Heading 1s demoted (The Introspection Myth, Steps 1–4, Communicating Arguments, Summary → level 2; Flawed Questions, Choosing a Question, Pro Tip → level 3). The indented bold "1) … 2) …" lines became numbered lists (not quotations); the summary's steps became a real numbered list.
- Fixes made while converting: "reason indicator" (was "indictor"); "some virtues require a level of interdependence" in the Pro Tip (was "independence"); "already presented with" (stray "in"); "buy into"; "What I want to do here… steps that I'm going to give you" (author alone); em dashes for " - " and "--"; "*clear and careful*" one italic span; empty lines dropped.
- Left for Dona: the article-writer example uses "he" throughout.

## Handbooks and printing (Nov 1)
- Each chapter ends with a handbook section (Dona's choice), printable on its own. Front matter `handbook: true`.
- Separate Word file per handbook (`downloads/Chapter-N-Handbook.docx`), linked in a box under the page title; built by `tools/build-handbooks.py` in the workflow after the book renders. Title without the section number ("Chapter 1 Handbook"); map descriptions in an "Appendix" at the end. Word chosen over PDF because tagged/accessible PDF output from the build tools isn't reliable.
- Printing any page from the browser prints only the content (no sidebar, header, search, contents, next/previous), black on white even from dark mode; collapsible descriptions left out. Handbook pages print the map descriptions in an "Appendix: Text Descriptions" at the end (on its own page), with "Text description: see the appendix, Figure N" under each map. Both are hidden on screen, including from screen readers.

## 1.10 Chapter 1 Handbook (Nov 1)
- Map: Ch1_Handbook (generic Ultimate Conclusion / Inference A / Premise). The .mup has an empty "Inference B" under the premise (nothing attached); not drawn in the PDF and the converter ignores it.
- Caption "A basic argument map." and alt text written by Claude (the Word document had no caption).
- Structure: headings shifted down one level under the page title; the bulleted terms (Ultimate Conclusion, Premise, Inference…) bolded with their explanations as paragraphs inside the bullet (were indented quotes); indicator lists nested under "Inference Indicator Expressions"; empty headings removed; the plain lines "Formulate the Thesis (our Conclusion)", "Argue in Favor of the Thesis", "Communicate the Argument" made level-3 headings; step 4 continues the numbering.
- Fixes: "A premise is a claim"; "That's why [conclusion]" spacing; "After all [reason]" (was [conclusion], as fixed in 1.3); "succeeds in establishing"; "Just because R, it doesn't follow"; "accept the claim at the top".
- Left for Dona: Step 3 reads "Formulate the answer you accept" here but "Identify the answer that you think is probably true" in 1.9.

## 2.1 Introduction (Nov 1)
- Chapter 2 part added: "Chapter 2: Premise / Subconclusion / Ultimate Conclusion Arguments" (from the Word document's title, "Chapter 2 - …").
- Illustrations (flattened, pasted by Dona in chat): boulders_one_ladder (140px), boulders_subconclusion (125px), sized in proportion to the Word document. Alt text written by Claude.
- Changes: headings shifted under "2.1 Introduction"; "Four Big Steps" capitalized as in 1.8; colon after "you'll learn"; comma after the last "Specifically"; empty lines dropped.

## 2.2 Example 1 (Nov 1)
- No maps or images; text only (a controversial passage that isn't an argument: censorship).
- Changes: Step heading dash; "Later on, though, we'll see" (comma); empty lines dropped.

## 2.3 Example 2 (Nov 3)
- Maps: Censorship2_partial, Censorship2, PU, PSU, Complex, Censorship2_I_Eval, Censorship2_P_Eval (12 figures). All Word images matched the PDFs, and both _Eval .mup files had their notes. PU/PSU/Complex are generic structure maps (PU.mup has an empty inference under the premise; ignored). Captions and alt text written by Claude.
- Fixes made while converting: heading "Step 2 – Analyzing the Argument" (was "an Argument"; matches the summary and Ch. 1); "get us to believe" (×2); "It's a claim that"; "two at a time—not three…—because"; "In this case, I gave"; "then the conclusion"; "If no part of the argument"; "real life"; "I think so" (was "We think so"; author alone); "refers"; stray comma before "recognize"; em dashes; Step heading dashes; summary "Our next question was"; "Turning to the ultimate conclusion"; empty heading and blank lines dropped.
- Content fixes flagged for Dona: "Premises 2 and 4" → "Premises 2 and 3 each provide their own line of support" (the Complex map has no Premise 4); summary "question Inference A and Claim 1 (a premise)" → "Claim 3"; the "We can allow our initial objection…—we should try…" sentence repunctuated as "(particularly … disagree)—but we should try…".
- Follow-up (Dona, Nov 3): "proven" → "established"; underlining removed from the summary's conclusion (a hold-over). "Evaluating Subconclusions" moved up from level 4 (under "Where to Start Evaluating") to level 3 so it shows in the page's contents list; "Start Where You Disagree" and "Start at the Top of the Map" stay at level 4. Still as written: "1 because 2 .... 9" (four dots).

## 2.4 Example 3 (Nov 3)
- No maps or images; text only (an explanation, not an argument: the student protests; Janice's interview).
- Changes: the underlined chapter title at the top of the Word document dropped (the part name in the sidebar carries it); Step heading dashes; "Chapter 3" (was "Chapter Three", to match the book's other chapter mentions); "\"because,\" it isn't" (comma inside the quotes); "passage—the claim" (em dash); empty bold/underlined lines and blank lines dropped.
- Follow-up (Dona): "of why" removed from "an explanation of why wants us to believe…".

## 2.5 Example 4 (Nov 4)
- Maps: Censorship4_Partial, Censorship4, Censorship4_mistake, Censorship4_IB_Eval (8 figures: partial ×2, full ×3, mistake ×1, IB_Eval ×2). All Word images matched the PDFs; the _IB_Eval .mup had its note. Captions and alt text written by Claude.
- Fixes made while converting: "get us to believe" (missing "to"); "because Claim 1 is the ultimate conclusion" (missing "is"); "(Gully) believes" (comma removed, ×2); "(i.e., claim 1)"; Step 1 question bolded as in 2.3; summary's Gully question given quote marks like the other bold questions; Step heading dashes; mid-paragraph line break split into two paragraphs; figures moved out of quotations; blank lines dropped.
- Left for Dona: the text says Inference B is "fairly bad" but the map's note says "This inference is bad."; "claim 2" / "Claim 2" capitalization varies within the section.

## 2.6 Example 5 (Nov 5)
- Statement commands and statement questions; skipping subconclusions when evaluating top-down.
- Maps: Censorship5_Partial, Censorship5, Censorship5_Eval (6 figures: each ×2). All Word images matched the PDFs; the _Eval .mup had all three notes. Censorship5.mup has an empty "Inference B" group and an empty inference under Claim 3 (ignored). Captions and alt text written by Claude.
- Map typo: Claim 1 read "stand upagainst" in the first .mup and PDFs. Dona sent corrected Censorship5 and Censorship5_Eval (.mup + PDF) the same day; new images are in, and the converter's outlines match the hand-fixed ones exactly. (Censorship5_Partial never had Claim 1.)
- Fixes made while converting: "Step 2 – Analyzing the Argument" (was "an Argument"); "Step 3 – Evaluating the Argument" (was "Step – Evaluating an Argument"); Step 1 question bolded as in 2.3/2.5; "get us to believe"; "more or less, "Stand up…"" (stray "the" removed); missing ")" after "help us to see this."; "related to the conclusion?" (was "."); "we see that the first sentence"; "the "after all," as a reason indicator, tells us" (comma); "the unit of reasoning supports"; "subconclusions." (period inside the bold); Step heading dashes; figures moved out of quotations; non-breaking-space lines dropped.
- Dona is fine with the text saying "fairly good" and the summary "good as a whole" (Nov 5).

## 2.7 Example 6 (Nov 5)
- Rephrasing an inflammatory claim ("Anyone would be stupid to think…" → Claim 2); stopping the evaluation at a bad inference.
- Maps: Censorship6_Partial, Censorship6, Censorship6_Eval (6 figures: each ×2). All Word images matched the PDFs; the _Eval .mup had its note (Inference B bad). Captions and alt text written by Claude.
- Fixes made while converting: "get us to believe"; "Inference B" (was "inference B"); "(Gully) believes" (comma removed, ×2, as in 2.5); "Claim 2" and "i.e.,"; em dash for "--"; "bad as a whole" (summary, missing "a"); "evaluate Inference A and the premise" (was "the Inference A and the Premise"); period added inside "[(2) Science can't advance… ideas.]" (×6, as in 2.6's bracketed claim); Step 1 question bolded; Step heading dashes; figures moved out of quotations; non-breaking-space lines dropped.
- Passage wording (Dona, Nov 5): "Anyone would be stupid" everywhere; Step 1 and the summary's opening copy said "crazy".

## 2.8 Example 7 (Nov 5)
- Longer passage: the author's question as a clue to the ultimate conclusion; emotional appeals left out; acknowledging opposition isn't part of the argument; double-checking inferences by reading down with "because"; tracing an objection to a subconclusion down to Inference A.
- Maps: Censorship7_Partial1, Censorship7_Partial2, Censorship7_Partial2_mistake, Censorship7, Censorship7_Eval (10 figures: Partial1 ×2, Partial2 ×2, mistake ×1, full ×3, Eval ×2). All Word images matched the PDFs; the _Eval .mup had its note. Censorship7_Partial2_mistake.mup has an empty extra "Inference B" group under Claim 2 (ignored). Captions and alt text written by Claude.
- Claims 3 and 4 had `<b>…</b>` tags inside the .mup text (not visible in the PDFs); converter fixed to drop them (re-running the 2.6/2.7 maps gave identical outlines).
- Push problem (Nov 5, evening): pushes were rejected for a few minutes with "remote rejected … fatal error in commit_refs_rules" (GitHub-side; the repo has no rulesets or branch protection). It cleared on its own ~10 minutes later; if it happens again, wait and retry.
- Fixes made while converting: "David Hume" (was "Human"); "get us to believe"; Step 2 question bolded and "What else is being claimed?" / "Are those claims part of the argument?" bolded as in other sections (body and summary); "uncomfortable," and we know" (missing closing quote); "Generally speaking,"; "inference indicator expressions attached" (plural); "the next sentence contains two claims" (was "the second sentence"; it's the passage's last sentence); "Claim 1/2/4" and "Inference A/B/C" capitalized throughout; "Because identifying inferences" (stray comma) with the bold ending after "because."; "whether or not our map" (was "or our not"); the two words of caution made a numbered list; "including double-checking" (stray "the"); "reasoning, though,"; "challenge, so"; "We're denying" (capital); "as we inspect" (was "as I inspect"); "*follow from*" one italic span; summary "by reading down" (was "be"); line break turned into a paragraph break; figures moved out of quotations; non-breaking-space lines dropped.
- Follow-up (Dona): "reading down the lines" (was "arrows"); "weak"/"bad" for inferences is fine (both usages OK book-wide); "Being able to map an argument is important because…" (was "is often an end in itself because…").

## 2.9 Constructing Arguments (Nov 5)
- Maps: Reason, Reason_for_Reason (2 figures). The first versions of both said "All virtues"; the text (and 1.9's revision) use "Some virtues". Dona chose to re-save them before publishing (held on a draft branch meanwhile); the corrected maps arrived the same evening. The new Reason map is identical to 1.9's Revised_Reason. Captions and alt text written by Claude.
- Structure: the Word document's Heading 1s ("Communicating Arguments", "Summary of Constructing Arguments") became level 2 under the page title, as in 1.9; "Provide Support for Reasons" level 2; "Conclusion Placement" level 3.
- Fixes: "transform such premises into subconclusions" (was "in"); "An exception to this rule, of course, is when…" (missing "is"); "once they reach it" (was "the"); stray period after "…affect you?)"; "unless it's controversial, and we saw"; "rugged individualism" (no hyphen); blank lines dropped.
- The temporary draft branch was deleted by Dona on GitHub (the session can't delete branches: git push --delete hangs up and the API path is blocked). To hold work without publishing, push to a branch; only main publishes.

## 2.10 Chapter 2 Handbook (Nov 5)
- Built like 1.10: `handbook: true`, download box for `downloads/Chapter-2-Handbook.docx` (build-handbooks.py picked it up with no changes), print-only appendix checked (6 printed pages from dark mode, appendix present, download box hidden).
- Map: Ch2_Handbook (generic Ultimate Conclusion / Inference A / Sub Conclusion / Inference B / Premise); matched its PDF. Caption and alt text written by Claude.
- Bold marks what's new since the Chapter 1 handbook (Dona confirmed, Nov 5). An italic note under the title says so: "Items in bold are new in Chapter 2 (apart from the key terms in the definitions at the start)." Term labels (Ultimate Conclusion, Premise, Inference…) are NOT bolded here (unlike 1.10), so bold only means new; "Subconclusion" and "Ultimate Conclusion & Subconclusion" stay bold. "Where to Start" became a heading, so it no longer stands out as new. Future handbooks: ask whether the same convention applies.
- Structure: headings shifted down one level; bold "Where to Start" made a level-3 heading; plain "Formulate the Thesis…", "Argue in Favor…", "Communicate the Argument" made level-3 headings; indented explanations moved inside their bullets; line breaks inside the "Think about only two things" / "Inference indicators" bullets made paragraphs; steps 4–6 continue the numbering; empty headings removed.
- Fixes (several the same as 1.10's): "A premise is a claim"; "That's why [conclusion]" spacing; "After all [reason]" (was [conclusion]); "succeeds in establishing"; "accept the claim at the top"; "Just because R, it doesn't follow"; one bold span for "but *don't map it right away* because…".
- "Subconclusion" is one word throughout the book (Dona, Nov 5). The handbook map's outline and alt text hand-fixed; Dona re-saved Ch2_Handbook the same evening; new image in, converter outline matches. 5.1's "sub-conclusion" also fixed.

## Next
- Run Silktide on 1.1–1.10 and 2.1–2.10; send IT the clean screenshots (preface, 1.1–1.10, 2.1–2.10, 5.1) plus the URL.
- Add the section links to Canvas and test embedding (External URL item).
- Share with the accessibility office for review.
- Convert further sections; rebuild .mup files, named to match their images.
- Watch the book-wide Word file's size (7 MB with 19 sections on Nov 5; projected ~18–20 MB for the full book). If it gets unwieldy for students, options: one Word file per chapter, or smaller map images in Word only. Revisit around Chapter 3–4. Build time isn't a concern (50 s render for 19 sections; ~4 min total projected for the full book).

## Later changes to Chapters 1–2 and the preface (reconstructed Nov 22 from git history and session transcripts)
- Nov 10, handbooks rebuilt (commits 0d4ff9f, e86a1b8, 9409e5c): 1.10 and 2.10 replaced with Dona's new Word handbooks. Terms and Analyzing steps as headings; new generic maps Ch1_Handbook and Ch2_Handbook ("Claim" boxes) and a new Inference map (Conclusion / Reason) in both; all matched their PDFs. Captions and alt text for the Inference map written by Claude; Dona's Chapter 2 caption kept (it names ultimate conclusion, subconclusion and premise although the boxes say "Claim"). New material marked with a bold "NEW:" label only, Word highlight dropped (replaces the Nov 6 whole-item-bold convention). Fixes: "That's why [conclusion]" spacing, "After all [reason]", "succeeds in establishing", "Just because R, it doesn't follow", "accept the claim at the top", "A subconclusion is a claim", "Subconclusions" one word, period after "presented in the argument"; the two Premise questions became a numbered list inside "Ask:".
- Nov 10, Dona's decisions: 1.10 gets "3) Continue to the End" (not marked NEW in 2.10; not substantive). "Research answers." and "Lead with the conclusion unless it would alienate your reader…" are the wording for all handbooks (they differ from 1.9/2.9, intentionally). Communicating order: Decide what claims (from Chapter 3) → Decide in what order (Chapter 2) → Make the connections clear (Chapter 1), numbered from 1) with only what the chapter covers. In 2.10, "NEW: 1) Decide in what order…" is a numbered heading (Claude's choice; a bullet in Dona's Word file). All recorded in CLAUDE.md.
- Nov 14, preface (296d615): "A claim marked "(Stopping Point)" has nothing further supporting or objecting to it." (added "or objecting to").
- Nov 15, 1.8 (93585b5): the six "Swallowing the Bitter Pill" subsections got Dona's short titles; each full objection now opens its subsection as a paragraph. "Some convincing arguments have false conclusions." uses "convincing" on purpose (Dona): "good" would read as the book's own claim in the right-hand contents list. Period added to match the other titles.
