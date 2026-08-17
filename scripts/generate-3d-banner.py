"""Generate animated isometric SVGs for the GitHub profile README."""
from __future__ import annotations

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(exist_ok=True)
rng = random.Random(4551)


def pts(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in points)


def cube(
    cx: float,
    cy: float,
    size: float,
    h: float,
    top: str,
    left: str,
    right: str,
    opacity: float = 1,
    delay: float = 0,
    dur: float = 4,
) -> str:
    hw, hh = size, size * 0.52
    top_pts = [
        (cx, cy - h),
        (cx + hw, cy + hh - h),
        (cx, cy + 2 * hh - h),
        (cx - hw, cy + hh - h),
    ]
    left_pts = [
        (cx - hw, cy + hh - h),
        (cx, cy + 2 * hh - h),
        (cx, cy + 2 * hh),
        (cx - hw, cy + hh),
    ]
    right_pts = [
        (cx + hw, cy + hh - h),
        (cx, cy + 2 * hh - h),
        (cx, cy + 2 * hh),
        (cx + hw, cy + hh),
    ]
    grow = max(6.0, h * 0.18)
    return f"""
  <g opacity="{opacity:.2f}">
    <animateTransform attributeName="transform" type="translate" values="0,0; 0,{-grow:.1f}; 0,0"
      dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>
    <polygon points="{pts(left_pts)}" fill="{left}"/>
    <polygon points="{pts(right_pts)}" fill="{right}"/>
    <polygon points="{pts(top_pts)}" fill="{top}"/>
  </g>"""


def iso_pos(col: int, row: int, origin_x: float, origin_y: float, size: float) -> tuple[float, float]:
    hw, hh = size, size * 0.52
    x = origin_x + (col - row) * hw
    y = origin_y + (col + row) * hh
    return x, y


PALETTES = [
    ("#67e8f9", "#0891b2", "#155e75"),
    ("#a78bfa", "#6d28d9", "#4c1d95"),
    ("#34d399", "#059669", "#064e3b"),
    ("#38bdf8", "#0284c7", "#0c4a6e"),
    ("#f0abfc", "#c026d3", "#701a75"),
    ("#fde047", "#ca8a04", "#713f12"),
]


def build_city(origin_x: float, origin_y: float, cols: int, rows: int, size: float) -> str:
    parts: list[str] = []
    cells = [(c, r) for r in range(rows) for c in range(cols)]
    cells.sort(key=lambda cr: cr[0] + cr[1])
    for i, (c, r) in enumerate(cells):
        x, y = iso_pos(c, r, origin_x, origin_y, size)
        roll = rng.random()
        if roll < 0.18:
            continue
        h = 6 + rng.random() * 54
        if roll > 0.92:
            h += 28
        top, left, right = PALETTES[rng.randint(0, len(PALETTES) - 1)]
        delay = (c + r) * 0.12 + rng.random() * 0.4
        dur = 3.2 + rng.random() * 2.4
        op = 0.82 + rng.random() * 0.18
        parts.append(cube(x, y, size, h, top, left, right, op, delay, dur))
        if roll > 0.9:
            parts.append(
                f'<circle cx="{x:.1f}" cy="{y - h - 10:.1f}" r="2.2" fill="#e0f2fe" opacity="0.9">'
                f'<animate attributeName="opacity" values="0.2;1;0.2" dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
                f"</circle>"
            )
    return "\n".join(parts)


def stars(n: int, w: int, h: int) -> str:
    bits = []
    for i in range(n):
        x = rng.random() * w
        y = rng.random() * h * 0.62
        r = 0.4 + rng.random() * 1.3
        dur = 1.8 + rng.random() * 3.5
        delay = rng.random() * 4
        bits.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="#e2e8f0">'
            f'<animate attributeName="opacity" values="0.15;0.95;0.15" dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
            f"</circle>"
        )
    return "\n".join(bits)


def grid_floor(origin_x: float, origin_y: float, cols: int, rows: int, size: float) -> str:
    lines = ['<g opacity="0.35" stroke="#22d3ee" stroke-width="0.6" fill="none">']
    hw, hh = size, size * 0.52
    for r in range(rows + 1):
        x1, y1 = iso_pos(0, r, origin_x, origin_y, size)
        x2, y2 = iso_pos(cols, r, origin_x, origin_y, size)
        lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    for c in range(cols + 1):
        x1, y1 = iso_pos(c, 0, origin_x, origin_y, size)
        x2, y2 = iso_pos(c, rows, origin_x, origin_y, size)
        lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    lines.append("</g>")
    return "\n".join(lines)


HERO = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 520" width="1400" height="520" role="img" aria-label="Claudio Tassis 3D profile banner">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="45%" stop-color="#0b1224"/>
      <stop offset="100%" stop-color="#1e1b4b"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="28%" r="55%">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0.28"/>
      <stop offset="55%" stop-color="#7c3aed" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0"/>
      <stop offset="50%" stop-color="#22d3ee" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/>
    </linearGradient>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
    <clipPath id="frame"><rect width="1400" height="520" rx="28"/></clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="1400" height="520" fill="url(#sky)"/>
    <rect width="1400" height="520" fill="url(#glow)"/>
    {stars(90, 1400, 520)}

    <rect x="0" y="-180" width="1400" height="220" fill="url(#scan)">
      <animateTransform attributeName="transform" type="translate" values="0,-40; 0,620; 0,-40" dur="9s" repeatCount="indefinite"/>
    </rect>

    <!-- camera fly-through: the 3D city slowly dollies like a scroll -->
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="0,24; 0,-86; 0,24" dur="14s" repeatCount="indefinite"/>
      <g>
        <animateTransform attributeName="transform" type="scale"
          values="1; 1.08; 1" dur="14s" additive="sum" repeatCount="indefinite"/>
        {grid_floor(700, 150, 14, 9, 32)}
        {build_city(700, 150, 14, 9, 32)}
      </g>
    </g>

    <rect x="0" y="0" width="1400" height="188" fill="#020617" opacity="0.22"/>
    <rect x="0" y="418" width="1400" height="102" fill="#020617" opacity="0.38"/>

    <text x="700" y="72" text-anchor="middle" font-family="Consolas, 'Courier New', monospace"
      font-size="16" letter-spacing="6" fill="#67e8f9">FULL STACK  ·  EDUCATION  ·  AI</text>
    <text x="700" y="128" text-anchor="middle" font-family="Arial, Helvetica, sans-serif"
      font-size="56" font-weight="700" fill="#f8fafc">CLAUDIO TASSIS</text>
    <text x="700" y="162" text-anchor="middle" font-family="Consolas, 'Courier New', monospace"
      font-size="18" fill="#c4b5fd">Cl4ud10 T4551S  |  Vitoria, ES</text>

    <!-- 3D scroll hint -->
    <g transform="translate(700, 455)">
      <polygon points="0,-18 22,-6 0,6 -22,-6" fill="#22d3ee" opacity="0.95"/>
      <polygon points="-22,-6 0,6 0,22 -22,10" fill="#0e7490"/>
      <polygon points="22,-6 0,6 0,22 22,10" fill="#155e75"/>
      <polyline points="-12,32 0,44 12,32" fill="none" stroke="#e0f2fe" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <animateTransform attributeName="transform" type="translate" values="700,448; 700,468; 700,448" dur="1.8s" repeatCount="indefinite"/>
    </g>
    <text x="700" y="508" text-anchor="middle" font-family="Consolas, 'Courier New', monospace"
      font-size="12" letter-spacing="4" fill="#94a3b8">SCROLL THE 3D WORLD</text>
  </g>
</svg>
'''

SCROLL = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 90" width="1400" height="90">
  <defs>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0"/>
      <stop offset="50%" stop-color="#22d3ee" stop-opacity="1"/>
      <stop offset="100%" stop-color="#a78bfa" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <line x1="80" y1="28" x2="1320" y2="28" stroke="url(#fade)" stroke-width="2"/>
  <g transform="translate(700, 48)">
    <polygon points="0,-14 16,-5 0,5 -16,-5" fill="#67e8f9"/>
    <polygon points="-16,-5 0,5 0,16 -16,7" fill="#0e7490"/>
    <polygon points="16,-5 0,5 0,16 16,7" fill="#155e75"/>
    <animateTransform attributeName="transform" type="translate" values="700,40; 700,58; 700,40" dur="1.6s" repeatCount="indefinite"/>
  </g>
</svg>
'''

# Rebuild city with a dedicated rng so hero and world can differ
rng = random.Random(2026)

WORLD = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 420" width="1400" height="420" role="img" aria-label="3D isometric contribution city">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <radialGradient id="spot" cx="50%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="round"><rect width="1400" height="420" rx="24"/></clipPath>
  </defs>
  <g clip-path="url(#round)">
    <rect width="1400" height="420" fill="url(#bg)"/>
    <rect width="1400" height="420" fill="url(#spot)"/>
    {stars(50, 1400, 420)}
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="40,30; -50,-55; 40,30" dur="16s" repeatCount="indefinite"/>
      {grid_floor(700, 80, 18, 12, 26)}
      {build_city(700, 80, 18, 12, 26)}
    </g>
  </g>
</svg>
'''

(OUT / "hero-3d.svg").write_text(HERO, encoding="utf-8")
(OUT / "scroll-hint.svg").write_text(SCROLL, encoding="utf-8")
(OUT / "world-3d.svg").write_text(WORLD, encoding="utf-8")
print("wrote", [p.name for p in OUT.glob("*.svg")])
print("sizes", {p.name: p.stat().st_size for p in OUT.glob("*.svg")})
