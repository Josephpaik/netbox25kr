# GitHub Actions 완벽 가이드

> 초보 개발자를 위한 단계별 튜토리얼

## 목차

1. [GitHub Actions란?](#1-github-actions란)
2. [기본 개념 이해하기](#2-기본-개념-이해하기)
3. [워크플로우 파일 구조](#3-워크플로우-파일-구조)
4. [실패(Failure)가 발생하는 주요 원인](#4-실패failure가-발생하는-주요-원인)
5. [실패 디버깅 방법](#5-실패-디버깅-방법)
6. [이 프로젝트의 워크플로우 이해하기](#6-이-프로젝트의-워크플로우-이해하기)
7. [모범 사례](#7-모범-사례)
8. [자주 묻는 질문 (FAQ)](#8-자주-묻는-질문-faq)

---

## 1. GitHub Actions란?

GitHub Actions는 GitHub에서 제공하는 **CI/CD(지속적 통합/지속적 배포)** 자동화 도구입니다.

### 쉽게 이해하기

집에서 매일 아침 일어나면 하는 루틴이 있다고 생각해보세요:
1. 알람이 울리면 (트리거)
2. 일어나서 세수하고 (작업 1)
3. 아침밥 먹고 (작업 2)
4. 출근 준비를 합니다 (작업 3)

GitHub Actions도 마찬가지입니다:
1. 코드를 push하면 (트리거)
2. 코드 스타일 검사하고 (작업 1)
3. 테스트를 실행하고 (작업 2)
4. 빌드를 확인합니다 (작업 3)

### 왜 필요한가?

```
개발자 A: 코드 작성 완료! push했어요!
GitHub Actions: 잠깐! 테스트 실패했어요. 수정해주세요.
개발자 A: 아차, 고마워! (버그 수정)
```

수동으로 매번 테스트하고 검사하는 것은 실수할 수 있고 시간도 많이 걸립니다.
GitHub Actions가 자동으로 해주면 실수를 줄이고 시간도 절약됩니다.

---

## 2. 기본 개념 이해하기

### 핵심 용어 정리

| 용어 | 설명 | 비유 |
|------|------|------|
| **Workflow** | 자동화된 전체 프로세스 | 요리 레시피 전체 |
| **Event** | 워크플로우를 시작시키는 트리거 | "주문이 들어왔다!" |
| **Job** | 같은 환경에서 실행되는 작업 묶음 | 요리 한 접시 만들기 |
| **Step** | Job 안의 개별 작업 | 재료 썰기, 볶기 등 |
| **Action** | 재사용 가능한 작업 단위 | 미리 만들어둔 소스 |
| **Runner** | 워크플로우를 실행하는 서버 | 요리하는 주방 |

### 시각적으로 이해하기

```
[Event: push 발생]
        |
        v
+------------------+
|    Workflow      |
|  (ci.yml 파일)   |
+------------------+
        |
        v
+------------------+     +------------------+
|      Job 1       |     |      Job 2       |
|  (Python 테스트) |     | (Node.js 빌드)   |
+------------------+     +------------------+
   |    |    |              |    |    |
   v    v    v              v    v    v
Step1 Step2 Step3       Step1 Step2 Step3
```

---

## 3. 워크플로우 파일 구조

워크플로우 파일은 `.github/workflows/` 폴더에 `.yml` 또는 `.yaml` 확장자로 저장됩니다.

### 기본 구조 설명

```yaml
# 파일 위치: .github/workflows/example.yml

# 1. 워크플로우 이름 (GitHub UI에 표시됨)
name: My First Workflow

# 2. 언제 실행할지 (트리거)
on:
  push:                    # push할 때
    branches: [main]       # main 브랜치에만
  pull_request:           # PR이 열릴 때
    branches: [main]

# 3. 권한 설정 (중요!)
permissions:
  contents: read          # 코드 읽기 권한만

# 4. 실행할 작업들
jobs:
  # Job 이름 (원하는대로 지정)
  build:
    # 어떤 환경에서 실행할지
    runs-on: ubuntu-latest

    # 이 Job의 단계들
    steps:
      # Step 1: 코드 체크아웃
      - name: 코드 가져오기
        uses: actions/checkout@v4

      # Step 2: 커맨드 실행
      - name: Hello 출력
        run: echo "Hello, World!"
```

### 각 섹션 상세 설명

#### 3.1 `name` - 워크플로우 이름

```yaml
name: CI
```
- GitHub Actions 탭에서 보이는 이름입니다
- 알아보기 쉽게 지으세요

#### 3.2 `on` - 트리거 이벤트

**자주 사용하는 트리거들:**

```yaml
on:
  # 1. push할 때
  push:
    branches: [main, develop]      # 특정 브랜치만
    paths:                         # 특정 파일이 변경될 때만
      - 'src/**'
      - '*.py'
    paths-ignore:                  # 특정 파일 제외
      - 'docs/**'
      - '*.md'

  # 2. PR이 열릴 때
  pull_request:
    branches: [main]
    types: [opened, synchronize]   # 열리거나 업데이트될 때

  # 3. 수동 실행
  workflow_dispatch:               # "Run workflow" 버튼 활성화

  # 4. 정해진 시간에 (크론)
  schedule:
    - cron: '0 9 * * *'           # 매일 오전 9시 (UTC)
```

**크론 표현식 이해하기:**

```
* * * * *
| | | | |
| | | | +-- 요일 (0-6, 일요일=0)
| | | +---- 월 (1-12)
| | +------ 일 (1-31)
| +-------- 시 (0-23)
+---------- 분 (0-59)

예시:
'0 9 * * *'     = 매일 09:00 UTC
'0 0 * * 0'     = 매주 일요일 00:00 UTC
'30 4 1 * *'    = 매월 1일 04:30 UTC
```

#### 3.3 `permissions` - 권한 설정

```yaml
permissions:
  contents: read       # 저장소 내용 읽기
  issues: write        # 이슈 작성/수정
  pull-requests: write # PR 작성/수정
  actions: write       # Actions 관련 작업
```

**중요**: 최소 권한 원칙을 따르세요. 필요한 권한만 부여합니다.

#### 3.4 `jobs` - 작업 정의

```yaml
jobs:
  # Job ID (영문, 숫자, -, _ 사용 가능)
  test:
    runs-on: ubuntu-latest    # 실행 환경

    # 다른 Job이 끝난 후 실행 (의존성)
    needs: [build]

    # 조건부 실행
    if: github.event_name == 'push'

    # 환경 변수
    env:
      NODE_ENV: test

    steps:
      - name: Step 이름
        run: npm test
```

#### 3.5 `steps` - 단계 정의

**Action 사용하기 (`uses`):**

```yaml
steps:
  # 공식 Action 사용
  - name: Checkout code
    uses: actions/checkout@v4

  # 다른 저장소의 Action 사용
  - name: Setup Python
    uses: actions/setup-python@v5
    with:                        # Action에 전달할 입력값
      python-version: '3.11'

  # Action 버전 지정 방법
  uses: actions/checkout@v4                    # 태그 (권장)
  uses: actions/checkout@main                  # 브랜치
  uses: actions/checkout@a5ac7e51b41094c92402 # 커밋 해시 (가장 안전)
```

**명령어 실행하기 (`run`):**

```yaml
steps:
  # 단일 명령어
  - name: 단일 명령어
    run: echo "Hello"

  # 여러 명령어
  - name: 여러 명령어
    run: |
      echo "Line 1"
      echo "Line 2"
      npm install
      npm test

  # 작업 디렉토리 지정
  - name: 특정 폴더에서 실행
    run: npm install
    working-directory: ./frontend
```

---

## 4. 실패(Failure)가 발생하는 주요 원인

### 4.1 Secrets 미설정 또는 잘못된 설정

**문제 상황:**
```yaml
env:
  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}  # Secret이 없으면 빈 값
```

**증상:**
- 환경 변수가 비어있어 연결 실패
- "Authentication failed" 에러

**해결 방법:**
1. GitHub 저장소 → Settings → Secrets and variables → Actions
2. 필요한 Secret 추가
3. Secret 이름이 워크플로우에서 사용하는 이름과 일치하는지 확인

```
[저장소] → Settings → Secrets and variables → Actions
                                               → New repository secret
                                               → Name: DB_PASSWORD
                                               → Value: 실제 비밀번호
```

### 4.2 조건문(`if`) 때문에 Job이 건너뛰어짐

**문제 상황:**
```yaml
jobs:
  deploy:
    if: github.repository == 'original-owner/original-repo'
```

Fork한 저장소에서는 `github.repository`가 다르므로 이 Job은 **절대 실행되지 않습니다**.

**증상:**
- Job이 "Skipped"로 표시됨
- 아무 에러 없이 그냥 넘어감

**해결 방법:**
- Fork 저장소용 조건 추가 또는
- 조건 제거/수정

```yaml
# 수정 전
if: github.repository == 'netbox-community/netbox'

# 수정 후 (자신의 저장소에서도 실행)
if: github.repository == 'netbox-community/netbox' || github.repository == 'your-username/netbox'

# 또는 조건 완전 제거
# if: ... (삭제)
```

### 4.3 서비스 컨테이너 시작 실패

**문제 상황:**
```yaml
services:
  postgres:
    image: postgres:15
    env:
      POSTGRES_PASSWORD: ${{ secrets.DB_PASSWORD }}  # 빈 값이면 실패
```

**증상:**
- "Container exited with code 1"
- Database 연결 실패

**해결 방법:**

```yaml
services:
  postgres:
    image: postgres:15
    env:
      # 테스트용이면 하드코딩도 괜찮음
      POSTGRES_USER: testuser
      POSTGRES_PASSWORD: testpass  # 또는 secrets 사용
      POSTGRES_DB: testdb
    options: >-
      --health-cmd="pg_isready -U testuser"
      --health-interval=10s
      --health-timeout=5s
      --health-retries=5
```

### 4.4 캐시 미스 또는 의존성 설치 실패

**문제 상황:**
```yaml
- name: Install dependencies
  run: pip install -r requirements.txt
```

**증상:**
- 네트워크 타임아웃
- 패키지 버전 충돌
- "Could not find a version that satisfies the requirement"

**해결 방법:**

```yaml
# 캐시 활용
- name: Cache pip packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

# 재시도 로직 추가
- name: Install dependencies with retry
  run: |
    for i in 1 2 3; do
      pip install -r requirements.txt && break
      echo "Retry $i failed, waiting..."
      sleep 10
    done
```

### 4.5 테스트 실패

**증상:**
- "X tests failed"
- Exit code 1

**해결 방법:**
1. 로컬에서 먼저 테스트 실행
2. 실패한 테스트 로그 확인
3. 테스트 환경과 로컬 환경 차이 확인

```bash
# 로컬에서 CI와 동일하게 테스트
python -m pytest tests/ -v

# 특정 테스트만 실행
python -m pytest tests/test_specific.py -v
```

### 4.6 권한 부족

**증상:**
- "Resource not accessible by integration"
- "Permission denied"

**해결 방법:**

```yaml
permissions:
  contents: read
  issues: write        # 이슈 작성 필요시
  pull-requests: write # PR 코멘트 필요시
```

### 4.7 타임아웃

**증상:**
- "The job running on runner has exceeded the maximum execution time"

**해결 방법:**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30  # 기본값 360분, 적절히 조절

    steps:
      - name: Long running task
        timeout-minutes: 10  # Step별 타임아웃도 설정 가능
        run: ./long-script.sh
```

---

## 5. 실패 디버깅 방법

### 5.1 GitHub UI에서 로그 확인

1. 저장소 → **Actions** 탭
2. 실패한 워크플로우 클릭
3. 실패한 Job 클릭
4. 실패한 Step 클릭하여 로그 확장

```
Actions 탭
    └── 워크플로우 실행 목록
            └── 실패한 실행 (빨간 X)
                    └── Jobs
                            └── 실패한 Job (빨간 X)
                                    └── Steps
                                            └── 실패한 Step (빨간 X) 클릭!
```

### 5.2 로그에서 에러 찾기

**팁**: 로그에서 아래 키워드 검색
- `Error`
- `error:`
- `failed`
- `FAILED`
- `exit code`
- `Exception`

### 5.3 디버그 로깅 활성화

**방법 1: Repository Secret 추가**
```
Settings → Secrets → Actions → New repository secret
Name: ACTIONS_STEP_DEBUG
Value: true
```

**방법 2: 워크플로우 재실행 시 디버그 모드**
```
Actions → 실패한 워크플로우 → Re-run jobs → Enable debug logging 체크
```

### 5.4 진단용 Step 추가

```yaml
steps:
  - name: Debug - 환경 정보 출력
    run: |
      echo "=== System Info ==="
      uname -a

      echo "=== Environment Variables ==="
      env | sort

      echo "=== Working Directory ==="
      pwd
      ls -la

      echo "=== Disk Space ==="
      df -h

      echo "=== Memory ==="
      free -h

  - name: Debug - 네트워크 확인
    run: |
      echo "=== DNS Resolution ==="
      nslookup google.com || echo "DNS failed"

      echo "=== Connectivity ==="
      curl -I https://github.com || echo "GitHub unreachable"

  # 실패해도 계속 진행하려면
  - name: This might fail
    continue-on-error: true
    run: ./risky-command.sh

  # 실패 시에만 실행
  - name: Debug on failure
    if: failure()
    run: |
      echo "Previous step failed!"
      cat /var/log/error.log || true
```

### 5.5 로컬에서 Actions 테스트하기

**[act](https://github.com/nektos/act)** 도구 사용:

```bash
# act 설치 (macOS)
brew install act

# act 설치 (Linux)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# 워크플로우 실행
act push                        # push 이벤트 시뮬레이션
act pull_request               # PR 이벤트 시뮬레이션
act -j build                   # 특정 Job만 실행
act --secret-file .secrets     # Secret 파일 사용

# .secrets 파일 예시
# DB_PASSWORD=mypassword
# API_KEY=myapikey
```

---

## 6. 이 프로젝트의 워크플로우 이해하기

이 저장소에는 6개의 워크플로우가 있습니다:

### 6.1 CI 워크플로우 (`ci.yml`)

**목적**: 코드 품질 검사 및 테스트

**실행 시점**:
- 코드 push 시
- Pull Request 시

**주요 단계**:
```
1. 코드 체크아웃
2. Python 설정
3. PostgreSQL, Redis 서비스 시작
4. 의존성 설치
5. 문서 빌드
6. 정적 파일 수집
7. 마이그레이션 체크
8. PEP8 (ruff) 린팅
9. 프론트엔드 린팅
10. 테스트 실행
11. 커버리지 리포트
```

**주의사항**:
- `secrets.NETBOX_DB_PASSWORD`가 설정되어 있어야 함
- Python 3.10, 3.11, 3.12에서 매트릭스 테스트

### 6.2 CodeQL (`codeql.yml`)

**목적**: 보안 취약점 분석

**실행 시점**:
- main, feature 브랜치에 push
- Pull Request
- 매주 목요일 16:38 UTC

**분석 대상**:
- GitHub Actions 워크플로우
- JavaScript/TypeScript
- Python

### 6.3 Stale Issues 관리 (`close-stale-issues.yml`)

**목적**: 오래된 이슈/PR 자동 정리

**실행 시점**: 매일 04:00 UTC

**조건**: `github.repository == 'netbox-community/netbox'`
- **이것이 Fork 저장소에서 실행되지 않는 이유입니다!**

**동작**:
- 90일 활동 없는 이슈 → stale 표시
- stale 후 30일 활동 없음 → 자동 닫힘
- PR은 30일/15일

### 6.4 Lock Threads (`lock-threads.yml`)

**목적**: 오래된 토론 잠금

**실행 시점**: 매일 03:00 UTC

**조건**: `github.repository == 'netbox-community/netbox'`

### 6.5 Close Incomplete Issues (`close-incomplete-issues.yml`)

**목적**: 정보가 부족한 이슈 정리

**실행 시점**: 매일 04:15 UTC

**조건**: `github.repository == 'netbox-community/netbox'`

### 6.6 Translation Strings (`update-translation-strings.yml`)

**목적**: 번역 문자열 자동 업데이트

**실행 시점**: 매일 05:00 UTC

**조건**: `github.repository == 'netbox-community/netbox'`

**필요한 Secret**: `HOUSEKEEPING_SECRET_KEY`

---

## 7. 모범 사례

### 7.1 버전 고정하기

```yaml
# 나쁜 예 - 예상치 못한 변경 발생 가능
uses: actions/checkout@main
uses: actions/checkout@v4

# 좋은 예 - 정확한 버전 고정
uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
```

**버전 해시 찾는 방법**:
1. https://github.com/actions/checkout/releases 방문
2. 원하는 버전의 커밋 해시 복사

### 7.2 환경 변수 관리

```yaml
# 전역 환경 변수 (모든 Job에 적용)
env:
  NODE_ENV: production

jobs:
  build:
    # Job 레벨 환경 변수
    env:
      CI: true

    steps:
      - name: Step with env
        # Step 레벨 환경 변수
        env:
          API_URL: https://api.example.com
        run: echo $API_URL
```

### 7.3 조건부 실행 활용

```yaml
steps:
  # 특정 브랜치에서만
  - name: Deploy to production
    if: github.ref == 'refs/heads/main'
    run: ./deploy.sh

  # PR에서만
  - name: Run extra tests
    if: github.event_name == 'pull_request'
    run: npm run test:full

  # 이전 Step 성공 시에만 (기본값)
  - name: After success
    if: success()
    run: echo "Previous step succeeded"

  # 이전 Step 실패 시에만
  - name: On failure
    if: failure()
    run: echo "Something failed"

  # 항상 실행 (cleanup 등)
  - name: Always run
    if: always()
    run: ./cleanup.sh
```

### 7.4 병렬 실행과 의존성

```yaml
jobs:
  # 이 Job들은 병렬로 실행됨
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  # 이 Job은 위 두 Job이 완료된 후 실행
  deploy:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
```

### 7.5 매트릭스 전략

```yaml
jobs:
  test:
    strategy:
      # 하나가 실패해도 나머지 계속 실행
      fail-fast: false
      matrix:
        python-version: ['3.10', '3.11', '3.12']
        os: [ubuntu-latest, macos-latest]
        # 특정 조합 제외
        exclude:
          - os: macos-latest
            python-version: '3.10'
        # 추가 조합
        include:
          - os: windows-latest
            python-version: '3.12'

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

### 7.6 캐싱으로 속도 향상

```yaml
steps:
  # pip 캐시
  - name: Cache pip
    uses: actions/cache@v4
    with:
      path: ~/.cache/pip
      key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      restore-keys: |
        ${{ runner.os }}-pip-

  # node_modules 캐시
  - name: Cache node modules
    uses: actions/cache@v4
    with:
      path: node_modules
      key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
      restore-keys: |
        ${{ runner.os }}-node-
```

### 7.7 재사용 가능한 워크플로우

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
    secrets:
      token:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
      - run: pytest

# 다른 워크플로우에서 호출
# .github/workflows/ci.yml
jobs:
  call-tests:
    uses: ./.github/workflows/reusable-test.yml
    with:
      python-version: '3.11'
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}
```

---

## 8. 자주 묻는 질문 (FAQ)

### Q1: Fork한 저장소에서 Actions가 실행되지 않아요

**A**: 두 가지 원인이 있습니다:

1. **Actions 비활성화**: Fork 저장소 → Settings → Actions → General → "Allow all actions" 선택

2. **조건문 제한**: 원본 저장소 전용 조건이 있을 수 있음
   ```yaml
   if: github.repository == 'original-owner/repo'
   ```
   이 조건을 수정하거나 제거하세요.

### Q2: Secret은 어떻게 추가하나요?

**A**:
1. 저장소 → Settings → Secrets and variables → Actions
2. "New repository secret" 클릭
3. Name과 Value 입력 후 저장

**주의**: Secret 값은 한 번 저장하면 다시 볼 수 없습니다. 새로 입력만 가능합니다.

### Q3: 워크플로우를 수동으로 실행하고 싶어요

**A**: `workflow_dispatch` 트리거 추가:

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
```

그 후 Actions 탭 → 워크플로우 선택 → "Run workflow" 버튼

### Q4: 로컬에서 테스트가 통과하는데 CI에서 실패해요

**A**: 환경 차이 확인:

1. **Python/Node 버전**: CI의 버전과 로컬 버전 일치 확인
2. **OS 차이**: CI는 보통 Linux, 로컬은 Windows/Mac
3. **환경 변수**: CI에만 있거나 없는 환경 변수
4. **데이터베이스**: CI는 빈 DB로 시작

```bash
# 로컬에서 CI 환경 시뮬레이션
docker run -it ubuntu:latest bash
# 그 안에서 테스트 실행
```

### Q5: 특정 파일 변경 시에만 워크플로우 실행하고 싶어요

**A**: `paths` 필터 사용:

```yaml
on:
  push:
    paths:
      - 'src/**'           # src 폴더 내 모든 파일
      - '*.py'             # 루트의 .py 파일
      - '!src/tests/**'    # src/tests 제외
    paths-ignore:
      - 'docs/**'
      - '*.md'
```

### Q6: 이전 워크플로우 실행을 취소하고 새 것만 실행하고 싶어요

**A**: `concurrency` 설정 사용:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Q7: 워크플로우 실패 시 알림 받고 싶어요

**A**: 여러 방법이 있습니다:

1. **GitHub 기본 알림**: Settings → Notifications → Actions 설정

2. **Slack 알림 추가**:
```yaml
- name: Notify Slack on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    channel: '#ci-alerts'
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Q8: 같은 워크플로우를 여러 번 정의하지 않고 재사용하고 싶어요

**A**: Composite Action 또는 Reusable Workflow 사용:

```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Common setup steps'

runs:
  using: 'composite'
  steps:
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - run: pip install -r requirements.txt
      shell: bash

# 사용하는 워크플로우
steps:
  - uses: ./.github/actions/setup-project
```

---

## 부록: 유용한 링크

- [GitHub Actions 공식 문서](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [act - 로컬 테스트 도구](https://github.com/nektos/act)
- [GitHub Actions 상태 페이지](https://www.githubstatus.com/)

---

## 체크리스트: 워크플로우 작성 전 확인사항

- [ ] 필요한 Secret이 모두 설정되어 있는가?
- [ ] Action 버전이 고정되어 있는가?
- [ ] 권한(permissions)이 최소한으로 설정되어 있는가?
- [ ] 타임아웃이 적절히 설정되어 있는가?
- [ ] 캐시가 활용되고 있는가?
- [ ] 에러 처리와 디버깅 Step이 있는가?
- [ ] 로컬에서 테스트해 보았는가?

---

*이 가이드가 도움이 되었기를 바랍니다. 추가 질문이 있으면 이슈를 열어주세요!*
