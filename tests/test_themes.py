"""Tests for theme resolution."""

from velog_readme_stats.themes import THEMES, resolve_theme


def test_resolve_theme_by_name():
    assert resolve_theme("ember") == THEMES["ember"]


def test_resolve_theme_unknown_name_falls_back_to_default():
    assert resolve_theme("does-not-exist") == THEMES["midnight"]


def test_resolve_theme_dict_overrides_default():
    theme = resolve_theme({"synapse_cyan": "#123456"})
    assert theme["synapse_cyan"] == "#123456"
    assert theme["void"] == THEMES["midnight"]["void"]


def test_all_themes_have_required_keys():
    required = {"void", "nebula", "synapse_cyan", "dendrite_violet", "axon_amber", "text_bright", "text_dim", "text_faint"}
    for name, theme in THEMES.items():
        assert required.issubset(theme.keys()), f"theme '{name}' missing keys"
