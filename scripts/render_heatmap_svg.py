#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render data/contributions.json as an aged-paper contribution LEDGER:
a 53-week x 7-day grid of ink boxes that print in diagonally, with a
legend and a stats footer. Emits heatmap-vellum.svg + heatmap-bond.svg
to match the hero banner's two paper stocks. Pure SVG + SMIL.
"""
import json
import os
from datetime import date, datetime

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data", "contributions.json")

# ---- geometry ----
W = 1180
CELL, GAP = 14, 4
PITCH = CELL + GAP
GUTTER = 30                 # weekday labels
TOPLBL = 22                 # month labels
PAD = 34
HEADER = 46
FOOTER = 46
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

MONO = ("'JetBrains Mono','Courier New','SFMono-Regular',ui-monospace,"
        "'Cascadia Code',Consolas,'Liberation Mono',Menlo,monospace")
SERIF = ("'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',"
         "'URW Palladio L',Georgia,'Times New Roman',serif")

# aged-ink density ramps (empty -> pale sepia -> oxblood-espresso), per paper
VELLUM = dict(
    name="vellum",
    bg="#D4C9B2", bg2="#C7BB9F", card="#DED5C0", cardTop="#E5DDCA",
    ink="#33291B", inkStrong="#231A0E", muted="#6A5C48", faint="#928873",
    border="#352A18", ox="#9A4436", gold="#8F6D30",
    border_op="0.32", rule_op="0.13", grain_op="0.06",
    shadow="#231A0E", shadow_op="0.20",
    empty="#CBBFA6",
    ramp=["#CBB185", "#BE9450", "#95622C", "#6E3A20"],
)
BOND = dict(
    name="bond",
    bg="#E4DBC7", bg2="#D8CEB6", card="#EEE7D6", cardTop="#F4EFE1",
    ink="#352B1B", inkStrong="#251B0C", muted="#6C5E48", faint="#96896B",
    border="#352B1A", ox="#9C4436", gold="#95712F",
    border_op="0.28", rule_op="0.10", grain_op="0.05",
    shadow="#352B1A", shadow_op="0.12",
    empty="#DBD1B8",
    ramp=["#D6C08F", "#C4994F", "#99652D", "#732F22"],
)


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def gh_row(d):  # GitHub weeks start Sunday (0=Sun .. 6=Sat)
    return (datetime.strptime(d, "%Y-%m-%d").weekday() + 1) % 7


def grid_positions(days):
    """Map each day to (col, row). Returns cells, n_cols, and month markers."""
    start_row = gh_row(days[0]["date"])
    cells = []
    month_marks = []
    last_month = None
    for i, d in enumerate(days):
        slot = start_row + i
        col, row = slot // 7, slot % 7
        cells.append((col, row, d))
        m = d["date"][5:7]
        if m != last_month and row <= 1:      # label a month at its first top-ish cell
            month_marks.append((col, int(m)))
            last_month = m
    n_cols = (start_row + len(days) + 6) // 7
    return cells, n_cols, month_marks


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fill_for(t, d):
    if d["level"] <= 0:
        return t["empty"]
    return t["ramp"][min(d["level"], 4) - 1]


def build(t, data):
    days = data["days"]
    cells, n_cols, month_marks = grid_positions(days)
    grid_w = n_cols * PITCH - GAP
    grid_h = 7 * PITCH - GAP
    gx = PAD + GUTTER + (W - 2 * PAD - GUTTER - grid_w) / 2   # centre the grid block
    gy = PAD + HEADER + TOPLBL
    H = gy + grid_h + FOOTER + PAD
    total = data.get("total_last_year", 0)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" fill="none" role="img" '
         f'aria-label="{total} contributions in the last year">']
    p.append(f'<title>{total} contributions in the last year — {esc(t["name"])} ledger</title>')

    # defs
    p.append(f'''<defs>
      <clipPath id="cardClip"><rect x="6" y="6" width="{W-12}" height="{H-12}" rx="8"/></clipPath>
      <linearGradient id="bgGrad" x1="0" y1="0" x2="0.7" y2="1">
        <stop offset="0" stop-color="{t['bg']}"/><stop offset="1" stop-color="{t['bg2']}"/>
      </linearGradient>
      <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" stitchTiles="stitch" result="n"/>
        <feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.85 0" result="a"/>
        <feFlood flood-color="#2A1B08" result="c"/><feComposite in="c" in2="a" operator="in"/></filter>
      <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
        <feDropShadow dx="0" dy="5" stdDeviation="14" flood-color="{t['shadow']}" flood-opacity="{t['shadow_op']}"/></filter>
      <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="{t['ox']}" stop-opacity="0"/>
        <stop offset="0.5" stop-color="{t['ox']}" stop-opacity="0.10"/>
        <stop offset="1" stop-color="{t['ox']}" stop-opacity="0"/></linearGradient>
    </defs>''')

    # sheet
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="8" fill="url(#bgGrad)" filter="url(#cardShadow)"/>')
    p.append(f'<g clip-path="url(#cardClip)"><rect x="6" y="6" width="{W-12}" height="{H-12}" filter="url(#grain)" opacity="{t["grain_op"]}"/></g>')
    # double rule border
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="8" fill="none" stroke="{t["border"]}" stroke-opacity="{t["border_op"]}" stroke-width="1.3"/>')
    p.append(f'<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="6" fill="none" stroke="{t["border"]}" stroke-opacity="{t["rule_op"]}" stroke-width="0.8"/>')

    # header
    hy = PAD + 20
    p.append(f'<text x="{PAD+4}" y="{hy}" font-family="{MONO}" font-size="12" letter-spacing="2.5" fill="{t["muted"]}">'
             f'<tspan fill="{t["ox"]}">❯</tspan> ./contributions.sh</text>')
    p.append(f'<text x="{W-PAD-4}" y="{hy}" text-anchor="end" font-family="{SERIF}" font-size="16" fill="{t["inkStrong"]}">'
             f'<tspan font-weight="700">{total:,}</tspan>'
             f'<tspan font-family="{MONO}" font-size="11.5" fill="{t["muted"]}">  contributions · last 365 days</tspan></text>')
    p.append(f'<line x1="{PAD+4}" y1="{hy+12}" x2="{W-PAD-4}" y2="{hy+12}" stroke="{t["border"]}" stroke-opacity="{t["border_op"]}"/>')

    # month labels
    for col, m in month_marks:
        mx = gx + col * PITCH
        if mx < gx + grid_w - 16:
            p.append(f'<text x="{mx:.1f}" y="{gy-8}" font-family="{MONO}" font-size="10.5" fill="{t["faint"]}">{MONTHS[m-1]}</text>')

    # weekday labels (Mon/Wed/Fri)
    for row, lab in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        wy = gy + row * PITCH + CELL - 3
        p.append(f'<text x="{gx-8:.1f}" y="{wy:.1f}" text-anchor="end" font-family="{MONO}" font-size="9.5" fill="{t["faint"]}">{lab}</text>')

    # cells -- diagonal print-in reveal, then freeze
    p.append('<g>')
    for col, row, d in cells:
        x = gx + col * PITCH
        y = gy + row * PITCH
        fill = fill_for(t, d)
        begin = (col * 0.9 + row * 1.6) * 0.016
        stroke = f' stroke="{t["border"]}" stroke-opacity="0.22" stroke-width="0.6"' if d["level"] <= 0 else ""
        p.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="3" fill="{fill}"{stroke} opacity="0">'
            f'<animate attributeName="opacity" values="0;1" dur="0.5s" begin="{begin:.2f}s" fill="freeze"/>'
            f'</rect>')
    p.append('</g>')

    # diagonal ink sheen sweeping across during the reveal (one cheap element)
    p.append(f'<rect x="{gx-40:.0f}" y="{gy-10:.0f}" width="80" height="{grid_h+20}" fill="url(#sheen)" opacity="0.9">'
             f'<animateTransform attributeName="transform" type="translate" values="0 0; {grid_w+80:.0f} 0" '
             f'dur="1.8s" begin="0.1s" fill="freeze"/></rect>')

    # ---- footer: stats (left) + legend (right) ----
    fy = gy + grid_h + 30
    cur = data.get("current_streak", 0)
    lon = data.get("longest_streak", 0)
    act = data.get("active_days", 0)
    best = data.get("best_day") or {}
    bd = ""
    if best.get("date"):
        try:
            bd = datetime.strptime(best["date"], "%Y-%m-%d").strftime("%b %-d")
        except ValueError:
            bd = best["date"]

    def stat(x, num, lab):
        p.append(f'<text x="{x:.0f}" y="{fy}" font-family="{SERIF}" font-size="17" font-weight="700" fill="{t["inkStrong"]}">{num}'
                 f'<tspan font-family="{MONO}" font-size="10.5" font-weight="400" letter-spacing="1" fill="{t["muted"]}">  {lab}</tspan></text>')

    x = PAD + 4
    stat(x, f'{cur}', 'CURRENT STREAK')
    stat(x + 210, f'{lon}', 'LONGEST STREAK')
    stat(x + 430, f'{act}', 'ACTIVE DAYS')
    if best.get("count"):
        stat(x + 610, f'{best["count"]}', f'BEST DAY · {bd.upper()}')

    # legend (right-aligned)
    lx = W - PAD - 4
    ramp = [t["empty"]] + t["ramp"]
    lw = CELL + 3
    total_leg = len(ramp) * lw + 96
    sx = lx - total_leg
    p.append(f'<text x="{sx-6:.0f}" y="{fy}" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="{t["faint"]}">Less</text>')
    for i, c in enumerate(ramp):
        cxp = sx + i * lw
        st = f' stroke="{t["border"]}" stroke-opacity="0.22" stroke-width="0.6"' if i == 0 else ""
        p.append(f'<rect x="{cxp:.0f}" y="{fy-11}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"{st}/>')
    p.append(f'<text x="{sx + len(ramp)*lw + 6:.0f}" y="{fy}" font-family="{MONO}" font-size="10.5" fill="{t["faint"]}">More</text>')

    p.append('</svg>')
    return "\n".join(p)


def main():
    data = load()
    for t in (VELLUM, BOND):
        svg = build(t, data)
        fn = os.path.join(HERE, "..", f"heatmap-{t['name']}.svg")
        with open(fn, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote heatmap-{t['name']}.svg ({len(svg.encode('utf-8'))//1024} KB)")


if __name__ == "__main__":
    main()
