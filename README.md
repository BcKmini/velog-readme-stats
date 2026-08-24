# velog-readme-stats

[![CI](https://github.com/BcKmini/velog-readme-stats/actions/workflows/ci.yml/badge.svg)](https://github.com/BcKmini/velog-readme-stats/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

[Velog](https://velog.io) 블로그 통계를 예쁘 **SVG 카드**로 만들어 GitHub 프로필 README, Pinned 레포, 어디든 바로 넣을 수 있게 해주는 도구입니다.

전체 조회수/좋아요/게시글 수 요약, 조회수 추이 그래프, 인기글 랭킹, 최근 게시글, 포스팅 활동 히트맵, 인라인 배지, 그리고 이 모든 걸 한 장으로 합친 대시보드 카드까지 — **카드 7종 × 테마 12종**을 조합해서 내 프로필에 딜 맞는 조합을 골라 쓸 수 있습니다.

velog.io는 조회수/좋아요 데이터를 작성자 본인에게만 공개하고 공개 API를 제공하지 않기 때문에, 이 도구는 **여러분 자신의 GitHub Actions에서, 여러분 자신의 Velog 인증 정보로** 돌아갑니다. 데이터와 토큰이 여러분의 레포 밖으로 나가지 않습니다.

---

## 카드 갤러리

### 📝 요약 (summary)

전체 조회수·좋아요·게시글 수와 N일 전 대비 증감을 한눈에.

<p align="center"><img src="demo/velog-summary.svg" width="90%" alt="summary card" /></p>

### 📈 조회수 추이 (trend)

최근 N일간 전체 조회수 변화를 영역+라인 차트로.

<p align="center"><img src="demo/velog-trend.svg" width="90%" alt="trend card" /></p>

### 🏆 인기글 랭킹 (ranking)

조회수 기준 Top N 게시글을 막대그래프와 함께.

<p align="center"><img src="demo/velog-ranking.svg" width="90%" alt="ranking card" /></p>

### 🕒 최근 게시글 (recent)

작성일 기준 가장 최근 게시글 N개.

<p align="center"><img src="demo/velog-recent.svg" width="90%" alt="recent card" /></p>

### 🔥 포스팅 활동 히트맵 (heatmap)

최근 N주간 포스팅 활동을 GitHub 컸트리붸션 그래프 스타일로.

<p align="center"><img src="demo/velog-heatmap.svg" width="55%" alt="heatmap card" /></p>

### 🏷️ 인라인 배지 (badge)

다른 shields.io 배지들 옷에 나란히 놓기 좋은 한 줄짜리 컴팩트 카드.

<p align="center"><img src="demo/velog-badge.svg" alt="badge card" /></p>

### 🧩 대시보드 (dashboard) — 여러 카드를 하나로 합치기

요약·추이·랭킹·최근 게시글을 **원하는 순서로 골라서** 한 장의 카드에 합칠 수 있습니다. 카드 하나만 관리하고 싶을 때, 혹은 README 공간을 아끼고 싶을 때 유용합니다.

<p align="center"><img src="demo/velog-dashboard.svg" width="90%" alt="dashboard card (summary + trend + recent)" /></p>

```bash
# 예: 요약 + 랭킹만, 이 순서로
--sections summary,ranking

# 예: 요약 + 추이 + 최근글 + 랭킹, 풀 버전
--sections summary,trend,recent,ranking
```

---

## 테마 갤러리

전부 다크/라이트 모드를 자동으로 지원합니다. 위 카드 예시는 `ember` 테마로 그렸고, 아래는 12개 테마 전부를 같은 데이터로 비교한 모습입니다.

| 테마 | 미리보기 |
| --- | --- |
| `midnight` (기본) | <img src="demo/themes/midnight.svg" width="420" alt="midnight theme" /> |
| `ember` | <img src="demo/themes/ember.svg" width="420" alt="ember theme" /> |
| `forest` | <img src="demo/themes/forest.svg" width="420" alt="forest theme" /> |
| `rose` | <img src="demo/themes/rose.svg" width="420" alt="rose theme" /> |
| `mono` | <img src="demo/themes/mono.svg" width="420" alt="mono theme" /> |
| `ocean` | <img src="demo/themes/ocean.svg" width="420" alt="ocean theme" /> |
| `sunset` | <img src="demo/themes/sunset.svg" width="420" alt="sunset theme" /> |
| `lavender` | <img src="demo/themes/lavender.svg" width="420" alt="lavender theme" /> |
| `cyberpunk` | <img src="demo/themes/cyberpunk.svg" width="420" alt="cyberpunk theme" /> |
| `sakura` | <img src="demo/themes/sakura.svg" width="420" alt="sakura theme" /> |
| `arctic` | <img src="demo/themes/arctic.svg" width="420" alt="arctic theme" /> |
| `coffee` | <img src="demo/themes/coffee.svg" width="420" alt="coffee theme" /> |

마음에 드는 테마가 없다면 색상 키(`void`, `nebula`, `synapse_cyan`, `dendrite_violet`, `axon_amber`, `text_bright`, `text_dim`, `text_faint`)를 직접 오버라이드해서 나만의 팔레트를 만들 수도 있습니다 (CLI로 직접 코드를 호출하는 경우; 자세한 내용은 아래 "GitHub Actions 없이 사용하기" 참고).

---

## 기능 요약

- **카드 7종**: `summary`, `trend`, `ranking`, `recent`, `heatmap`, `badge`, `dashboard`
- **테마 12종**: `midnight`, `ember`, `forest`, `rose`, `mono`, `ocean`, `sunset`, `lavender`, `cyberpunk`, `sakura`, `arctic`, `coffee`
- **DIY 대시보드**: `dashboard` 카드는 어떤 섬션을 어떤 순서로 넣을지 자유롭게 조합 가능
- **다크/라이트 모드 자동 대응** (`prefers-color-scheme`), 별도 설정 불필요
- **DB도 외부 서비스도 없음** — 여러분 레포에 커밋되는 작은 JSON 스냅샷 파일로 추이/증감을 계산
- **전부 여러분의 GitHub Actions 안에서 실행** — Velog 쿠키는 여러분 레포의 시크릿에만 존재
- **GitHub Action**(`uses: BcKmini/velog-readme-stats@main`)으로도, **독립 CLI**(`python -m velog_readme_stats.cli`)로도 사용 가능

---

## 빠르게 시작하기

### 1. Velog 토큰 발급받기

1. [velog.io](https://velog.io) 로그인
2. 개발자도구 → Application → Cookies → `velog.io`
3. `access_token`, `refresh_token` 값 복사

### 2. 리포지토리 시크릿으로 등록

프로필 레포(GitHub 아이디와 이름이 같은 그 레포)의 **Settings → Secrets and variables → Actions**에서 아래 두 개를 등록하세요:

- `VELOG_ACCESS_TOKEN`
- `VELOG_REFRESH_TOKEN`

### 3. 워크플로우 추가

[`examples/workflow.yml`](examples/workflow.yml) 내용을 여러분 레포의 `.github/workflows/velog-stats.yml`로 복사하고, `velog_username`을 본인 Velog 아이디로 바꿔주세요:

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
          cards: summary,trend,recent,heatmap
          theme: ember

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

카드 하나로 합치고 싶다면 `cards: dashboard`와 `sections: summary,trend,recent,ranking`을 대신 사용하세요.

### 4. README에 카드 넣기

```markdown
![Velog summary](https://raw.githubusercontent.com/<본인아이디>/<본인아이디>/main/assets/velog/velog-summary.svg)
![Velog recent posts](https://raw.githubusercontent.com/<본인아이디>/<본인아이디>/main/assets/velog/velog-recent.svg)
```

Actions 탭에서 *Update Velog Stats* 워크플로우를 한 번 수동 실행(workflow_dispatch)하면 첫 SVG들이 생성됩니다.

---

## 설정값 레퍼런스

`velog_username`, `access_token`, `refresh_token`을 제외한 나머지는 전부 선택 사항입니다.

| 입력값 | 기본값 | 설명 |
| --- | --- | --- |
| `velog_username` | — | Velog 아이디 (`velog.io/@아이디`의 `@` 뒷부분) |
| `access_token` | — | Velog `access_token` 쿠키 (시크릿으로 저장) |
| `refresh_token` | — | Velog `refresh_token` 쿠키 (시크릿으로 저장) |
| `cards` | `summary,trend,recent` | `summary`, `trend`, `ranking`, `recent`, `heatmap`, `badge`, `dashboard` 중 콤마로 구분해서 선택 |
| `theme` | `midnight` | `midnight`, `ember`, `forest`, `rose`, `mono`, `ocean`, `sunset`, `lavender`, `cyberpunk`, `sakura`, `arctic`, `coffee` |
| `output_dir` | `assets/velog` | SVG(와 히스토리 JSON)를 쓸 디렉토리 |
| `history_path` | `<output_dir>/velog-history.json` | 추이 히스토리 파일 경로 직접 지정 |
| `trend_days` | `30` | 추이 카드에 보여줄 히스토리 일수 |
| `diff_days` | `7` | 요약 카드의 증감을 며칠 전 대비로 계산할지 |
| `count` | `5` | 랭킹/최근 게시글 카드에 보여줄 게시글 수 (dashboard 안에서는 3개 정도가 보기 좋습니다) |
| `weeks` | `20` | 활동 히트맵 카드에 보여줄 주(week) 수 |
| `sections` | `summary,trend,recent` | `dashboard` 카드에 어떤 섬션을 어떤 순서로 넣을지 (`summary`, `trend`, `ranking`, `recent`) |

## 카드 종류

| 카드 | 내용 |
| --- | --- |
| `summary` | 전체 조회수/좋아요/게시글 수 + N일 증감 |
| `trend` | 최근 N일 전체 조회수 영역+라인 차트 |
| `ranking` | 조회수 기준 인기글 Top N |
| `recent` | 작성일 기준 최근 게시글 N개 |
| `heatmap` | 최근 N주 포스팅 활동을 GitHub 컸트리붸션 그래프 스타일로 표시 |
| `badge` | 다른 shields.io 배지 옷에 나란히 넣기 좋은 한 줄짜리 컴팩트 카드 |
| `dashboard` | `summary`/`trend`/`ranking`/`recent`를 원하는 조합·순서로 합친 카드 |

---

## GitHub Actions 없이 사용하기

핵심 로직은 순수 Python 패키지라, 로컬이나 다른 CI에서도 그대로 돌릴 수 있습니다:

```bash
pip install -r requirements.txt
export VELOG_ACCESS_TOKEN=...
export VELOG_REFRESH_TOKEN=...
python -m velog_readme_stats.cli \
  --username your-velog-id \
  --cards summary,trend,recent,ranking,heatmap,badge,dashboard \
  --theme forest \
  --sections summary,trend,ranking
```

Python 코드에서 직접 호출해서 색상을 완전히 커스텀마이즈할 수도 있습니다:

```python
from velog_readme_stats.cards import summary
from velog_readme_stats.themes import resolve_theme

my_theme = resolve_theme({
    "synapse_cyan": "#ff0055",
    "dendrite_violet": "#00e0ff",
    "axon_amber": "#ffe600",
})

svg = summary.generate(my_theme, velog_stats_dict)
```

---

## 기여하기

이슈와 PR을 환영합니다 — 새 테마, 새 카드 종류, 버그 리포트 모두 좋습니다. PR 올리기 전에 `pip install -r requirements-dev.txt && pytest`를 실행해주세요.

## 라이선스

[Apache License 2.0](LICENSE)
