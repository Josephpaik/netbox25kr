<div align="center">
  <img src="https://raw.githubusercontent.com/netbox-community/netbox/main/docs/netbox_logo_light.svg" width="400" alt="NetBox 로고" />
  <p><strong>모든 자동화 네트워크의 초석</strong></p>
  <a href="https://github.com/netbox-community/netbox/releases"><img src="https://img.shields.io/github/v/release/netbox-community/netbox" alt="최신 릴리스" /></a>
  <a href="https://github.com/netbox-community/netbox/blob/main/LICENSE.txt"><img src="https://img.shields.io/badge/license-Apache_2.0-blue.svg" alt="라이선스" /></a>
  <a href="https://github.com/netbox-community/netbox/graphs/contributors"><img src="https://img.shields.io/github/contributors/netbox-community/netbox?color=blue" alt="기여자" /></a>
  <a href="https://github.com/netbox-community/netbox/stargazers"><img src="https://img.shields.io/github/stars/netbox-community/netbox?style=flat" alt="GitHub 스타" /></a>
  <a href="https://explore.transifex.com/netbox-community/netbox/"><img src="https://img.shields.io/badge/languages-15-blue" alt="지원 언어" /></a>
  <a href="https://github.com/netbox-community/netbox/actions/workflows/ci.yml"><img src="https://github.com/netbox-community/netbox/actions/workflows/ci.yml/badge.svg" alt="CI 상태" /></a>
  <p>
    <strong><a href="https://netboxlabs.com/community/">NetBox Community</a></strong> |
    <strong><a href="https://netboxlabs.com/netbox-cloud/">NetBox Cloud</a></strong> |
    <strong><a href="https://netboxlabs.com/netbox-enterprise/">NetBox Enterprise</a></strong>
  </p>
</div>

NetBox는 네트워크 엔지니어에게 힘을 실어주기 위해 존재합니다. 2016년 출시 이후, 전 세계 수천 개 조직에서 네트워크 인프라를 모델링하고 문서화하는 솔루션으로 자리잡았습니다. 레거시 IPAM 및 DCIM 애플리케이션의 후속작으로서, NetBox는 모든 네트워크 관련 요소에 대한 일관성 있고 광범위하며 접근 가능한 데이터 모델을 제공합니다. 케이블 맵부터 장치 구성까지 모든 것에 대한 강력한 사용자 인터페이스와 프로그래밍 API를 제공함으로써, NetBox는 현대 네트워크의 중앙 정보 원천 역할을 합니다.

<p align="center">
  <a href="#netbox의-역할">NetBox의 역할</a> |
  <a href="#왜-netbox인가">왜 NetBox인가?</a> |
  <a href="#시작하기">시작하기</a> |
  <a href="#참여하기">참여하기</a> |
  <a href="#스크린샷">스크린샷</a>
</p>

<p align="center">
  <img src="docs/media/screenshots/home-light.png" width="600" alt="NetBox 사용자 인터페이스 스크린샷" />
</p>

## NetBox의 역할

NetBox는 네트워크 인프라의 **정보 원천(Source of Truth)**으로 작동합니다. 모든 네트워크 구성 요소와 리소스의 _의도된 상태_를 정의하고 검증하는 것이 NetBox의 역할입니다. NetBox는 네트워크 노드와 직접 상호작용하지 않으며, 대신 이 데이터를 전용 자동화, 모니터링 및 보증 도구에 프로그래밍 방식으로 제공합니다. 이러한 역할 분리를 통해 강력하면서도 유연한 자동화 시스템을 구축할 수 있습니다.

<p align="center">
  <img src="docs/media/misc/reference_architecture.png" alt="참조 네트워크 자동화 아키텍처" />
</p>

위 다이어그램은 NetBox를 네트워크 상태의 중앙 권한으로 활용하는 자동화 네트워크의 권장 배포 아키텍처를 보여줍니다. 이 접근 방식을 통해 팀은 예측 가능하고 모듈화된 워크플로를 유지하면서 변화하는 요구사항에 맞춰 개별 도구를 교체할 수 있습니다.

## 왜 NetBox인가?

### 포괄적인 데이터 모델

랙, 장치, 케이블, IP 주소, VLAN, 회선, 전원, VPN 등: NetBox는 네트워크를 위해 만들어졌습니다. 포괄적이고 철저하게 상호 연결된 데이터 모델은 범용 도구로는 불가능한 다양한 네트워크 기본 요소의 자연스럽고 고도로 구조화된 모델링을 제공합니다. 데이터베이스 구축 방법을 고민할 필요가 없습니다. 설치 즉시 모든 것이 준비되어 있습니다.

### 집중적인 개발

NetBox는 단 하나의 목표를 달성하고자 합니다: 네트워크 인프라를 프로그래밍 방식으로 접근할 수 있도록 하는 최고의 솔루션을 제공하는 것입니다. 모든 기능을 체크하려고 어설프게 기능을 추가하는 "올인원" 도구와 달리, NetBox는 핵심 기능에 전념합니다. NetBox는 네트워크 인프라 모델링을 위한 최상의 솔루션을 제공하며, 네트워크 자동화의 다른 영역에서 뛰어난 도구와 통합할 수 있는 풍부한 API를 제공합니다.

### 확장 가능하고 커스터마이징 가능

두 개의 네트워크가 완전히 동일하지는 않습니다. 사용자는 고유한 요구사항에 맞게 사용자 정의 필드와 태그를 사용하여 NetBox의 기본 데이터 모델을 확장할 수 있습니다. 심지어 완전히 새로운 객체와 기능을 도입하는 자체 플러그인을 작성할 수도 있습니다!

### 유연한 권한 관리

NetBox는 완전히 커스터마이징 가능한 권한 시스템을 포함하고 있어, 관리자가 사용자와 그룹에 역할을 할당할 때 매우 세밀한 제어가 가능합니다. 특정 사용자를 케이블링 작업만 할 수 있도록 제한하고 IP 주소는 변경하지 못하게 하고 싶으신가요? 또는 각 팀이 특정 테넌트에만 접근하도록 하고 싶으신가요? NetBox를 사용하면 원하는 대로 역할을 설정할 수 있습니다.

### 사용자 정의 검증 및 보호 규칙

NetBox에 입력하는 데이터는 네트워크 운영에 매우 중요합니다. 강력한 기본 검증 규칙 외에도, NetBox는 관리자가 객체에 대한 자체 사용자 정의 검증 규칙을 정의할 수 있는 메커니즘을 제공합니다. 사용자 정의 검증은 새로운 객체나 수정된 객체가 규칙 세트를 준수하는지 확인하고, 특정 기준을 충족하지 않는 객체의 삭제를 방지하는 데 사용할 수 있습니다. (예를 들어, "활성" 상태인 장치의 삭제를 방지할 수 있습니다.)

### 장치 구성 렌더링

NetBox는 자체 데이터에서 장치 구성을 생성하기 위해 사용자가 만든 Jinja2 템플릿을 렌더링할 수 있습니다. 구성 템플릿은 개별적으로 업로드하거나 Git 저장소와 같은 외부 소스에서 자동으로 가져올 수 있습니다. 렌더링된 구성은 Ansible 또는 Salt와 같은 프로비저닝 도구를 통해 네트워크 장치에 직접 적용하기 위해 REST API를 통해 검색할 수 있습니다.

### 사용자 정의 스크립트

새 지점 사무실 프로비저닝과 같은 복잡한 워크플로는 사용자 인터페이스를 통해 수행하기에 번거로울 수 있습니다. NetBox를 사용하면 UI에서 직접 실행할 수 있는 사용자 정의 스크립트를 작성하고 업로드할 수 있습니다. 스크립트는 사용자에게 입력을 요청한 다음 필요한 작업을 자동화하여 부담스러운 프로세스를 크게 단순화합니다.

### 자동화된 이벤트

사용자는 NetBox 이벤트에 대응하여 사용자 정의 스크립트 또는 아웃바운드 웹훅을 자동으로 트리거하는 이벤트 규칙을 정의할 수 있습니다. 예를 들어, NetBox에 새 장치가 추가될 때 네트워크 모니터링 서비스를 자동으로 업데이트하거나 IP 범위가 할당될 때 DHCP 서버를 업데이트할 수 있습니다.

### 포괄적인 변경 로그

NetBox는 모든 관리 객체의 생성, 수정 및 삭제를 자동으로 기록하여 철저한 변경 이력을 제공합니다. 변경 사항은 실행 사용자에게 귀속될 수 있으며, 관련 변경 사항은 요청 ID별로 자동으로 그룹화됩니다.

> [!NOTE]
> NetBox의 다양한 기능의 전체 목록은 [소개 문서](https://docs.netbox.dev/en/stable/introduction/)에서 확인할 수 있습니다.

## 시작하기

* 단순히 둘러보고 싶으신가요? [공개 데모](https://demo.netbox.dev/)를 지금 바로 확인하세요!
* [공식 문서](https://docs.netbox.dev)는 포괄적인 소개를 제공합니다.
* **한글 가이드**:
  * [빠른 시작 가이드 (10분)](docs/QUICKSTART_KR.md) - Linux/Ubuntu 환경에서 빠르게 시작
  * [상세 설치 및 사용 가이드](docs/NetBox%20macOS%20설치%20및%20사용%20가이드%20(한글).md) - macOS 및 Linux 설치 상세 안내
  * [한국어 번역 가이드](netbox/translations/ko/README.md) - 한국어 번역 기여 방법
* [위키](https://github.com/netbox-community/netbox/wiki/Community-Contributions)에서 NetBox를 최대한 활용하기 위한 더 많은 프로젝트를 확인하세요!

## 한글 버전 빠른 설치

```bash
# 1. 필수 패키지 설치 (Ubuntu/Debian)
sudo apt install -y python3 python3-venv git postgresql redis-server

# 2. NetBox 클론 및 설정
git clone https://github.com/netbox-community/netbox.git
cd netbox/netbox
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 데이터베이스 생성 (비밀번호: NetBox_DB_2024!)
sudo -u postgres psql << EOF
CREATE DATABASE netbox;
CREATE USER netbox WITH PASSWORD 'NetBox_DB_2024!';
ALTER DATABASE netbox OWNER TO netbox;
GRANT ALL PRIVILEGES ON DATABASE netbox TO netbox;
EOF

# 4. 설정 및 초기화
cp netbox/configuration_example.py netbox/configuration.py
# configuration.py 편집:
# - DATABASE['PASSWORD'] = 'NetBox_DB_2024!'
# - SECRET_KEY 생성 및 설정
# - ALLOWED_HOSTS 설정

python3 manage.py migrate

# 슈퍼유저 생성 (웹 로그인용 - 비밀번호: Admin2024!Pass)
python3 manage.py createsuperuser
# Username: admin
# Password: Admin2024!Pass (10자 이상)

python3 manage.py collectstatic --noinput

# 5. 한국어 번역 컴파일 ⭐
python3 manage.py compilemessages -l ko

# 6. 서버 실행
python3 manage.py runserver 0.0.0.0:8000
```

**브라우저에서**: http://localhost:8000 → 로그인 (admin / Admin2024!Pass) → Preferences → Language: Korean

> **⚠️ 비밀번호 구분**:
> - **DB 비밀번호** (`NetBox_DB_2024!`): PostgreSQL 연결용 (configuration.py에 저장)
> - **웹 로그인 비밀번호** (`Admin2024!Pass`): NetBox 웹 UI 로그인용 (10자 이상 권장)

자세한 내용은 [한글 빠른 시작 가이드](docs/QUICKSTART_KR.md)를 참조하세요.

## 참여하기

* Twitter에서 [@NetBoxOfficial](https://twitter.com/NetBoxOfficial)을 팔로우하세요!
* [토론 포럼](https://github.com/netbox-community/netbox/discussions) 및 [Slack](https://netdev.chat/)에서 대화에 참여하세요!
* 이미 파워 유저이신가요? GitHub에서 [기능 제안](https://github.com/netbox-community/netbox/issues/new?assignees=&labels=type%3A+feature&template=feature_request.yaml) 또는 [버그 보고](https://github.com/netbox-community/netbox/issues/new?assignees=&labels=type%3A+bug&template=bug_report.yaml)를 할 수 있습니다.
* 커뮤니티의 기여를 환영하고 감사드립니다! [기여 가이드](CONTRIBUTING.md)를 확인하여 시작하세요.
* **한국어 번역 기여**: [한국어 번역 가이드](netbox/translations/ko/README.md)를 참조하세요.

## 스크린샷

<p align="center">
  <strong>NetBox 대시보드 (라이트 모드)</strong><br />
  <img src="docs/media/screenshots/home-light.png" width="600" alt="NetBox 대시보드 (라이트 모드)" />
</p>
<p align="center">
  <strong>NetBox 대시보드 (다크 모드)</strong><br />
  <img src="docs/media/screenshots/home-dark.png" width="600" alt="NetBox 대시보드 (다크 모드)" />
</p>
<p align="center">
  <strong>프리픽스 목록</strong><br />
  <img src="docs/media/screenshots/prefixes-list.png" width="600" alt="프리픽스 목록" />
</p>
<p align="center">
  <strong>랙 뷰</strong><br />
  <img src="docs/media/screenshots/rack.png" width="600" alt="랙 뷰" />
</p>
<p align="center">
  <strong>케이블 추적</strong><br />
  <img src="docs/media/screenshots/cable-trace.png" width="600" alt="케이블 추적" />
</p>

---

## 라이선스

NetBox는 Apache 2.0 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE.txt](LICENSE.txt)를 참조하세요.

## 한국어 커뮤니티

NetBox 한국어 사용자 커뮤니티에 오신 것을 환영합니다!

- **번역 기여**: [Transifex](https://www.transifex.com/netbox-community/netbox/)에서 한국어 번역에 참여하세요
- **문의 및 지원**: GitHub Issues 또는 Slack #netbox 채널 활용
- **문서**: [한글 설치 가이드](docs/QUICKSTART_KR.md) | [번역 가이드](netbox/translations/ko/README.md)

---

**NetBox Version**: 4.4.4
**문서 업데이트**: 2024-11-16
**한글 문서 관리**: NetBox Korean Community
