from pathlib import Path

R = Path(__file__).resolve().parent
source = R / 'apply_v08_redesign_fixed.py'
text = source.read_text(encoding='utf-8')

old_start = "CAP_REVIEW = r'''cap_svg = f'''<svg"
new_start = 'CAP_REVIEW = r"""cap_svg = f\'\'\'<svg'
if old_start not in text:
    raise RuntimeError('CAP_REVIEW start marker not found')
text = text.replace(old_start, new_start, 1)

old_end = "(D / 'Drawing_V08_Overlap_Lid_Side.svg').write_text(side_svg, encoding='utf-8')\n'''\n\n\nPAGE1"
new_end = "(D / 'Drawing_V08_Overlap_Lid_Side.svg').write_text(side_svg, encoding='utf-8')\n\"\"\"\n\n\nPAGE1"
if old_end not in text:
    raise RuntimeError('CAP_REVIEW end marker not found')
text = text.replace(old_end, new_end, 1)

code = compile(text, str(source), 'exec')
namespace = {'__name__': '__main__', '__file__': str(source)}
exec(code, namespace)
