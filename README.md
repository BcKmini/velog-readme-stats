# velog-readme-stats

[![CI](https://github.com/BcKmini/velog-readme-stats/actions/workflows/ci.yml/badge.svg)](https://github.com/BcKmini/velog-readme-stats/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

[Velog](https://velog.io) 통계(전체 조회수, 좋아요, 인기글 랭킹, 최근 게시글, 조회수 추이, 포스팅 활동 히트맵)를 예쁘 **SVG 카드**로 만들어 GitHub 프로필 README나 Pinned 레포에 바로 넣을 수 있게 해주는 도구입니다.

[github-profile-trophy](https://github.com/ryo-ma/github-profile-trophy)에서 영감을 받았지만, Velog에 맞게 다르게 설계했습니다. Velog 조회수/좋아요 데이터는 작성자 본인에게만 공개되는 비공개 데이터라 공개 API가 없기 때문에, 이 도구는 **여러분 자신의 GitHub Actions에서, 여러분 자신의 인증 정보로 실행되는 GitHub Action**으로 배포됩니다. 데이터와 토큰이 여러분의 Actions 러너 밖으로 나가는 일이 없습니다.

<p align="center">
  <img src="demo/velog-summary.svg" width="90%" alt="요약 카드 예시" />
</p>
<p align="center">
  <img src="demo/velog-recent.svg" width="90%" alt="최근 게시글 카드 예시" />
</p>
<p align="center">
  <img src="demo/velog-ranking.svg" width="90%" alt="랭킹 카드 예시" />
</p>
<p align="center">
  <img src="demo/velog-trend.svg" width="90%" alt="추이 카드 예시" />
</p>
<p align="center">
  <img src="demo/velog-heatmap.svg" width="60%" alt="활동 히트맵 카드 예시" />
</p>
<p align="center">
  <img src="demo/velog-badge.svg" alt="인라인 배지 카드 예시" />
</p>

*(샘플 데이터, `ember` 테마 적용)*

## 기능

- **카드 6종, 원하는 조합만 선택**: `summary`, `trend`, `ranking`, `recent`, `heatmap`, `badge`
- **내장 테마 12종**: `midnight`(기본), `ember`, `forest`, `rose`, `mono`, `ocean`, `sunset`, `lavender`, `cyberpunk`, `sakura`, `arctic`, `coffee` — 색상 개별 오버라이드도 가능
- **다크/라이트 모드 자동 대응** (`prefers-color-scheme`), 별도 설정 불필요
- **DB도 외부 서비스도 없음** — 여러분 레포에 커밋되는 작은 JSON 스냅샷 파일로 추이를 계산
- **전부 여러분의 GitHub Actions 안에서 실행** — Velog 쿠키는 여러분 레포의 시크릿에만 존재
- **GitHub Action**(`uses: BcKmini/velog-readme-stats@main`)으로도, **독립 CLI**(`python -m velog_readme_stats.cli`)로도 사용 가능

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

### 4. README에 카드 넣기

```markdown
![Velog summary](https://raw.githubusercontent.com/<본인아이디>/<본인아이디>/main/assets/velog/velog-summary.svg)
![Velog recent posts](https://raw.githubusercontent.com/<본인아이디>/<본인아이디>/main/assets/velog/velog-recent.svg)
```

Actions 탭에서 *Update Velog Stats* 워크플로우를 한 번 수동 실행(workflow_dispatch)하면 첫 SVG들이 생성됩니다.

## 설정값 레퍼런스

`velog_username`, `access_token`, `refresh_token`을 제외한 나머지는 전부 선택 사항입니다.

| 입력값          | 기본값                             | 설명                                                        |
| -------------- | --------------------------------- | -------------------------------------------------------------------- |
| `velog_username` | —                                | Velog 아이디 (`velog.io/@아이디`의 `@` 뒷부분)                |
| `access_token`   | —                                | Velog `access_token` 쿠키 (시크릿으로 저장)                     |
| `refresh_token`  | —                                | Velog `refresh_token` 쿠키 (시크릿으로 저장)                    |
| `cards`          | `summary,trend,recent`           | `summary`, `trend`, `ranking`, `recent`, `heatmap`, `badge` 중 콤마로 구분해서 선택   |
| `theme`          | `midnight`                       | `midnight`, `ember`, `forest`, `rose`, `mono`, `ocean`, `sunset`, `lavender`, `cyberpunk`, `sakura`, `arctic`, `coffee` |
| `output_dir`     | `assets/velog`                   | SVG(와 히스토리 JSON)를 쓸 디렉토리                       |
| `history_path`   | `<output_dir>/velog-history.json`| 추이 히스토리 파일 경로 직접 지정                            |
| `trend_days`     | `30`                              | 추이 카드에 보여줄 히스토리 일수                             |
| `diff_days`      | `7`                               | 요약 카드의 증감을 며칠 전 대비로 계산할지                     |
| `count`          | `5`                               | 랭킹/최근 게시글 카드에 보여줄 게시글 수                             |
| `weeks`          | `20`                              | 활동 히트맵 카드에 보여줄 주(week) 수                             |

## 카드 종류

| 카드      | 내용                                                            |
| --------- | -------------------------------------------------------------------------- |
| `summary` | 전체 조회수/좋아요/게시글 수 + N일 증감                     |
| `trend`   | 최근 N일 전체 조회수 영역+라인 차트                       |
| `ranking` | 조회수 기준 인기글 Top N                                               |
| `recent`  | 작성일 기준 최근 게시글 N개                                     |
| `heatmap` | 최근 N주 포스팅 활동을 GitHub 컸트리붸션 그래프 스타일로 표시              |
| `badge`   | 다른 shields.io 배지 옷에 나란히 넣기 좋은 한 줄짜리 컴팩트 카드            |

## GitHub Actions 없이 사용하기

핵심 로직은 순수 Python 패키지라, 로컬이나 다른 CI에서도 그대로 돌릴 수 있습니다:

```bash
pip install -r requirements.txt
export VELOG_ACCESS_TOKEN=...
export VELOG_REFRESH_TOKEN=...
python -m velog_readme_stats.cli --username your-velog-id --cards summary,trend,recent,ranking,heatmap,badge --theme forest
```

## 왜 github-profile-trophy처럼 호스팅된 서비스가 아닌가요?

`github-profile-trophy`가 URL 하나로 동작할 수 있는 이유는 GitHub의 컸트리붸션 통계가 공개 데이터이기 때문입니다. Velog의 조회수/좋아요는 **작성자 본인에게만 공개**되고, Velog 자체에 공개 통계 API가 없습니다. 이 데이터를 가져오려면 작성자 본인의 세션 쿠키가 필요한데, 이걸 공용 호스팅 서비스에 보내는 건 공 인증 정보를 제3자에게 넘기는 셀입니다. 이 도구를 여러분 자신의 레포의 GitHub Actions로 실행하면 그 문제가 아예 발생하지 않습니다 — 아무것도 여러분의 Actions 러너 밖으로 나가지 않습니다.

## 기여하기

이슈와 PR을 환영합니다 — 새 테마, 새 카드 종류, 버그 리포트 모두 좋습니다. PR 올리기 전에 `pip install -r requirements-dev.txt && pytest`를 실행해주세요.

## 라이선스

[Apache License 2.0](LICENSE)
