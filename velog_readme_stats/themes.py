"""Built-in color themes for the generated cards.

Pick one with `--theme <name>`, or pass a full override dict programmatically.
Every theme provides the same set of dark-mode keys; each card also defines
its own light-mode palette for `prefers-color-scheme: light`.
"""

THEMES = {
    "midnight": {
        "void": "#080c14",
        "nebula": "#0f1623",
        "synapse_cyan": "#00d4ff",
        "dendrite_violet": "#a78bfa",
        "axon_amber": "#ffb020",
        "text_bright": "#f1f5f9",
        "text_dim": "#94a3b8",
        "text_faint": "#64748b",
    },
    "ember": {
        "void": "#0D1117",
        "nebula": "#130800",
        "synapse_cyan": "#FF4500",
        "dendrite_violet": "#FF8C00",
        "axon_amber": "#8B0000",
        "text_bright": "#ffffff",
        "text_dim": "#d4a0a0",
        "text_faint": "#8b6060",
    },
    "forest": {
        "void": "#0a120d",
        "nebula": "#0f1a13",
        "synapse_cyan": "#34d399",
        "dendrite_violet": "#a3e635",
        "axon_amber": "#facc15",
        "text_bright": "#ecfdf5",
        "text_dim": "#86efac",
        "text_faint": "#4d7c62",
    },
    "rose": {
        "void": "#120a0f",
        "nebula": "#1a0f16",
        "synapse_cyan": "#fb7185",
        "dendrite_violet": "#f472b6",
        "axon_amber": "#fbbf24",
        "text_bright": "#fff1f2",
        "text_dim": "#fda4af",
        "text_faint": "#8b5a63",
    },
    "mono": {
        "void": "#0d0d0d",
        "nebula": "#161616",
        "synapse_cyan": "#e5e5e5",
        "dendrite_violet": "#a3a3a3",
        "axon_amber": "#737373",
        "text_bright": "#fafafa",
        "text_dim": "#a3a3a3",
        "text_faint": "#737373",
    },
}

DEFAULT_THEME_NAME = "midnight"


def resolve_theme(theme) -> dict:
    """Accepts a theme name (str) or a full/partial override dict."""
    if isinstance(theme, dict):
        base = THEMES[DEFAULT_THEME_NAME]
        return {**base, **theme}
    return THEMES.get(theme, THEMES[DEFAULT_THEME_NAME])
