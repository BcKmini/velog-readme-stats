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
    "ocean": {
        "void": "#061219",
        "nebula": "#0a1e29",
        "synapse_cyan": "#22d3ee",
        "dendrite_violet": "#38bdf8",
        "axon_amber": "#5eead4",
        "text_bright": "#ecfeff",
        "text_dim": "#7dd3fc",
        "text_faint": "#4a7a8c",
    },
    "sunset": {
        "void": "#160a14",
        "nebula": "#231029",
        "synapse_cyan": "#fb923c",
        "dendrite_violet": "#e879f9",
        "axon_amber": "#facc15",
        "text_bright": "#fff7ed",
        "text_dim": "#fdba74",
        "text_faint": "#8a5a6b",
    },
    "lavender": {
        "void": "#100c1a",
        "nebula": "#1a1428",
        "synapse_cyan": "#c084fc",
        "dendrite_violet": "#818cf8",
        "axon_amber": "#f0abfc",
        "text_bright": "#f5f3ff",
        "text_dim": "#c4b5fd",
        "text_faint": "#6b6091",
    },
    "cyberpunk": {
        "void": "#08060f",
        "nebula": "#120a24",
        "synapse_cyan": "#00f5d4",
        "dendrite_violet": "#ff2fb0",
        "axon_amber": "#fee440",
        "text_bright": "#f0f9ff",
        "text_dim": "#a5f3fc",
        "text_faint": "#6b6b8f",
    },
    "sakura": {
        "void": "#160f12",
        "nebula": "#221419",
        "synapse_cyan": "#ffb7c5",
        "dendrite_violet": "#ff8fab",
        "axon_amber": "#ffe4ec",
        "text_bright": "#fff0f3",
        "text_dim": "#ffc2d1",
        "text_faint": "#8f6b73",
    },
    "arctic": {
        "void": "#0a0f14",
        "nebula": "#101922",
        "synapse_cyan": "#7dd3fc",
        "dendrite_violet": "#bae6fd",
        "axon_amber": "#e0f2fe",
        "text_bright": "#f0f9ff",
        "text_dim": "#a5c8de",
        "text_faint": "#5a7a8c",
    },
    "coffee": {
        "void": "#140f0b",
        "nebula": "#1e1712",
        "synapse_cyan": "#d4a373",
        "dendrite_violet": "#e9c46a",
        "axon_amber": "#bc6c25",
        "text_bright": "#faedcd",
        "text_dim": "#e0c9a6",
        "text_faint": "#8a7358",
    },
}

DEFAULT_THEME_NAME = "midnight"


def resolve_theme(theme) -> dict:
    """Accepts a theme name (str) or a full/partial override dict."""
    if isinstance(theme, dict):
        base = THEMES[DEFAULT_THEME_NAME]
        return {**base, **theme}
    return THEMES.get(theme, THEMES[DEFAULT_THEME_NAME])
