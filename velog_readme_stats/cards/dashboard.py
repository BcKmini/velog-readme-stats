"""Dashboard card — combines multiple sections into a single DIY-composable
card. Pick which sections go in and in what order via `sections`, e.g.
`("summary", "trend", "recent")` or `("summary", "ranking")`.
"""

from ..utils import esc, format_number, wrap_text

LIGHT_OVERRIDES = {
    "void": "#ffffff",
    "text_bright": "#1f2328",
    "text_faint": "#6e7781",
}

WIDTH = 860
PAD = 24
SECTION_GAP = 18

SECTION_TITLES = {
    "summary": "TOTAL STATS",
    "trend": "VIEWS TREND",
    "recent": "RECENT POSTS",
    "ranking": "TOP POSTS",
}

SUMMARY_METRICS = [
    ("total_views", "VIEWS", "synapse_cyan", "view_diff"),
    ("total_likes", "LIKES", "dendrite_violet", "like_diff"),
    ("total_posts", "POSTS", "axon_amber", "post_diff"),
]


def _diff_label(value: int) -> str:
    if value > 0:
        return f"▲ {value:,}"
    if value < 0:
        return f"▼ {abs(value):,}"
    return "– 0"


def _diff_class(value: int) -> str:
    if value > 0:
        return "up"
    if value < 0:
        return "down"
    return "flat"


def _header(title: str, y: float) -> tuple[float, list]:
    parts = [
        f'<text x="{PAD}" y="{y+14}" class="section" font-family="\'JetBrains Mono\', monospace" '
        f'font-size="10" font-weight="700" letter-spacing="2">{esc(title)}</text>',
    ]
    return y + 30, parts


def _render_summary(theme: dict, velog: dict, diff_days: int, y: float) -> tuple[float, list]:
    y, parts = _header(SECTION_TITLES["summary"], y)
    item_w = (WIDTH - PAD * 2) / len(SUMMARY_METRICS)
    for i, (key, label, color_key, diff_key) in enumerate(SUMMARY_METRICS):
        x = PAD + i * item_w + item_w / 2
        color = theme.get(color_key, theme["synapse_cyan"])
        value = format_number(velog.get(key, 0))
        diff = velog.get(diff_key, 0)
        parts.append(
            f'<text x="{x:.1f}" y="{y+26}" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" '
            f'font-size="24" font-weight="700" fill="{color}">{esc(value)}</text>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{y+42}" text-anchor="middle" class="sub" font-family="\'JetBrains Mono\', monospace" '
            f'font-size="9" letter-spacing="1">{esc(label)}</text>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{y+56}" text-anchor="middle" class="{_diff_class(diff)}" '
            f'font-family="\'JetBrains Mono\', monospace" font-size="10">{esc(_diff_label(diff))} / {diff_days}d</text>'
        )
    return y + 68, parts


def _render_trend(theme: dict, history: list, days: int, y: float) -> tuple[float, list]:
    y, parts = _header(SECTION_TITLES["trend"], y)
    points = history[-days:]
    chart_h = 70
    top = y

    if len(points) < 2:
        msg = "No data collected yet." if not points else f"{format_number(points[0].get('total_views', 0))} · needs more days for a trend"
        parts.append(
            f'<text x="{WIDTH/2}" y="{top+chart_h/2+4:.1f}" text-anchor="middle" class="sub" '
            f'font-family="\'JetBrains Mono\', monospace" font-size="11">{esc(msg)}</text>'
        )
        return top + chart_h + 14, parts

    values = [p.get("total_views", 0) for p in points]
    v_min, v_max = min(values), max(values)
    if v_min == v_max:
        v_min -= 1
        v_max += 1

    plot_w = WIDTH - PAD * 2
    n = len(points)

    def px(i):
        return PAD + (i / (n - 1)) * plot_w

    def py(v):
        return top + chart_h - ((v - v_min) / (v_max - v_min)) * chart_h

    coords = [(px(i), py(v)) for i, v in enumerate(values)]
    line_path = "M " + " L ".join(f"{x:.1f} {y_:.1f}" for x, y_ in coords)
    area_path = line_path + f" L {coords[-1][0]:.1f} {top+chart_h:.1f} L {coords[0][0]:.1f} {top+chart_h:.1f} Z"

    parts.append(f'<path d="{area_path}" fill="{theme["synapse_cyan"]}" opacity="0.12"/>')
    parts.append(f'<path d="{line_path}" fill="none" stroke="{theme["synapse_cyan"]}" stroke-width="2"/>')
    parts.append(f'<circle cx="{coords[-1][0]:.1f}" cy="{coords[-1][1]:.1f}" r="3.5" fill="{theme["synapse_cyan"]}"/>')
    parts.append(
        f'<text x="{PAD}" y="{top+chart_h+14:.1f}" class="sub" font-family="\'JetBrains Mono\', monospace" '
        f'font-size="9">{esc(points[0]["date"])}</text>'
    )
    parts.append(
        f'<text x="{WIDTH-PAD}" y="{top+chart_h+14:.1f}" text-anchor="end" class="sub" '
        f'font-family="\'JetBrains Mono\', monospace" font-size="9">{esc(points[-1]["date"])}</text>'
    )
    return top + chart_h + 26, parts


def _render_posts(title_key: str, theme: dict, posts: list, y: float, show_rank: bool) -> tuple[float, list]:
    y, parts = _header(SECTION_TITLES[title_key], y)
    row_h = 26
    if not posts:
        parts.append(
            f'<text x="{PAD}" y="{y+16}" class="sub" font-family="\'JetBrains Mono\', monospace" '
            f'font-size="11">No data yet.</text>'
        )
        return y + 30, parts

    for i, post in enumerate(posts):
        row_y = y + i * row_h + 12
        title = wrap_text(post["title"], 52)
        title = title[0] if title else "(untitled)"
        prefix_x = PAD
        if show_rank:
            parts.append(
                f'<text x="{PAD}" y="{row_y:.1f}" font-family="\'JetBrains Mono\', monospace" '
                f'font-size="11" font-weight="700" fill="{theme["axon_amber"] if i == 0 else theme["text_dim"]}">#{i+1}</text>'
            )
            prefix_x = PAD + 22
        parts.append(
            f'<text x="{prefix_x}" y="{row_y:.1f}" class="row-title" font-family="\'JetBrains Mono\', monospace" '
            f'font-size="11">{esc(title)}</text>'
        )
        parts.append(
            f'<text x="{WIDTH-PAD}" y="{row_y:.1f}" text-anchor="end" class="sub" '
            f'font-family="\'JetBrains Mono\', monospace" font-size="10">'
            f'{format_number(post["views"])} views · {format_number(post["likes"])}♥</text>'
        )
    return y + len(posts) * row_h + 8, parts


SECTION_RENDERERS = {
    "summary": lambda theme, velog, history, diff_days, count, trend_days, y: _render_summary(theme, velog, diff_days, y),
    "trend": lambda theme, velog, history, diff_days, count, trend_days, y: _render_trend(theme, history, trend_days, y),
    "recent": lambda theme, velog, history, diff_days, count, trend_days, y: _render_posts(
        "recent", theme, velog.get("recent_posts", [])[:count], y, show_rank=False
    ),
    "ranking": lambda theme, velog, history, diff_days, count, trend_days, y: _render_posts(
        "ranking", theme, velog.get("top_posts", [])[:count], y, show_rank=True
    ),
}


def generate(
    theme: dict,
    velog: dict,
    history: list = None,
    sections: tuple = ("summary", "trend", "recent"),
    diff_days: int = 7,
    count: int = 3,
    trend_days: int = 30,
) -> str:
    history = history or []
    sections = [s for s in sections if s in SECTION_RENDERERS]
    if not sections:
        sections = ["summary"]

    body_parts: list = []
    y = 30.0
    username = velog.get("username", "")
    body_parts.append(
        f'<text x="{PAD}" y="{y}" class="title" font-family="\'JetBrains Mono\', monospace" '
        f'font-size="16" font-weight="700">📝 Velog Dashboard</text>'
    )
    body_parts.append(
        f'<text x="{WIDTH-PAD}" y="{y}" text-anchor="end" class="sub" font-family="\'JetBrains Mono\', monospace" '
        f'font-size="11">@{esc(username)}</text>'
    )
    y += 20
    body_parts.append(f'<line x1="0" y1="{y}" x2="{WIDTH}" y2="{y}" class="border" stroke-width="1" stroke-opacity="0.15"/>')
    y += 16

    for i, section in enumerate(sections):
        y, section_parts = SECTION_RENDERERS[section](theme, velog, history, diff_days, count, trend_days, y)
        body_parts.extend(section_parts)
        if i < len(sections) - 1:
            y += SECTION_GAP / 2
            body_parts.append(f'<line x1="{PAD}" y1="{y:.1f}" x2="{WIDTH-PAD}" y2="{y:.1f}" class="border" stroke-width="1" stroke-opacity="0.1"/>')
            y += SECTION_GAP / 2

    height = int(y + 20)

    style = f"""<style>
      .bg {{ fill: {theme['void']}; }}
      .border {{ stroke: {theme['synapse_cyan']}; }}
      .title {{ fill: {theme['text_bright']}; }}
      .section {{ fill: {theme['synapse_cyan']}; opacity: 0.85; }}
      .sub {{ fill: {theme['text_faint']}; }}
      .row-title {{ fill: {theme['text_bright']}; }}
      .up {{ fill: #3fb950; }}
      .down {{ fill: #f85149; }}
      .flat {{ fill: {theme['text_faint']}; }}
      @media (prefers-color-scheme: light) {{
        .bg {{ fill: {LIGHT_OVERRIDES['void']}; }}
        .title {{ fill: {LIGHT_OVERRIDES['text_bright']}; }}
        .sub {{ fill: {LIGHT_OVERRIDES['text_faint']}; }}
        .row-title {{ fill: {LIGHT_OVERRIDES['text_bright']}; }}
      }}
    </style>"""

    header = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}">',
        style,
        f'<rect class="bg" width="{WIDTH}" height="{height}" rx="14"/>',
        f'<rect x="1" y="1" width="{WIDTH-2}" height="{height-2}" fill="none" class="border" stroke-width="1" stroke-opacity="0.25" rx="14"/>',
    ]

    return "\n".join(header + body_parts + ["</svg>"])
