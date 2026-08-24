"""Tests for pure helper functions in api.py (no network involved)."""

from velog_readme_stats.api import _daily_activity


def test_daily_activity_counts_by_date():
    posts = [
        {"released_at": "2026-01-01T10:00:00.000Z"},
        {"released_at": "2026-01-01T18:00:00.000Z"},
        {"released_at": "2026-01-03T09:00:00.000Z"},
    ]
    assert _daily_activity(posts) == {"2026-01-01": 2, "2026-01-03": 1}


def test_daily_activity_ignores_missing_dates():
    posts = [{"released_at": ""}, {"released_at": None}, {}]
    assert _daily_activity(posts) == {}


def test_daily_activity_empty_list():
    assert _daily_activity([]) == {}
