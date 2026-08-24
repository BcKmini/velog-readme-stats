# velog-readme-stats

[![CI](https://github.com/BcKmini/velog-readme-stats/actions/workflows/ci.yml/badge.svg)](https://github.com/BcKmini/velog-readme-stats/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

Generate beautiful, customizable **SVG cards from your [Velog](https://velog.io) stats** — total views, likes, post ranking, recent posts, and a views trend chart — and drop them straight into your GitHub profile README or any pinned repo.

Inspired by [github-profile-trophy](https://github.com/ryo-ma/github-profile-trophy), but built for Velog: since Velog stats are private to the author (there's no public API for them), this ships as a **GitHub Action you run in your own repo with your own credentials** — your data and tokens never leave your GitHub Actions runner.

<p align="center">
  <img src="demo/velog-summary.svg" width="90%" alt="summary card demo" />
</p>
<p align="center">
  <img src="demo/velog-recent.svg" width="90%" alt="recent posts card demo" />
</p>
<p align="center">
  <img src="demo/velog-ranking.svg" width="90%" alt="ranking card demo" />
</p>
<p align="center">
  <img src="demo/velog-trend.svg" width="90%" alt="trend card demo" />
</p>

*(sample data — themed with the `ember` preset)*

## Features

- **4 cards, pick any combination**: `summary`, `trend`, `ranking`, `recent`
- **5 built-in themes**: `midnight` (default), `ember`, `forest`, `rose`, `mono` — or override any color
- **Automatic light/dark mode** via `prefers-color-scheme`, no extra config
- **No database, no external service** — a small JSON snapshot file (committed to your own repo) tracks history for the trend card
- **Runs entirely in your GitHub Actions** — your Velog cookies stay in your repo's secrets, never sent anywhere else
- Usable as a **GitHub Action** (`uses: BcKmini/velog-readme-stats@main`) or as a **standalone CLI** (`python -m velog_readme_stats.cli`)

## Quick start

### 1. Get your Velog tokens

1. Log into [velog.io](https://velog.io)
2. Open DevTools → Application → Cookies → `velog.io`
3. Copy the `access_token` and `refresh_token` values

### 2. Add them as repository secrets

In your profile repo (the one named exactly like your GitHub username), go to **Settings → Secrets and variables → Actions** and add:

- `VELOG_ACCESS_TOKEN`
- `VELOG_REFRESH_TOKEN`

### 3. Add the workflow

Copy [`examples/workflow.yml`](examples/workflow.yml) into `.github/workflows/velog-stats.yml` in your repo, and set `velog_username` to your Velog id:

```yaml
name: Update Velog Stats

on:
  schedule:
    - cron: "0 */6 * * *"
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - uses: BcKmini/velog-readme-stats@main
        with:
          velog_username: your-velog-id
          access_token: ${{ secrets.VELOG_ACCESS_TOKEN }}
          refresh_token: ${{ secrets.VELOG_REFRESH_TOKEN }}
          cards: summary,trend,recent
          theme: midnight

      - name: Commit changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add assets/velog
          if ! git diff --staged --quiet; then
            git commit -m "chore: update velog stats"
            git push
          fi
```

### 4. Embed the cards in your README

```markdown
![Velog summary](https://raw.githubusercontent.com/<you>/<you>/main/assets/velog/velog-summary.svg)
![Velog recent posts](https://raw.githubusercontent.com/<you>/<you>/main/assets/velog/velog-recent.svg)
```

Run the workflow once manually (Actions tab → *Update Velog Stats* → *Run workflow*) to generate the first set of SVGs.

## Configuration reference

All inputs are optional except `velog_username`, `access_token`, and `refresh_token`.

| Input          | Default                          | Description                                                        |
| -------------- | --------------------------------- | -------------------------------------------------------------------- |
| `velog_username` | —                                | Your Velog id (the part after `@` in `velog.io/@id`)                |
| `access_token`   | —                                | Velog `access_token` cookie (store as a secret)                     |
| `refresh_token`  | —                                | Velog `refresh_token` cookie (store as a secret)                    |
| `cards`          | `summary,trend,recent`           | Comma-separated list from `summary`, `trend`, `ranking`, `recent`   |
| `theme`          | `midnight`                       | `midnight`, `ember`, `forest`, `rose`, `mono`                       |
| `output_dir`     | `assets/velog`                   | Where the SVGs (and history JSON) get written                       |
| `history_path`   | `<output_dir>/velog-history.json`| Override the trend history file location                            |
| `trend_days`     | `30`                              | Days of history shown on the trend card                             |
| `diff_days`      | `7`                               | How many days back the summary card's delta is computed against     |
| `count`          | `5`                               | Posts shown on the ranking/recent cards                             |

## Cards

| Card      | What it shows                                                            |
| --------- | -------------------------------------------------------------------------- |
| `summary` | Total views / likes / posts, each with an N-day delta                     |
| `trend`   | Area+line chart of total views over the last N days                       |
| `ranking` | Top N posts sorted by views                                               |
| `recent`  | Latest N posts sorted by release date                                     |

## Using it without GitHub Actions

The core is a plain Python package, so you can run it locally or from any CI:

```bash
pip install -r requirements.txt
export VELOG_ACCESS_TOKEN=...
export VELOG_REFRESH_TOKEN=...
python -m velog_readme_stats.cli --username your-velog-id --cards summary,trend,recent,ranking --theme forest
```

## Why not a hosted service, like github-profile-trophy?

`github-profile-trophy` can be a single hosted URL because GitHub's contribution stats are public. Velog view/like counts are **only visible to the post author** — Velog itself has no public stats API. Getting them requires the author's own session cookies, so a shared hosted endpoint would mean sending your credentials to a third party. Running this as a GitHub Action in your own repo avoids that entirely: nothing ever leaves your own Actions runner.

## Contributing

Issues and PRs are welcome — new themes, new card types, and bug reports all count. Run `pip install -r requirements-dev.txt && pytest` before opening a PR.

## License

[Apache License 2.0](LICENSE)
