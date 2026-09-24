#!/usr/bin/env python3
"""Generate the anime "episode title card" SVGs used as section headers.

Run from the repo root:  python3 scripts/gen_cards.py
Regenerate whenever you rename a section or want new colours.
"""
from pathlib import Path

# Tokyo Night palette
BG0, BG1, LINE, MUTED, FG = "#1a1b26", "#1f2335", "#292e42", "#565f89", "#c0caf5"

CARDS = [
    # file, accent, episode, JP title, EN title, CN title
    ("ep01", "#7aa2f7", "01", "自己紹介", "ABOUT ME", "关于我"),
    ("ep02", "#bb9af7", "02", "装備", "TECH STACK", "装备栏"),
    ("ep03", "#e0af68", "03", "代表作", "FEATURED WORKS", "代表作"),
    ("ep04", "#9ece6a", "04", "進行中", "NOW HACKING ON", "正在折腾"),
    ("ep05", "#7dcfff", "05", "最新記事", "LATEST POSTS", "博客"),
    ("ep06", "#f7768e", "06", "戦績", "STATS", "战绩"),
    ("ep07", "#ff9e64", "07", "今日の一言", "ANIME QUOTE OF THE DAY", "今日一言"),
]

W, H = 880, 72
JP_FONT = ("'Noto Sans JP','Noto Sans CJK JP','Hiragino Sans','Yu Gothic UI',"
           "'Microsoft YaHei','PingFang SC','Noto Sans SC',sans-serif")
MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,monospace"

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Episode {ep}: {en}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{BG1}"/>
      <stop offset="1" stop-color="{BG0}"/>
    </linearGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{accent}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{accent}" fill-opacity="0.10"/>
    </pattern>
    <clipPath id="clip"><rect width="{W}" height="{H}" rx="12"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect x="480" width="400" height="{H}" fill="url(#dots)"/>
    <!-- episode block -->
    <rect width="104" height="{H}" fill="{accent}" fill-opacity="0.12"/>
    <rect width="5" height="{H}" fill="{accent}"/>
    <text x="22" y="28" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{accent}" fill-opacity="0.85">EPISODE</text>
    <text x="21" y="58" font-family="{MONO}" font-size="30" font-weight="700" fill="{accent}">{ep}</text>
    <!-- titles -->
    <text x="126" y="36" font-family="{JP}" font-size="25" font-weight="700" fill="{FG}">{jp}</text>
    <text x="127" y="58" font-family="{MONO}" font-size="12" letter-spacing="3.5" fill="{accent}">{en}</text>
    <text x="852" y="45" text-anchor="end" font-family="{JP}" font-size="17" fill="{MUTED}">{cn}</text>
    <!-- accent hairline along the bottom -->
    <rect x="104" y="{H1}" width="{WL}" height="1" fill="url(#fade)"/>
  </g>
  <rect x="0.5" y="0.5" width="{W1}" height="{H1}" rx="12" fill="none" stroke="{LINE}"/>
</svg>
"""

out = Path(__file__).resolve().parent.parent / "assets"
out.mkdir(exist_ok=True)
for name, accent, ep, jp, en, cn in CARDS:
    svg = TEMPLATE.format(W=W, H=H, W1=W - 1, H1=H - 1, WL=W - 104, ep=ep, jp=jp, en=en, cn=cn,
                          accent=accent, BG0=BG0, BG1=BG1, LINE=LINE, MUTED=MUTED, FG=FG,
                          JP=JP_FONT, MONO=MONO)
    (out / f"{name}.svg").write_text(svg, encoding="utf-8")
    print("wrote", out / f"{name}.svg")
