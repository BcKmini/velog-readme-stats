"""Tests for the SVG card templates."""

from velog_readme_stats.cards import ranking, recent, summary, trend


def test_summary_returns_svg(theme, sample_velog_stats):
    svg = summary.generate(theme, sample_velog_stats)
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_summary_contains_values(theme, sample_velog_stats):
    svg = summary.generate(theme, sample_velog_stats)
    assert "12.3k" in svg  # format_number(12345)
    assert "testvelog" in svg


def test_summary_handles_zero_diff(theme, sample_velog_stats):
    stats = {**sample_velog_stats, "post_diff": 0}
    svg = summary.generate(theme, stats)
    assert "– 0" in svg


def test_ranking_returns_svg(theme, sample_velog_stats):
    svg = ranking.generate(theme, sample_velog_stats["top_posts"])
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_ranking_contains_titles(theme, sample_velog_stats):
    svg = ranking.generate(theme, sample_velog_stats["top_posts"])
    assert "Most popular post" in svg


def test_ranking_empty_posts(theme):
    svg = ranking.generate(theme, [])
    assert "<svg" in svg
    assert "No data yet." in svg


def test_recent_returns_svg(theme, sample_velog_stats):
    svg = recent.generate(theme, sample_velog_stats["recent_posts"])
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_recent_contains_titles(theme, sample_velog_stats):
    svg = recent.generate(theme, sample_velog_stats["recent_posts"])
    assert "Latest post" in svg


def test_recent_empty_posts(theme):
    svg = recent.generate(theme, [])
    assert "<svg" in svg
    assert "No data yet." in svg


def test_trend_returns_svg(theme, sample_velog_history):
    svg = trend.generate(theme, sample_velog_history)
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_trend_no_history(theme):
    svg = trend.generate(theme, [])
    assert "<svg" in svg
    assert "No data collected yet." in svg


def test_trend_single_point(theme):
    svg = trend.generate(theme, [{"date": "2026-01-01", "total_views": 100}])
    assert "<svg" in svg
    assert "more days are collected" in svg


def test_card_custom_theme_color(sample_velog_stats):
    custom = {"void": "#000000", "nebula": "#111111", "synapse_cyan": "#123456",
              "dendrite_violet": "#abcabc", "axon_amber": "#654321",
              "text_bright": "#fff", "text_dim": "#ccc", "text_faint": "#999"}
    svg = summary.generate(custom, sample_velog_stats)
    assert "#123456" in svg
