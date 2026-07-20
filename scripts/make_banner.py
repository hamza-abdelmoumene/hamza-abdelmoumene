#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Holographic-glass GitHub profile hero banner.
Emits banner-dark.svg + banner-light.svg -- frosted dark-glass panels floating
on a deep indigo aurora, a holographic portrait scan, prismatic sheen sweeps and
a live HUD. Electric-cyan / ice-blue palette. Pure SVG + SMIL (no JS).
"""
import os
import random

STATIC = os.environ.get("STATIC") == "1"

# ---- layout ----
W, H = 1180, 610
CARD_R = 18
M = 22
LP_X, LP_Y = M, M
LP_W, LP_H = 440, H - 2 * M
RP_X = LP_X + LP_W + 18
RP_Y = M
RP_W = W - RP_X - M
RP_H = H - 2 * M
CX = LP_X + LP_W / 2

# ---- content ----
NAME_FULL = "Abdelmoumene Hamza"
ROLES = [
    "Machine Learning Engineer",
    "Data Scientist in Training",
    "CS Student @ ESI Algiers",
    "Open Source Contributor",
    "Data Pipeline Builder",
]
INFO = [
    ("LOCATION",  "Algiers, Algeria"),
    ("EDUCATION", "Computer Science @ ESI Algiers"),
    ("FOCUS",     "Machine Learning · Data Science"),
    ("PORTFOLIO", "github.com/hamza-abdelmoumene"),
    ("EMAIL",     "ph_abdelmoumene@esi.dz"),
]
SKILLS = ["Python", "C", "NumPy", "pandas", "scikit-learn",
          "Matplotlib", "Jupyter", "Linux", "Git", "Bash", "SQL"]

ASCII = [
    "                    +....................:",
    "                *=:-.......................:",
    "              +-.............................:",
    "            *-.................................:",
    "           *.....................................=",
    "          =........................................*",
    "         =....-....................................-",
    "        =:..--......................................=",
    "       +:=--:........................................*",
    "      *====:-........................................:",
    "      ======-....-...................................-",
    "     #==+=+==-...-.............-.....................-",
    "     *+++++====:.--............--.....................*",
    "    *++++++++=====*-...........-...-......-...........:",
    "   *+*+****++++++#@+-.-........-....-..................-+",
    "  ##%************%@%=--:--....--.---:==--......--....=:++*",
    " ##  ****##****#%@%@@*-::-----::=+##%%#*=:.......-...",
    " #   #**#####*#%@@@@@@#+*+:::=+==*++=::+::--...--..-.:",
    "     ***#####**%@@@%%%%%###++++=-..----..-::-..-:..-:::*",
    "    %#*#%#######@@@%#+=*#%*+++*+-........-=:=-..:=-.=",
    "    %##%%%%####%#@@%%%%%*:-:-.-:=-.......--:*=-.::=+=+",
    "    %#%    %##%%%#@@%%%+-----...-----------*%:=::..=",
    "    %#      @%#%@%%%%=:::::::-------------*#%::+=...*",
    "     #       %%%%%##%*=:::::::-:::::----=*#%@:: #:..-",
    "     @        %%%%%%%%#+:::::=:==:::--:*#%@ %:   %*:.:",
    "               %%%%%%%@%#*=::::::---:+%%@   %       #:=",
    "                @%%%%%%@@@%%*=:--:=*%@",
    "                 @@@@@%@@@     ##%",
]

# ---- palettes ----
DARK = dict(
    name="dark",
    bg0="#05060E", bg1="#090C1E", bg2="#0B1030",
    glass="#0B1230", glass_op="0.60", sheen="#CFEBFF", sheen_op="0.10",
    text="#EAF2FF", muted="#93A6CC", faint="#5E6F97",
    cyan="#39E4FF", blue="#5C8DFF", ice="#9FE6FF",
    aur1="#22D3EE", aur2="#4C6FFF", aur3="#8B5CF6",
    border="#7FD8FF", border_op="0.55", hair_op="0.14",
    chip="#0C1740", chip_op="0.55",
    glow="#39E4FF", glow_op="0.75",
    grid_op="0.05", star="#BFE9FF", online="#37F5C6",
    shadow_op="0.55",
)
LIGHT = dict(
    name="light",
    bg0="#EEF4FF", bg1="#E6EEFC", bg2="#DBE7FB",
    glass="#FFFFFF", glass_op="0.62", sheen="#FFFFFF", sheen_op="0.5",
    text="#101E42", muted="#46587E", faint="#8092BA",
    cyan="#0E8FB8", blue="#2563EB", ice="#3AA0E0",
    aur1="#7DE3F4", aur2="#9DB8FF", aur3="#C7B8FD",
    border="#2563EB", border_op="0.40", hair_op="0.12",
    chip="#FFFFFF", chip_op="0.72",
    glow="#5AB6E8", glow_op="0.35",
    grid_op="0.05", star="#6AA6D8", online="#10B981",
    shadow_op="0.16",
)

# ---- fonts ----
MONO = ("'JetBrains Mono','SFMono-Regular',ui-monospace,'Cascadia Code',"
        "Consolas,'Liberation Mono',Menlo,monospace")
SANS = ("'Inter','SF Pro Display','Segoe UI',ui-sans-serif,system-ui,Roboto,"
        "'Helvetica Neue',Arial,sans-serif")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def anim(**kw):
    return "<animate " + " ".join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items()) + "/>"


# ---- defs ----
def defs(t):
    p = ["<defs>"]
    p.append(f'<clipPath id="cardClip"><rect x="0" y="0" width="{W}" height="{H}" rx="{CARD_R}"/></clipPath>')
    p.append(f'<clipPath id="lpClip"><rect x="{LP_X}" y="{LP_Y}" width="{LP_W}" height="{LP_H}" rx="14"/></clipPath>')
    p.append(f'<clipPath id="rpClip"><rect x="{RP_X}" y="{RP_Y}" width="{RP_W}" height="{RP_H}" rx="14"/></clipPath>')

    p.append(f'''<radialGradient id="bgGrad" cx="0.5" cy="0.1" r="1.1" color-interpolation="sRGB">
      <stop offset="0" stop-color="{t['bg2']}"/><stop offset="0.6" stop-color="{t['bg1']}"/>
      <stop offset="1" stop-color="{t['bg0']}"/></radialGradient>''')

    # aurora blobs
    for bid, col in (("aurA", t['aur1']), ("aurB", t['aur2']), ("aurC", t['aur3'])):
        p.append(f'''<radialGradient id="{bid}" color-interpolation="sRGB">
          <stop offset="0" stop-color="{col}" stop-opacity="{0.5 if t['name']=='dark' else 0.4}"/>
          <stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>''')

    # holographic text gradient (cyan -> ice -> blue), gently shimmering
    p.append(f'''<linearGradient id="holo" gradientUnits="userSpaceOnUse" x1="{RP_X}" y1="0" x2="{RP_X+RP_W}" y2="0" color-interpolation="sRGB">
      <stop offset="0" stop-color="{t['cyan']}">{anim(attributeName="stop-color", values=f"{t['cyan']};{t['ice']};{t['blue']};{t['cyan']}", dur="8s", repeatCount="indefinite")}</stop>
      <stop offset="0.5" stop-color="{t['ice']}">{anim(attributeName="stop-color", values=f"{t['ice']};{t['blue']};{t['cyan']};{t['ice']}", dur="8s", repeatCount="indefinite")}</stop>
      <stop offset="1" stop-color="{t['blue']}">{anim(attributeName="stop-color", values=f"{t['blue']};{t['cyan']};{t['ice']};{t['blue']}", dur="8s", repeatCount="indefinite")}</stop>
    </linearGradient>''')

    # portrait holo gradient (diagonal, drifting)
    p.append(f'''<linearGradient id="holoP" gradientUnits="userSpaceOnUse" x1="{LP_X}" y1="{LP_Y}" x2="{LP_X+LP_W}" y2="{LP_Y+LP_H}" color-interpolation="sRGB">
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0; 30 20; 0 0" dur="10s" repeatCount="indefinite"/>
      <stop offset="0" stop-color="{t['cyan']}"/><stop offset="0.5" stop-color="{t['ice']}"/>
      <stop offset="1" stop-color="{t['blue']}"/></linearGradient>''')

    # glass sheen (top light)
    p.append(f'''<linearGradient id="glassSheen" x1="0" y1="0" x2="0" y2="1" color-interpolation="sRGB">
      <stop offset="0" stop-color="{t['sheen']}" stop-opacity="{t['sheen_op']}"/>
      <stop offset="0.4" stop-color="{t['sheen']}" stop-opacity="0"/></linearGradient>''')

    # border gradient (cyan -> blue -> transparent)
    p.append(f'''<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1" color-interpolation="sRGB">
      <stop offset="0" stop-color="{t['cyan']}" stop-opacity="{t['border_op']}"/>
      <stop offset="0.5" stop-color="{t['blue']}" stop-opacity="{float(t['border_op'])*0.6:.2f}"/>
      <stop offset="1" stop-color="{t['cyan']}" stop-opacity="{float(t['border_op'])*0.3:.2f}"/></linearGradient>''')

    # prismatic sheen sweep band
    p.append(f'''<linearGradient id="prism" x1="0" y1="0" x2="1" y2="0" color-interpolation="sRGB">
      <stop offset="0" stop-color="{t['sheen']}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{t['sheen']}" stop-opacity="{0.16 if t['name']=='dark' else 0.5}"/>
      <stop offset="1" stop-color="{t['sheen']}" stop-opacity="0"/></linearGradient>''')

    # travelling frame shimmer
    p.append(f'''<linearGradient id="frameShimmer" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0" color-interpolation="sRGB">
      <stop offset="0" stop-color="{t['cyan']}" stop-opacity="0"/>
      <stop offset="0.45" stop-color="{t['cyan']}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{t['cyan']}" stop-opacity="0.9"/>
      <stop offset="0.55" stop-color="{t['blue']}" stop-opacity="0"/>
      <stop offset="1" stop-color="{t['blue']}" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="{-W} 0; {W} 0" dur="7s" repeatCount="indefinite"/>
    </linearGradient>''')

    # grid
    p.append(f'''<pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">
      <path d="M34 0H0V34" fill="none" stroke="{t['cyan']}" stroke-opacity="{t['grid_op']}" stroke-width="1"/></pattern>''')

    # portrait scan line
    p.append(f'''<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1" color-interpolation="sRGB">
      <stop offset="0" stop-color="{t['cyan']}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{t['cyan']}" stop-opacity="{0.55 if t['name']=='dark' else 0.35}"/>
      <stop offset="1" stop-color="{t['cyan']}" stop-opacity="0"/></linearGradient>''')

    # cyan glow
    p.append(f'''<filter id="glow" x="-70%" y="-70%" width="240%" height="240%" color-interpolation-filters="sRGB">
      <feGaussianBlur in="SourceAlpha" stdDeviation="3" result="b"/>
      <feFlood flood-color="{t['glow']}" flood-opacity="{t['glow_op']}" result="c"/>
      <feComposite in="c" in2="b" operator="in" result="g"/>
      <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>''')
    p.append(f'''<filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%" color-interpolation-filters="sRGB">
      <feGaussianBlur in="SourceAlpha" stdDeviation="5" result="b"/>
      <feFlood flood-color="{t['glow']}" flood-opacity="{float(t['glow_op'])*0.6:.2f}" result="c"/>
      <feComposite in="c" in2="b" operator="in" result="g"/>
      <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>''')
    p.append(f'''<filter id="cardShadow" x="-30%" y="-30%" width="160%" height="160%" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="12" stdDeviation="26" flood-color="{t['bg0'] if t['name']=='light' else '#000000'}" flood-opacity="{t['shadow_op']}"/></filter>''')
    p.append(f'''<filter id="blurBlob" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="10"/></filter>''')
    p.append("</defs>")
    return "\n".join(p)


def background(t):
    g = ['<g clip-path="url(#cardClip)">']
    g.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bgGrad)"/>')
    # aurora blobs, slow drift
    blobs = [("aurA", 200, 90, 360, "0 0; 30 40; -18 20; 0 0", "26s"),
             ("aurB", 1010, 470, 420, "0 0; -40 -26; 24 -16; 0 0", "30s"),
             ("aurC", 720, 30, 340, "0 0; 22 30; -26 12; 0 0", "34s"),
             ("aurA", 1080, 120, 280, "0 0; -22 26; 12 -20; 0 0", "28s")]
    for bid, x, y, r, vals, dur in blobs:
        g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{bid})">'
                 f'<animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur}" repeatCount="indefinite"/></circle>')
    # grid
    g.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#grid)"/>')
    # starfield
    rnd = random.Random(7)
    for _ in range(34):
        x = rnd.randint(20, W - 20)
        y = rnd.randint(20, H - 20)
        r = rnd.choice([0.6, 0.8, 1.0, 1.3])
        dur = rnd.uniform(3, 7)
        dly = rnd.uniform(0, 5)
        g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["star"]}" opacity="0.0">'
                 f'{anim(attributeName="opacity", values="0;0.9;0.1;0.7;0", dur=f"{dur:.1f}s", begin=f"{dly:.1f}s", repeatCount="indefinite")}</circle>')
    g.append('</g>')
    return "\n".join(g)


def glass_card(t, x, y, w, h, clip):
    g = [f'<g filter="url(#cardShadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}"/></g>']
    g.append(f'<g clip-path="url(#{clip})">')
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#glassSheen)"/>')
    # prismatic sheen sweep, once
    g.append(f'<g transform="skewX(-16)"><rect x="{x-160}" y="{y-40}" width="120" height="{h+80}" fill="url(#prism)">'
             f'<animateTransform attributeName="transform" type="translate" values="0 0; {w+260} 0" dur="1.6s" begin="0.3s" fill="freeze"/></rect></g>')
    g.append('</g>')
    # border + bright top edge
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="none" stroke="url(#edge)" stroke-width="1.2"/>')
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="none" stroke="{t["text"]}" stroke-opacity="{t["hair_op"]}" stroke-width="1"/>')
    return "\n".join(g)


def brackets(t, x, y, w, h):
    g = []
    for cxp, cyp, sx, sy in [(x+12, y+12, 1, 1), (x+w-12, y+12, -1, 1),
                             (x+12, y+h-12, 1, -1), (x+w-12, y+h-12, -1, -1)]:
        g.append(f'<path d="M {cxp+12*sx} {cyp} H {cxp} V {cyp+12*sy}" fill="none" stroke="{t["cyan"]}" stroke-width="1.5" opacity="0.7"/>')
    return "\n".join(g)


# ---- left panel: holographic portrait scan ----
def left_panel(t):
    g = [glass_card(t, LP_X, LP_Y, LP_W, LP_H, "lpClip")]
    g.append(brackets(t, LP_X, LP_Y, LP_W, LP_H))

    hy = LP_Y + 32
    g.append(f'<circle cx="{LP_X+24}" cy="{hy-4}" r="3.5" fill="{t["cyan"]}" filter="url(#glow)"><animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/></circle>')
    g.append(f'<text x="{LP_X+38}" y="{hy}" font-family="{MONO}" font-size="11.5" letter-spacing="2.5" fill="{t["cyan"]}">IDENT · SCAN</text>')
    g.append(f'<text x="{LP_X+LP_W-24}" y="{hy}" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="1.5" fill="{t["faint"]}">v2.0</text>')
    g.append(f'<line x1="{LP_X+22}" y1="{hy+13}" x2="{LP_X+LP_W-22}" y2="{hy+13}" stroke="{t["text"]}" stroke-opacity="{t["hair_op"]}"/>')

    lines = ASCII
    cols = max(len(l) for l in lines)
    rows = len(lines)
    avail_w = LP_W - 56
    avail_h = LP_H - 200
    cw = avail_w / cols
    fs = cw / 0.60
    stepv = fs * 0.94
    if rows * stepv > avail_h:
        stepv = avail_h / rows
        fs = stepv / 0.94
        cw = fs * 0.60
    block_w = cols * cw
    x0 = LP_X + (LP_W - block_w) / 2
    total_h = rows * stepv
    top = LP_Y + 92 + max(0, (avail_h - total_h) / 2) + fs
    reveal_span = min(1.9, 0.06 * rows)

    g.append('<g clip-path="url(#lpClip)">')
    # glow underlayer, fades in after scan
    g.append(f'<g filter="url(#softGlow)" opacity="0">{anim(attributeName="opacity", values="0;1", dur="0.7s", begin=f"{reveal_span:.2f}s", fill="freeze")}')
    for i, line in enumerate(lines):
        y = top + i * stepv
        g.append(f'<text x="{x0:.1f}" y="{y:.2f}" font-family="{MONO}" font-size="{fs:.2f}" fill="{t["cyan"]}" xml:space="preserve">{esc(line)}</text>')
    g.append('</g>')
    # sharp holo layer, scan-in row by row
    for i, line in enumerate(lines):
        y = top + i * stepv
        begin = (reveal_span / max(1, rows)) * i
        g.append(f'<text x="{x0:.1f}" y="{y:.2f}" font-family="{MONO}" font-size="{fs:.2f}" fill="url(#holoP)" opacity="0" xml:space="preserve">{esc(line)}'
                 f'{anim(attributeName="opacity", values="0;1", dur="0.28s", begin=f"{begin:.2f}s", fill="freeze")}</text>')
    # scan bar sweeping down once (the scanner), then a perpetual soft scan line
    fb_top = top - fs
    fb_bot = top + rows * stepv - fs
    g.append(f'<rect x="{LP_X+26}" y="{fb_top:.0f}" width="{LP_W-52}" height="2.5" rx="1.25" fill="{t["cyan"]}" filter="url(#glow)" opacity="0">'
             f'{anim(attributeName="opacity", values="0;0.9;0.9;0", keyTimes="0;0.1;0.85;1", dur="2.4s", fill="freeze")}'
             f'<animateTransform attributeName="transform" type="translate" values="0 0; 0 {fb_bot-fb_top:.0f}" dur="2.4s" fill="freeze"/></rect>')
    g.append(f'<rect x="{LP_X+20}" y="{fb_top-30:.0f}" width="{LP_W-40}" height="30" fill="url(#scan)" opacity="0">'
             f'{anim(attributeName="opacity", values="0;1", dur="0.4s", begin="2.6s", fill="freeze")}'
             f'<animateTransform attributeName="transform" type="translate" values="0 0; 0 {total_h+40:.0f}" dur="4s" begin="2.6s" repeatCount="indefinite"/></rect>')

    # caption
    py = LP_Y + LP_H - 30
    g.append(f'<text x="{LP_X+24}" y="{py}" font-family="{MONO}" font-size="12" fill="{t["muted"]}" opacity="0">'
             f'<tspan fill="{t["cyan"]}">scan</tspan> ❯ render self.holo'
             f'{anim(attributeName="opacity", values="0;1", dur="0.3s", begin="2.7s", fill="freeze")}</text>')
    g.append(f'<rect x="{LP_X+196}" y="{py-11}" width="8" height="14" rx="1.5" fill="{t["cyan"]}" opacity="0">'
             f'{anim(attributeName="opacity", values="0;1", dur="0.1s", begin="3s", fill="freeze")}'
             f'{anim(attributeName="opacity", values="1;0", dur="1.1s", begin="3.1s", calcMode="discrete", repeatCount="indefinite")}</rect>')

    # hex sigil (monogram), lower-right
    sx, sy = LP_X + LP_W - 52, LP_Y + LP_H - 48
    hexpts = " ".join(f"{sx+20*__import__('math').cos(a):.1f},{sy+20*__import__('math').sin(a):.1f}"
                      for a in [i*3.14159/3 for i in range(6)])
    g.append(f'<g opacity="0">{anim(attributeName="opacity", values="0;1", dur="0.6s", begin="3.2s", fill="freeze")}'
             f'<polygon points="{hexpts}" fill="none" stroke="{t["cyan"]}" stroke-width="1.3" opacity="0.8" filter="url(#glow)"/>'
             f'<polygon points="{" ".join(f"{sx+14*__import__("math").cos(a):.1f},{sy+14*__import__("math").sin(a):.1f}" for a in [i*3.14159/3 for i in range(6)])}" fill="none" stroke="{t["blue"]}" stroke-width="0.7" opacity="0.6"/>'
             f'<text x="{sx}" y="{sy+5.5}" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="700" fill="{t["ice"]}">AH</text></g>')

    g.append('</g>')
    return "\n".join(g)


# ---- role typing ----
def build_typing(t, start_x, base_y):
    CW = 11.4
    FS = 19
    per, hold, era, gap = 0.085, 1.7, 0.04, 0.35
    segs, cur = [], 0.0
    for r in ROLES:
        n = len(r)
        t0 = cur; t1 = t0 + n*per; t2 = t1 + hold; t3 = t2 + n*era
        segs.append((r, n, t0, t1, t2, t3)); cur = t3 + gap
    LOOP = cur
    out = []
    if STATIC:
        r0, n0 = segs[0][0], segs[0][1]; w0 = n0*CW
        out.append(f'<text x="{start_x}" y="{base_y}" font-family="{MONO}" font-size="{FS}" font-weight="600" fill="url(#holo)" textLength="{w0:.1f}" lengthAdjust="spacingAndGlyphs">{esc(r0)}</text>')
        out.append(f'<rect x="{start_x+w0:.1f}" y="{base_y-FS+2}" width="3" height="{FS+2}" rx="1.5" fill="{t["cyan"]}"/>')
        return "\n".join(out)
    for idx, (r, n, t0, t1, t2, t3) in enumerate(segs):
        wpx = n*CW; cid = f"typ{idx}"
        pts = [(0.0, 0.0)]
        if t0 > 0: pts.append((t0, 0.0))
        pts += [(t1, wpx), (t2, wpx), (t3, 0.0)]
        if t3 < LOOP: pts.append((LOOP, 0.0))
        times, vals = [], []
        for tm, v in pts:
            if times and abs(tm-times[-1]) < 1e-6: continue
            times.append(tm); vals.append(v)
        kt = ";".join(f"{tm/LOOP:.5f}" for tm in times)
        vv = ";".join(f"{v:.1f}" for v in vals)
        out.append(f'<clipPath id="{cid}"><rect x="{start_x}" y="{base_y-FS}" width="0" height="{FS+8}">'
                   f'<animate attributeName="width" values="{vv}" keyTimes="{kt}" dur="{LOOP:.2f}s" repeatCount="indefinite"/></rect></clipPath>')
        out.append(f'<text x="{start_x}" y="{base_y}" clip-path="url(#{cid})" font-family="{MONO}" font-size="{FS}" font-weight="600" fill="url(#holo)" textLength="{wpx:.1f}" lengthAdjust="spacingAndGlyphs">{esc(r)}</text>')
    cpts = [(0.0, start_x)]
    for (r, n, t0, t1, t2, t3) in segs:
        wpx = n*CW
        cpts += [(t0, start_x), (t1, start_x+wpx), (t2, start_x+wpx), (t3, start_x)]
    cpts.append((LOOP, start_x))
    ctimes, cvals = [], []
    for tm, v in cpts:
        if ctimes and abs(tm-ctimes[-1]) < 1e-6: cvals[-1] = v; continue
        ctimes.append(tm); cvals.append(v)
    ckt = ";".join(f"{tm/LOOP:.5f}" for tm in ctimes)
    cvv = ";".join(f"{v:.1f}" for v in cvals)
    out.append(f'<rect x="0" y="{base_y-FS+2}" width="3" height="{FS+2}" rx="1.5" fill="{t["cyan"]}">'
               f'<animate attributeName="x" values="{cvv}" keyTimes="{ckt}" dur="{LOOP:.2f}s" repeatCount="indefinite"/>'
               f'<animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    return "\n".join(out)


# ---- right panel: identity HUD ----
def right_panel(t):
    g = [glass_card(t, RP_X, RP_Y, RP_W, RP_H, "rpClip")]
    px = RP_X + 32
    g.append('<g clip-path="url(#rpClip)">')

    # title bar
    g.append(f'<line x1="{RP_X}" y1="{RP_Y+44}" x2="{RP_X+RP_W}" y2="{RP_Y+44}" stroke="{t["text"]}" stroke-opacity="{t["hair_op"]}"/>')
    g.append(f'<circle cx="{RP_X+26}" cy="{RP_Y+22}" r="4.5" fill="{t["online"]}" filter="url(#glow)"><animate attributeName="opacity" values="1;0.4;1" dur="1.8s" repeatCount="indefinite"/></circle>')
    g.append(f'<text x="{RP_X+38}" y="{RP_Y+26}" font-family="{MONO}" font-size="11.5" letter-spacing="1.5" fill="{t["online"]}">ONLINE</text>')
    # signal bars
    for i, hh in enumerate((5, 8, 11, 14)):
        g.append(f'<rect x="{RP_X+108+i*6}" y="{RP_Y+27-hh}" width="4" height="{hh}" rx="1" fill="{t["cyan"]}" opacity="{0.4+i*0.15:.2f}"/>')
    g.append(f'<text x="{RP_X+RP_W/2}" y="{RP_Y+27}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["muted"]}">hamza@esi:~/profile</text>')
    g.append(f'<text x="{RP_X+RP_W-22}" y="{RP_Y+27}" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="1" fill="{t["faint"]}">SYS//DZ</text>')

    y = RP_Y + 78
    g.append(f'<text x="{px}" y="{y}" font-family="{MONO}" font-size="13" fill="{t["faint"]}" opacity="0">'
             f'<tspan fill="{t["cyan"]}">❯</tspan> whoami --profile'
             f'{anim(attributeName="opacity", values="0;1", dur="0.3s", begin="0.2s", fill="freeze")}</text>')

    gy = y + 44
    g.append(f'<g opacity="0">{anim(attributeName="opacity", values="0;1", dur="0.5s", begin="0.5s", fill="freeze")}'
             f'<text x="{px}" y="{gy-26}" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{t["muted"]}">IDENTITY</text>'
             f'<g filter="url(#glow)"><text x="{px}" y="{gy+10}" font-family="{SANS}" font-size="35" font-weight="800" letter-spacing="0.5" fill="url(#holo)">{esc(NAME_FULL)}</text></g>'
             f'<rect x="{px+1}" y="{gy+22}" width="58" height="2.5" rx="1.25" fill="{t["cyan"]}"/></g>')

    ry = gy + 48
    g.append(f'<text x="{px}" y="{ry}" font-family="{MONO}" font-size="19" font-weight="600" fill="{t["muted"]}" opacity="0">'
             f'{anim(attributeName="opacity", values="0;1", dur="0.3s", begin="1.1s", fill="freeze")}❯ </text>')
    g.append(f'<g opacity="0">{anim(attributeName="opacity", values="0;1", dur="0.3s", begin="1.2s", fill="freeze")}')
    g.append(build_typing(t, px + 24, ry))
    g.append('</g>')

    dy = ry + 28
    g.append(f'<g opacity="0">{anim(attributeName="opacity", values="0;1", dur="0.4s", begin="1.5s", fill="freeze")}'
             f'<line x1="{px}" y1="{dy}" x2="{RP_X+RP_W-30}" y2="{dy}" stroke="{t["text"]}" stroke-opacity="{t["hair_op"]}"/>'
             f'<line x1="{px}" y1="{dy}" x2="{RP_X+RP_W-30}" y2="{dy}" stroke="url(#frameShimmer)" stroke-width="1.5"/></g>')

    iy = dy + 32
    istep = 29
    for k, (label, val) in enumerate(INFO):
        ly = iy + k*istep
        begin = 1.7 + k*0.2
        is_link = label in ("PORTFOLIO", "EMAIL")
        vcol = t['cyan'] if is_link else t['text']
        g.append(f'<g opacity="0" transform="translate(-8 0)">'
                 f'{anim(attributeName="opacity", values="0;1", dur="0.45s", begin=f"{begin:.2f}s", fill="freeze")}'
                 f'<animateTransform attributeName="transform" type="translate" values="-8 0; 0 0" dur="0.45s" begin="{begin:.2f}s" fill="freeze"/>'
                 f'<path d="M {px} {ly-9} l 5 4 l -5 4 z" fill="{t["cyan"]}"/>'
                 f'<text x="{px+16}" y="{ly}" font-family="{MONO}" font-size="11" letter-spacing="1.5" fill="{t["faint"]}">{label}</text>'
                 f'<text x="{px+120}" y="{ly}" font-family="{MONO}" font-size="13" fill="{vcol}">{esc(val)}</text>'
                 + (f'<line x1="{px+120}" y1="{ly+3}" x2="{px+120+len(val)*7.6:.0f}" y2="{ly+3}" stroke="{t["cyan"]}" stroke-opacity="0.4"/>' if is_link else '')
                 + '</g>')

    sy = iy + len(INFO)*istep + 16
    g.append(f'<text x="{px}" y="{sy}" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{t["muted"]}" opacity="0">'
             f'{anim(attributeName="opacity", values="0;1", dur="0.4s", begin="2.9s", fill="freeze")}'
             f'<tspan fill="{t["cyan"]}">❯</tspan> stack --load</text>')

    CWp = 7.6; FSp = 12.5; padx = 14; ph = 28; gapx, gapy = 10, 11
    x = px; row_y = sy + 18; maxx = RP_X + RP_W - 30; pill_i = 0
    for label in SKILLS:
        w = len(label)*CWp + 2*padx
        if x + w > maxx:
            x = px; row_y += ph + gapy
        begin = 3.1 + pill_i*0.08
        g.append(f'<g opacity="0">'
                 f'{anim(attributeName="opacity", values="0;1", dur="0.4s", begin=f"{begin:.2f}s", fill="freeze")}'
                 f'<animateTransform attributeName="transform" type="translate" values="0 5; 0 0" dur="0.4s" begin="{begin:.2f}s" fill="freeze"/>'
                 f'<rect x="{x:.1f}" y="{row_y}" width="{w:.1f}" height="{ph}" rx="7" fill="{t["chip"]}" fill-opacity="{t["chip_op"]}" stroke="{t["cyan"]}" stroke-opacity="0.4" stroke-width="0.9"/>'
                 f'<circle cx="{x+padx-1:.1f}" cy="{row_y+ph/2}" r="2.2" fill="{t["cyan"]}"/>'
                 f'<text x="{x+padx+8:.1f}" y="{row_y+ph/2+4.5}" font-family="{MONO}" font-size="{FSp}" fill="{t["text"]}" textLength="{len(label)*CWp:.1f}" lengthAdjust="spacingAndGlyphs">{esc(label)}</text></g>')
        x += w + gapx; pill_i += 1

    soc_y = row_y + ph + 32
    g.append(f'<text x="{px}" y="{soc_y-14}" font-family="{MONO}" font-size="11" letter-spacing="1.5" fill="{t["faint"]}" opacity="0">'
             f'{anim(attributeName="opacity", values="0;1", dur="0.4s", begin="3.8s", fill="freeze")}UPLINK</text>')
    g.append(social_icons(t, px, soc_y + 4))

    g.append('</g>')
    return "\n".join(g)


GH_PATH = ("M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 "
           "0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 "
           "1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 "
           "0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 "
           "1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 "
           "3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 "
           "8.013 0 0016 8c0-4.42-3.58-8-8-8z")
LI_PATH = ("M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.5 8h4v16h-4V8zm7.5 "
           "0h3.8v2.2h.05c.53-1 1.83-2.2 3.77-2.2 4.03 0 4.78 2.65 4.78 6.1V24h-4v-7.1c0-1.7-.03-3.9-2.38-3.9-2.38 "
           "0-2.75 1.86-2.75 3.78V24h-4V8z")
X_PATH = ("M18.24 2.25h3.31l-7.23 8.26 8.5 11.24h-6.66l-5.21-6.82L4.99 21.75H1.68l7.73-8.84L1.25 2.25H8.08l4.71 "
          "6.23zm-1.16 17.52h1.83L7.08 4.13H5.12z")


def icon_wrap(t, cx, cy, inner, begin):
    r = 18
    return (f'<g opacity="0">{anim(attributeName="opacity", values="0;1", dur="0.4s", begin=f"{begin:.2f}s", fill="freeze")}'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["chip"]}" fill-opacity="{t["chip_op"]}" stroke="{t["cyan"]}" stroke-opacity="0.45" stroke-width="0.9"/>'
            f'<g filter="url(#glow)">{inner}</g></g>')


def social_icons(t, x0, y):
    g = []; cy = y + 16; step = 48; col = t['ice']
    x = x0 + 18; s = 1.2; off = 16*s/2
    g.append(icon_wrap(t, x, cy, f'<path transform="translate({x-off:.1f} {cy-off:.1f}) scale({s})" d="{GH_PATH}" fill="{col}"/>', 3.9))
    x += step; s = 0.8; off = 24*s/2
    g.append(icon_wrap(t, x, cy, f'<path transform="translate({x-off:.1f} {cy-off:.1f}) scale({s})" d="{LI_PATH}" fill="{col}"/>', 4.0))
    x += step; off = 24*s/2
    g.append(icon_wrap(t, x, cy, f'<path transform="translate({x-off:.1f} {cy-off:.1f}) scale({s})" d="{X_PATH}" fill="{col}"/>', 4.1))
    x += step; gr = 8.5
    globe = (f'<g stroke="{col}" stroke-width="1.3" fill="none"><circle cx="{x}" cy="{cy}" r="{gr}"/>'
             f'<ellipse cx="{x}" cy="{cy}" rx="{gr*0.42}" ry="{gr}"/><line x1="{x-gr}" y1="{cy}" x2="{x+gr}" y2="{cy}"/>'
             f'<path d="M {x-gr+1.5} {cy-4} H {x+gr-1.5} M {x-gr+1.5} {cy+4} H {x+gr-1.5}"/></g>')
    g.append(icon_wrap(t, x, cy, globe, 4.2))
    return "\n".join(g)


def borders(t):
    g = [f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="{CARD_R}" fill="none" stroke="url(#edge)" stroke-width="1.4"/>']
    g.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{CARD_R}" fill="none" stroke="url(#frameShimmer)" stroke-width="2"/>')
    return "\n".join(g)


def build(t):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" '
             f'aria-label="{esc(NAME_FULL)} — {ROLES[0]}">',
             f'<title>{esc(NAME_FULL)} — GitHub profile</title>',
             defs(t), background(t), left_panel(t), right_panel(t), borders(t), '</svg>']
    return "\n".join(parts)


if __name__ == "__main__":
    for theme in (DARK, LIGHT):
        svg = build(theme)
        if STATIC:
            svg = svg.replace(' opacity="0"', ' opacity="1"')
        fn = f"banner-{theme['name']}{'-static' if STATIC else ''}.svg"
        with open(fn, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {fn} ({len(svg.encode('utf-8'))//1024} KB)")
