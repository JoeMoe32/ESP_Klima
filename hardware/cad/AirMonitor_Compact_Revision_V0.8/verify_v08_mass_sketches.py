from __future__ import annotations

from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageOps, ImageStat

R = Path(__file__).resolve().parent
PDF = R / "AirMonitor_V08_Massskizzen_1zu1.pdf"
OUT = R / "03_Renders_Drawings"
OUT.mkdir(parents=True, exist_ok=True)

EXPECTED_PAGES = 11
REVIEW_PAGES = {
    4: "MassSketch_V08_Page04_Lid.png",
    9: "MassSketch_V08_Page09_Assembly.png",
    10: "MassSketch_V08_Page10_PrintDetail.png",
    11: "MassSketch_V08_Page11_Checklist.png",
}

if not PDF.exists():
    raise SystemExit(f"Missing PDF: {PDF}")

pdf = pdfium.PdfDocument(str(PDF))
if len(pdf) != EXPECTED_PAGES:
    raise SystemExit(f"Expected {EXPECTED_PAGES} pages, got {len(pdf)}")

thumbs: list[Image.Image] = []
for index in range(len(pdf)):
    page = pdf[index]
    preview = page.render(scale=0.55).to_pil().convert("RGB")
    stat = ImageStat.Stat(preview.convert("L"))
    if stat.stddev[0] < 3.0:
        raise SystemExit(f"Page {index + 1} appears blank (stddev={stat.stddev[0]:.2f})")

    thumb = ImageOps.contain(preview, (510, 350))
    framed = Image.new("RGB", (530, 390), "white")
    framed.paste(thumb, ((530 - thumb.width) // 2, 25))
    draw = ImageDraw.Draw(framed)
    draw.text((12, 6), f"Seite {index + 1}", fill="black")
    thumbs.append(framed)

    page_no = index + 1
    if page_no in REVIEW_PAGES:
        full = page.render(scale=1.65).to_pil().convert("RGB")
        full.save(OUT / REVIEW_PAGES[page_no])

cols = 3
rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 530, rows * 390), "white")
for i, thumb in enumerate(thumbs):
    sheet.paste(thumb, ((i % cols) * 530, (i // cols) * 390))
sheet.save(OUT / "MassSketches_V08_ContactSheet.png")

verification = R / "MASS_SKETCH_VERIFICATION.txt"
verification.write_text(
    "\n".join(
        [
            "AirMonitor Compact V0.8 - Mass sketch verification",
            f"PDF: {PDF.name}",
            f"Page count: {len(pdf)}",
            "Blank-page check: passed for all pages",
            "Dedicated guide print detail: page 10",
            "Review renders:",
            *[f"- 03_Renders_Drawings/{name}" for name in REVIEW_PAGES.values()],
            "- 03_Renders_Drawings/MassSketches_V08_ContactSheet.png",
        ]
    )
    + "\n",
    encoding="utf-8",
)

print(verification.read_text(encoding="utf-8"))
