"""Compact single-line badge — a small pill you can drop inline (e.g. next
to other shields.io badges) instead of a full card.
"""

from ..utils import format_number, esc

LIGHT_OVERRIDES = {
    "void": "#ffffff",
    "text_bright": "#1f2328",
}

HEIGHT = 40
PAD_X = 16


def generate(theme: dict, velog: dict) -> str:
    text = (
        f"\U0001F4DD {format_number(velog.get('total_views', 0))} views · "
        f"{format_number(velog.get('total_likes', 0))}♥ · "
        f"{velog.get('total_posts', 0)} posts"
    )
    # rough monospace width estimate so the pill hugs the text
    width = PAD_X * 2 + int(len(text) * 7.3)

    style = f"""<style>
      .bg {{ fill: {theme['void']}; }}
      .border {{ stroke: {theme['synapse_cyan']}; }}
      .text {{ fill: {theme['text_bright']}; }}
      @media (prefers-color-scheme: light) {{
        .bg {{ fill: {LIGHT_OVERRIDES['void']}; }}
        .text {{ fill: {LIGHT_OVERRIDES['text_bright']}; }}
      }}
    </style>"""

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{HEIGHT}" viewBox="0 0 {width} {HEIGHT}">',
        style,
        f'<rect class="bg" width="{width}" height="{HEIGHT}" rx="{HEIGHT/2:.0f}"/>',
        f'<rect x="1" y="1" width="{width-2}" height="{HEIGHT-2}" fill="none" class="border" stroke-width="1" stroke-opacity="0.4" rx="{HEIGHT/2-1:.0f}"/>',
        f'<text x="{width/2:.1f}" y="{HEIGHT/2+5:.1f}" text-anchor="middle" class="text" '
        f'font-family="\'JetBrains Mono\', monospace" font-size="13" font-weight="600">{esc(text)}</text>',
        "</svg>",
    ]
    return "\n".join(parts)
