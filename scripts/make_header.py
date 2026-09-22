#!/usr/bin/env python3
"""Render the profile header as a static dark/light SVG pair.

    python3 scripts/make_header.py      -> header-dark.svg, header-light.svg

The README picks one with <picture> + prefers-color-scheme. GitHub serves SVGs
through <img>, which cannot load web fonts, so the text uses system font stacks.
Colours are GitHub's own surface/border/text tokens, so the card sits in the
page instead of on top of it; the one accent is the thin bar on the left.
"""
from pathlib import Path

NAME = "Hamza Ayoub Abdelmoumene"
ROLE = "Computer Science student · ESI Algiers"
META = ["Algiers, Algeria", "Python · C · C++ · Linux"]

THEMES = {
    "dark":  {"bg": "#161b22", "border": "#30363d", "text": "#e6edf3", "muted": "#8d96a0", "accent": "#4493f8"},
    "light": {"bg": "#f6f8fa", "border": "#d0d7de", "text": "#1f2328", "muted": "#59636e", "accent": "#0969da"},
}

W, H = 1000, 150
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def render(c: dict) -> str:
    meta = "\n".join(
        f'  <text x="{W - 40}" y="{68 + i * 24}" text-anchor="end" font-family="{MONO}" '
        f'font-size="14" fill="{c["muted"]}">{line}</text>'
        for i, line in enumerate(META)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">{NAME} — {ROLE}</title>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="{c["bg"]}" stroke="{c["border"]}"/>
  <rect x="24" y="38" width="3" height="{H - 76}" rx="1.5" fill="{c["accent"]}"/>
  <text x="48" y="74" font-family="{SANS}" font-size="34" font-weight="600" fill="{c["text"]}">{NAME}</text>
  <text x="48" y="106" font-family="{SANS}" font-size="17" fill="{c["muted"]}">{ROLE}</text>
{meta}
</svg>
"""


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    for mode, colours in THEMES.items():
        (root / f"header-{mode}.svg").write_text(render(colours), encoding="utf-8")
        print(f"wrote header-{mode}.svg")


if __name__ == "__main__":
    main()
