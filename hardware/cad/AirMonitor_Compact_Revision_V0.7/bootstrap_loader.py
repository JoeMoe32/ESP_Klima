"""Load and execute compressed V0.7 bootstrap payload."""
from pathlib import Path
import base64
R=Path(__file__).resolve().parent
parts=sorted(R.glob("bootstrap_v07.part*"))
if not parts:
    raise SystemExit("bootstrap parts missing")
code=base64.b64decode("".join(p.read_text().strip() for p in parts))
exec(compile(code, str(R/"bootstrap_v07_payload.py"), "exec"))
