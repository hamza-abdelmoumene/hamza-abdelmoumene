#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aged-paper GitHub profile hero banner.
Emits banner-vellum.svg (dark-mode viewers) and banner-bond.svg (light-mode) --
identical layout & animation, paper-swapped. A typeset technical dossier that
"prints" itself in, then rests. Pure SVG + SMIL (no JS). GitHub-compatible.
"""
import math
import os
import random

STATIC = os.environ.get("STATIC") == "1"   # bake final frame for still-image QA

# ----------------------------------------------------------------------------
# Canvas / layout geometry
# ----------------------------------------------------------------------------
W, H = 1180, 610
CARD_R = 10                 # paper cards have crisp, near-square corners
M = 22

LP_X, LP_Y = M, M
LP_W, LP_H = 440, H - 2 * M
RP_X = LP_X + LP_W + 18
RP_Y = M
RP_W = W - RP_X - M
RP_H = H - 2 * M

CX = LP_X + LP_W / 2

# ----------------------------------------------------------------------------
# Content (from the user's real profile)
# ----------------------------------------------------------------------------
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

# Shaded portrait bust -- horizontally symmetric, centred via text-anchor.
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

# ----------------------------------------------------------------------------
# Palettes -- two sheets of the same aged stock
# ----------------------------------------------------------------------------
DARK = dict(  # dark-mode viewers: aged dark ledger — lamplit leather, cream ink
    name="dark",
    # flat warm surfaces (no gradient): rsvg interpolates gradients in linearRGB,
    # which greens very-dark warm midtones. Grain + vignette carry the depth.
    bg="#1E160C", bg2="#1E160C",
    panel="#251C0F", panelTop="#251C0F", titlebar="#1C1509",
    ink="#E7D6AF", inkStrong="#F5EACC", muted="#B29A6E", faint="#87714E",
    border="#E7D6AF", hi="#0E0A05",
    ox="#D06E4F", teal="#6BA88F", gold="#CFA24C",
    dotR="#C8664F", dotY="#CBA24C", dotG="#7FA36B",
    border_op="0.14", border2_op="0.24",
    grain_op="0.05", vignette_op="0.30",
    grain_col="#E9DBBB", fibre_col="#C7B487", vign_col="#000000",
    shadow="#000000", shadow_op="0.50", shadow_blur="22",
    pill="#2C2113", pill_op="0.70",
    rule_op="0.10",
)
LIGHT = dict(  # light-mode viewers: aged greige paper (muted, de-yellowed)
    name="light",
    bg="#E4DBC7", bg2="#D8CEB6",
    panel="#EEE7D6", panelTop="#F4EFE1", titlebar="#E5DDCB",
    ink="#352B1B", inkStrong="#251B0C", muted="#6C5E48", faint="#96896B",
    border="#352B1A", hi="#F5F1E5",
    ox="#9C4436", teal="#41695A", gold="#95712F",
    dotR="#A5573F", dotY="#B08A40", dotG="#617A55",
    border_op="0.16", border2_op="0.30",
    grain_op="0.05", vignette_op="0.13",
    grain_col="#2A1B08", fibre_col="#3A2B15", vign_col="#2A1B08",
    shadow="#352B1A", shadow_op="0.12", shadow_blur="16",
    pill="#F1EBDC", pill_op="0.85",
    rule_op="0.09",
)

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

# Typewriter mono for the "teletype" body, and a book serif for typeset display.
MONO = ("'JetBrains Mono','Courier New','SFMono-Regular',ui-monospace,"
        "'Cascadia Code',Consolas,'Liberation Mono',Menlo,monospace")
SERIF = ("'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',"
         "'URW Palladio L',Georgia,'Times New Roman',serif")


def anim(**kw):
    attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    return f"<animate {attrs}/>"


# ----------------------------------------------------------------------------
# DEFS: gradients, filters, clips
# ----------------------------------------------------------------------------
def defs(t):
    p = ["<defs>"]

    p.append(f'<clipPath id="cardClip"><rect x="0" y="0" width="{W}" height="{H}" rx="{CARD_R}"/></clipPath>')
    p.append(f'<clipPath id="lpClip"><rect x="{LP_X}" y="{LP_Y}" width="{LP_W}" height="{LP_H}" rx="6"/></clipPath>')
    p.append(f'<clipPath id="rpClip"><rect x="{RP_X}" y="{RP_Y}" width="{RP_W}" height="{RP_H}" rx="6"/></clipPath>')

    # -- paper base gradient (subtle warm gradient across the sheet) --
    p.append(f'''<linearGradient color-interpolation="sRGB" id="bgGrad" x1="0" y1="0" x2="0.7" y2="1">
      <stop offset="0" stop-color="{t['bg']}"/>
      <stop offset="1" stop-color="{t['bg2']}"/>
    </linearGradient>''')

    # -- inset card (laid-paper) gradient --
    p.append(f'''<linearGradient color-interpolation="sRGB" id="panelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t['panelTop']}"/>
      <stop offset="1" stop-color="{t['panel']}"/>
    </linearGradient>''')

    # -- accent (aged inks): oxblood -> antique gold. static, muted. --
    p.append(f'''<linearGradient color-interpolation="sRGB" id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['ox']}"/>
      <stop offset="1" stop-color="{t['gold']}"/>
    </linearGradient>''')

    # -- edge vignette: transparent centre -> darker corners (ages the sheet) --
    p.append(f'''<radialGradient color-interpolation="sRGB" id="vignette" cx="0.5" cy="0.42" r="0.75">
      <stop offset="0" stop-color="{t['bg2']}" stop-opacity="0"/>
      <stop offset="0.72" stop-color="{t['bg2']}" stop-opacity="0"/>
      <stop offset="1" stop-color="{t['vign_col']}" stop-opacity="{t['vignette_op']}"/>
    </radialGradient>''')

    # -- paper grain: specks with noise-driven alpha (dark on paper, light on leather) --
    p.append(f'''<filter id="grain" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" stitchTiles="stitch" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.85 0" result="a"/>
      <feFlood flood-color="{t['grain_col']}" result="c"/>
      <feComposite in="c" in2="a" operator="in"/>
    </filter>''')

    # -- fibrous long grain (very low freq, gives the sheet a "laid" texture) --
    p.append(f'''<filter id="fibre" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.012 0.16" numOctaves="2" seed="4" stitchTiles="stitch" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.5 0" result="a"/>
      <feFlood flood-color="{t['fibre_col']}" result="c"/>
      <feComposite in="c" in2="a" operator="in"/>
    </filter>''')

    # -- warm paper drop shadow for the inset cards --
    p.append(f'''<filter id="panelShadow" color-interpolation-filters="sRGB" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="{t['shadow_blur']}" flood-color="{t['shadow']}" flood-opacity="{t['shadow_op']}"/>
    </filter>''')

    # -- ink bleed: a whisper of spread so glyphs read as pressed into fibre --
    p.append(f'''<filter id="inkBleed" color-interpolation-filters="sRGB" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="0.6" result="b"/>
      <feFlood flood-color="{t['ink']}" flood-opacity="0.5" result="c"/>
      <feComposite in="c" in2="b" operator="in" result="g"/>
      <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>''')

    p.append("</defs>")
    return "\n".join(p)


# ----------------------------------------------------------------------------
# Background layer -- the sheet itself
# ----------------------------------------------------------------------------
def background(t):
    g = ['<g clip-path="url(#cardClip)">']
    g.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bgGrad)"/>')
    # long fibre + speckle grain
    g.append(f'<rect x="0" y="0" width="{W}" height="{H}" filter="url(#fibre)" opacity="{float(t["grain_op"])*0.6:.3f}"/>')
    g.append(f'<rect x="0" y="0" width="{W}" height="{H}" filter="url(#grain)" opacity="{t["grain_op"]}"/>')
    # aged corners
    g.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#vignette)"/>')
    # a couple of drifting dust motes -- barely-there life, not neon
    rnd = random.Random(11)
    for _ in range(6):
        x = rnd.randint(40, W - 40)
        y = rnd.randint(40, H - 40)
        r = rnd.choice([0.7, 0.9, 1.1])
        dur = rnd.uniform(9, 16)
        dly = rnd.uniform(0, 6)
        dy = rnd.uniform(-10, 10)
        g.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["muted"]}" opacity="0">'
            f'{anim(attributeName="opacity", values="0;0.18;0", dur=f"{dur:.1f}s", begin=f"{dly:.1f}s", repeatCount="indefinite")}'
            f'<animateTransform attributeName="transform" type="translate" values="0 0; 0 {dy:.0f}; 0 0" dur="{dur*1.4:.1f}s" begin="{dly:.1f}s" repeatCount="indefinite"/>'
            f'</circle>')
    g.append('</g>')
    return "\n".join(g)


def card_shell(t, x, y, w, h):
    """Inset laid-paper card: soft shadow, fill, double letterpress rule."""
    g = [f'<g filter="url(#panelShadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="url(#panelGrad)"/></g>']
    # subtle fibre over the card
    g.append(f'<g clip-path="url(#{ "lpClip" if x==LP_X else "rpClip" })"><rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#grain)" opacity="{float(t["grain_op"])*0.6:.3f}"/></g>')
    # double rule (outer + inset hairline) -- classic bordered certificate
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{t["border"]}" stroke-opacity="{t["border2_op"]}" stroke-width="1.2"/>')
    g.append(f'<rect x="{x+4}" y="{y+4}" width="{w-8}" height="{h-8}" rx="4" fill="none" stroke="{t["border"]}" stroke-opacity="{t["border_op"]}" stroke-width="0.8"/>')
    return "\n".join(g)


def crop_marks(t, x, y, w, h):
    g = []
    for cxp, cyp, sx, sy in [(x+11, y+11, 1, 1), (x+w-11, y+11, -1, 1),
                             (x+11, y+h-11, 1, -1), (x+w-11, y+h-11, -1, -1)]:
        g.append(f'<path d="M {cxp+9*sx} {cyp} H {cxp} V {cyp+9*sy}" fill="none" stroke="{t["ox"]}" stroke-width="1.1" opacity="0.55"/>')
    return "\n".join(g)


# ----------------------------------------------------------------------------
# Left panel: the portrait plate
# ----------------------------------------------------------------------------
def left_panel(t):
    g = [card_shell(t, LP_X, LP_Y, LP_W, LP_H)]
    g.append(crop_marks(t, LP_X, LP_Y, LP_W, LP_H))

    # header: PLATE label + folio number
    hy = LP_Y + 32
    g.append(f'<text x="{LP_X+24}" y="{hy}" font-family="{MONO}" font-size="11.5" letter-spacing="2.5" fill="{t["muted"]}">PLATE I · SELF</text>')
    g.append(f'<text x="{LP_X+LP_W-24}" y="{hy}" text-anchor="end" font-family="{SERIF}" font-size="12" font-style="italic" fill="{t["faint"]}">No. 001</text>')
    g.append(f'<line x1="{LP_X+22}" y1="{hy+13}" x2="{LP_X+LP_W-22}" y2="{hy+13}" stroke="{t["border"]}" stroke-opacity="{t["border2_op"]}"/>')

    # ASCII portrait geometry
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

    # ink-bleed underlayer (etched-plate feel), fades in once after the reveal
    g.append('<g filter="url(#inkBleed)" opacity="0">')
    g.append(anim(attributeName="opacity", values="0;0.5", dur="0.7s", begin=f"{reveal_span:.2f}s", fill="freeze"))
    for i, line in enumerate(lines):
        y = top + i * stepv
        g.append(f'<text x="{x0:.1f}" y="{y:.2f}" font-family="{MONO}" font-size="{fs:.2f}" '
                 f'letter-spacing="0" fill="{t["ink"]}" xml:space="preserve">{esc(line)}</text>')
    g.append('</g>')

    # sharp ink, printed row by row
    for i, line in enumerate(lines):
        y = top + i * stepv
        begin = (reveal_span / max(1, rows)) * i
        g.append(
            f'<text x="{x0:.1f}" y="{y:.2f}" font-family="{MONO}" '
            f'font-size="{fs:.2f}" letter-spacing="0" fill="{t["ink"]}" opacity="0" '
            f'xml:space="preserve">{esc(line)}'
            f'{anim(attributeName="opacity", values="0;1", dur="0.28s", begin=f"{begin:.2f}s", fill="freeze")}'
            f'</text>')

    # platen line: the printing head sweeping down once
    fb_top = top - fs
    fb_bot = top + rows * stepv - fs
    g.append(
        f'<rect x="{LP_X+30}" y="{fb_top:.0f}" width="{LP_W-60}" height="2" rx="1" fill="{t["ox"]}" opacity="0">'
        f'{anim(attributeName="opacity", values="0;0.8;0.8;0", keyTimes="0;0.1;0.85;1", dur="2.6s", fill="freeze")}'
        f'<animateTransform attributeName="transform" type="translate" values="0 0; 0 {fb_bot-fb_top:.0f}" dur="2.6s" fill="freeze"/>'
        f'</rect>')

    # caption + blinking cursor
    py = LP_Y + LP_H - 30
    g.append(f'<text x="{LP_X+24}" y="{py}" font-family="{MONO}" font-size="12" fill="{t["muted"]}" opacity="0">'
             f'<tspan fill="{t["ox"]}">plate</tspan> <tspan fill="{t["muted"]}">❯ etch --self</tspan>'
             f'{anim(attributeName="opacity", values="0;1", dur="0.3s", begin="2.7s", fill="freeze")}</text>')
    g.append(f'<rect x="{LP_X+186}" y="{py-11}" width="8" height="14" rx="1" fill="{t["ox"]}" opacity="0">'
             f'{anim(attributeName="opacity", values="0;1", dur="0.1s", begin="3s", fill="freeze")}'
             f'{anim(attributeName="opacity", values="1;0", dur="1.1s", begin="3.1s", calcMode="discrete", repeatCount="indefinite")}'
             f'</rect>')

    # monogram seal (personal letterhead stamp), lower-right of the plate
    sx, sy = LP_X + LP_W - 54, LP_Y + LP_H - 50
    g.append(
        f'<g opacity="0">'
        f'{anim(attributeName="opacity", values="0;1", dur="0.6s", begin="3.3s", fill="freeze")}'
        f'<circle cx="{sx}" cy="{sy}" r="22" fill="none" stroke="{t["ox"]}" stroke-width="1.4" opacity="0.75"/>'
        f'<circle cx="{sx}" cy="{sy}" r="17.5" fill="none" stroke="{t["gold"]}" stroke-width="0.8" opacity="0.7"/>'
        f'<text x="{sx}" y="{sy+6.5}" text-anchor="middle" font-family="{SERIF}" font-size="17" '
        f'font-weight="700" letter-spacing="0.5" fill="{t["ink"]}" opacity="0.9">AH</text>'
        f'<text x="{sx}" y="{sy-11.5}" text-anchor="middle" font-family="{MONO}" font-size="4.6" '
        f'letter-spacing="1.4" fill="{t["muted"]}">· EST · ALGIERS ·</text>'
        f'</g>')

    g.append('</g>')  # lpClip
    return "\n".join(g)


# ----------------------------------------------------------------------------
# Typing timeline for the role line
# ----------------------------------------------------------------------------
def build_typing(t, start_x, base_y):
    CW = 11.4
    FS = 19
    per, hold, era, gap = 0.085, 1.7, 0.04, 0.35

    segs = []
    cur = 0.0
    for r in ROLES:
        n = len(r)
        t0 = cur
        t1 = t0 + n * per
        t2 = t1 + hold
        t3 = t2 + n * era
        segs.append((r, n, t0, t1, t2, t3))
        cur = t3 + gap
    LOOP = cur

    out = []
    if STATIC:
        r0, n0 = segs[0][0], segs[0][1]
        w0 = n0 * CW
        out.append(f'<text x="{start_x}" y="{base_y}" font-family="{MONO}" font-size="{FS}" '
                   f'font-weight="600" fill="{t["ox"]}" textLength="{w0:.1f}" '
                   f'lengthAdjust="spacingAndGlyphs">{esc(r0)}</text>')
        out.append(f'<rect x="{start_x+w0:.1f}" y="{base_y-FS+2}" width="3" height="{FS+2}" rx="1" fill="{t["ink"]}"/>')
        return "\n".join(out)

    for idx, (r, n, t0, t1, t2, t3) in enumerate(segs):
        wpx = n * CW
        cid = f"typ{idx}"
        pts = [(0.0, 0.0)]
        if t0 > 0:
            pts.append((t0, 0.0))
        pts += [(t1, wpx), (t2, wpx), (t3, 0.0)]
        if t3 < LOOP:
            pts.append((LOOP, 0.0))
        times, vals = [], []
        for tm, v in pts:
            if times and abs(tm - times[-1]) < 1e-6:
                continue
            times.append(tm)
            vals.append(v)
        kt = ";".join(f"{tm/LOOP:.5f}" for tm in times)
        vv = ";".join(f"{v:.1f}" for v in vals)
        out.append(f'<clipPath id="{cid}"><rect x="{start_x}" y="{base_y-FS}" width="0" height="{FS+8}">'
                   f'<animate attributeName="width" values="{vv}" keyTimes="{kt}" dur="{LOOP:.2f}s" repeatCount="indefinite"/>'
                   f'</rect></clipPath>')
        out.append(f'<text x="{start_x}" y="{base_y}" clip-path="url(#{cid})" font-family="{MONO}" '
                   f'font-size="{FS}" font-weight="600" fill="{t["ox"]}" textLength="{wpx:.1f}" '
                   f'lengthAdjust="spacingAndGlyphs">{esc(r)}</text>')

    cpts = [(0.0, start_x)]
    for (r, n, t0, t1, t2, t3) in segs:
        wpx = n * CW
        cpts += [(t0, start_x), (t1, start_x + wpx), (t2, start_x + wpx), (t3, start_x)]
    cpts.append((LOOP, start_x))
    ctimes, cvals = [], []
    for tm, v in cpts:
        if ctimes and abs(tm - ctimes[-1]) < 1e-6:
            cvals[-1] = v
            continue
        ctimes.append(tm)
        cvals.append(v)
    ckt = ";".join(f"{tm/LOOP:.5f}" for tm in ctimes)
    cvv = ";".join(f"{v:.1f}" for v in cvals)
    out.append(
        f'<rect x="0" y="{base_y-FS+2}" width="3" height="{FS+2}" rx="1" fill="{t["ink"]}">'
        f'<animate attributeName="x" values="{cvv}" keyTimes="{ckt}" dur="{LOOP:.2f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/>'
        f'</rect>')
    return "\n".join(out)


# ----------------------------------------------------------------------------
# Right panel: the dossier body
# ----------------------------------------------------------------------------
def right_panel(t):
    g = [card_shell(t, RP_X, RP_Y, RP_W, RP_H)]
    px = RP_X + 32
    g.append('<g clip-path="url(#rpClip)">')

    # header strip: teleprinter caption + three faded stamp dots
    g.append(f'<rect x="{RP_X}" y="{RP_Y}" width="{RP_W}" height="44" fill="{t["titlebar"]}"/>')
    g.append(f'<line x1="{RP_X}" y1="{RP_Y+44}" x2="{RP_X+RP_W}" y2="{RP_Y+44}" stroke="{t["border"]}" stroke-opacity="{t["border2_op"]}"/>')
    for i, col in enumerate((t['dotR'], t['dotY'], t['dotG'])):
        g.append(f'<circle cx="{RP_X+24+i*18}" cy="{RP_Y+22}" r="5" fill="{col}" opacity="0.85" stroke="{t["border"]}" stroke-opacity="0.25"/>')
    g.append(f'<text x="{RP_X+RP_W/2}" y="{RP_Y+27}" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="0.5" fill="{t["muted"]}">'
             f'hamza@esi — ~/profile — zsh</text>')
    g.append(f'<text x="{RP_X+RP_W-22}" y="{RP_Y+27}" text-anchor="end" font-family="{SERIF}" font-size="11.5" font-style="italic" fill="{t["faint"]}">est. Algiers</text>')

    # ---- body ----
    y = RP_Y + 78
    g.append(f'<text x="{px}" y="{y}" font-family="{MONO}" font-size="13" fill="{t["faint"]}" opacity="0">'
             f'<tspan fill="{t["teal"]}">❯</tspan> whoami --profile'
             f'{anim(attributeName="opacity", values="0;1", dur="0.3s", begin="0.2s", fill="freeze")}</text>')

    # greeting + name (serif display, letterpress relief)
    gy = y + 42
    g.append(f'<g opacity="0">{anim(attributeName="opacity", values="0;1", dur="0.5s", begin="0.5s", fill="freeze")}'
             f'<text x="{px}" y="{gy-26}" font-family="{SERIF}" font-size="15" font-style="italic" fill="{t["muted"]}">Hi, I’m</text>'
             # relief highlight underlayer
             f'<text x="{px}" y="{gy+9}" font-family="{SERIF}" font-size="37" font-weight="700" letter-spacing="-0.3" '
             f'fill="{t["hi"]}" opacity="0.6">{esc(NAME_FULL)}</text>'
             # ink
             f'<text x="{px}" y="{gy+8}" font-family="{SERIF}" font-size="37" font-weight="700" letter-spacing="-0.3" '
             f'fill="{t["inkStrong"]}">{esc(NAME_FULL)}</text>'
             # short oxblood underscore rule
             f'<rect x="{px+1}" y="{gy+20}" width="54" height="2.5" rx="1" fill="{t["ox"]}"/>'
             f'</g>')

    # role typing line
    ry = gy + 46
    g.append(f'<text x="{px}" y="{ry}" font-family="{MONO}" font-size="19" font-weight="600" fill="{t["muted"]}" opacity="0">'
             f'{anim(attributeName="opacity", values="0;1", dur="0.3s", begin="1.1s", fill="freeze")}❯ </text>')
    role_x = px + 24
    g.append(f'<g opacity="0">{anim(attributeName="opacity", values="0;1", dur="0.3s", begin="1.2s", fill="freeze")}')
    g.append(build_typing(t, role_x, ry))
    g.append('</g>')

    # divider with a centred fleuron
    dy = ry + 28
    mid = (px + (RP_X + RP_W - 30)) / 2
    g.append(f'<g opacity="0">{anim(attributeName="opacity", values="0;1", dur="0.4s", begin="1.5s", fill="freeze")}'
             f'<line x1="{px}" y1="{dy}" x2="{mid-16}" y2="{dy}" stroke="{t["border"]}" stroke-opacity="{t["border2_op"]}"/>'
             f'<line x1="{mid+16}" y1="{dy}" x2="{RP_X+RP_W-30}" y2="{dy}" stroke="{t["border"]}" stroke-opacity="{t["border2_op"]}"/>'
             f'<text x="{mid}" y="{dy+4.5}" text-anchor="middle" font-family="{SERIF}" font-size="13" fill="{t["gold"]}">❦</text>'
             f'</g>')

    # info block
    iy = dy + 32
    istep = 29
    for k, (label, val) in enumerate(INFO):
        ly = iy + k * istep
        begin = 1.7 + k * 0.2
        is_link = label in ("PORTFOLIO", "EMAIL")
        vcol = t['teal'] if is_link else t['ink']
        g.append(
            f'<g opacity="0" transform="translate(-8 0)">'
            f'{anim(attributeName="opacity", values="0;1", dur="0.45s", begin=f"{begin:.2f}s", fill="freeze")}'
            f'<animateTransform attributeName="transform" type="translate" values="-8 0; 0 0" dur="0.45s" begin="{begin:.2f}s" fill="freeze"/>'
            f'<rect x="{px}" y="{ly-12}" width="3" height="15" rx="1" fill="{t["ox"]}"/>'
            f'<text x="{px+14}" y="{ly}" font-family="{MONO}" font-size="11" letter-spacing="1.5" fill="{t["faint"]}">{label}</text>'
            f'<text x="{px+118}" y="{ly}" font-family="{MONO}" font-size="13" fill="{vcol}">{esc(val)}</text>'
            + (f'<line x1="{px+118}" y1="{ly+3}" x2="{px+118+len(val)*7.6:.0f}" y2="{ly+3}" stroke="{t["teal"]}" stroke-opacity="0.4"/>' if is_link else '')
            + '</g>')

    # skills header
    sy = iy + len(INFO) * istep + 16
    g.append(f'<text x="{px}" y="{sy}" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{t["muted"]}" opacity="0">'
             f'{anim(attributeName="opacity", values="0;1", dur="0.4s", begin="2.9s", fill="freeze")}'
             f'<tspan fill="{t["teal"]}">❯</tspan> skills --stack</text>')

    # ink-stamped tags
    CWp = 7.6
    FSp = 12.5
    padx = 14
    ph = 28
    gapx, gapy = 10, 11
    x = px
    row_y = sy + 18
    maxx = RP_X + RP_W - 30
    pill_i = 0
    for label in SKILLS:
        w = len(label) * CWp + 2 * padx
        if x + w > maxx:
            x = px
            row_y += ph + gapy
        begin = 3.1 + pill_i * 0.08
        g.append(
            f'<g opacity="0">'
            f'{anim(attributeName="opacity", values="0;1", dur="0.4s", begin=f"{begin:.2f}s", fill="freeze")}'
            f'<animateTransform attributeName="transform" type="translate" values="0 5; 0 0" dur="0.4s" begin="{begin:.2f}s" fill="freeze"/>'
            f'<rect x="{x:.1f}" y="{row_y}" width="{w:.1f}" height="{ph}" rx="3" '
            f'fill="{t["pill"]}" fill-opacity="{t["pill_op"]}" stroke="{t["border"]}" stroke-opacity="{t["border2_op"]}" stroke-width="0.9"/>'
            f'<circle cx="{x+padx-1:.1f}" cy="{row_y+ph/2}" r="2.2" fill="{t["ox"]}"/>'
            f'<text x="{x+padx+8:.1f}" y="{row_y+ph/2+4.5}" font-family="{MONO}" font-size="{FSp}" fill="{t["ink"]}" '
            f'textLength="{len(label)*CWp:.1f}" lengthAdjust="spacingAndGlyphs">{esc(label)}</text>'
            f'</g>')
        x += w + gapx
        pill_i += 1

    # connect
    soc_y = row_y + ph + 32
    g.append(f'<text x="{px}" y="{soc_y-14}" font-family="{MONO}" font-size="11" letter-spacing="1.5" fill="{t["faint"]}" opacity="0">'
             f'{anim(attributeName="opacity", values="0;1", dur="0.4s", begin="3.8s", fill="freeze")}CONNECT</text>')
    g.append(social_icons(t, px, soc_y + 4))

    g.append('</g>')  # rpClip
    return "\n".join(g)


# ----------------------------------------------------------------------------
# Social icons (ink on paper, hairline rings)
# ----------------------------------------------------------------------------
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
    return (
        f'<g opacity="0">'
        f'{anim(attributeName="opacity", values="0;1", dur="0.4s", begin=f"{begin:.2f}s", fill="freeze")}'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["pill"]}" fill-opacity="{t["pill_op"]}" '
        f'stroke="{t["border"]}" stroke-opacity="{t["border2_op"]}" stroke-width="0.9"/>'
        f'{inner}'
        f'</g>')


def social_icons(t, x0, y):
    g = []
    cy = y + 16
    step = 48
    col = t['ink']
    x = x0 + 18
    s = 1.2
    off = 16 * s / 2
    g.append(icon_wrap(t, x, cy, f'<path transform="translate({x-off:.1f} {cy-off:.1f}) scale({s})" d="{GH_PATH}" fill="{col}"/>', 3.9))
    x += step
    s = 0.8
    off = 24 * s / 2
    g.append(icon_wrap(t, x, cy, f'<path transform="translate({x-off:.1f} {cy-off:.1f}) scale({s})" d="{LI_PATH}" fill="{col}"/>', 4.0))
    x += step
    off = 24 * s / 2
    g.append(icon_wrap(t, x, cy, f'<path transform="translate({x-off:.1f} {cy-off:.1f}) scale({s})" d="{X_PATH}" fill="{col}"/>', 4.1))
    x += step
    gr = 8.5
    globe = (
        f'<g stroke="{col}" stroke-width="1.3" fill="none">'
        f'<circle cx="{x}" cy="{cy}" r="{gr}"/>'
        f'<ellipse cx="{x}" cy="{cy}" rx="{gr*0.42}" ry="{gr}"/>'
        f'<line x1="{x-gr}" y1="{cy}" x2="{x+gr}" y2="{cy}"/>'
        f'<path d="M {x-gr+1.5} {cy-4} H {x+gr-1.5} M {x-gr+1.5} {cy+4} H {x+gr-1.5}"/>'
        f'</g>')
    g.append(icon_wrap(t, x, cy, globe, 4.2))
    return "\n".join(g)


# ----------------------------------------------------------------------------
# Outer border: double letterpress rule
# ----------------------------------------------------------------------------
def borders(t):
    g = [f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="{CARD_R}" fill="none" '
         f'stroke="{t["border"]}" stroke-opacity="{t["border2_op"]}" stroke-width="1.4"/>']
    g.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="{CARD_R-3}" fill="none" '
             f'stroke="{t["border"]}" stroke-opacity="{t["border_op"]}" stroke-width="0.8"/>')
    return "\n".join(g)


def build(t):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" fill="none" role="img" '
             f'aria-label="{esc(NAME_FULL)} — {ROLES[0]}">',
             f'<title>{esc(NAME_FULL)} — GitHub profile</title>',
             defs(t), background(t), left_panel(t), right_panel(t), borders(t),
             '</svg>']
    return "\n".join(parts)


if __name__ == "__main__":
    for theme in (DARK, LIGHT):
        svg = build(theme)
        if STATIC:
            svg = svg.replace(' opacity="0"', ' opacity="1"')
        fn = f"banner-{theme['name']}{'-static' if STATIC else ''}.svg"
        with open(fn, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {fn}  ({len(svg.encode('utf-8'))//1024} KB)")
