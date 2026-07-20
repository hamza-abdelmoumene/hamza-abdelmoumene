#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render data/contributions.json as a holographic-glass contribution ledger:
a 53-week x 7-day grid of cells whose intensity glows cyan, printing in
diagonally, with a legend and a stats footer. Emits heatmap-dark.svg +
heatmap-light.svg to match the hero banner. Pure SVG + SMIL.
"""
import json
import os
import random
from datetime import datetime

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data", "contributions.json")

W = 1180
CELL, GAP = 14, 4
PITCH = CELL + GAP
GUTTER = 30
TOPLBL = 22
PAD = 34
HEADER = 46
FOOTER = 46
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

MONO = ("'JetBrains Mono','SFMono-Regular',ui-monospace,'Cascadia Code',"
        "Consolas,'Liberation Mono',Menlo,monospace")
SANS = ("'Inter','SF Pro Display','Segoe UI',ui-sans-serif,system-ui,Roboto,"
        "'Helvetica Neue',Arial,sans-serif")

DARK = dict(
    name="dark",
    bg0="#05060E", bg1="#090C1E", bg2="#0B1030",
    glass="#0B1230", glass_op="0.60", sheen="#CFEBFF", sheen_op="0.10",
    text="#EAF2FF", inkStrong="#FFFFFF", muted="#93A6CC", faint="#5E6F97",
    cyan="#39E4FF", blue="#5C8DFF", ice="#9FE6FF",
    aur1="#22D3EE", aur2="#4C6FFF", aur3="#8B5CF6",
    hair_op="0.14", glow="#39E4FF", glow_op="0.7", grid_op="0.05", star="#BFE9FF",
    shadow="#000000", shadow_op="0.55",
    empty="#0E1A3C", ramp=["#123A57", "#1E6E9E", "#2CB2DC", "#4DE8FF"],
)
LIGHT = dict(
    name="light",
    bg0="#EEF4FF", bg1="#E6EEFC", bg2="#DBE7FB",
    glass="#FFFFFF", glass_op="0.62", sheen="#FFFFFF", sheen_op="0.5",
    text="#101E42", inkStrong="#0A1330", muted="#46587E", faint="#8092BA",
    cyan="#0E8FB8", blue="#2563EB", ice="#3AA0E0",
    aur1="#7DE3F4", aur2="#9DB8FF", aur3="#C7B8FD",
    hair_op="0.12", glow="#5AB6E8", glow_op="0.35", grid_op="0.05", star="#6AA6D8",
    shadow="#25407A", shadow_op="0.16",
    empty="#DCE6F5", ramp=["#B9D6F2", "#7FB3E8", "#3F7FD6", "#2563EB"],
)


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def gh_row(d):
    return (datetime.strptime(d, "%Y-%m-%d").weekday() + 1) % 7


def grid_positions(days):
    start_row = gh_row(days[0]["date"])
    cells, month_marks, last_month = [], [], None
    for i, d in enumerate(days):
        slot = start_row + i
        col, row = slot // 7, slot % 7
        cells.append((col, row, d))
        m = d["date"][5:7]
        if m != last_month and row <= 1:
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
    gx = PAD + GUTTER + (W - 2 * PAD - GUTTER - grid_w) / 2
    gy = PAD + HEADER + TOPLBL
    H = gy + grid_h + FOOTER + PAD
    total = data.get("total_last_year", 0)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'fill="none" role="img" aria-label="{total} contributions in the last year">']
    p.append(f'<title>{total} contributions in the last year</title>')

    p.append(f'''<defs>
      <clipPath id="cardClip"><rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16"/></clipPath>
      <radialGradient id="bgGrad" cx="0.5" cy="0" r="1.2" color-interpolation="sRGB">
        <stop offset="0" stop-color="{t['bg2']}"/><stop offset="0.6" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg0']}"/></radialGradient>
      <radialGradient id="aurA" color-interpolation="sRGB"><stop offset="0" stop-color="{t['aur1']}" stop-opacity="{0.42 if t['name']=='dark' else 0.34}"/><stop offset="1" stop-color="{t['aur1']}" stop-opacity="0"/></radialGradient>
      <radialGradient id="aurB" color-interpolation="sRGB"><stop offset="0" stop-color="{t['aur2']}" stop-opacity="{0.42 if t['name']=='dark' else 0.34}"/><stop offset="1" stop-color="{t['aur2']}" stop-opacity="0"/></radialGradient>
      <linearGradient id="glassSheen" x1="0" y1="0" x2="0" y2="1" color-interpolation="sRGB">
        <stop offset="0" stop-color="{t['sheen']}" stop-opacity="{t['sheen_op']}"/><stop offset="0.4" stop-color="{t['sheen']}" stop-opacity="0"/></linearGradient>
      <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1" color-interpolation="sRGB">
        <stop offset="0" stop-color="{t['cyan']}" stop-opacity="0.5"/><stop offset="0.5" stop-color="{t['blue']}" stop-opacity="0.28"/><stop offset="1" stop-color="{t['cyan']}" stop-opacity="0.14"/></linearGradient>
      <linearGradient id="prism" x1="0" y1="0" x2="1" y2="0" color-interpolation="sRGB">
        <stop offset="0" stop-color="{t['sheen']}" stop-opacity="0"/><stop offset="0.5" stop-color="{t['sheen']}" stop-opacity="{0.14 if t['name']=='dark' else 0.5}"/><stop offset="1" stop-color="{t['sheen']}" stop-opacity="0"/></linearGradient>
      <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0H0V34" fill="none" stroke="{t['cyan']}" stroke-opacity="{t['grid_op']}" stroke-width="1"/></pattern>
      <filter id="glow" x="-70%" y="-70%" width="240%" height="240%" color-interpolation-filters="sRGB">
        <feGaussianBlur in="SourceAlpha" stdDeviation="2" result="b"/><feFlood flood-color="{t['glow']}" flood-opacity="{t['glow_op']}" result="c"/>
        <feComposite in="c" in2="b" operator="in" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">
        <feDropShadow dx="0" dy="10" stdDeviation="22" flood-color="{t['shadow']}" flood-opacity="{t['shadow_op']}"/></filter>
    </defs>''')

    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}" filter="url(#cardShadow)"/>')
    p.append('<g clip-path="url(#cardClip)">')
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="url(#bgGrad)"/>')
    p.append(f'<circle cx="180" cy="0" r="240" fill="url(#aurA)"/><circle cx="1000" cy="{H}" r="280" fill="url(#aurB)"/>')
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="url(#grid)"/>')
    rnd = random.Random(9)
    for _ in range(16):
        sx = rnd.randint(20, W-20); sy = rnd.randint(20, H-20)
        p.append(f'<circle cx="{sx}" cy="{sy}" r="{rnd.choice([0.6,0.9,1.2])}" fill="{t["star"]}" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0.8;0" dur="{rnd.uniform(3,6):.1f}s" begin="{rnd.uniform(0,4):.1f}s" repeatCount="indefinite"/></circle>')
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="url(#glassSheen)"/>')
    p.append('</g>')
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16" fill="none" stroke="url(#edge)" stroke-width="1.2"/>')
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16" fill="none" stroke="{t["text"]}" stroke-opacity="{t["hair_op"]}" stroke-width="1"/>')
    for cxp, cyp, sxx, syy in [(20,20,1,1),(W-20,20,-1,1),(20,H-20,1,-1),(W-20,H-20,-1,-1)]:
        p.append(f'<path d="M {cxp+12*sxx} {cyp} H {cxp} V {cyp+12*syy}" fill="none" stroke="{t["cyan"]}" stroke-width="1.5" opacity="0.7"/>')

    # header
    hy = PAD + 20
    p.append(f'<circle cx="{PAD+10}" cy="{hy-4}" r="3.5" fill="{t["cyan"]}" filter="url(#glow)"><animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/></circle>')
    p.append(f'<text x="{PAD+24}" y="{hy}" font-family="{MONO}" font-size="12" letter-spacing="2.5" fill="{t["cyan"]}">CONTRIBUTION MATRIX</text>')
    p.append(f'<text x="{W-PAD-6}" y="{hy}" text-anchor="end" font-family="{SANS}" font-size="16" fill="{t["inkStrong"]}">'
             f'<tspan font-weight="800">{total:,}</tspan>'
             f'<tspan font-family="{MONO}" font-size="11.5" fill="{t["muted"]}">  in the last 365 days</tspan></text>')
    p.append(f'<line x1="{PAD+6}" y1="{hy+12}" x2="{W-PAD-6}" y2="{hy+12}" stroke="{t["text"]}" stroke-opacity="{t["hair_op"]}"/>')

    for col, m in month_marks:
        mx = gx + col * PITCH
        if mx < gx + grid_w - 16:
            p.append(f'<text x="{mx:.1f}" y="{gy-8}" font-family="{MONO}" font-size="10.5" fill="{t["faint"]}">{MONTHS[m-1]}</text>')
    for row, lab in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        wy = gy + row * PITCH + CELL - 3
        p.append(f'<text x="{gx-8:.1f}" y="{wy:.1f}" text-anchor="end" font-family="{MONO}" font-size="9.5" fill="{t["faint"]}">{lab}</text>')

    # cells
    p.append('<g>')
    for col, row, d in cells:
        x = gx + col * PITCH
        y = gy + row * PITCH
        fill = fill_for(t, d)
        begin = (col * 0.9 + row * 1.6) * 0.016
        extra = ' filter="url(#glow)"' if d["level"] >= 4 else ""
        stroke = f' stroke="{t["cyan"]}" stroke-opacity="0.18" stroke-width="0.6"' if d["level"] <= 0 else ""
        p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="3" fill="{fill}"{stroke}{extra} opacity="0">'
                 f'<animate attributeName="opacity" values="0;1" dur="0.5s" begin="{begin:.2f}s" fill="freeze"/></rect>')
    p.append('</g>')
    # prismatic scan across during reveal
    p.append(f'<rect x="{gx-40:.0f}" y="{gy-10:.0f}" width="80" height="{grid_h+20}" fill="url(#prism)" opacity="0.9">'
             f'<animateTransform attributeName="transform" type="translate" values="0 0; {grid_w+80:.0f} 0" dur="1.8s" begin="0.1s" fill="freeze"/></rect>')

    # footer stats
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
        p.append(f'<text x="{x:.0f}" y="{fy}" font-family="{SANS}" font-size="17" font-weight="800" fill="{t["inkStrong"]}">{num}'
                 f'<tspan font-family="{MONO}" font-size="10.5" font-weight="400" letter-spacing="1" fill="{t["muted"]}">  {lab}</tspan></text>')

    x = PAD + 6
    stat(x, f'{cur}', 'CURRENT STREAK')
    stat(x + 210, f'{lon}', 'LONGEST STREAK')
    stat(x + 430, f'{act}', 'ACTIVE DAYS')
    if best.get("count"):
        stat(x + 610, f'{best["count"]}', f'BEST · {bd.upper()}')

    # legend
    lx = W - PAD - 6
    ramp = [t["empty"]] + t["ramp"]
    lw = CELL + 3
    total_leg = len(ramp) * lw + 96
    sx = lx - total_leg
    p.append(f'<text x="{sx-6:.0f}" y="{fy}" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="{t["faint"]}">Less</text>')
    for i, c in enumerate(ramp):
        cxp = sx + i * lw
        st = f' stroke="{t["cyan"]}" stroke-opacity="0.18" stroke-width="0.6"' if i == 0 else ""
        gl = ' filter="url(#glow)"' if i == len(ramp) - 1 else ""
        p.append(f'<rect x="{cxp:.0f}" y="{fy-11}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"{st}{gl}/>')
    p.append(f'<text x="{sx + len(ramp)*lw + 6:.0f}" y="{fy}" font-family="{MONO}" font-size="10.5" fill="{t["faint"]}">More</text>')

    p.append('</svg>')
    return "\n".join(p)


def main():
    data = load()
    for t in (DARK, LIGHT):
        svg = build(t, data)
        fn = os.path.join(HERE, "..", f"heatmap-{t['name']}.svg")
        with open(fn, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote heatmap-{t['name']}.svg ({len(svg.encode('utf-8'))//1024} KB)")


if __name__ == "__main__":
    main()
