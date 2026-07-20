#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aged-paper "Selected Work" panel — a typeset index card of real public repos.
Emits worklog-dark.svg + worklog-light.svg to match the hero banner + ledger.
Static: rerun when the featured projects change. Pure SVG + SMIL.
"""
import os

STATIC = os.environ.get("STATIC") == "1"

W = 1180
PAD = 34
HEADER = 48
FOOTER = 40
ROW_H = 66

# Real public repositories (github.com/hamza-abdelmoumene), most representative first.
OWNER = "hamza-abdelmoumene"
PROJECTS = [
    ("vespera", "C++", 1,
     "Distro-agnostic Linux music-player companion — MPRIS control, synced lyrics, cava visualiser & EasyEffects EQ."),
    ("lyrics-tool", "Python", 1,
     "Terminal live-lyrics visualiser and LRC/WLRC processing suite (playerctl + LRCLIB)."),
    ("math-algorithms-toolkit", "C", 2,
     "Fundamental algorithms in C — primes, GCD, Fibonacci, factorials and sorting."),
    ("adds-set-theory", "C", 2,
     "Set-theory operations over text via BST & linked lists — ESI data-structures lab."),
]
ROMAN = ["I", "II", "III", "IV", "V", "VI"]

MONO = ("'JetBrains Mono','Courier New','SFMono-Regular',ui-monospace,"
        "'Cascadia Code',Consolas,'Liberation Mono',Menlo,monospace")
SERIF = ("'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',"
         "'URW Palladio L',Georgia,'Times New Roman',serif")

DARK = dict(
    name="dark",
    bg="#1E160C", bg2="#1E160C", panel="#251C0F", panelTop="#251C0F",
    ink="#E7D6AF", inkStrong="#F5EACC", muted="#B29A6E", faint="#87714E",
    border="#E7D6AF", ox="#D06E4F", teal="#6BA88F", gold="#CFA24C",
    border_op="0.22", rule_op="0.13", grain_op="0.05", grain_col="#E9DBBB",
    shadow="#000000", shadow_op="0.50",
    chip="#2C2113", chip_op="0.8",
)
LIGHT = dict(
    name="light",
    bg="#E4DBC7", bg2="#D8CEB6", panel="#EEE7D6", panelTop="#F4EFE1",
    ink="#352B1B", inkStrong="#251B0C", muted="#6C5E48", faint="#96896B",
    border="#352B1A", ox="#9C4436", teal="#41695A", gold="#95712F",
    border_op="0.28", rule_op="0.10", grain_op="0.05", grain_col="#2A1B08",
    shadow="#352B1A", shadow_op="0.12",
    chip="#F1EBDC", chip_op="0.9",
)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def anim(**kw):
    return "<animate " + " ".join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items()) + "/>"


def build(t):
    n = len(PROJECTS)
    gy = PAD + HEADER
    H = gy + n * ROW_H + FOOTER + PAD
    px = PAD + 4
    rx = W - PAD - 4
    total_stars = sum(p[2] for p in PROJECTS)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Selected work — public repositories">']
    p.append('<title>Selected work — public repositories</title>')

    p.append(f'''<defs>
      <clipPath id="cardClip"><rect x="6" y="6" width="{W-12}" height="{H-12}" rx="8"/></clipPath>
      <linearGradient color-interpolation="sRGB" id="bgGrad" x1="0" y1="0" x2="0.7" y2="1">
        <stop offset="0" stop-color="{t['bg']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
      <filter id="grain" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" stitchTiles="stitch" result="n"/>
        <feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.85 0" result="a"/>
        <feFlood flood-color="{t['grain_col']}" result="c"/><feComposite in="c" in2="a" operator="in"/></filter>
      <filter id="cardShadow" color-interpolation-filters="sRGB" x="-10%" y="-10%" width="120%" height="120%">
        <feDropShadow dx="0" dy="5" stdDeviation="14" flood-color="{t['shadow']}" flood-opacity="{t['shadow_op']}"/></filter>
    </defs>''')

    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="8" fill="url(#bgGrad)" filter="url(#cardShadow)"/>')
    p.append(f'<g clip-path="url(#cardClip)"><rect x="6" y="6" width="{W-12}" height="{H-12}" filter="url(#grain)" opacity="{t["grain_op"]}"/></g>')
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="8" fill="none" stroke="{t["border"]}" stroke-opacity="{t["border_op"]}" stroke-width="1.3"/>')
    p.append(f'<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="6" fill="none" stroke="{t["border"]}" stroke-opacity="{t["rule_op"]}" stroke-width="0.8"/>')

    # header
    hy = PAD + 22
    p.append(f'<text x="{px}" y="{hy}" font-family="{MONO}" font-size="12" letter-spacing="2.5" fill="{t["muted"]}">'
             f'<tspan fill="{t["ox"]}">❯</tspan> git log --selected</text>')
    p.append(f'<text x="{rx}" y="{hy}" text-anchor="end" font-family="{SERIF}" font-size="14" font-style="italic" fill="{t["faint"]}">Selected Work · No. 002</text>')
    p.append(f'<line x1="{px}" y1="{hy+12}" x2="{rx}" y2="{hy+12}" stroke="{t["border"]}" stroke-opacity="{t["border_op"]}"/>')

    # rows
    for i, (name, lang, stars, desc) in enumerate(PROJECTS):
        ry = gy + i * ROW_H
        cy = ry + ROW_H / 2
        begin = 0.25 + i * 0.18
        # right-side meta: language chip + star count
        chip_w = len(lang) * 7.4 + 20
        star_txt = f"★ {stars}"
        star_w = len(star_txt) * 7.0
        chip_x = rx - chip_w
        star_x = chip_x - star_w - 14
        rows = [
            f'<g opacity="0" transform="translate(-10 0)">',
            anim(attributeName="opacity", values="0;1", dur="0.5s", begin=f"{begin:.2f}s", fill="freeze"),
            f'<animateTransform attributeName="transform" type="translate" values="-10 0; 0 0" dur="0.5s" begin="{begin:.2f}s" fill="freeze"/>',
            # index numeral
            f'<text x="{px+2}" y="{cy-6}" font-family="{SERIF}" font-size="20" font-style="italic" fill="{t["gold"]}">{ROMAN[i]}</text>',
            # name
            f'<text x="{px+48}" y="{cy-6}" font-family="{SERIF}" font-size="19" font-weight="700" fill="{t["inkStrong"]}">{esc(name)}</text>',
            # description
            f'<text x="{px+48}" y="{cy+16}" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(desc)}</text>',
            # star count
            f'<text x="{star_x:.0f}" y="{cy-2}" font-family="{MONO}" font-size="12" fill="{t["gold"]}">{star_txt}</text>',
            # language chip
            f'<rect x="{chip_x:.0f}" y="{cy-15}" width="{chip_w:.0f}" height="24" rx="4" fill="{t["chip"]}" fill-opacity="{t["chip_op"]}" stroke="{t["border"]}" stroke-opacity="{t["border_op"]}" stroke-width="0.9"/>',
            f'<text x="{chip_x+chip_w/2:.0f}" y="{cy+1}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["teal"]}">{esc(lang)}</text>',
            '</g>',
        ]
        p.append("".join(rows))
        if i < len(PROJECTS) - 1:
            p.append(f'<line x1="{px}" y1="{ry+ROW_H}" x2="{rx}" y2="{ry+ROW_H}" stroke="{t["border"]}" stroke-opacity="{t["rule_op"]}" stroke-dasharray="2 3"/>')

    # footer
    fy = gy + n * ROW_H + 24
    p.append(f'<text x="{px}" y="{fy}" font-family="{MONO}" font-size="11.5" letter-spacing="0.5" fill="{t["faint"]}">'
             f'{n} selected · {total_stars}★ across public repositories</text>')
    p.append(f'<text x="{rx}" y="{fy}" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{t["teal"]}">'
             f'github.com/{OWNER}?tab=repositories →</text>')

    p.append('</svg>')
    return "\n".join(p)


if __name__ == "__main__":
    for theme in (DARK, LIGHT):
        svg = build(theme)
        if STATIC:
            svg = svg.replace(' opacity="0"', ' opacity="1"')
        fn = f"worklog-{theme['name']}{'-static' if STATIC else ''}.svg"
        with open(fn, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {fn} ({len(svg.encode('utf-8'))//1024} KB)")
