# NetBox 한글 버전 빠른 시작 가이드

> **10분 만에 한글 NetBox 시작하기**

이 가이드는 Linux/Ubuntu 환경에서 NetBox를 빠르게 설치하고 한글로 사용하는 방법을 안내합니다.

## 전제 조건

- Ubuntu 20.04 이상 또는 Debian 11 이상
- sudo 권한
- 최소 4GB RAM

## 빠른 설치 (Linux/Ubuntu)

### 1. 시스템 패키지 설치 (3분)

```bash
# 시스템 업데이트
sudo apt update

# 필수 패키지 설치
sudo apt install -y python3 python3-pip python3-venv python3-dev git \
    postgresql postgresql-contrib libpq-dev redis-server \
    build-essential libssl-dev libffi-dev

# 서비스 시작
sudo systemctl start postgresql redis-server
sudo systemctl enable postgresql redis-server
```

### 2. 데이터베이스 설정 (2분)

```bash
# PostgreSQL 데이터베이스 생성
sudo -u postgres psql << EOF
CREATE DATABASE netbox;
CREATE USER netbox WITH PASSWORD 'netbox123';
ALTER DATABASE netbox OWNER TO netbox;
GRANT ALL PRIVILEGES ON DATABASE netbox TO netbox;
EOF

# Redis 확인
redis-cli ping  # 응답: PONG
```

### 3. NetBox 다운로드 및 설치 (3분)

```bash
# 작업 디렉토리 생성
mkdir -p ~/netbox && cd ~/netbox

# NetBox 클론 (현재 리포지토리 사용)
git clone https://github.com/netbox-community/netbox.git .
cd netbox

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. NetBox 설정 (2분)

```bash
# 설정 파일 생성
cd netbox
cp netbox/configuration_example.py netbox/configuration.py

# SECRET_KEY 생성
SECRET_KEY=$(python3 ../generate_secret_key.py)

# 설정 파일 자동 수정
cat > netbox/configuration.py << EOF
ALLOWED_HOSTS = ['*']

DATABASE = {
    'NAME': 'netbox',
    'USER': 'netbox',
    'PASSWORD': 'netbox123',
    'HOST': 'localhost',
    'PORT': '',
    'CONN_MAX_AGE': 300,
}

REDIS = {
    'tasks': {
        'HOST': 'localhost',
        'PORT': 6379,
        'PASSWORD': '',
        'DATABASE': 0,
    },
    'caching': {
        'HOST': 'localhost',
        'PORT': 6379,
        'PASSWORD': '',
        'DATABASE': 1,
    }
}

SECRET_KEY = '$SECRET_KEY'
DEBUG = True
TIME_ZONE = 'Asia/Seoul'
EOF
```

### 5. 데이터베이스 초기화 및 관리자 생성 (2분)

```bash
# 마이그레이션 실행
python3 manage.py migrate

# 슈퍼유저 생성 (대화형)
python3 manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123 (입력 시 보이지 않음)

# 또는 비대화형으로:
# DJANGO_SUPERUSER_PASSWORD=admin123 python3 manage.py createsuperuser --noinput --username admin --email admin@example.com

# 정적 파일 수집
python3 manage.py collectstatic --noinput
```

### 6. 한국어 번역 컴파일 ⭐

```bash
# 한국어 번역 컴파일
python3 manage.py compilemessages -l ko

# 성공 메시지 확인
# processing file django.po in .../translations/ko/LC_MESSAGES
```

### 7. NetBox 실행

```bash
# 개발 서버 시작
python3 manage.py runserver 0.0.0.0:8000

# 새 터미널에서 백그라운드 워커 실행 (선택사항)
# cd ~/netbox/netbox
# source ../venv/bin/activate
# python3 manage.py rqworker
```

## 한글 UI로 변경하기

1. **브라우저로 접속**: http://localhost:8000 (또는 서버 IP:8000)
2. **로그인**: admin / admin123
3. **사용자 메뉴 클릭** (오른쪽 상단)
4. **Preferences** 선택
5. **Language**: `Korean (한국어)` 선택
6. **Update** 클릭 후 **페이지 새로고침 (F5)**

**완료!** 🎉 NetBox가 한글로 표시됩니다!

## 첫 데이터 입력해보기

한글 UI에서 다음 순서로 테스트해보세요:

```
1. 조직 → 사이트 → 추가
   - 이름: 서울 데이터센터
   - 상태: 활성

2. 장치 → 제조사 → 추가
   - 이름: Cisco

3. 장치 → 장치 역할 → 추가
   - 이름: 코어 라우터
   - 색상: 빨강

4. 장치 → 장치 타입 → 추가
   - 제조사: Cisco
   - 모델: ASR-1000

5. 장치 → 장치 → 추가
   - 이름: seoul-router-01
   - 사이트: 서울 데이터센터
   - 장치 역할: 코어 라우터
   - 장치 타입: ASR-1000
```

## 유용한 명령어

```bash
# 서버 재시작
cd ~/netbox/netbox
source ../venv/bin/activate
python3 manage.py runserver 0.0.0.0:8000

# 번역 업데이트
python3 manage.py makemessages -l ko -i "project-static/*"
python3 manage.py compilemessages -l ko

# 번역 상태 확인
grep -c 'msgstr ""' translations/ko/LC_MESSAGES/django.po  # 미번역 개수
```

## 문제 해결

### PostgreSQL 연결 오류
```bash
sudo systemctl restart postgresql
sudo -u postgres psql -c "SELECT version();"
```

### Redis 연결 오류
```bash
sudo systemctl restart redis-server
redis-cli ping
```

### 한글이 표시되지 않을 때
```bash
# 번역 재컴파일
cd ~/netbox/netbox
python3 manage.py compilemessages -l ko

# 서버 재시작 (Ctrl+C 후)
python3 manage.py runserver 0.0.0.0:8000

# 브라우저 캐시 삭제 (Ctrl+Shift+R)
```

## 다음 단계

- **상세 가이드**: [NetBox 설치 및 사용 가이드](NetBox%20macOS%20설치%20및%20사용%20가이드%20(한글).md)
- **번역 기여**: [한국어 번역 가이드](../netbox/translations/ko/README.md)
- **공식 문서**: https://docs.netbox.dev
- **커뮤니티**: https://github.com/netbox-community/netbox/discussions

## 프로덕션 배포

개발 서버는 테스트용입니다. 실제 운영 환경에서는:
- Gunicorn/uWSGI 사용
- Nginx 리버스 프록시 설정
- Systemd 서비스 등록
- HTTPS 인증서 설정

자세한 내용은 [공식 설치 문서](https://docs.netbox.dev/en/stable/installation/)를 참조하세요.

---

**문서 버전**: 1.0
**최종 수정**: 2024-11-16
**NetBox 버전**: 4.4.4

**도움이 필요하신가요?**
- GitHub Issues: https://github.com/netbox-community/netbox/issues
- Slack: https://netdev.chat (채널: #netbox)
