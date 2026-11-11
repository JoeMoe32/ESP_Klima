"""Kollisions- und Massprüfung AirMonitor Compact V0.6.

Aufruf: python check_clearances.py   -> Exitcode 0 = alles i. O.
Wird von build_compact_revision.py vor dem Export ausgeführt.

V0.6 ergänzt gezielte Prüfungen für die rechte Rückwand:
- Die 80-mm-Tasterplatine und ihr 76-mm-Lochbild sind auf der Wand zentriert.
- Die vier Halter liegen frei zwischen den beiden Deckelschraubsäulen.
- ZERO/SPAN behalten ihre gemessenen Offsets auf der Platine.
- DC5521 liegt unterhalb und mittig zwischen ZERO und SPAN.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compact_params as C  # noqa: E402

MIN_GAP = 0.3  # mm Mindestabstand zwischen getrennten Körpern [Entscheidung]


def rect_dist(px, py, x0, x1, y0, y1):
    dx = max(x0 - px, 0.0, px - x1)
    dy = max(y0 - py, 0.0, py - y1)
    return math.hypot(dx, dy)


def interval_gap(a0, a1, b0, b1):
    if a1 < b0:
        return b0 - a1
    if b1 < a0:
        return a0 - b1
    return 0.0


def aabb_gap(a, b):
    """Kleinster 3D-Abstand zweier achsparalleler Boxen x0,x1,y0,y1,z0,z1."""
    dx = interval_gap(a[0], a[1], b[0], b[1])
    dy = interval_gap(a[2], a[3], b[2], b[3])
    dz = interval_gap(a[4], a[5], b[4], b[5])
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def run():
    rows, bad = [], 0

    def chk(name, value, limit, unit='mm', ge=True):
        nonlocal bad
        ok = value >= limit - 1e-9 if ge else value <= limit + 1e-9
        bad += not ok
        rows.append(f"{'OK ' if ok else 'NOK'} {name}: {value:.2f} {unit} ({'≥' if ge else '≤'} {limit:.2f})")

    lid_boss_r = C.LID_BOSS_D / 2
    cr = C.CARRIER
    tongues = [(*C.TONGUE_X, *ty) for ty in (C.TONGUE_FRONT_Y, C.TONGUE_BACK_Y)]
    bp = C.BTN_PCB_DUMMY
    dc_y, dc_z, dc_d = C.DC5521

    # DC5521-Kontermutter innen [Annahme: SW14 -> Ø16, 3,0 dick an der Wand]
    nut = (C.L - C.WALL - 3.0, C.L - C.WALL,
           dc_y - 8.0, dc_y + 8.0,
           dc_z - 8.0, dc_z + 8.0)

    for x, y in C.LID_BOSSES:
        tag = f'P01 Deckelbosse ({x:.1f}/{y:.1f})'
        chk(f'{tag} ↔ Waveshare-Träger', rect_dist(x, y, cr[0], cr[1], cr[2], cr[3]) - lid_boss_r, MIN_GAP)
        for i, t in enumerate(tongues):
            chk(f'{tag} ↔ P03-Zunge {i+1}', rect_dist(x, y, *t) - lid_boss_r, MIN_GAP)
        chk(f'{tag} ↔ Tasterplatine', rect_dist(x, y, bp[0], bp[1], bp[2], bp[3]) - lid_boss_r, MIN_GAP)
        chk(f'{tag} ↔ DC5521-Mutter [Annahme]', rect_dist(x, y, nut[0], nut[1], nut[2], nut[3]) - lid_boss_r, MIN_GAP)
        chk(f'{tag} ↔ Pod-Aussenkörper', rect_dist(x, y, C.POD[0], C.POD[1], C.POD[2], C.POD[3]) - lid_boss_r, MIN_GAP)

    pod_boss_r = C.POD_BOSS_D / 2
    for x, y in C.POD_MOUNTS:
        tag = f'P02 Pod-Bosse ({x:.1f}/{y:.1f})'
        chk(f'{tag} ↔ P03-Wand', rect_dist(x, y, *C.POD[:4]) - pod_boss_r, MIN_GAP)
        chk(f'{tag} ↔ P08-Dichtung', rect_dist(x, y, *C.P08['x'], *C.P08['y']) - pod_boss_r, MIN_GAP)
        for bx, by in C.LID_BOSSES:
            chk(f'{tag} ↔ P01-Deckelbosse ({bx:.1f}/{by:.1f})', math.hypot(x - bx, y - by) - pod_boss_r - lid_boss_r, MIN_GAP)
        on = any(t[0] + C.TONGUE_HOLE_D / 2 <= x <= t[1] - C.TONGUE_HOLE_D / 2 and
                 t[2] + C.TONGUE_HOLE_D / 2 <= y <= t[3] - C.TONGUE_HOLE_D / 2 for t in tongues)
        chk(f'{tag} Schraubloch liegt in Zunge', float(on), 1.0, unit='')
    chk('P02 Pod-Bosse Unterkante = Zungen-Oberkante', abs(C.POD_BOSS_Z0 - C.TONGUE_Z[1]), 0.0, ge=False)
    chk('P03 Zungen-Unterkante über Waveshare', C.TONGUE_Z[0] - C.BOARD_TOP_Z, 5.0)

    hs_r = C.HOOD_SCREW_BOSS_D / 2
    for x, y in C.HOOD_SCREWS:
        tag = f'P02 Haubenschraub-Bosse ({x:.1f}/{y:.1f})'
        chk(f'{tag} ↔ P03-Wand', rect_dist(x, y, *C.POD[:4]) - hs_r, MIN_GAP)
        chk(f'{tag} ↔ P08-Dichtung', rect_dist(x, y, *C.P08['x'], *C.P08['y']) - hs_r, MIN_GAP)
        chk(f'{tag} über P03-Zunge (Z-Abstand)', C.HOOD_SCREW_BOSS_Z0 - C.TONGUE_Z[1], MIN_GAP)
        for bx, by in C.LID_BOSSES + C.POD_MOUNTS:
            r2 = lid_boss_r if (bx, by) in C.LID_BOSSES else pod_boss_r
            chk(f'{tag} ↔ Bosse ({bx:.1f}/{by:.1f})', math.hypot(x - bx, y - by) - hs_r - r2, MIN_GAP)
        chk(f'{tag} ausserhalb P04-Dichtung', rect_dist(x, y, *C.P04['x'], *C.P04['y']) - 1.1, 0.5)

    # ---------- Rechte Rückwand V0.6 ----------
    chk('Tasterplatine ↔ Rückwand innen', (C.W - C.WALL) - bp[3], MIN_GAP)
    chk('Tasterplatine ↔ Vorderwand innen', bp[2] - C.WALL, MIN_GAP)
    chk('Tasterplatine ↔ Waveshare-Träger (X)', bp[0] - cr[1], MIN_GAP)
    chk('Tasterplatine ↔ DC5521-Mutter 3D [Annahme]', aabb_gap(bp, nut), MIN_GAP)

    # Platinenkörper und Lochbild müssen geometrisch in der Wandmitte liegen.
    pcb_y_center = (bp[2] + bp[3]) / 2
    holder_y_center = sum(C.BTN_HOLDER_Y) / 2
    chk('Tasterplatine auf Wandmitte Y', abs(pcb_y_center - C.W / 2), 0.01, ge=False)
    chk('Halter-Lochbild auf Wandmitte Y', abs(holder_y_center - C.W / 2), 0.01, ge=False)

    # Projektion der beiden senkrechten Deckelsäulen an der rechten Stirnwand.
    rear_column_y = sorted(y for x, y in C.LID_BOSSES if x > C.L - 30.0)
    if len(rear_column_y) == 2:
        low_col, high_col = rear_column_y
        chk('Platine frei von unterer Deckelsäule (Y-Projektion)', bp[2] - (low_col + lid_boss_r), MIN_GAP)
        chk('Platine frei von oberer Deckelsäule (Y-Projektion)', (high_col - lid_boss_r) - bp[3], MIN_GAP)
        holder_r = C.BTN_HOLDER_D / 2
        chk('Halter unten frei von Deckelsäule', C.BTN_HOLDER_Y[0] - low_col - holder_r - lid_boss_r, MIN_GAP)
        chk('Halter oben frei von Deckelsäule', high_col - C.BTN_HOLDER_Y[1] - holder_r - lid_boss_r, MIN_GAP)

    # ZERO/SPAN bleiben auf der Platine und behalten das gemessene 16-mm-Raster.
    pcb_y0, pcb_z0 = bp[2], bp[4]
    chk('ZERO Offset ab Platinenkante Y', abs((C.ZERO[0] - pcb_y0) - 20.0), 0.01, ge=False)
    chk('SPAN Offset ab Platinenkante Y', abs((C.SPAN[0] - pcb_y0) - 36.0), 0.01, ge=False)
    chk('ZERO/SPAN Mittenabstand', abs((C.SPAN[0] - C.ZERO[0]) - 16.0), 0.01, ge=False)
    chk('ZERO Höhe ab Platinenunterkante', abs((C.ZERO[1] - pcb_z0) - 8.0), 0.01, ge=False)
    chk('SPAN Höhe ab Platinenunterkante', abs((C.SPAN[1] - pcb_z0) - 8.0), 0.01, ge=False)

    for nm, (y, z, d) in (('ZERO', C.ZERO), ('SPAN', C.SPAN)):
        chk(f'{nm}-Bohrung innerhalb Tasterplatine (Y)', min(y - bp[2], bp[3] - y) - d / 2, 1.0)
        chk(f'{nm}-Bohrung innerhalb Tasterplatine (Z)', min(z - bp[4], bp[5] - z) - d / 2, 1.0)

    # DC5521 genau unter und mittig zwischen den beiden Microtastern.
    switch_mid_y = (C.ZERO[0] + C.SPAN[0]) / 2
    chk('DC5521 Y mittig unter ZERO/SPAN', abs(dc_y - switch_mid_y), 0.01, ge=False)
    service_bottom = min(C.ZERO[1] - C.ZERO[2] / 2, C.SPAN[1] - C.SPAN[2] / 2)
    dc_top = dc_z + dc_d / 2
    chk('Vertikaler Abstand DC5521 zu Serviceöffnungen', service_bottom - dc_top, 1.0)

    # Vertikal – unverändert aus V0.3
    chk('Freiraum Waveshare → Pod', C.POD[4] - C.BOARD_TOP_Z, 10.0)
    chk('Freiraum SEN0661 → Deckel', C.LID_Z - C.SEN_CON[5], 0.5)
    gap8 = C.LID_Z - C.POD[5]
    chk('P08 Verpressung', (C.P08['t'] - gap8) / C.P08['t'] * 100, 15.0, unit='%')
    chk('P08 Verpressung max', (C.P08['t'] - gap8) / C.P08['t'] * 100, 35.0, unit='%', ge=False)
    gap4 = C.HOOD_Z0 - (C.LID_Z + C.LID_T)
    chk('P04 Verpressung', (C.P04['t'] - gap4) / C.P04['t'] * 100, 15.0, unit='%')
    chk('P04 Verpressung max', (C.P04['t'] - gap4) / C.P04['t'] * 100, 35.0, unit='%', ge=False)

    # Luftweg – unverändert aus V0.3
    px0, px1, py0, py1 = C.POD[0] + C.POD_WALL, C.POD[1] - C.POD_WALL, C.POD[2] + C.POD_WALL, C.POD[3] - C.POD_WALL
    w4x = (C.P04['x'][0] + C.P04['web'], C.P04['x'][1] - C.P04['web'])
    win = [(C.P04['y'][0] + C.P04['web'], C.P04['bar_y'][0]), (C.P04['bar_y'][1], C.P04['y'][1] - C.P04['web'])]
    fo = C.HOOD_FLOOR_OPEN
    side = {}
    for i, (x, y, lx, ly) in enumerate(C.VENTS, 1):
        chk(f'Schlitz {i} in Sensorzelle', min(x - px0, px1 - x - lx, y - py0, py1 - y - ly), 1.0)
        k = [j for j, (a, b) in enumerate(win) if a + 0.5 <= y and y + ly <= b - 0.5]
        chk(f'Schlitz {i} vollständig in einem P04-Fenster', float(len(k) == 1), 1.0, unit='')
        chk(f'Schlitz {i} unter Haubenöffnung (X)', min(x - fo[0], fo[1] - x - lx), 0.5)
        if k:
            side.setdefault(k[0], []).append(i)
        chk(f'Schlitz {i} innerhalb P04 (X)', min(x - w4x[0], w4x[1] - x - lx), 0.5)
    rows.append(f"    IN-Seite Schlitze {side.get(0)}, OUT-Seite Schlitze {side.get(1)}")
    chk('Trennsteg Haube = P04-Quersteg', abs(C.HOOD_DIVIDER_Y[0] - C.P04['bar_y'][0]) + abs(C.HOOD_DIVIDER_Y[1] - C.P04['bar_y'][1]), 0.0, ge=False)
    it = C.HOOD_IN[1]
    cxh, cyh = C.HOOD_CENTER
    for nm, (x, y) in C.HOOD_PORTS.items():
        inside_top = rect_dist(x, y, cxh - it[0] / 2, cxh + it[0] / 2, cyh - it[1] / 2, cyh + it[1] / 2) == 0
        chk(f'Anschluss {nm} innerhalb Kammerdecke', float(inside_top), 1.0, unit='')
        on_in = y + C.HOOD_PORT_D / 2 <= C.HOOD_DIVIDER_Y[0]
        on_out = y - C.HOOD_PORT_D / 2 >= C.HOOD_DIVIDER_Y[1]
        chk(f'Anschluss {nm} auf richtiger Seite', float(on_in if nm == 'IN' else on_out), 1.0, unit='')
    chk('P05 füllt Durchlass in Z', min(C.GRAVITY_SLOT[4] - C.P05[4], C.P05[5] - min(C.GRAVITY_SLOT[5], C.POD[5])), 0.0)
    chk('P05 füllt Durchlass in Y', (C.P05[3] - C.P05[2]) - (C.GRAVITY_SLOT[3] - C.GRAVITY_SLOT[2]), 0.0)

    print('\n'.join(rows))
    print(f'\n{len(rows)} Zeilen, {bad} NOK')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(run())
