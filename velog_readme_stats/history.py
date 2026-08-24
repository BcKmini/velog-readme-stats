"""Local JSON snapshot history for Velog stats.

There's no database — daily snapshots are appended to a small JSON file
that the consumer's own workflow commits alongside the generated SVGs.
That's enough history to draw a trend chart and compute N-day deltas
without any external storage.
"""

import json
import os
from datetime import date

MAX_HISTORY_DAYS = 90


def load_history(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def update_history(path: str, stats: dict, today: str = None) -> list[dict]:
    """Add (or overwrite) today's snapshot and persist it. Returns full history."""
    today = today or date.today().isoformat()

    history = load_history(path)
    history = [h for h in history if h["date"] != today]
    history.append(
        {
            "date": today,
            "total_views": stats["total_views"],
            "total_likes": stats["total_likes"],
            "total_posts": stats["total_posts"],
        }
    )
    history.sort(key=lambda h: h["date"])
    history = history[-MAX_HISTORY_DAYS:]

    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    return history


def diff_from_days_ago(history: list[dict], days: int, key: str) -> int:
    """Difference between the latest value and the value `days` ago (or the
    oldest point available, whichever is closer)."""
    if len(history) < 2:
        return 0
    latest = history[-1][key]
    idx = max(len(history) - 1 - days, 0)
    baseline = history[idx][key]
    return latest - baseline
