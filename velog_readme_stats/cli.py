"""CLI entry point: python -m velog_readme_stats.cli --username ..."""

import argparse
import logging
import os
import sys

from .api import VelogClient, VelogError
from .cards import badge, dashboard, heatmap, ranking, recent, summary, trend
from .history import diff_from_days_ago, update_history
from .themes import THEMES, resolve_theme

logger = logging.getLogger(__name__)

CARD_NAMES = ("summary", "trend", "ranking", "recent", "heatmap", "badge", "dashboard")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Velog stats SVG cards.")
    parser.add_argument("--username", required=True, help="Velog username (the part after @ in velog.io/@username)")
    parser.add_argument("--access-token", default=None, help="Velog access_token cookie (defaults to $VELOG_ACCESS_TOKEN)")
    parser.add_argument("--refresh-token", default=None, help="Velog refresh_token cookie (defaults to $VELOG_REFRESH_TOKEN)")
    parser.add_argument(
        "--cards",
        default="summary,trend,recent",
        help=f"Comma-separated list of cards to generate. Available: {', '.join(CARD_NAMES)}",
    )
    parser.add_argument(
        "--theme",
        default="midnight",
        help=f"Built-in theme name ({', '.join(THEMES)}) or leave default and override later",
    )
    parser.add_argument("--output-dir", default="assets/velog", help="Directory to write SVGs into")
    parser.add_argument("--history-path", default=None, help="Path to the trend history JSON (default: <output-dir>/velog-history.json)")
    parser.add_argument("--trend-days", type=int, default=30, help="How many days of history the trend card shows")
    parser.add_argument("--diff-days", type=int, default=7, help="How many days back the summary card's delta is computed against")
    parser.add_argument("--count", type=int, default=5, help="Number of posts shown in the ranking/recent cards")
    parser.add_argument("--weeks", type=int, default=20, help="Number of weeks shown on the heatmap card")
    parser.add_argument(
        "--sections",
        default="summary,trend,recent",
        help="Comma-separated sections to stack inside the 'dashboard' card, in order. Available: summary, trend, ranking, recent",
    )
    return parser


def run(args) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    theme = resolve_theme(args.theme)
    history_path = args.history_path or os.path.join(args.output_dir, "velog-history.json")
    requested_cards = [c.strip() for c in args.cards.split(",") if c.strip()]

    unknown = [c for c in requested_cards if c not in CARD_NAMES]
    if unknown:
        logger.error("Unknown card(s): %s. Available: %s", ", ".join(unknown), ", ".join(CARD_NAMES))
        sys.exit(1)

    client = VelogClient(args.username, args.access_token, args.refresh_token)
    logger.info("Fetching Velog stats for @%s...", args.username)
    stats = client.fetch_user_stats(count=args.count)
    logger.info(
        "Fetched %d posts, %d total views, %d total likes",
        stats["total_posts"], stats["total_views"], stats["total_likes"],
    )

    history = update_history(history_path, stats)
    stats["view_diff"] = diff_from_days_ago(history, args.diff_days, "total_views")
    stats["like_diff"] = diff_from_days_ago(history, args.diff_days, "total_likes")
    stats["post_diff"] = diff_from_days_ago(history, args.diff_days, "total_posts")

    os.makedirs(args.output_dir, exist_ok=True)

    renderers = {
        "summary": lambda: summary.generate(theme, stats, diff_days=args.diff_days),
        "trend": lambda: trend.generate(theme, history, days=args.trend_days),
        "ranking": lambda: ranking.generate(theme, stats["top_posts"]),
        "recent": lambda: recent.generate(theme, stats["recent_posts"]),
        "heatmap": lambda: heatmap.generate(theme, stats.get("activity", {}), weeks=args.weeks),
        "badge": lambda: badge.generate(theme, stats),
        "dashboard": lambda: dashboard.generate(
            theme, stats, history,
            sections=tuple(s.strip() for s in args.sections.split(",") if s.strip()),
            diff_days=args.diff_days, count=args.count, trend_days=args.trend_days,
        ),
    }

    for card in requested_cards:
        svg = renderers[card]()
        path = os.path.join(args.output_dir, f"velog-{card}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        logger.info("Wrote %s", path)


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        run(args)
    except VelogError as e:
        logger.error("Velog API error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
