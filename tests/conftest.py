"""Shared pytest fixtures."""

import pytest

from velog_readme_stats.themes import THEMES

SAMPLE_VELOG_STATS = {
    "username": "testvelog",
    "total_views": 12345,
    "total_likes": 234,
    "total_posts": 18,
    "view_diff": 456,
    "like_diff": -3,
    "post_diff": 0,
    "top_posts": [
        {"title": "Most popular post", "url_slug": "popular-post", "released_at": "2026-01-01", "views": 5000, "likes": 100},
        {"title": "Second most popular", "url_slug": "second-post", "released_at": "2026-01-05", "views": 3000, "likes": 60},
    ],
    "recent_posts": [
        {"title": "Latest post", "url_slug": "latest-post", "released_at": "2026-01-15", "views": 800, "likes": 20},
        {"title": "Prior post", "url_slug": "prior-post", "released_at": "2026-01-05", "views": 3000, "likes": 60},
    ],
}

SAMPLE_VELOG_HISTORY = [
    {"date": "2026-01-01", "total_views": 10000, "total_likes": 200, "total_posts": 17},
    {"date": "2026-01-08", "total_views": 11200, "total_likes": 215, "total_posts": 17},
    {"date": "2026-01-15", "total_views": 12345, "total_likes": 234, "total_posts": 18},
]


@pytest.fixture
def theme():
    return THEMES["midnight"]


@pytest.fixture
def sample_velog_stats():
    return SAMPLE_VELOG_STATS


@pytest.fixture
def sample_velog_history():
    return SAMPLE_VELOG_HISTORY
