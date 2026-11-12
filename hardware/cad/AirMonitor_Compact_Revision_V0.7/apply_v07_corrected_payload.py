from pathlib import Path
import base64,zlib,json
R=Path(__file__).resolve().parent
parts=sorted(R.glob("v07_corrected_payload.part*"))
if not parts: raise SystemExit("payload parts missing")
enc="".join(p.read_text().strip() for p in parts)
data=json.loads(zlib.decompress(base64.b64decode(enc)).decode("utf-8"))
for rel,content in data.items():
    p=R/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding="utf-8")
    print("wrote",rel,len(content))
