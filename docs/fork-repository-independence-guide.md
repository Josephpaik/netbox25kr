# Fork 저장소 독립 운영 가이드

> 원본 저장소(netbox-community/netbox)와 분리하여 독립적으로 GitHub Actions를 운영하는 방법

## 목차

1. [현재 상황 분석](#1-현재-상황-분석)
2. [독립 운영을 위한 변경 방법](#2-독립-운영을-위한-변경-방법)
3. [워크플로우별 수정 가이드](#3-워크플로우별-수정-가이드)
4. [필요한 Secrets 설정](#4-필요한-secrets-설정)
5. [수정 시 주의사항](#5-수정-시-주의사항)
6. [업스트림 동기화 전략](#6-업스트림-동기화-전략)

---

## 1. 현재 상황 분석

### 1.1 왜 일부 워크플로우가 실행되지 않는가?

원본 저장소(netbox-community/netbox)의 워크플로우에는 **저장소 확인 조건**이 포함되어 있습니다:

```yaml
jobs:
  some-job:
    if: github.repository == 'netbox-community/netbox'
```

이 조건은 Fork된 저장소에서 **의도치 않은 동작을 방지**하기 위한 것입니다:
- 원본 저장소의 이슈/PR 관리 정책이 Fork에 적용되는 것 방지
- 원본 저장소 전용 자동화가 Fork에서 실행되는 것 방지

### 1.2 현재 워크플로우 상태

| 워크플로우 파일 | 목적 | 조건문 | Fork에서 상태 |
|----------------|------|--------|--------------|
| `ci.yml` | CI/CD 테스트 | 없음 | ✅ 정상 실행 |
| `codeql.yml` | 보안 분석 | 없음 | ✅ 정상 실행 |
| `close-stale-issues.yml` | 오래된 이슈 닫기 | 있음 | ⏭️ Skipped |
| `lock-threads.yml` | 스레드 잠금 | 있음 | ⏭️ Skipped |
| `close-incomplete-issues.yml` | 불완전 이슈 닫기 | 있음 | ⏭️ Skipped |
| `update-translation-strings.yml` | 번역 업데이트 | 있음 | ⏭️ Skipped |

---

## 2. 독립 운영을 위한 변경 방법

### 2.1 방법 1: 조건문 완전 제거 (권장)

가장 간단한 방법입니다. `if` 조건을 삭제합니다.

**변경 전:**
```yaml
jobs:
  stale:
    if: github.repository == 'netbox-community/netbox'
    runs-on: ubuntu-latest
```

**변경 후:**
```yaml
jobs:
  stale:
    runs-on: ubuntu-latest
```

### 2.2 방법 2: 자신의 저장소로 조건 변경

저장소 이름을 본인 것으로 변경합니다.

**변경 전:**
```yaml
if: github.repository == 'netbox-community/netbox'
```

**변경 후:**
```yaml
if: github.repository == 'Josephpaik/netbox25kr'
```

### 2.3 방법 3: 환경 변수 활용 (유연한 방법)

저장소 변수를 사용하여 유연하게 관리합니다.

```yaml
jobs:
  stale:
    # ENABLE_AUTOMATION 변수가 'true'일 때만 실행
    if: vars.ENABLE_AUTOMATION == 'true'
    runs-on: ubuntu-latest
```

**설정 방법:**
1. 저장소 → Settings → Secrets and variables → Actions
2. Variables 탭 클릭
3. "New repository variable" 클릭
4. Name: `ENABLE_AUTOMATION`, Value: `true`

---

## 3. 워크플로우별 수정 가이드

### 3.1 close-stale-issues.yml

**파일 위치:** `.github/workflows/close-stale-issues.yml`

**목적:** 90일 이상 활동 없는 이슈를 자동으로 닫음

**수정 내용:**
```yaml
# 수정 전 (16-17줄)
jobs:
  stale:
    if: github.repository == 'netbox-community/netbox'
    runs-on: ubuntu-latest

# 수정 후
jobs:
  stale:
    runs-on: ubuntu-latest
```

**고려사항:**
- 이 워크플로우가 필요한가요? Fork 저장소에서 이슈 관리가 필요하다면 활성화
- 일수(days-before-stale)를 프로젝트에 맞게 조정 권장

---

### 3.2 lock-threads.yml

**파일 위치:** `.github/workflows/lock-threads.yml`

**목적:** 오래된 이슈/PR/토론 스레드를 잠금

**수정 내용:**
```yaml
# 수정 전 (15-16줄)
jobs:
  lock:
    if: github.repository == 'netbox-community/netbox'
    runs-on: ubuntu-latest

# 수정 후
jobs:
  lock:
    runs-on: ubuntu-latest
```

**고려사항:**
- 커뮤니티 규모가 작다면 불필요할 수 있음
- 비활성화하려면 파일 삭제 또는 이름 변경 (예: `lock-threads.yml.disabled`)

---

### 3.3 close-incomplete-issues.yml

**파일 위치:** `.github/workflows/close-incomplete-issues.yml`

**목적:** 정보가 부족한 이슈를 자동으로 닫음

**수정 내용:**
```yaml
# 수정 전 (14-15줄)
jobs:
  stale:
    if: github.repository == 'netbox-community/netbox'
    runs-on: ubuntu-latest

# 수정 후
jobs:
  stale:
    runs-on: ubuntu-latest
```

**고려사항:**
- `status: revisions needed` 라벨이 있는 이슈에만 적용됨
- 이 라벨을 사용하지 않는다면 이 워크플로우는 무의미

---

### 3.4 update-translation-strings.yml

**파일 위치:** `.github/workflows/update-translation-strings.yml`

**목적:** 번역 문자열을 자동으로 업데이트

**수정 내용:**
```yaml
# 수정 전 (16-17줄)
jobs:
  makemessages:
    if: github.repository == 'netbox-community/netbox'
    runs-on: ubuntu-latest

# 수정 후
jobs:
  makemessages:
    runs-on: ubuntu-latest
```

**추가 필요 사항 - Secret 설정:**

이 워크플로우는 `HOUSEKEEPING_SECRET_KEY` Secret이 필요합니다.

**옵션 A: GitHub App 토큰 사용 (원본과 동일)**
1. GitHub App 생성 필요
2. Private Key를 Secret으로 저장
3. `app-id` 값 변경 필요

**옵션 B: Personal Access Token 사용 (더 간단)**

워크플로우를 수정:
```yaml
jobs:
  makemessages:
    runs-on: ubuntu-latest
    steps:
    - name: Check out repo
      uses: actions/checkout@v4
      with:
        token: ${{ secrets.PAT_TOKEN }}  # Personal Access Token 사용
```

Secret 설정:
1. GitHub → Settings → Developer settings → Personal access tokens
2. "Generate new token (classic)" 선택
3. `repo` 권한 선택
4. 생성된 토큰을 저장소 Secret으로 추가 (이름: `PAT_TOKEN`)

---

## 4. 필요한 Secrets 설정

### 4.1 전체 Secrets 목록

| Secret 이름 | 사용 워크플로우 | 필수 여부 | 설명 |
|------------|----------------|----------|------|
| `NETBOX_DB_PASSWORD` | ci.yml | ✅ 필수 | PostgreSQL 비밀번호 |
| `HOUSEKEEPING_SECRET_KEY` | update-translation-strings.yml | 선택 | GitHub App Private Key |
| `PAT_TOKEN` | update-translation-strings.yml | 선택 | Personal Access Token (대안) |

### 4.2 Secret 설정 방법

1. 저장소 페이지로 이동
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret** 클릭
4. Name과 Value 입력 후 저장

```
저장소
  └── Settings
        └── Secrets and variables
              └── Actions
                    └── New repository secret
                          ├── Name: NETBOX_DB_PASSWORD
                          └── Value: [비밀번호 입력]
```

### 4.3 ci.yml을 위한 DB 비밀번호 설정

CI 테스트용이므로 복잡한 비밀번호가 필요 없습니다:

```
Name: NETBOX_DB_PASSWORD
Value: testpassword123
```

---

## 5. 수정 시 주의사항

### 5.1 하지 말아야 할 것

```yaml
# ❌ 잘못된 예 - 하드코딩된 토큰
env:
  GITHUB_TOKEN: ghp_xxxxxxxxxxxx

# ❌ 잘못된 예 - 실제 비밀번호 노출
env:
  DB_PASSWORD: "my-real-password"
```

### 5.2 해야 할 것

```yaml
# ✅ 올바른 예 - Secret 사용
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

### 5.3 워크플로우 비활성화 방법

특정 워크플로우가 필요 없다면:

**방법 1: 파일 삭제**
```bash
rm .github/workflows/lock-threads.yml
```

**방법 2: 파일 이름 변경**
```bash
mv .github/workflows/lock-threads.yml .github/workflows/lock-threads.yml.disabled
```

**방법 3: GitHub UI에서 비활성화**
1. Actions 탭 → 워크플로우 선택
2. 우측 상단 "..." 메뉴 → "Disable workflow"

---

## 6. 업스트림 동기화 전략

### 6.1 문제점

원본 저장소(upstream)에서 변경 사항을 가져올 때 워크플로우 파일도 덮어쓰여질 수 있습니다.

### 6.2 권장 전략

**전략 A: 워크플로우 변경사항 별도 관리**

```bash
# 1. 업스트림 추가
git remote add upstream https://github.com/netbox-community/netbox.git

# 2. 업스트림 변경사항 가져오기
git fetch upstream

# 3. 머지 (워크플로우 제외)
git merge upstream/main --no-commit

# 4. 워크플로우 변경사항 되돌리기
git checkout HEAD -- .github/workflows/

# 5. 커밋
git commit -m "Merge upstream changes (excluding workflow modifications)"
```

**전략 B: .gitattributes 활용**

`.gitattributes` 파일 생성:
```
.github/workflows/*.yml merge=ours
```

이렇게 하면 머지 시 워크플로우 파일은 현재 브랜치 것을 유지합니다.

### 6.3 동기화 스크립트 예시

```bash
#!/bin/bash
# scripts/sync-upstream.sh

set -e

echo "=== Fetching upstream ==="
git fetch upstream

echo "=== Creating backup of workflows ==="
cp -r .github/workflows .github/workflows.backup

echo "=== Merging upstream/main ==="
git merge upstream/main --no-commit || true

echo "=== Restoring our workflows ==="
rm -rf .github/workflows
mv .github/workflows.backup .github/workflows

echo "=== Committing ==="
git add .
git commit -m "Sync with upstream (preserved local workflows)"

echo "=== Done ==="
```

---

## 빠른 시작 체크리스트

Fork 저장소를 독립적으로 운영하려면:

- [ ] **1단계:** `NETBOX_DB_PASSWORD` Secret 설정
- [ ] **2단계:** 필요한 워크플로우의 `if` 조건 제거
- [ ] **3단계:** 불필요한 워크플로우 비활성화/삭제
- [ ] **4단계:** (선택) 번역 자동화용 `PAT_TOKEN` 설정
- [ ] **5단계:** Actions 탭에서 워크플로우 실행 확인

---

## 요약: 최소 변경으로 독립 운영하기

**즉시 실행 가능하게 하려면:**

1. `close-stale-issues.yml` 17줄의 `if:` 줄 삭제
2. `lock-threads.yml` 16줄의 `if:` 줄 삭제
3. `close-incomplete-issues.yml` 15줄의 `if:` 줄 삭제
4. `update-translation-strings.yml` 17줄의 `if:` 줄 삭제 + Secret 설정

**또는 간단히:**

필요 없는 워크플로우라면 해당 파일을 삭제하세요. CI와 CodeQL만으로도 충분할 수 있습니다.

---

*이 가이드에 대한 질문이나 개선 제안이 있으면 이슈를 열어주세요.*
