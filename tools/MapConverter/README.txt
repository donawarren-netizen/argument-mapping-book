ARGUMENT MAP CONVERTER
======================

What it does
------------
This converter turns argument maps made in Because (app.philmaps.com),
saved as .mup files, into text descriptions that screen reader users can
explore. For each map it produces two files:

  MapName_description.html   Web version. The map as a nested bulleted
                             list inside a collapsible "Text description"
                             section. Paste it into a web page, such as a
                             WordPress Custom HTML block, below the map image.

  MapName_description.docx   Word version. The map as a Word outline, with
                             one heading per claim and per connector, so
                             screen reader users can jump between them.

  MapName_list.md            The same description as a plain bulleted
                             list in Markdown, with no drop-down. Paste it
                             anywhere Markdown is accepted, such as a
                             Quarto page or a Quarto callout box.

If you also save a PDF of the map (see "Map images" below) with the same
name as the .mup file, it also produces:

  MapName.png                The map image, trimmed, at high resolution.

  MapName_quarto.md          A ready-to-paste block for a Quarto page: the
                             image at the right display size, with short
                             alt text, followed by the collapsible text
                             description.

You can convert one map or a whole folder of maps at once.


What's in this folder
---------------------
  convert_maps.py        The program you run.
  mup_to_html_list.py    Builds the web version.
  mup_to_outline.py      Reads the .mup files (shared by all versions).
  pdf_to_image.py        Turns map PDFs into trimmed images.
  build_docx.js          Builds the Word version.
  README.txt             This file.

Keep all of these files together in the same folder.


One-time setup (Windows)
------------------------
1. Install Python.
   Go to python.org, choose Downloads, and run the installer. On the first
   installer screen, check the box "Add python.exe to PATH" before
   clicking Install Now. This box is easy to miss and it matters.

2. Install Node.js.
   Go to nodejs.org, download the version marked LTS, and run the
   installer with the default options.

3. Open a command window in this folder.
   Open this folder in File Explorer. Click in the address bar at the top
   (or press Alt+D), type  cmd  and press Enter. A Command Prompt window
   opens, already pointed at this folder.

4. Check that both installed.
   Type each of these and press Enter:
       python --version
       node --version
   Each should reply with a version number. If one says it is "not
   recognized," restart the computer and try again. If Python still isn't
   found, rerun its installer and check the PATH box.

5. Install the Word library.
   In the same window, type this and press Enter:
       npm install docx
   A folder called node_modules will appear here. Leave it in place.

6. Install the image libraries (only needed for map images).
   In the same window, type this and press Enter:
       pip install pypdfium2 pillow
   (On a Mac: pip3 install pypdfium2 pillow)


One-time setup (Mac)
--------------------
Same as Windows, with these differences:
  - Install Python from python.org (there is no PATH box to check).
  - To open a command window in this folder: open Terminal, type  cd
    followed by a space, drag this folder onto the Terminal window, and
    press Return.
  - Type  python3  wherever these instructions say  python .


Converting maps
---------------
1. Put your .mup files in a subfolder of this folder, for example one
   called  maps .

2. Open a command window in this folder (setup step 3).

3. Type this and press Enter:
       python convert_maps.py maps

The converter lists each map as it goes. The web and Word versions appear
in the maps folder next to the original .mup files. If a map can't be
converted, the others still are, and a list of any failures appears at
the end.

Other ways to run it:
  One map:
       python convert_maps.py maps\Chapter6_Map1.mup
  Put the results in a separate folder (here, one called "output"):
       python convert_maps.py maps output
  Choose the name used in a single map's web summary line:
       python convert_maps.py maps\Chapter6_Map1.mup --name "Map 6.1"

(On a Mac, use / instead of \ in folder paths, and python3 instead of
python.)

By default, the web version's summary line reads just "(Text description)".
File names are for your own reference and don't appear in either version.
To include a name, use --name, which gives e.g. "(Text description of Map 6.1)".


Map images
----------
Because saves maps only as PDFs (through the browser's print dialog).
Save each map's PDF in the same folder as its .mup file, with the same
name: Chapter6_Map1.mup and Chapter6_Map1.pdf. The converter then makes
the image and the Quarto block too. Maps without a PDF still get their
web and Word descriptions.

  - The browser's header and footer (date, page title, web address,
    page number) are removed automatically, along with the white margins.
  - Keep the print scale the same for every map (don't use "fit to
    page"). The display width is worked out from the PDF, so maps
    printed at the same scale show text at the same size.
  - Each map should fit on one page. If a PDF has more than one page,
    only the first is used and the converter prints a warning.

Quarto blocks point to the image in a folder called "images". To point
to a different folder, add --images, for example:
       python convert_maps.py maps --images images/ch06
Put the .png files in that folder of your Quarto project.


Using the results
-----------------
Quarto:
  Open the _quarto.md file in a plain text editor, copy everything, and
  paste it into your .qmd page where the map belongs. The description is
  wrapped in a raw HTML block (```{=html} ... ```) so Quarto passes it
  through exactly as written. To give a drop-down its own label, edit
  the words between <summary> and </summary>.

Web (WordPress):
  Open the .html file in a plain text editor such as Notepad (not in a
  browser, and not in Word). Copy everything, then paste it into a
  Custom HTML block directly below the map image. Don't paste it into a
  regular paragraph block, which can strip the list structure.

Word:
  Open the .docx file and copy its contents into your document, or use
  it as is. It uses Word's built-in heading styles, so it shows up in
  the Navigation Pane.

Checking accessibility:
  After publishing a web page, you can run it through a free checker such
  as WAVE (wave.webaim.org) or the axe DevTools browser extension.


How maps are read
-----------------
The descriptions follow these conventions, so a few habits when making
maps in Because will give the best results:

  - Connector labels: "Inf." is written out as "Inference" and "Outf." as
    "Outference." A "Not So" or "So What" qualifier is moved after the
    letter, so every connector entry starts with its type, e.g.
    "Outference D - Not So."
  - Unlabeled connectors are read as "(unlabeled)" rather than skipped.
  - Role 2 claims: type  (r2)  anywhere in the claim's text. It is read as
    a "Role 2:" prefix. (An asterisk also works, for older maps, but some
    screen reader settings skip asterisks, so (r2) is preferred.)
  - A claim with nothing beneath it is marked "(Stopping Point)."
  - Empty connector groups and sticky notes are left out.
  - Boxes with no words in them (blank, or just "." used for spacing)
    are left out. A blank box with claims beneath it is read as
    "(blank claim)" so the structure under it stays in place.
  - Depth: the web version has no depth limit. Word allows nine heading
    levels, so in the Word version anything deeper than level 9 stays at
    Heading 9.


Troubleshooting
---------------
"python is not recognized" or "node is not recognized"
  Restart the computer. If it continues, reinstall, and for Python make
  sure "Add python.exe to PATH" is checked.

"Cannot find module 'docx'"
  Run  npm install docx  in this folder (setup step 5). The node_modules
  folder must be in the same folder as build_docx.js.

"No .mup files found"
  Check the folder name you typed, and that the maps end in .mup.

A description doesn't match the map
  Open the map in Because and check the connector labels and (r2)
  markers; the converter reads exactly what is typed in the map.
