"""Tests for the SVG card templates."""

from velog_readme_stats.cards import badge, dashboard, heatmap, ranking, recent, summary, trend


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


def test_badge_returns_svg(theme, sample_velog_stats):
    svg = badge.generate(theme, sample_velog_stats)
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_badge_contains_values(theme, sample_velog_stats):
    svg = badge.generate(theme, sample_velog_stats)
    assert "12.3k" in svg
    assert "18" in svg  # total_posts


def test_heatmap_returns_svg(theme):
    svg = heatmap.generate(theme, {"2026-01-01": 2, "2026-01-15": 1})
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_heatmap_empty_activity(theme):
    svg = heatmap.generate(theme, {})
    assert "<svg" in svg
    assert "0 posts" in svg


def test_heatmap_reflects_activity_tooltip(theme):
    from datetime import date, timedelta

    recent_day = (date.today() - timedelta(days=3)).isoformat()
    svg = heatmap.generate(theme, {recent_day: 3})
    assert "3 posts" in svg


def test_dashboard_returns_svg(theme, sample_velog_stats, sample_velog_history):
    svg = dashboard.generate(theme, sample_velog_stats, sample_velog_history)
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg


def test_dashboard_default_sections_present(theme, sample_velog_stats, sample_velog_history):
    svg = dashboard.generate(theme, sample_velog_stats, sample_velog_history)
    assert "TOTAL STATS" in svg
    assert "VIEWS TREND" in svg
    assert "RECENT POSTS" in svg


def test_dashboard_custom_sections(theme, sample_velog_stats, sample_velog_history):
    svg = dashboard.generate(theme, sample_velog_stats, sample_velog_history, sections=("summary", "ranking"))
    assert "TOTAL STATS" in svg
    assert "TOP POSTS" in svg
    assert "VIEWS TREND" not in svg
    assert "RECENT POSTS" not in svg


def test_dashboard_falls_back_to_summary_when_no_valid_sections(theme, sample_velog_stats):
    svg = dashboard.generate(theme, sample_velog_stats, [], sections=("nonsense",))
    assert "TOTAL STATS" in svg


def test_dashboard_empty_history_trend_section(theme, sample_velog_stats):
    svg = dashboard.generate(theme, sample_velog_stats, [], sections=("trend",))
    assert "No data collected yet." in svg


def test_dashboard_username_shown(theme, sample_velog_stats, sample_velog_history):
    svg = dashboard.generate(theme, sample_velog_stats, sample_velog_history)
    assert "testvelog" in svg


def test_card_custom_theme_color(sample_velog_stats):
    custom = {"void": "#000000", "nebula": "#111111", "synapse_cyan": "#123456",
              "dendrite_violet": "#abcabc", "axon_amber": "#654321",
              "text_bright": "#fff", "text_dim": "#ccc", "text_faint": "#999"}
    svg = summary.generate(custom, sample_velog_stats)
    assert "#123456" in svg
