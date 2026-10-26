#!/usr/bin/env python3
"""
Turn a map PDF printed from Because into a trimmed, high-resolution PNG,
and work out the display width that keeps text the same size across maps.

The PDF is the browser's printout of the map, so it carries the browser's
header and footer (date, page title, web address, page number) in the
page margins. That text is blanked out, the remaining white space is
trimmed, and the map is saved at 300 dpi -- about 3x screen resolution,
so it stays sharp when readers zoom in.

Usage:
    python3 pdf_to_image.py Map.pdf            -> Map.png, prints its width
Requires:  pip install pypdfium2 pillow
"""
import sys
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageChops, ImageDraw

DPI = 300
SCALE = DPI / 72            # PDF points -> image pixels
CSS_PX_PER_PIXEL = 96 / DPI  # image pixels -> on-screen (CSS) pixels
EDGE_BAND = 28              # points; browser header/footer text sits within this of the edge
PAD = 40                    # pixels of white space kept around the map


def pdf_to_png(pdf_path, png_path):
    """Write the trimmed PNG. Returns (display_width_px, page_count)."""
    pdf = pdfium.PdfDocument(str(pdf_path))
    pages = len(pdf)
    page = pdf[0]
    page_w, page_h = page.get_size()

    im = page.render(scale=SCALE).to_pil().convert("RGB")

    # Blank out only text lying entirely within the edge bands: that's the
    # browser's header and footer. Map content sits inside the margins.
    draw = ImageDraw.Draw(im)
    text = page.get_textpage()
    for i in range(text.count_rects()):
        left, bottom, right, top = text.get_rect(i)  # PDF coords, origin bottom-left
        near_top = bottom >= page_h - EDGE_BAND
        near_bottom = top <= EDGE_BAND
        if near_top or near_bottom:
            draw.rectangle(
                [left * SCALE - 4, (page_h - top) * SCALE - 4,
                 right * SCALE + 4, (page_h - bottom) * SCALE + 4],
                fill="white")

    diff = ImageChops.difference(im, Image.new("RGB", im.size, "white"))
    mask = diff.convert("L").point(lambda p: 255 if p > 12 else 0)
    box = mask.getbbox()
    if box is None:
        raise ValueError("the PDF page is blank")
    x0, y0, x1, y1 = box
    im = im.crop((max(x0 - PAD, 0), max(y0 - PAD, 0),
                  min(x1 + PAD, im.width), min(y1 + PAD, im.height)))
    im.save(png_path, optimize=True)
    pdf.close()
    return round(im.width * CSS_PX_PER_PIXEL), pages


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".png")
    width, pages = pdf_to_png(src, out)
    print(f"Wrote {out} (display width {width}px)")
    if pages > 1:
        print(f"Warning: the PDF has {pages} pages; only page 1 was used.")
