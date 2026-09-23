#!/usr/bin/env python3
"""Render every image on the profile as a static dark/light SVG pair.

    python3 scripts/make_art.py

    header-{dark,light}.svg          name + role card
    card-<project>-{dark,light}.svg  one card per project, laid out 2x2 in the README
    stack-{dark,light}.svg           tools, grouped into rows of tags

The README picks a variant with <picture> + prefers-color-scheme. GitHub serves
SVGs through <img>, which cannot load web fonts, so text uses system font
stacks. Colours are GitHub's own surface/border/text tokens so every panel sits
in the page instead of on top of it. Nothing is animated.
"""
from html import escape
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parent.parent

NAME = "Hamza Ayoub Abdelmoumene"
ROLE = "Computer Science student · ESI Algiers"
META = ["Algiers, Algeria", "Python · C · C++ · Linux"]

# (slug, title, description, language, stack, tag)
PROJECTS = [
    ("vespera", "vespera",
     "Standalone Linux music player companion: MPRIS control, synced lyrics, "
     "a cava visualiser and an EasyEffects equaliser. Distro-agnostic.",
     "C++", "C++ · Qt 6 / QML · CMake", "yay -S vespera"),
    ("lyrics-tool", "lyrics-tool",
     "Terminal live-lyrics visualiser and LRC/WLRC processing suite built on "
     "playerctl and LRCLIB, with tagged, automated releases.",
     "Python", "Python", "pipx install lyrics-tool"),
    ("adds-set-theory", "adds-set-theory",
     "Set operations (union, intersection, difference) on text using binary "
     "search trees and linked lists. ESI data-structures lab exam, 2025–26.",
     "C", "C · Make", "ESI coursework"),
    ("math-algorithms-toolkit", "math-algorithms-toolkit",
     "Mathematical algorithms implemented twice, in C and Python, with "
     "complexity analysis: primes, GCD, combinatorics, Fibonacci and sorting.",
     "C", "C · Python", "Study reference"),
]

STACK = [
    ("Languages", ["Python", "C", "C++", "Java", "QML", "Bash", "SQL"]),
    ("Data & ML", ["NumPy", "pandas", "scikit-learn", "Matplotlib", "Jupyter"]),
    ("Environment", ["Arch Linux", "Git", "Qt 6", "CMake", "GitHub Actions"]),
]

# GitHub linguist colours, so the language dot means what it means everywhere else.
LANG = {"C++": "#f34b7d", "Python": "#3572A5", "C": "#555555"}

THEMES = {
    "dark":  {"bg": "#161b22", "inset": "#0d1117", "border": "#30363d", "text": "#e6edf3",
              "muted": "#8d96a0", "accent": "#4493f8"},
    "light": {"bg": "#f6f8fa", "inset": "#ffffff", "border": "#d0d7de", "text": "#1f2328",
              "muted": "#59636e", "accent": "#0969da"},
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def svg(w: int, h: int, title: str, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">\n'
            f'  <title id="t">{escape(title)}</title>\n{body}</svg>\n')


def panel(w: int, h: int, c: dict) -> str:
    return (f'  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" '
            f'fill="{c["bg"]}" stroke="{c["border"]}"/>\n')


def header(c: dict) -> str:
    w, h = 1000, 150
    body = panel(w, h, c)
    body += f'  <rect x="24" y="38" width="3" height="{h - 76}" rx="1.5" fill="{c["accent"]}"/>\n'
    body += (f'  <text x="48" y="74" font-family="{SANS}" font-size="34" font-weight="600" '
             f'fill="{c["text"]}">{escape(NAME)}</text>\n')
    body += (f'  <text x="48" y="106" font-family="{SANS}" font-size="17" '
             f'fill="{c["muted"]}">{escape(ROLE)}</text>\n')
    for i, line in enumerate(META):
        body += (f'  <text x="{w - 40}" y="{68 + i * 24}" text-anchor="end" font-family="{MONO}" '
                 f'font-size="14" fill="{c["muted"]}">{escape(line)}</text>\n')
    return svg(w, h, f"{NAME} — {ROLE}", body)


def card(project: tuple, c: dict) -> str:
    _, title, desc, lang, stack, tag = project
    w, h = 490, 170
    body = panel(w, h, c)
    body += (f'  <text x="24" y="42" font-family="{SANS}" font-size="19" font-weight="600" '
             f'fill="{c["accent"]}">{escape(title)}</text>\n')
    for i, line in enumerate(textwrap.wrap(desc, 66, break_on_hyphens=False)[:3]):
        body += (f'  <text x="24" y="{72 + i * 20}" font-family="{SANS}" font-size="13.5" '
                 f'fill="{c["muted"]}">{escape(line)}</text>\n')
    # footer: language dot + stack on the left, a mono tag pill on the right
    y = h - 26
    body += f'  <circle cx="30" cy="{y - 4.5}" r="5.5" fill="{LANG[lang]}"/>\n'
    body += (f'  <text x="44" y="{y}" font-family="{SANS}" font-size="13" '
             f'fill="{c["text"]}">{escape(stack)}</text>\n')
    pill_w = round(len(tag) * 7.4 + 22)
    px = w - 20 - pill_w
    body += (f'  <rect x="{px}" y="{y - 19}" width="{pill_w}" height="26" rx="6" '
             f'fill="{c["inset"]}" stroke="{c["border"]}"/>\n')
    body += (f'  <text x="{px + pill_w / 2}" y="{y - 1.5}" text-anchor="middle" font-family="{MONO}" '
             f'font-size="12" fill="{c["text"]}">{escape(tag)}</text>\n')
    return svg(w, h, f"{title}: {desc}", body)


def stack(c: dict) -> str:
    w, row_h, pad = 1000, 44, 22
    h = pad * 2 + row_h * len(STACK) - 12
    body = panel(w, h, c)
    for r, (label, items) in enumerate(STACK):
        y = pad + r * row_h
        body += (f'  <text x="24" y="{y + 20}" font-family="{SANS}" font-size="13" font-weight="600" '
                 f'fill="{c["muted"]}">{escape(label)}</text>\n')
        x = 150
        for item in items:
            cw = round(len(item) * 7.2 + 24)
            body += (f'  <rect x="{x}" y="{y}" width="{cw}" height="30" rx="15" '
                     f'fill="{c["inset"]}" stroke="{c["border"]}"/>\n')
            body += (f'  <text x="{x + cw / 2}" y="{y + 19.5}" text-anchor="middle" font-family="{SANS}" '
                     f'font-size="13" fill="{c["text"]}">{escape(item)}</text>\n')
            x += cw + 8
    summary = "; ".join(f"{label}: {', '.join(items)}" for label, items in STACK)
    return svg(w, h, summary, body)


def main() -> None:
    outputs = {}
    for mode, c in THEMES.items():
        outputs[f"header-{mode}.svg"] = header(c)
        outputs[f"stack-{mode}.svg"] = stack(c)
        for p in PROJECTS:
            outputs[f"card-{p[0]}-{mode}.svg"] = card(p, c)
    for name, text in outputs.items():
        (ROOT / name).write_text(text, encoding="utf-8")
    print(f"wrote {len(outputs)} files")


if __name__ == "__main__":
    main()
