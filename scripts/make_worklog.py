#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Holographic-glass "Selected Work" panel — a HUD index of real public repos.
Emits worklog-dark.svg + worklog-light.svg to match the hero banner. SVG + SMIL.
"""
import os

STATIC = os.environ.get("STATIC") == "1"

W = 1180
PAD = 34
HEADER = 48
FOOTER = 40
ROW_H = 66

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
IDX = ["01", "02", "03", "04", "05", "06"]

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
    hair_op="0.14", chip="#0C1740", chip_op="0.55",
    glow="#39E4FF", glow_op="0.7", grid_op="0.05", star="#BFE9FF",
    shadow="#000000", shadow_op="0.55",
)
LIGHT = dict(
    name="light",
    bg0="#EEF4FF", bg1="#E6EEFC", bg2="#DBE7FB",
    glass="#FFFFFF", glass_op="0.62", sheen="#FFFFFF", sheen_op="0.5",
    text="#101E42", inkStrong="#0A1330", muted="#46587E", faint="#8092BA",
    cyan="#0E8FB8", blue="#2563EB", ice="#3AA0E0",
    aur1="#7DE3F4", aur2="#9DB8FF", aur3="#C7B8FD",
    hair_op="0.12", chip="#FFFFFF", chip_op="0.72",
    glow="#5AB6E8", glow_op="0.35", grid_op="0.05", star="#6AA6D8",
    shadow="#25407A", shadow_op="0.16",
)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def anim(**kw):
    return "<animate " + " ".join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items()) + "/>"


def build(t):
    import random
    n = len(PROJECTS)
    gy = PAD + HEADER
    H = gy + n * ROW_H + FOOTER + PAD
    px = PAD + 6
    rx = W - PAD - 6
    total_stars = sum(p[2] for p in PROJECTS)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'fill="none" role="img" aria-label="Selected work — public repositories">']
    p.append('<title>Selected work — public repositories</title>')

    p.append(f'''<defs>
      <clipPath id="cardClip"><rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16"/></clipPath>
      <radialGradient id="bgGrad" cx="0.5" cy="0" r="1.2" color-interpolation="sRGB">
        <stop offset="0" stop-color="{t['bg2']}"/><stop offset="0.6" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg0']}"/></radialGradient>
      <radialGradient id="aurA" color-interpolation="sRGB"><stop offset="0" stop-color="{t['aur1']}" stop-opacity="{0.42 if t['name']=='dark' else 0.35}"/><stop offset="1" stop-color="{t['aur1']}" stop-opacity="0"/></radialGradient>
      <radialGradient id="aurB" color-interpolation="sRGB"><stop offset="0" stop-color="{t['aur3']}" stop-opacity="{0.42 if t['name']=='dark' else 0.35}"/><stop offset="1" stop-color="{t['aur3']}" stop-opacity="0"/></radialGradient>
      <linearGradient id="glassSheen" x1="0" y1="0" x2="0" y2="1" color-interpolation="sRGB">
        <stop offset="0" stop-color="{t['sheen']}" stop-opacity="{t['sheen_op']}"/><stop offset="0.4" stop-color="{t['sheen']}" stop-opacity="0"/></linearGradient>
      <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1" color-interpolation="sRGB">
        <stop offset="0" stop-color="{t['cyan']}" stop-opacity="0.5"/><stop offset="0.5" stop-color="{t['blue']}" stop-opacity="0.28"/><stop offset="1" stop-color="{t['cyan']}" stop-opacity="0.14"/></linearGradient>
      <linearGradient id="prism" x1="0" y1="0" x2="1" y2="0" color-interpolation="sRGB">
        <stop offset="0" stop-color="{t['sheen']}" stop-opacity="0"/><stop offset="0.5" stop-color="{t['sheen']}" stop-opacity="{0.14 if t['name']=='dark' else 0.5}"/><stop offset="1" stop-color="{t['sheen']}" stop-opacity="0"/></linearGradient>
      <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0H0V34" fill="none" stroke="{t['cyan']}" stroke-opacity="{t['grid_op']}" stroke-width="1"/></pattern>
      <filter id="glow" x="-70%" y="-70%" width="240%" height="240%" color-interpolation-filters="sRGB">
        <feGaussianBlur in="SourceAlpha" stdDeviation="2.5" result="b"/><feFlood flood-color="{t['glow']}" flood-opacity="{t['glow_op']}" result="c"/>
        <feComposite in="c" in2="b" operator="in" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">
        <feDropShadow dx="0" dy="10" stdDeviation="22" flood-color="{t['shadow']}" flood-opacity="{t['shadow_op']}"/></filter>
    </defs>''')

    # sheet
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}" filter="url(#cardShadow)"/>')
    p.append(f'<g clip-path="url(#cardClip)">')
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="url(#bgGrad)"/>')
    p.append(f'<circle cx="180" cy="0" r="260" fill="url(#aurA)"/><circle cx="1000" cy="{H}" r="300" fill="url(#aurB)"/>')
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="url(#grid)"/>')
    rnd = random.Random(5)
    for _ in range(18):
        sx = rnd.randint(20, W-20); sy = rnd.randint(20, H-20)
        p.append(f'<circle cx="{sx}" cy="{sy}" r="{rnd.choice([0.6,0.9,1.2])}" fill="{t["star"]}" opacity="0">'
                 f'{anim(attributeName="opacity", values="0;0.8;0", dur=f"{rnd.uniform(3,6):.1f}s", begin=f"{rnd.uniform(0,4):.1f}s", repeatCount="indefinite")}</circle>')
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="url(#glassSheen)"/>')
    p.append(f'<g transform="skewX(-16)"><rect x="-180" y="-20" width="140" height="{H+40}" fill="url(#prism)">'
             f'<animateTransform attributeName="transform" type="translate" values="0 0; {W+320} 0" dur="1.8s" begin="0.2s" fill="freeze"/></rect></g>')
    p.append('</g>')
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16" fill="none" stroke="url(#edge)" stroke-width="1.2"/>')
    p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16" fill="none" stroke="{t["text"]}" stroke-opacity="{t["hair_op"]}" stroke-width="1"/>')
    for cxp, cyp, sxx, syy in [(20,20,1,1),(W-20,20,-1,1),(20,H-20,1,-1),(W-20,H-20,-1,-1)]:
        p.append(f'<path d="M {cxp+12*sxx} {cyp} H {cxp} V {cyp+12*syy}" fill="none" stroke="{t["cyan"]}" stroke-width="1.5" opacity="0.7"/>')

    # header
    hy = PAD + 22
    p.append(f'<circle cx="{px+4}" cy="{hy-4}" r="3.5" fill="{t["cyan"]}" filter="url(#glow)"><animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/></circle>')
    p.append(f'<text x="{px+18}" y="{hy}" font-family="{MONO}" font-size="12" letter-spacing="2.5" fill="{t["cyan"]}">SELECTED WORK</text>')
    p.append(f'<text x="{rx}" y="{hy}" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{t["faint"]}">./repositories --pinned</text>')
    p.append(f'<line x1="{px}" y1="{hy+12}" x2="{rx}" y2="{hy+12}" stroke="{t["text"]}" stroke-opacity="{t["hair_op"]}"/>')

    for i, (name, lang, stars, desc) in enumerate(PROJECTS):
        ry = gy + i * ROW_H
        cy = ry + ROW_H / 2
        begin = 0.25 + i * 0.16
        chip_w = len(lang) * 7.4 + 20
        star_txt = f"★ {stars}"
        star_w = len(star_txt) * 7.0
        chip_x = rx - chip_w
        star_x = chip_x - star_w - 14
        p.append("".join([
            f'<g opacity="0" transform="translate(-10 0)">',
            anim(attributeName="opacity", values="0;1", dur="0.5s", begin=f"{begin:.2f}s", fill="freeze"),
            f'<animateTransform attributeName="transform" type="translate" values="-10 0; 0 0" dur="0.5s" begin="{begin:.2f}s" fill="freeze"/>',
            f'<text x="{px+2}" y="{cy-5}" font-family="{MONO}" font-size="13" font-weight="600" fill="{t["cyan"]}">{IDX[i]}</text>',
            f'<text x="{px+46}" y="{cy-4}" font-family="{SANS}" font-size="19" font-weight="700" fill="{t["inkStrong"]}">{esc(name)}</text>',
            f'<text x="{px+46}" y="{cy+16}" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(desc)}</text>',
            f'<text x="{star_x:.0f}" y="{cy-1}" font-family="{MONO}" font-size="12" fill="{t["ice"]}">{star_txt}</text>',
            f'<rect x="{chip_x:.0f}" y="{cy-14}" width="{chip_w:.0f}" height="24" rx="6" fill="{t["chip"]}" fill-opacity="{t["chip_op"]}" stroke="{t["cyan"]}" stroke-opacity="0.4" stroke-width="0.9"/>',
            f'<text x="{chip_x+chip_w/2:.0f}" y="{cy+2}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["cyan"]}">{esc(lang)}</text>',
            '</g>',
        ]))
        if i < n - 1:
            p.append(f'<line x1="{px}" y1="{ry+ROW_H}" x2="{rx}" y2="{ry+ROW_H}" stroke="{t["text"]}" stroke-opacity="0.08" stroke-dasharray="2 4"/>')

    fy = gy + n * ROW_H + 24
    p.append(f'<text x="{px}" y="{fy}" font-family="{MONO}" font-size="11.5" letter-spacing="0.5" fill="{t["faint"]}">'
             f'{n} selected · {total_stars}★ across public repositories</text>')
    p.append(f'<text x="{rx}" y="{fy}" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{t["cyan"]}">'
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
