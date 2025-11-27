# act 초보자 가이드: GitHub Actions를 로컬에서 실행하기

## 목차

1. [act란 무엇인가?](#1-act란-무엇인가)
2. [왜 act를 사용해야 할까?](#2-왜-act를-사용해야-할까)
3. [설치하기](#3-설치하기)
4. [첫 번째 실행](#4-첫-번째-실행)
5. [기본 명령어 익히기](#5-기본-명령어-익히기)
6. [실전 예제: NetBox CI 워크플로우 실행](#6-실전-예제-netbox-ci-워크플로우-실행)
7. [Secrets 관리하기](#7-secrets-관리하기)
8. [자주 발생하는 문제와 해결법](#8-자주-발생하는-문제와-해결법)
9. [고급 사용법](#9-고급-사용법)
10. [팁과 베스트 프랙티스](#10-팁과-베스트-프랙티스)

---

## 1. act란 무엇인가?

### 한 줄 요약
**act**는 GitHub Actions 워크플로우를 로컬 컴퓨터에서 실행할 수 있게 해주는 도구입니다.

### 상세 설명
GitHub Actions는 GitHub에서 제공하는 CI/CD(지속적 통합/지속적 배포) 서비스입니다. 코드를 push하거나 PR을 생성하면 자동으로 테스트, 빌드, 배포 등을 수행합니다.

하지만 문제가 있습니다:
- 워크플로우가 제대로 동작하는지 확인하려면 매번 GitHub에 push해야 합니다
- 오류가 발생하면 수정 후 다시 push... 이 과정을 반복해야 합니다
- GitHub Actions 사용량에는 제한이 있습니다 (무료 계정 기준 월 2,000분)

**act**는 이런 문제를 해결합니다. Docker를 사용해 GitHub Actions 환경을 로컬에 재현하므로, push 없이도 워크플로우를 테스트할 수 있습니다.

### act의 작동 원리

```
┌─────────────────────────────────────────────────────────────┐
│                    당신의 로컬 컴퓨터                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                     Docker                           │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │     GitHub Actions Runner 이미지             │    │   │
│  │  │  ┌───────────────────────────────────────┐  │    │   │
│  │  │  │     워크플로우 (.github/workflows/)    │  │    │   │
│  │  │  │  - 테스트 실행                        │  │    │   │
│  │  │  │  - 빌드 수행                          │  │    │   │
│  │  │  │  - 린트 검사                          │  │    │   │
│  │  │  └───────────────────────────────────────┘  │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 왜 act를 사용해야 할까?

### 장점

| 장점 | 설명 |
|------|------|
| **빠른 피드백** | Push 없이 즉시 워크플로우 테스트 가능 |
| **비용 절감** | GitHub Actions 무료 사용량 소모 없음 |
| **오프라인 작업** | 인터넷 연결 없이도 테스트 가능 (이미지 캐시 후) |
| **디버깅 용이** | 로컬에서 상세한 로그 확인 및 디버깅 가능 |
| **반복 테스트** | 동일한 테스트를 빠르게 반복 실행 가능 |

### 실제 사용 시나리오

```
[Before act]
코드 수정 → git push → GitHub에서 CI 실행 (5분 대기) → 실패
→ 코드 수정 → git push → GitHub에서 CI 실행 (5분 대기) → 실패
→ 코드 수정 → git push → ... (무한 반복)

[After act]
코드 수정 → act 실행 (1분) → 실패 → 코드 수정 → act 실행 (1분) → 성공!
→ git push (자신감 있게!)
```

---

## 3. 설치하기

### 사전 요구사항

act를 사용하려면 **Docker**가 설치되어 있어야 합니다.

#### Docker 설치 확인

```bash
# Docker가 설치되어 있는지 확인
docker --version

# 출력 예시: Docker version 24.0.7, build afdd53b
```

Docker가 없다면 [Docker 공식 사이트](https://docs.docker.com/get-docker/)에서 설치하세요.

### act 설치 방법

#### macOS (Homebrew 사용)

```bash
# Homebrew로 설치 (가장 쉬운 방법)
brew install act

# 설치 확인
act --version
```

#### Linux

```bash
# 방법 1: 공식 설치 스크립트 사용 (권장)
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# 방법 2: 수동 다운로드
# 1. https://github.com/nektos/act/releases 에서 최신 버전 확인
# 2. Linux용 바이너리 다운로드
wget https://github.com/nektos/act/releases/download/v0.2.57/act_Linux_x86_64.tar.gz
tar -xzf act_Linux_x86_64.tar.gz
sudo mv act /usr/local/bin/

# 설치 확인
act --version
```

#### Windows

```powershell
# 방법 1: Chocolatey 사용
choco install act-cli

# 방법 2: Scoop 사용
scoop install act

# 방법 3: winget 사용
winget install nektos.act

# 설치 확인
act --version
```

#### 설치 확인

```bash
$ act --version
act version 0.2.57
```

버전 번호가 출력되면 설치 완료입니다!

---

## 4. 첫 번째 실행

### 프로젝트 디렉토리로 이동

```bash
# NetBox 프로젝트 디렉토리로 이동
cd /path/to/netbox25kr

# GitHub Actions 워크플로우 파일 확인
ls -la .github/workflows/
```

출력 예시:
```
total 32
drwxr-xr-x 2 user user 4096 Nov 26 10:00 .
drwxr-xr-x 4 user user 4096 Nov 26 10:00 ..
-rw-r--r-- 1 user user 3245 Nov 26 10:00 ci.yml
-rw-r--r-- 1 user user 1523 Nov 26 10:00 close-stale-issues.yml
-rw-r--r-- 1 user user  892 Nov 26 10:00 codeql.yml
...
```

### 워크플로우 목록 확인

```bash
# 실행 가능한 워크플로우 목록 보기
act -l
```

출력 예시:
```
Stage  Job ID  Job name  Workflow name  Workflow file         Events
0      build   build     CI             ci.yml                push,pull_request
0      stale   stale     Close stale... close-stale-issues... schedule,workflow_dispatch
...
```

### 첫 번째 실행 (Dry Run)

실제 실행 전에 어떤 작업이 수행될지 미리 확인합니다:

```bash
# -n 옵션: dry run (실제로 실행하지 않고 계획만 보여줌)
act -n
```

### 실제 실행

```bash
# 기본 실행 (push 이벤트로 트리거되는 모든 워크플로우 실행)
act

# 첫 실행 시 이미지 선택 프롬프트가 나타남
# ? Please choose the default image you want to use with act:
#   - Large size image: +20GB Docker image, includes almost everything
#   - Medium size image: ~500MB, includes only necessary tools (~500MB)
#   - Micro size image: ~200MB, only contains basic tools
```

#### 이미지 선택 가이드

| 이미지 | 크기 | 추천 상황 |
|--------|------|----------|
| **Micro** | ~200MB | 간단한 스크립트, 빠른 테스트 |
| **Medium** | ~500MB | 일반적인 CI/CD 워크플로우 (권장) |
| **Large** | ~20GB | 복잡한 빌드 환경, 다양한 도구 필요 시 |

초보자는 **Medium** 이미지를 권장합니다.

---

## 5. 기본 명령어 익히기

### 명령어 구조

```
act [이벤트] [옵션]
```

### 주요 이벤트

| 이벤트 | 설명 | 예시 |
|--------|------|------|
| `push` | 코드 push 시 트리거 (기본값) | `act push` 또는 `act` |
| `pull_request` | PR 생성/업데이트 시 트리거 | `act pull_request` |
| `workflow_dispatch` | 수동 트리거 | `act workflow_dispatch` |
| `schedule` | 예약된 시간에 트리거 | `act schedule` |

### 주요 옵션

```bash
# 1. 워크플로우 목록 보기
act -l
act -l --workflows .github/workflows/ci.yml  # 특정 파일만

# 2. Dry Run (실제 실행 없이 계획 확인)
act -n

# 3. 특정 job만 실행
act -j build           # 'build' job만 실행
act -j test -j lint    # 여러 job 실행

# 4. 특정 워크플로우 파일만 실행
act -W .github/workflows/ci.yml

# 5. 상세 로그 출력
act -v                 # verbose 모드
act -vv                # 더 상세한 로그

# 6. 이미지 지정
act -P ubuntu-latest=catthehacker/ubuntu:act-latest

# 7. 환경 변수 전달
act --env MY_VAR=value

# 8. Secrets 전달
act -s MY_SECRET=secret_value

# 9. 컨테이너 아키텍처 지정 (Apple Silicon Mac 등)
act --container-architecture linux/amd64
```

### 실습 예제

```bash
# 예제 1: push 이벤트의 모든 워크플로우 실행
act push

# 예제 2: pull_request 이벤트로 CI 워크플로우만 실행
act pull_request -W .github/workflows/ci.yml

# 예제 3: 특정 job만 dry run
act -n -j build

# 예제 4: 상세 로그와 함께 실행
act -v -j build
```

---

## 6. 실전 예제: NetBox CI 워크플로우 실행

NetBox 프로젝트의 실제 CI 워크플로우를 로컬에서 실행해보겠습니다.

### CI 워크플로우 분석

`.github/workflows/ci.yml` 파일의 구조:

```yaml
name: CI

on:
  push:
    paths-ignore:
      - 'docs/**'
      ...
  pull_request:
    ...

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
        node-version: ['20.x']
    services:
      redis:
        image: redis
        ports:
          - 6379:6379
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: netbox
          POSTGRES_PASSWORD: ${{ secrets.NETBOX_DB_PASSWORD }}
          ...
    steps:
      - name: Check out repo
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
      ...
      - name: Run tests
        run: coverage run ...
```

### 단계별 실행

#### Step 1: Secrets 파일 생성

CI 워크플로우는 데이터베이스 비밀번호를 필요로 합니다. `.secrets` 파일을 생성합니다:

```bash
# 프로젝트 루트에 .secrets 파일 생성
cat > .secrets << 'EOF'
NETBOX_DB_PASSWORD=your_test_password_here
EOF

# 보안을 위해 파일 권한 설정
chmod 600 .secrets

# .gitignore에 추가 (이미 되어있을 수 있음)
echo ".secrets" >> .gitignore
```

#### Step 2: 워크플로우 확인

```bash
# CI 워크플로우의 job 목록 확인
act -l -W .github/workflows/ci.yml
```

출력:
```
Stage  Job ID  Job name  Workflow name  Workflow file  Events
0      build   build     CI             ci.yml         push,pull_request
```

#### Step 3: Dry Run 실행

```bash
# 실제 실행 전 계획 확인
act -n -W .github/workflows/ci.yml --secret-file .secrets
```

#### Step 4: 실제 실행

```bash
# 전체 CI 워크플로우 실행
act -W .github/workflows/ci.yml --secret-file .secrets

# 특정 Python 버전만 테스트하고 싶다면
act -W .github/workflows/ci.yml --secret-file .secrets \
    --matrix python-version:3.11

# 상세 로그와 함께 실행
act -v -W .github/workflows/ci.yml --secret-file .secrets
```

### 자주 사용하는 조합

```bash
# 1. 빠른 린트 체크만 (특정 step까지만 실행은 불가, job 단위 실행)
# ci.yml에 별도 lint job이 있다면:
act -j lint --secret-file .secrets

# 2. Python 3.11로만 테스트
act -W .github/workflows/ci.yml \
    --secret-file .secrets \
    --matrix python-version:3.11 \
    --matrix node-version:20.x

# 3. 컨테이너 내부에서 디버깅
act -W .github/workflows/ci.yml \
    --secret-file .secrets \
    --reuse  # 컨테이너를 재사용 (빠른 반복 테스트)
```

---

## 7. Secrets 관리하기

### 방법 1: 명령줄에서 직접 전달

```bash
# 단일 secret
act -s MY_SECRET=my_value

# 여러 secrets
act -s SECRET1=value1 -s SECRET2=value2
```

### 방법 2: .secrets 파일 사용 (권장)

```bash
# .secrets 파일 생성
cat > .secrets << 'EOF'
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
NETBOX_DB_PASSWORD=test_password
API_KEY=your_api_key_here
EOF

# 파일 권한 설정 (보안 중요!)
chmod 600 .secrets

# 사용
act --secret-file .secrets
```

### 방법 3: 환경 변수에서 읽기

```bash
# 현재 쉘의 환경 변수를 secret으로 사용
export NETBOX_DB_PASSWORD="my_password"
act -s NETBOX_DB_PASSWORD

# 또는 .env 파일 사용
cat > .env << 'EOF'
NETBOX_DB_PASSWORD=test_password
EOF

act --env-file .env
```

### 주의사항

```bash
# .secrets와 .env 파일을 .gitignore에 추가!
echo ".secrets" >> .gitignore
echo ".env" >> .gitignore

# 파일에 민감한 정보가 있는지 확인
git status  # .secrets가 추적되고 있지 않은지 확인
```

---

## 8. 자주 발생하는 문제와 해결법

### 문제 1: Docker가 실행되지 않음

```
Error: Cannot connect to the Docker daemon
```

**해결법:**
```bash
# Linux
sudo systemctl start docker
sudo systemctl enable docker

# macOS
# Docker Desktop 앱 실행

# Docker 상태 확인
docker info
```

### 문제 2: 권한 오류

```
Error: permission denied while trying to connect to Docker daemon
```

**해결법:**
```bash
# Linux에서 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 로그아웃 후 다시 로그인하거나
newgrp docker

# 확인
docker run hello-world
```

### 문제 3: 이미지 다운로드 실패

```
Error: failed to pull image
```

**해결법:**
```bash
# Docker 로그인 (Docker Hub rate limit 때문일 수 있음)
docker login

# 또는 다른 이미지 사용
act -P ubuntu-latest=catthehacker/ubuntu:act-latest

# 미리 이미지 다운로드
docker pull catthehacker/ubuntu:act-latest
```

### 문제 4: Services가 작동하지 않음 (PostgreSQL, Redis 등)

```
Error: service "postgres" is not reachable
```

**해결법:**
act는 services를 약간 다르게 처리합니다.

```bash
# 방법 1: 로컬에서 직접 서비스 실행
docker run -d --name postgres-test \
    -e POSTGRES_USER=netbox \
    -e POSTGRES_PASSWORD=test \
    -e POSTGRES_DB=netbox \
    -p 5432:5432 \
    postgres:15

docker run -d --name redis-test -p 6379:6379 redis

# act 실행 (네트워크 연결을 위해)
act --network host --secret-file .secrets
```

```bash
# 방법 2: docker-compose 사용
cat > docker-compose.test.yml << 'EOF'
version: '3'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: netbox
      POSTGRES_PASSWORD: test
      POSTGRES_DB: netbox
    ports:
      - "5432:5432"
  redis:
    image: redis
    ports:
      - "6379:6379"
EOF

# 서비스 시작
docker-compose -f docker-compose.test.yml up -d

# act 실행
act --network host --secret-file .secrets

# 완료 후 정리
docker-compose -f docker-compose.test.yml down
```

### 문제 5: Apple Silicon Mac (M1/M2/M3)에서 오류

```
Error: exec format error
```

**해결법:**
```bash
# amd64 아키텍처 명시
act --container-architecture linux/amd64

# 또는 ARM 호환 이미지 사용
act -P ubuntu-latest=catthehacker/ubuntu:act-22.04-arm
```

### 문제 6: actions/checkout이 실패함

```
Error: Unable to find a ref named
```

**해결법:**
```bash
# 로컬 파일 바인딩 사용
act -b  # --bind 플래그: 로컬 디렉토리를 컨테이너에 바인딩
```

### 문제 7: Node.js/Python 버전 관련 오류

```
Error: Version X.X is not available
```

**해결법:**
```bash
# 더 큰 이미지 사용
act -P ubuntu-latest=catthehacker/ubuntu:full-latest

# 또는 특정 버전의 이미지 사용
act -P ubuntu-latest=catthehacker/ubuntu:act-22.04
```

### 문제 8: 메모리 부족

```
Error: OOMKilled
```

**해결법:**
```bash
# Docker Desktop에서 메모리 할당량 늘리기
# Settings > Resources > Memory: 4GB 이상 권장

# 또는 동시에 실행되는 job 수 제한
act --parallel 1
```

---

## 9. 고급 사용법

### 9.1 커스텀 이벤트 페이로드

실제 GitHub 이벤트와 동일한 페이로드로 테스트:

```bash
# 이벤트 페이로드 파일 생성
cat > event.json << 'EOF'
{
  "pull_request": {
    "number": 123,
    "head": {
      "ref": "feature-branch"
    },
    "base": {
      "ref": "main"
    }
  }
}
EOF

# 페이로드와 함께 실행
act pull_request -e event.json
```

### 9.2 로컬 Action 개발

자체 GitHub Action을 개발할 때:

```bash
# action.yml이 있는 디렉토리에서
act -W ./test-workflow.yml
```

### 9.3 조건부 실행

```bash
# if 조건을 무시하고 모든 step 실행
act --if-always

# 특정 actor로 실행
act --actor my-username
```

### 9.4 아티팩트 처리

```bash
# 아티팩트 저장 경로 지정
act --artifact-server-path ./artifacts

# 이전 아티팩트 사용
act --artifact-server-path ./artifacts --reuse
```

### 9.5 Matrix 전략 활용

```bash
# 특정 matrix 조합만 실행
act --matrix os:ubuntu-latest --matrix python:3.11

# 모든 matrix 조합 나열
act -l --matrix
```

### 9.6 .actrc 설정 파일

반복적인 옵션을 설정 파일로 관리:

```bash
# 프로젝트 루트에 .actrc 파일 생성
cat > .actrc << 'EOF'
-P ubuntu-latest=catthehacker/ubuntu:act-latest
--secret-file .secrets
--env-file .env
--container-architecture linux/amd64
-v
EOF

# 이제 간단히 실행
act
```

### 9.7 컨테이너 재사용

빠른 반복 테스트를 위해:

```bash
# 컨테이너 재사용 (첫 실행 후 재실행 시 빠름)
act --reuse

# 완료 후 컨테이너 정리
act --rm
```

---

## 10. 팁과 베스트 프랙티스

### 개발 워크플로우

```
1. 코드 수정
   ↓
2. act로 로컬 테스트 (빠른 피드백)
   ↓
3. 문제 발견 시 수정 후 2번으로
   ↓
4. 성공 시 git commit & push
   ↓
5. GitHub Actions에서 최종 검증
```

### 권장 설정 (.actrc)

```bash
# .actrc - 프로젝트별 기본 설정
-P ubuntu-latest=catthehacker/ubuntu:act-latest
-P ubuntu-22.04=catthehacker/ubuntu:act-22.04
--secret-file .secrets
--reuse
-v
```

### 디렉토리 구조

```
your-project/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── .actrc           # act 설정 (git에 커밋 가능)
├── .secrets         # 민감 정보 (.gitignore에 추가!)
├── .env             # 환경 변수 (.gitignore에 추가!)
└── ...
```

### 성능 최적화 팁

1. **이미지 캐싱**: 처음 한 번만 다운로드
   ```bash
   docker pull catthehacker/ubuntu:act-latest
   ```

2. **병렬 실행 제한**: 메모리 부족 시
   ```bash
   act --parallel 2
   ```

3. **특정 job만 실행**: 전체 실행 대신
   ```bash
   act -j build  # 필요한 job만
   ```

4. **컨테이너 재사용**:
   ```bash
   act --reuse
   ```

### 디버깅 팁

```bash
# 1. 상세 로그 보기
act -v    # verbose
act -vv   # very verbose

# 2. Dry run으로 계획 확인
act -n

# 3. 특정 step에서 shell 접근 (워크플로우에 추가)
# - name: Debug shell
#   run: |
#     echo "=== Debug Info ==="
#     env | sort
#     pwd
#     ls -la

# 4. 컨테이너 직접 접근
docker ps  # 실행 중인 컨테이너 확인
docker exec -it <container_id> /bin/bash
```

### 주의사항 체크리스트

- [ ] `.secrets` 파일이 `.gitignore`에 있는가?
- [ ] Docker가 실행 중인가?
- [ ] 충분한 디스크 공간이 있는가? (이미지 크기 고려)
- [ ] 메모리가 충분한가? (최소 4GB 권장)
- [ ] Apple Silicon Mac이라면 아키텍처 설정했는가?

---

## 요약: 빠른 시작 가이드

```bash
# 1. 설치 (macOS)
brew install act

# 2. Docker 실행 확인
docker --version

# 3. 프로젝트 디렉토리로 이동
cd your-project

# 4. Secrets 파일 생성 (필요시)
echo "MY_SECRET=value" > .secrets
chmod 600 .secrets

# 5. 워크플로우 목록 확인
act -l

# 6. 실행!
act --secret-file .secrets
```

---

## 추가 리소스

- [act 공식 GitHub](https://github.com/nektos/act)
- [act 문서](https://nektosact.com/)
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Docker 설치 가이드](https://docs.docker.com/get-docker/)

---

*이 가이드가 도움이 되었다면, act를 사용해 더 빠르고 효율적인 CI/CD 개발을 경험해보세요!*
