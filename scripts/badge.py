"""Write a shields.io-style flat badge SVG, so the README doesn't depend on a live badge service."""

import sys
from xml.sax.saxutils import escape

# Approximate Verdana 11px advance widths, the font shields.io measures with.
WIDTHS = {
    **dict.fromkeys("0123456789", 7.0),
    " ": 3.9, ",": 4.0, ".": 4.0,
    "a": 6.7, "b": 6.9, "c": 5.8, "d": 6.9, "e": 6.6, "f": 3.9, "g": 6.9, "h": 7.0,
    "i": 3.0, "j": 3.8, "k": 6.5, "l": 3.0, "m": 10.7, "n": 7.0, "o": 6.7, "p": 6.9,
    "q": 6.9, "r": 4.7, "s": 5.7, "t": 4.3, "u": 7.0, "v": 6.5, "w": 9.0, "x": 6.5,
    "y": 6.5, "z": 5.8, "F": 6.3,
}


def text_width(text: str) -> float:
    return sum(WIDTHS.get(ch, 7.5) for ch in text)


def badge(label: str, value: str, color: str) -> str:
    lw = round(text_width(label)) + 10
    vw = round(text_width(value)) + 10
    w = lw + vw
    label_e, value_e = escape(label), escape(value)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="20" role="img" aria-label="{label_e}: {value_e}">
  <title>{label_e}: {value_e}</title>
  <linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient>
  <clipPath id="r"><rect width="{w}" height="20" rx="3" fill="#fff"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="{lw}" height="20" fill="#555"/>
    <rect x="{lw}" width="{vw}" height="20" fill="{color}"/>
    <rect width="{w}" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="11">
    <text x="{lw / 2}" y="15" fill="#010101" fill-opacity=".3">{label_e}</text>
    <text x="{lw / 2}" y="14">{label_e}</text>
    <text x="{lw + vw / 2}" y="15" fill="#010101" fill-opacity=".3">{value_e}</text>
    <text x="{lw + vw / 2}" y="14">{value_e}</text>
  </g>
</svg>
"""


if __name__ == "__main__":
    label, value, color, path = sys.argv[1:5]
    if not value.strip():
        sys.exit(f"empty value for {label} badge")
    with open(path, "w", encoding="utf-8") as f:
        f.write(badge(label, value.strip(), color))
