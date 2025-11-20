# NetBox 설치 및 사용 가이드 (한글)
INSTALLATION_GUIDE_KR.md  2025.11.16

> **참고**: 이 가이드는 macOS 및 Linux(Ubuntu/Debian) 환경에서 NetBox를 설치하는 방법을 안내합니다.
## 목차
- [소개](#소개)
- [시스템 요구사항](#시스템-요구사항)
- [1단계: 사전 준비](#1단계-사전-준비)
- [2단계: 데이터베이스 및 Redis 설치](#2단계-데이터베이스-및-redis-설치)
- [3단계: NetBox 설치](#3단계-netbox-설치)
- [4단계: NetBox 설정](#4단계-netbox-설정)
- [5단계: 데이터베이스 초기화](#5단계-데이터베이스-초기화)
- [6단계: NetBox 실행](#6단계-netbox-실행)
- [주요 기능 사용 가이드](#주요-기능-사용-가이드)
- [문제 해결](#문제-해결)

---

## 소개

**NetBox**는 네트워크 인프라 관리를 위한 오픈소스 웹 애플리케이션입니다. 이 가이드는 macOS에서 NetBox를 설치하고 주요 기능을 테스트하는 방법을 단계별로 안내합니다.

**설치 시간**: 약 30-45분
**난이도**: 중급 (터미널 사용 경험 필요)

---

## 시스템 요구사항

- **macOS**: 10.15 (Catalina) 이상
- **Python**: 3.10 이상
- **PostgreSQL**: 12 이상
- **Redis**: 6.0 이상
- **디스크 공간**: 최소 2GB
- **메모리**: 최소 4GB RAM 권장

---

## 1단계: 사전 준비

### 1.1 Homebrew 설치 확인

Homebrew가 설치되어 있지 않다면 먼저 설치합니다:

```bash
# Homebrew 설치 여부 확인
brew --version

# 설치되어 있지 않다면:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 1.2 Python 3.10+ 설치

```bash
# Python 버전 확인
python3 --version

# Python 3.10 이상이 아니라면:
brew install python@3.11
```

### 1.3 필수 도구 설치

```bash
# Git 설치 (이미 설치되어 있을 수 있음)
brew install git

# 기타 필수 도구
brew install pkg-config
```

---

## 2단계: 데이터베이스 및 Redis 설치

### 2.1 PostgreSQL 설치 및 설정

```bash
# PostgreSQL 설치
brew install postgresql@15

# PostgreSQL 서비스 시작
brew services start postgresql@15

# 설치 확인
psql --version
```

### 2.2 NetBox용 데이터베이스 생성

```bash
# PostgreSQL에 접속 (사용자명은 자동으로 현재 macOS 사용자명이 됩니다)
psql postgres

# PostgreSQL 프롬프트에서 다음 명령어를 하나씩 실행:
```

```sql
-- NetBox용 데이터베이스 생성
CREATE DATABASE netbox;

-- NetBox용 사용자 생성 (⚠️ 보안: 실제 환경에서는 강력한 비밀번호 사용 필수!)
CREATE USER netbox WITH PASSWORD 'netbox1234!';  

-- 권한 부여
ALTER DATABASE netbox OWNER TO netbox;
GRANT ALL PRIVILEGES ON DATABASE netbox TO netbox;

-- 종료
\q
```

> **⚠️ 보안 주의사항**:
> - `netbox1234!`는 **데이터베이스 연결용 비밀번호**입니다
> - 실제 운영 환경에서는 더 복잡한 비밀번호를 사용하세요
> - 이 비밀번호는 `configuration.py` 파일에 저장됩니다 (웹 로그인 비밀번호와 다름)

### 2.3 Redis 설치 및 시작

```bash
# Redis 설치
brew install redis

# Redis 서비스 시작
brew services start redis

# Redis 작동 확인
redis-cli ping
# 응답: PONG
```

---

## 3단계: NetBox 설치

### 3.1 NetBox 소스코드 다운로드

```bash
# 작업 디렉토리로 이동 (원하는 위치로 변경 가능)
cd ~/Documents

# NetBox 저장소 클론
git clone https://github.com/netbox-community/netbox.git
cd netbox

# 최신 stable 버전으로 체크아웃 (또는 현재 브랜치 사용)
git checkout master
```

> **참고**: 이미 NetBox 소스코드가 있다면 해당 디렉토리로 이동하세요.
### 3.2 Python 가상환경 생성

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 프롬프트가 (venv)로 시작하면 성공!
```

### 3.3 Python 의존성 설치

```bash
# pip 업그레이드
pip3 install --upgrade pip

# NetBox 의존성 설치
pip3 install -r requirements.txt

# 설치 확인 (5-10분 소요)
pip3 list | grep Django
# Django가 목록에 나타나면 성공
```

---

## 4단계: NetBox 설정

### 4.1 설정 파일 생성

```bash
# netbox 디렉토리로 이동
cd netbox

# 설정 예제 파일 복사
cp netbox/configuration_example.py netbox/configuration.py
```

### 4.2 SECRET_KEY 생성

```bash
# SECRET_KEY 생성 스크립트 실행
python3 generate_secret_key.py

# 출력된 키를 복사해둡니다 (아래 키 사용):
# k9m@3n!8$p2v&q7w*e5r4t6y8u9i0o1p2a3s5d6f7g8h9j0k1l
```

### 4.3 설정 파일 편집

선호하는 텍스트 에디터로 설정 파일을 엽니다:

```bash
# VS Code 사용 시:
code netbox/configuration.py

# nano 사용 시:
nano netbox/configuration.py

# vim 사용 시:
vim netbox/configuration.py
```

다음 설정을 수정합니다:

```python
# 1. ALLOWED_HOSTS 설정 (약 11번째 줄)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '::1']

# 2. DATABASE 설정 (약 15번째 줄)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'netbox',
        'USER': 'netbox',
        'PASSWORD': 'netbox1234!',  # 2.2단계에서 설정한 비밀번호
        'HOST': 'localhost',
        'PORT': '',
        'CONN_MAX_AGE': 300,
    }
}

# 3. REDIS 설정 (약 30번째 줄) - 기본값 그대로 사용
# 변경사항 없음 (이미 localhost:6379로 설정되어 있음)

# 4. SECRET_KEY 설정 (약 69번째 줄)
SECRET_KEY = 'k9m@3n!8$p2v&q7w*e5r4t6y8u9i0o1p2a3s5d6f7g8h9j0k1l'  # 4.2단계에서 생성한 키

# 5. DEBUG 모드 활성화 (약 119번째 줄) - 개발/테스트용
DEBUG = True

# 6. TIME_ZONE 설정 (약 250번째 줄) - 선택사항
TIME_ZONE = 'Asia/Seoul'
```

**저장하고 종료** (nano: Ctrl+X → Y → Enter, vim: :wq)

### 4.4 설정 검증

```bash
# NetBox 설정이 올바른지 확인
python3 manage.py check

# 성공 메시지:
# System check identified no issues (0 silenced).
```

---

## 5단계: 데이터베이스 초기화

### 5.1 데이터베이스 마이그레이션

```bash
# 데이터베이스 스키마 생성 (2-3분 소요)
python3 manage.py migrate

# 성공 시 다음과 같은 메시지가 출력됩니다:
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying auth.0001_initial... OK
#   ...
#   Applying wireless.0001_initial... OK
```

### 5.2 슈퍼유저(관리자) 계정 생성

```bash
# 슈퍼유저 생성
python3 manage.py createsuperuser

# 프롬프트에 따라 입력:
# Username: admin
# Email address: wk.paik@somansa.com
# Password: netbox1234!  (입력 시 화면에 표시되지 않음 - 10자 이상)
# Password (again): netbox1234!
# Superuser created successfully.
```

> **⚠️ 보안 주의사항**:
> - `netbox1234!`는 **웹 로그인용 비밀번호**입니다 (데이터베이스 비밀번호와 다름)
> - 최소 10자 이상, 영문 대소문자, 숫자, 특수문자 조합 권장
> - 실제 운영 환경에서는 더 복잡하고 추측하기 어려운 비밀번호를 사용하세요
> - 비밀번호는 Django의 해시 알고리즘으로 암호화되어 데이터베이스에 저장됩니다
### 5.3 정적 파일 수집

```bash
# CSS, JavaScript, 이미지 등의 정적 파일 수집
python3 manage.py collectstatic --noinput

# 성공 메시지:
# XXX static files copied to '/path/to/netbox/netbox/static'.
```

---

## 6단계: NetBox 실행

### 6.1 개발 서버 실행

```bash
# 개발 서버 시작 (netbox/netbox 디렉토리에서)
python3 manage.py runserver 0.0.0.0:8000

# 성공 메시지:
# Django version 5.2.7, using settings 'netbox.settings'
# Starting development server at http://0.0.0.0:8000/
# Quit the server with CONTROL-C.
```

### 6.2 백그라운드 작업 워커 실행 (새 터미널)

NetBox의 모든 기능을 사용하려면 백그라운드 워커도 실행해야 합니다.

**새 터미널 창을 열고**:

```bash
# NetBox 디렉토리로 이동
cd ~/Documents/netbox/netbox

# 가상환경 활성화
source ../venv/bin/activate

# RQ 워커 시작
python3 manage.py rqworker

# 성공 메시지:
# 12:00:00 Worker rq:worker:... started with PID ...
# 12:00:00 Listening on default...
```

### 6.3 웹 브라우저로 접속

웹 브라우저를 열고 다음 주소로 접속:

```
http://localhost:8000
```

**로그인 화면이 나타나면 성공!** 🎉

---

## 7단계: 한국어 UI 활성화

NetBox를 한국어로 사용하려면 한국어 번역 파일을 컴파일하고 언어 설정을 변경해야 합니다.

### 7.1 한국어 번역 파일 확인

```bash
# NetBox 번역 파일 디렉토리로 이동
cd ~/Documents/netbox/netbox/translations/ko/LC_MESSAGES

# 번역 파일 확인
ls -la
# django.po (번역 소스)
# django.mo (컴파일된 파일)
```

### 7.2 번역 파일 컴파일

```bash
# netbox/netbox 디렉토리로 이동
cd ~/Documents/netbox/netbox

# 가상환경이 활성화되어 있는지 확인
source ../venv/bin/activate

# 한국어 번역 컴파일
python3 manage.py compilemessages -l ko

# 성공 메시지:
# processing file django.po in .../translations/ko/LC_MESSAGES
# compiling message catalogs for ko
```

### 7.3 개발 서버 재시작

```bash
# 기존 서버 중지 (Ctrl+C)
# 서버 재시작
python3 manage.py runserver 0.0.0.0:8000
```

### 7.4 브라우저에서 한국어로 변경

1. **NetBox에 로그인**: `http://localhost:8000`
2. **오른쪽 상단 사용자 아이콘 클릭** → **Preferences** 선택
3. **User Interface 섹션**:
   - **Language**: `Korean (한국어)` 선택
4. **Update 버튼 클릭**
5. **페이지 새로고침 (F5)**

**결과**: NetBox 인터페이스가 한국어로 표시됩니다! 🎉

### 7.5 한국어 번역 상태 확인

```bash
# 번역되지 않은 항목 개수 확인
cd ~/Documents/netbox/netbox/translations/ko/LC_MESSAGES
grep -c 'msgstr ""' django.po

# 전체 번역 항목 개수
grep -c 'msgid' django.po
```

### 7.6 번역 업데이트 (선택사항)

NetBox가 업데이트되면 새로운 번역 문자열이 추가될 수 있습니다:

```bash
# 새로운 번역 문자열 추출 및 병합
cd ~/Documents/netbox/netbox
python3 manage.py makemessages -l ko -i "project-static/*"

# 번역 파일 편집 (선택사항)
vim translations/ko/LC_MESSAGES/django.po

# 재컴파일
python3 manage.py compilemessages -l ko

# 서버 재시작
python3 manage.py runserver
```

---

## 주요 기능 사용 가이드

이제 NetBox의 주요 기능들을 테스트해보겠습니다.

### 1. 로그인

1. **URL**: `http://localhost:8000`
2. **Username**: `admin` (5.2단계에서 생성한 계정)
3. **Password**: `netbox1234!` 
4. **"Log In" 버튼 클릭**

로그인 후 NetBox 대시보드가 나타납니다.

> **참고**: 데이터베이스 비밀번호('netbox1234!`)가 아닌 웹 로그인 비밀번호를 사용해야 합니다.

---

### 2. 사이트(Site) 생성하기

NetBox에서 모든 장비는 특정 사이트에 속합니다. 먼저 사이트를 생성해봅시다.

#### 단계:

1. **상단 메뉴**: `Organization` → `Sites` 클릭
2. **오른쪽 상단**: `+ Add` 버튼 클릭
3. **정보 입력**:
   - **Name**: `Pangyo DC1` (서울 데이터센터)
   - **Slug**: `pangyo-dc1` (자동 생성됨)
   - **Status**: `Active` 선택
   - **Region**: (선택사항) - 일단 비워둠
   - **Description**: `서울 본사 데이터센터`
4. **하단**: `Create` 버튼 클릭

**결과**: 첫 번째 사이트가 생성되었습니다! 목록에서 확인할 수 있습니다.

#### 추가 사이트 생성 (선택사항):

같은 방법으로 더 많은 사이트를 생성해봅니다:
- `Busan DC1` (부산 데이터센터)
- `Tokyo DC1` (도쿄 데이터센터)

---

### 3. 제조사(Manufacturer) 생성하기

장비 타입을 정의하기 전에 제조사를 추가합니다.

#### 단계:

1. **상단 메뉴**: `Devices` → `Device Types` → `Manufacturers` 클릭
2. **오른쪽 상단**: `+ Add` 버튼 클릭
3. **정보 입력**:
   - **Name**: `Cisco`
   - **Slug**: `cisco` (자동 생성됨)
   - **Description**: `Cisco Systems, Inc.`
4. **`Create` 버튼 클릭**

#### 추가 제조사 생성:
- `Juniper Networks`
- `Arista Networks`
- `Dell`

---

### 4. 장비 역할(Device Role) 생성하기

장비의 용도를 정의합니다.

#### 단계:

1. **상단 메뉴**: `Devices` → `Device Roles` 클릭
2. **`+ Add` 버튼 클릭**
3. **정보 입력**:
   - **Name**: `Core Router` (코어 라우터)
   - **Slug**: `core-router`
   - **Color**: 원하는 색상 선택 (예: 빨강)
   - **Description**: `네트워크 코어 라우터`
4. **`Create` 버튼 클릭**

#### 추가 역할 생성:
- `Access Switch` (액세스 스위치) - 파랑
- `Distribution Switch` (분산 스위치) - 초록
- `Firewall` (방화벽) - 주황

---

### 5. 장비 타입(Device Type) 생성하기

특정 장비 모델을 정의합니다.

#### 단계:

1. **상단 메뉴**: `Devices` → `Device Types` 클릭
2. **`+ Add` 버튼 클릭**
3. **정보 입력**:
   - **Manufacturer**: `Cisco` 선택
   - **Model**: `Catalyst 9300-48P`
   - **Slug**: `catalyst-9300-48p` (자동 생성)
   - **U Height**: `1` (1U 랙 유닛)
   - **Part Number**: `C9300-48P`
   - **Description**: `48-port PoE switch`
4. **`Create` 버튼 클릭**

#### 추가 장비 타입:
- **Cisco ASR 1000** (라우터)
- **Juniper EX4300** (스위치)

---

### 6. 랙(Rack) 생성하기

물리적 랙을 정의합니다.

#### 단계:

1. **상단 메뉴**: `Devices` → `Racks` 클릭
2. **`+ Add` 버튼 클릭**
3. **정보 입력**:
   - **Site**: `Pangyo DC1` 선택
   - **Name**: `Rack-A01`
   - **Status**: `Active`
   - **Width**: `19 inches` 선택
   - **Height (U)**: `42` (표준 42U 랙)
   - **Description**: `서울 DC 1번 랙`
4. **`Create` 버튼 클릭**

**결과**: 랙이 생성되고 시각적 레이아웃을 볼 수 있습니다!

---

### 7. 장비(Device) 생성하기

실제 네트워크 장비를 추가합니다.

#### 단계:

1. **상단 메뉴**: `Devices` → `Devices` 클릭
2. **`+ Add` 버튼 클릭**
3. **정보 입력**:
   - **Name**: `pangyo-core-rt01`
   - **Device Role**: `Core Router` 선택
   - **Device Type**: `Cisco ASR 1000` 선택
   - **Site**: `pangyo DC1` 선택
   - **Rack**: `Rack-A01` 선택
   - **Position**: `40` (랙의 40U 위치)
   - **Face**: `Front` 선택
   - **Status**: `Active`
   - **Serial Number**: `FCH2XXX1234`
4. **`Create` 버튼 클릭**

**결과**: 장비가 생성되고 상세 페이지가 표시됩니다!

#### 추가 장비 생성:
- `pangyo-core-rt02` (백업 코어 라우터)
- `pangyo-dist-sw01` (분산 스위치)
- `pangyo-access-sw01` (액세스 스위치)

---

### 8. 인터페이스(Interface) 추가하기

장비에 네트워크 인터페이스를 추가합니다.

#### 단계:

1. **Devices 목록**에서 `pangyo-core-rt01` 클릭
2. **상단 탭**: `Interfaces` 클릭
3. **`+ Add Interface` 버튼 클릭**
4. **정보 입력**:
   - **Name**: `GigabitEthernet0/0/0`
   - **Type**: `1000BASE-T (1GE)` 선택
   - **Enabled**: 체크
   - **Description**: `Uplink to Distribution`
5. **`Create` 버튼 클릭**

#### 여러 인터페이스 추가 (선택사항):
- `GigabitEthernet0/0/1`
- `GigabitEthernet0/0/2`
- `Management0` (관리 포트)

---

### 9. IP 주소 할당하기

먼저 IP 프리픽스를 생성하고, 그 안에서 IP 주소를 할당합니다.

#### 9.1 프리픽스(Prefix) 생성:

1. **상단 메뉴**: `IPAM` → `Prefixes` 클릭
2. **`+ Add` 버튼 클릭**
3. **정보 입력**:
   - **Prefix**: `10.0.0.0/24`
   - **Status**: `Active`
   - **Site**: `pangyo DC1` 선택
   - **Description**: `Core Network Subnet`
4. **`Create` 버튼 클릭**

#### 9.2 IP 주소 생성:

1. **IPAM** → `IP Addresses` 클릭
2. **`+ Add` 버튼 클릭**
3. **정보 입력**:
   - **IP Address**: `10.0.0.1/24`
   - **Status**: `Active`
   - **DNS Name**: `pangyo-core-rt01.example.com`
   - **Description**: `Core Router Primary IP`
4. **`Create` 버튼 클릭**

#### 9.3 IP를 인터페이스에 할당:

1. 방금 생성한 IP 주소 `10.0.0.1/24` 클릭
2. **Edit** 버튼 클릭
3. **Assigned Object**:
   - **Device**: `pangyo-core-rt01` 선택
   - **Interface**: `GigabitEthernet0/0/0` 선택
4. **`Save` 버튼 클릭**

5. 다시 **Devices** → `pangyo-core-rt01` 페이지로 이동
6. **Edit** 버튼 클릭
7. **Primary IPv4**: `10.0.0.1/24` 선택
8. **`Save` 버튼 클릭**

**결과**: 장비에 IP 주소가 할당되고 장비 상세 페이지에서 확인할 수 있습니다!

---

### 10. VLAN 생성하기

#### 단계:

1. **상단 메뉴**: `IPAM` → `VLANs` 클릭
2. **`+ Add` 버튼 클릭**
3. **정보 입력**:
   - **Site**: `Pangyo DC1` 선택
   - **VLAN ID**: `100`
   - **Name**: `Management`
   - **Status**: `Active`
   - **Description**: `관리 VLAN`
4. **`Create` 버튼 클릭**

#### 추가 VLAN:
- **VLAN 200** - `Servers` (서버 VLAN)
- **VLAN 300** - `Voice` (음성 VLAN)

---

### 11. 케이블 연결하기

두 장비 간의 물리적 케이블 연결을 문서화합니다.

#### 준비:
먼저 두 번째 장비에도 인터페이스가 있어야 합니다.
1. `pangyo-dist-sw01` 장비 생성 (아직 안했다면)
2. 해당 장비에 `GigabitEthernet1/0/1` 인터페이스 추가

#### 케이블 연결:

1. **Devices** → `pangyo-core-rt01` → **Interfaces** 탭
2. `GigabitEthernet0/0/0` 인터페이스 클릭
3. **Connect** 버튼 (케이블 아이콘) 클릭
4. **Cable 연결 정보**:
   - **Side B Device**: `pangyo-dist-sw01` 선택
   - **Side B Interface**: `GigabitEthernet1/0/1` 선택
   - **Cable Type**: `Cat6` 선택
   - **Cable Length**: `5` (미터)
   - **Cable Color**: 원하는 색상 선택
5. **`Create` 버튼 클릭**

**결과**: 케이블 연결이 생성되고 Cable Trace 기능으로 연결 경로를 시각화할 수 있습니다!

---

### 12. 랙 시각화 확인하기

1. **Devices** → **Racks** 클릭
2. `Rack-A01` 클릭
3. **Rack Elevation** 섹션에서 시각적 랙 레이아웃 확인

**결과**: 랙에 장착된 장비들이 시각적으로 표시됩니다!

---

### 13. 태그(Tag) 사용하기

객체를 분류하고 필터링하기 위한 태그를 생성합니다.

#### 단계:

1. **상단 메뉴**: `Organization` → `Tags` 클릭
2. **`+ Add` 버튼 클릭**
3. **정보 입력**:
   - **Name**: `Production`
   - **Slug**: `production`
   - **Color**: 빨강 선택
   - **Description**: `운영 환경`
4. **`Create` 버튼 클릭**

#### 태그를 장비에 적용:

1. **Devices** → `pangyo-core-rt01` → **Edit**
2. **Tags** 필드에서 `Production` 선택
3. **`Save` 버튼 클릭**

---

### 14. 검색 및 필터링

#### 전역 검색:

1. **상단 검색 바**에 `pangyo` 입력
2. 관련된 모든 객체(장비, 사이트 등)가 검색됩니다

#### 고급 필터:

1. **Devices** → **Devices** 목록
2. **오른쪽 패널** - **Filters** 사용:
   - **Site**: `Pangyo DC1` 선택
   - **Status**: `Active` 선택
   - **Role**: `Core Router` 선택
3. **Apply** 클릭

**결과**: 조건에 맞는 장비만 표시됩니다!

---

### 15. REST API 사용해보기

NetBox는 강력한 REST API를 제공합니다.

#### API 토큰 생성:

1. **오른쪽 상단 사용자 아이콘** → **API Tokens** 클릭
2. **`+ Add Token` 버튼 클릭**
3. **Write enabled** 체크
4. **`Create` 버튼 클릭**
5. **토큰 복사** (예: `abc123def456...`)

#### API 테스트 (터미널에서):

**새 터미널 창을 열고**:

```bash
# 모든 사이트 조회
curl -H "Authorization: Token abc123def456..." \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/dcim/sites/

# 특정 장비 조회
curl -H "Authorization: Token abc123def456..." \
     http://localhost:8000/api/dcim/devices/?name=pangyo-core-rt01

# 새 사이트 생성
curl -X POST \
     -H "Authorization: Token abc123def456..." \
     -H "Content-Type: application/json" \
     -d '{"name": "Incheon DC1", "slug": "incheon-dc1", "status": "active"}' \
     http://localhost:8000/api/dcim/sites/
```

#### API 문서 확인:

브라우저에서 접속:
```
http://localhost:8000/api/docs/
```

**결과**: 전체 API 문서를 Swagger UI로 확인하고 테스트할 수 있습니다!

---

### 16. GraphQL API 사용해보기

NetBox는 GraphQL API도 지원합니다.

#### GraphQL 인터페이스:

1. 브라우저에서 접속: `http://localhost:8000/graphql/`
2. 왼쪽 패널에 다음 쿼리 입력:

```graphql
query {
  site_list {
    id
    name
    status
    description
  }
}
```

3. **실행 버튼 (▶)** 클릭
4. 오른쪽 패널에 JSON 결과가 표시됩니다

#### 복잡한 쿼리 예시:

```graphql
query {
  device_list(filters: {site: "pangyo-dc1"}) {
    id
    name
    device_type {
      manufacturer {
        name
      }
      model
    }
    primary_ip4 {
      address
    }
    interfaces {
      name
      type
    }
  }
}
```

---

### 17. 변경 로그(Change Log) 확인

모든 변경 사항이 자동으로 기록됩니다.

#### 단계:

1. **오른쪽 상단**: **사용자 아이콘** → **Activity** → **Change Log** 클릭
2. 모든 생성/수정/삭제 작업을 시간순으로 확인

#### 특정 객체의 변경 이력:

1. 아무 **Device** 상세 페이지로 이동
2. **상단 탭**: **Change Log** 클릭
3. 해당 장비의 모든 변경 이력 확인

---

### 18. 대시보드 커스터마이징

#### 단계:

1. **홈 페이지** (NetBox 로고 클릭)
2. **오른쪽 상단**: **Customize** 버튼 클릭
3. 원하는 위젯을 드래그 앤 드롭으로 배치
4. 위젯 크기 조정
5. **Save Layout** 클릭

---

### 19. CSV로 일괄 가져오기 (Bulk Import)

많은 데이터를 한 번에 입력할 수 있습니다.

#### 예시: 여러 장비를 한 번에 생성

1. **Devices** → **Devices** 목록
2. **오른쪽 상단**: **Import** 버튼 클릭
3. **CSV 데이터 입력**:

```csv
name,device_role,device_type,site,status
pangyo-access-sw02,access-switch,catalyst-9300-48p,pangyo-dc1,active
pangyo-access-sw03,access-switch,catalyst-9300-48p,pangyo-dc1,active
pangyo-access-sw04,access-switch,catalyst-9300-48p,pangyo-dc1,active
```

4. **Submit** 클릭
5. 검증 후 **Import** 버튼 클릭

**결과**: 3개의 장비가 한 번에 생성됩니다!

---

### 20. 다크 모드 전환

#### 단계:

1. **오른쪽 상단**: **사용자 아이콘** → **Preferences** 클릭
2. **User Interface** 섹션
3. **Color Mode**: `Dark` 선택
4. **Update** 버튼 클릭

**결과**: 인터페이스가 다크 모드로 전환됩니다!

---

## 문제 해결

### 문제 1: `psycopg` 설치 오류

**증상**:
```
ERROR: Failed building wheel for psycopg
```

**해결책**:
```bash
# PostgreSQL 개발 헤더 설치
brew install libpq
export LDFLAGS="-L/opt/homebrew/opt/libpq/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libpq/include"

# 다시 설치
pip install psycopg[c,pool]
```

---

### 문제 2: PostgreSQL 연결 오류

**증상**:
```
django.db.utils.OperationalError: could not connect to server
```

**해결책**:
```bash
# PostgreSQL 서비스 상태 확인
brew services list

# PostgreSQL 재시작
brew services restart postgresql@15

# 연결 테스트
psql -U netbox -d netbox -h localhost
```

---

### 문제 3: Redis 연결 오류

**증상**:
```
redis.exceptions.ConnectionError: Error connecting to Redis
```

**해결책**:
```bash
# Redis 서비스 상태 확인
brew services list

# Redis 재시작
brew services restart redis

# 연결 테스트
redis-cli ping
```

---

### 문제 4: 포트 8000이 이미 사용 중

**증상**:
```
Error: That port is already in use.
```

**해결책**:
```bash
# 다른 포트 사용
python3 manage.py runserver 8080

# 또는 기존 프로세스 종료
lsof -ti:8000 | xargs kill -9
```

---

### 문제 5: 정적 파일이 로드되지 않음

**증상**: CSS/JavaScript가 적용되지 않아 화면이 깨짐

**해결책**:
```bash
# 정적 파일 다시 수집
cd ~/Documents/netbox/netbox
python3 manage.py collectstatic --clear --noinput

# 개발 서버 재시작
python3 manage.py runserver
```

---

### 문제 6: 가상환경 활성화 안됨

**증상**: `(venv)`가 프롬프트에 표시되지 않음

**해결책**:
```bash
# 가상환경 활성화 확인
source ~/Documents/netbox/venv/bin/activate

# 프롬프트가 (venv)로 시작하는지 확인
which python
# 출력: /Users/[username]/Documents/netbox/venv/bin/python
```

---

## 추가 학습 자료

### 공식 문서
- **NetBox 공식 문서**: https://docs.netbox.dev
- **REST API 문서**: http://localhost:8000/api/docs/
- **GitHub**: https://github.com/netbox-community/netbox

### 커뮤니티
- **공식 Slack**: https://netdev.chat/
- **Discussion Forum**: https://github.com/netbox-community/netbox/discussions

### 데모 사이트
- **공식 데모**: https://demo.netbox.dev
  - Username: `demo`
  - Password: 사이트에서 확인

---

## 서비스 종료 및 재시작

### 종료:

```bash
# 개발 서버 종료 (터미널에서)
Ctrl + C

# RQ 워커 종료 (다른 터미널에서)
Ctrl + C

# 가상환경 비활성화
deactivate
```

### 재시작:

```bash
# 1. NetBox 디렉토리로 이동
cd ~/Documents/netbox/netbox

# 2. 가상환경 활성화
source ../venv/bin/activate

# 3. PostgreSQL/Redis 실행 확인
brew services list

# 4. 개발 서버 시작
python3 manage.py runserver

# 5. (새 터미널) RQ 워커 시작
cd ~/Documents/netbox/netbox
source ../venv/bin/activate
python3 manage.py rqworker
```

---

## 프로덕션 배포 (선택사항)

개발 서버는 테스트용으로만 사용하세요. 실제 운영 환경에서는 다음을 사용합니다:

1. **Gunicorn** (WSGI 서버)
2. **Nginx** (리버스 프록시)
3. **Supervisor** (프로세스 관리)

자세한 내용은 공식 문서의 "Installation" 섹션을 참고하세요:
https://docs.netbox.dev/en/stable/installation/

---

## 요약

축하합니다! 🎉 이제 NetBox를 성공적으로 설치하고 다음 기능들을 테스트했습니다:

✅ **기본 객체 생성**
- 사이트, 제조사, 장비 역할, 장비 타입
- 랙, 장비, 인터페이스

✅ **네트워크 관리**
- IP 프리픽스 및 주소
- VLAN 관리
- 케이블 연결

✅ **고급 기능**
- 태그 및 필터링
- REST API 사용
- GraphQL 쿼리
- 변경 로그
- 일괄 가져오기

✅ **사용자 인터페이스**
- 대시보드 커스터마이징
- 다크 모드
- 랙 시각화

NetBox는 매우 강력한 도구이며, 이 가이드는 시작점에 불과합니다. 공식 문서를 통해 더 많은 기능을 탐색해보세요!

---

## Linux (Ubuntu/Debian) 설치 간단 가이드

macOS 대신 Linux 환경에서 설치하려면:

### 필수 패키지 설치

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 및 필수 도구
sudo apt install -y python3 python3-pip python3-venv python3-dev git

# PostgreSQL
sudo apt install -y postgresql postgresql-contrib libpq-dev

# Redis
sudo apt install -y redis-server

# 기타 시스템 패키지
sudo apt install -y build-essential libssl-dev libffi-dev
```

### PostgreSQL 설정

```bash
# PostgreSQL 서비스 시작
sudo systemctl start postgresql
sudo systemctl enable postgresql

# NetBox 데이터베이스 생성
sudo -u postgres psql
```

```sql
CREATE DATABASE netbox;
CREATE USER netbox WITH PASSWORD 'NetBox_DB_2024!';
ALTER DATABASE netbox OWNER TO netbox;
GRANT ALL PRIVILEGES ON DATABASE netbox TO netbox;
\q
```

> **참고**: 데이터베이스 비밀번호는 `configuration.py`에서 설정해야 합니다.

### Redis 설정

```bash
# Redis 서비스 시작
sudo systemctl start redis-server
sudo systemctl enable redis-server

# 확인
redis-cli ping  # 응답: PONG
```

이후 **3단계: NetBox 설치**부터는 macOS 가이드와 동일하게 진행하면 됩니다.

---

**문서 작성일**: 2024-11-16
**NetBox 버전**: 4.4.4
**작성자**: NetBox Korean Community

질문이나 문제가 있다면 NetBox 커뮤니티나 GitHub Issues를 활용하세요!

**관련 문서**:
- [한국어 번역 가이드](../netbox/translations/ko/README.md)
- [공식 설치 문서](https://docs.netbox.dev/en/stable/installation/)
- [한국어 번역 용어 사전](../netbox/translations/ko/TERMINOLOGY.md)



#정보보안(SMS)/NetBox#
