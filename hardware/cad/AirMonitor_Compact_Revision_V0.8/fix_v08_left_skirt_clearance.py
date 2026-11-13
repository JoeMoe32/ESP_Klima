from pathlib import Path

p = Path(__file__).resolve().parent / "build_v08.py"
text = p.read_text(encoding="utf-8")
old = "                           C.LID_SKIRT_W + 0.6,\n"
new = "                           C.WALL + 0.8,\n"
if text.count(old) != 1:
    raise RuntimeError(f"expected one skirt-clearance expression, found {text.count(old)}")
p.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Expanded open insertion end to clear the full-height left wall")
