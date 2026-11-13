from pathlib import Path

R = Path(__file__).resolve().parent
P = R / "generate_mass_sketches_v08.py"
MARKER = "PAGE10_LABEL_SPACING_FIX_V3"

text = P.read_text(encoding="utf-8")
if MARKER in text:
    print("V0.8 page-10 label spacing already fixed")
    raise SystemExit(0)

text = text.replace(
    "PAGE10_LAYOUT_FIX_V2 = True\n",
    "PAGE10_LAYOUT_FIX_V2 = True\nPAGE10_LABEL_SPACING_FIX_V3 = True\n",
    1,
)
text = text.replace(
    "label(c, x, sy + 98 * mm, title, 8, True)",
    "label(c, x, sy + 106 * mm, title, 8, True)",
    1,
)
text = text.replace(
    "sy + 10.0 * scale + 5 * mm, \"Haut 1,60\", 1.2)",
    "sy + 10.0 * scale + 2 * mm, \"Haut 1,60\", 1.2)",
    1,
)

P.write_text(text, encoding="utf-8")
print("Applied V0.8 page-10 label spacing fix")
