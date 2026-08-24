"""Posting-activity heatmap card — a GitHub-contribution-style grid built
from each post's release date.
"""

from datetime import date, timedelta

from ..utils import esc

LIGHT_OVERRIDES = {
    "void": "#ffffff",
    "text_bright": "#1f2328",
    "text_faint": "#6e7781",
}

CELL = 13
GAP = 3
PAD = 24
HEADER_H = 40
LEGEND_H = 26
OPACITY_STEPS = (0.08, 0.35, 0.55, 0.75, 1.0)


def generate(theme: dict, activity: dict, weeks: int = 20) -> str:
    today = date.today()
    end = today
    start = end - timedelta(days=weeks * 7 - 1)
    start -= timedelta(days=(start.weekday() + 1) % 7)  # roll back to the preceding Sunday

    total_cols = ((end - start).days // 7) + 1
    width = PAD * 2 + total_cols * (CELL + GAP)
    height = HEADER_H + 7 * (CELL + GAP) + LEGEND_H

    max_count = max(activity.values(), default=0) or 1
    total_posts_in_range = sum(c for d, c in activity.items() if start.isoformat() <= d <= end.isoformat())

    style = f"""<style>
      .bg {{ fill: {theme['void']}; }}
      .border {{ stroke: {theme['synapse_cyan']}; }}
      .title {{ fill: {theme['text_bright']}; }}
      .sub {{ fill: {theme['text_faint']}; }}
      @media (prefers-color-scheme: light) {{
        .bg {{ fill: {LIGHT_OVERRIDES['void']}; }}
        .title {{ fill: {LIGHT_OVERRIDES['text_bright']}; }}
        .sub {{ fill: {LIGHT_OVERRIDES['text_faint']}; }}
      }}
    </style>"""

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        style,
        f'<rect class="bg" width="{width}" height="{height}" rx="12"/>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" fill="none" class="border" stroke-width="1" stroke-opacity="0.25" rx="12"/>',
        f'<text x="{PAD}" y="26" class="title" font-family="\'JetBrains Mono\', monospace" font-size="14" font-weight="700">Posting Activity — {total_posts_in_range} posts / {weeks*7}d</text>',
    ]

    d = start
    col = 0
    while d <= end:
        for row in range(7):
            day = d + timedelta(days=row)
            if day > end:
                break
            count = activity.get(day.isoformat(), 0)
            level = 0 if count == 0 else min(4, 1 + int((count / max_count) * 3))
            opacity = OPACITY_STEPS[level]
            x = PAD + col * (CELL + GAP)
            y = HEADER_H + row * (CELL + GAP)
            title = f"{day.isoformat()}: {count} post{'s' if count != 1 else ''}"
            parts.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{theme["synapse_cyan"]}" opacity="{opacity:.2f}"><title>{esc(title)}</title></rect>'
            )
        d += timedelta(days=7)
        col += 1

    legend_y = HEADER_H + 7 * (CELL + GAP) + 16
    legend_x = width - PAD - len(OPACITY_STEPS) * (CELL + GAP) - 40
    parts.append(
        f'<text x="{legend_x - 8}" y="{legend_y+10}" text-anchor="end" class="sub" '
        f'font-family="\'JetBrains Mono\', monospace" font-size="10">Less</text>'
    )
    for i, opacity in enumerate(OPACITY_STEPS):
        x = legend_x + i * (CELL + GAP)
        parts.append(f'<rect x="{x}" y="{legend_y}" width="{CELL}" height="{CELL}" rx="2" fill="{theme["synapse_cyan"]}" opacity="{opacity:.2f}"/>')
    parts.append(
        f'<text x="{legend_x + len(OPACITY_STEPS)*(CELL+GAP) + 6}" y="{legend_y+10}" class="sub" '
        f'font-family="\'JetBrains Mono\', monospace" font-size="10">More</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts)
