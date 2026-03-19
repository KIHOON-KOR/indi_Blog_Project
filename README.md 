<div align=center>

# 🌿 나만의 기술 블로그 플랫폼 (Coding Garden)
<div align="center">
        <img src="https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/19/82603493b2f749b4a2011163191040d3.png" alt="ERD 다이어그램" width="100%" />
</div>

---
<div align=center> 

### 🔗 <a href="https://coding-garden.site/" target="_blank"> 블로그 서비스 바로가기</a>
</div>

---
## 📖 프로젝트 소개
<div align=center>

> 본 프로젝트는 개발 학습 내용을 기록하고 공유하기 위해 직접 구축한 개인 기술 블로그 플랫폼입니다. <br>Markdown 에디터를 지원하여 편리한 글 작성이 가능하며, <br>검색 엔진 최적화(SEO)와 빠르고 직관적인 UI/UX를 통해 최적의 읽기 경험을 제공하는 것을 목표로 합니다.

</div>

---
## 🗓️ 프로젝트 기간
<div align="center">

### 2026년 2월 15일 ~ 2026년 3월 20일 (개인 프로젝트)

</div>

---
## 🛠️ 사용 스택 
<div align=center> 
    <img src="https://img.shields.io/badge/Amazon%20EC2-FF9900?style=for-the-badge&logo=Amazon%20EC2&logoColor=white">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"> 
    <img src="https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white">
    <br>
    <img src="https://img.shields.io/badge/Python_3.13-3776AB?style=for-the-badge&logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"> 
    <br>
    <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"> 
    <img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white">
    <img src="https://img.shields.io/badge/S3_Presigned_URL-569A31?style=for-the-badge&logo=Amazon%20S3&logoColor=white">
</div>

---
## 📊 ERD
<div align="center">
    <a href="https://dbdiagram.io/d/%EA%B0%9C%EC%9D%B8%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EB%B8%94%EB%A1%9C%EA%B7%B8-69746791bd82f5fce2775210" target="_blank">
        <img src="https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/19/bb6c92bd62c34bbd9d0d04e069daafaf.png" alt="ERD 다이어그램" width="100%" />
    </a>
</div>

---
## 👨‍💻 개발자 소개 

<table align="center">
  <tr>
    <td align="center" width="250px"><b>Full Stack Developer</b></td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/KIHOON-KOR">
        <img src="https://avatars.githubusercontent.com/u/221495533?v=4" width="120px" style="border-radius:50%"/>
      </a><br/>
      <b>김기훈</b><br/>
      <a href="https://github.com/KIHOON-KOR">@KIHOON-KOR</a>
    </td>
  </tr>
</table>

---
# 🖥️ 주요 기능 소개 (Key Features)

## 📝 1. 콘텐츠 및 시리즈 관리 (Content & Series)
### ` 💬 Toast UI 에디터 / 📚 시리즈 연재 / ♻️ 휴지통 및 임시저장 `

> 개발 블로그의 본질인 '글쓰기 경험'을 극대화하기 위해 에디터 편의성과 체계적인 글 관리 시스템을 구축했습니다.

<details> <summary><strong>✍️ 포스트 작성 및 관리 (Post Management)</strong></summary><br>
1. 마크다운 및 WYSIWYG 에디터

- Toast UI Editor 연동으로 직관적인 글 작성 환경 제공
- 실시간 글자 수 카운트 기능 적용

<br>
2. 임시저장 및 상태 관리

- 글 작성 중 데이터 유실 방지를 위한 자동 임시저장
- 공개/비공개 상태 전환 기능
- 삭제된 게시글 휴지통 이동 및 복구/미리보기 기능 지원

<br></details>

<details> <summary><strong>📚 시리즈 및 태그 생태계 (Series & Tags)</strong></summary><br>
1. 시리즈 (연재글) 관리

- 연관된 포스트를 하나의 시리즈로 묶어 발행
- 글 상세 페이지 내 해당 시리즈의 전체 목차 제공

<br>
2. 태그 및 필터링

- 다중 태그 설정 및 태그별 개수 카운트
- 특정 태그 클릭 시 해당 글만 모아보는 동적 필터링 구현

<br></details>

---

## ⚙️ 2. 코어 기능 및 시스템 최적화 (Core & Optimization)
### ` ☁️ S3 Presigned URL / ❤️ 동시성 제어 / 🌱 렌더링 최적화 `

> 대용량 파일 업로드와 다중 사용자 접근 시 발생할 수 있는 병목 및 데이터 정합성 문제를 해결했습니다.

<details> <summary><strong>🔗 미디어 인프라 최적화 (Image Upload)</strong></summary><br>
1. S3 Presigned URL 도입

- 백엔드 서버를 거치지 않고 프론트엔드에서 S3로 직접 이미지 업로드
- 일회성 서명된 URL 발급으로 보안 유지 및 서버 네트워크 부하 감소

<br></details>

<details> <summary><strong>🎮 게이미피케이션 및 활동 지표 (Gamification)</strong></summary><br>
1. 사용자 등급 (Tier) 및 일일 활동(잔디)

- 활동량 기반 등급 SVG 아이콘 부여 (백엔드 로직 처리)
- Github 형태의 365일 활동 그래프 제공
- 365번의 연산/조회를 1번의 쿼리로 압축하여 렌더링 최적화 달성

<br>
2. 상호작용 (좋아요 & 댓글)

- 좋아요 클릭 시 DB 인덱스(Index) 및 멱등성 설계를 통한 동시성 제어
- 댓글 CRUD 및 대댓글 구조 설계

<br></details>

---

## 🤖 3. AI 및 보안 (AI & Security)
### ` ✨ 스트리밍 AI 문체 변환 / 🔐 통합 인증 시스템 `

> 생성형 AI를 활용한 차별화된 기능과 안전한 사용자 인증 생태계를 제공합니다.

<details> <summary><strong>✨ AI 기반 문체 변환기 (AI Tone Converter)</strong></summary><br>
1. 작성 톤 앤 매너 변환

- AI 연동을 통해 작성된 본문을 '전문적인', '친근한' 등의 문체로 자동 재작성
- 토큰 제한 최적화 적용

<br>
2. 스트리밍 응답 (SSE) 처리

- AI 응답 결과를 스트리밍 방식으로 클라이언트에 전달
- 초기 응답 시간(TTFB) 단축 및 실시간 타이핑 효과로 사용자 경험(UX) 극대화

<br></details>

<details> <summary><strong>🔑 유저 인증 및 보안 (Auth & Security)</strong></summary><br>
1. 통합 로그인 시스템

- 이메일 인증을 포함한 자체 회원가입 및 비밀번호 찾기 (이메일 발송)
- Github, Discord OAuth 2.0 소셜 로그인 지원

<br>
2. 계정 정합성 관리

- 일반 계정과 소셜 계정 간 닉네임 중복 방지 처리
- 마이페이지 내 실시간 닉네임 중복 여부 검증

<br></details>

<br/>

---

# 💡 트러블 슈팅 및 회고 (Troubleshooting & Retrospective)

### 🚨 1. 좋아요 기능의 동시성 문제와 데이터 정합성 확보
* **문제:** 여러 사용자가 동시에 '좋아요'를 누르거나, 한 사용자가 짧은 시간에 여러 번 클릭할 경우(따닥 클릭), '좋아요 취소'가 정상적으로 반영되지 않거나 중복 카운트되는 데이터 정합성 문제가 발생했습니다. (03/01)
* **해결:** 단순히 서버(Application) 단에서 상태를 체크하고 업데이트하는 로직의 한계를 인지했습니다. 이를 해결하기 위해 DB 단에서 유저와 게시글 간의 조합에 **유니크 인덱스(Unique Index)**를 걸어 중복 생성을 원천 차단하고, 요청에 대한 **멱등성(Idempotency)**을 보장하도록 로직을 수정하여 동시성 이슈를 안전하게 제어했습니다.

### 🚨 2. .env 파일 유출 대처 및 보안 의식 강화
* **문제:** 프로젝트 초기 세팅 당시 실수로 DB 비밀번호 및 주요 키가 포함된 `.env` 파일이 Github에 함께 푸시된 것을 S3 연동 작업 중 뒤늦게 인지했습니다. (03/09)
* **해결:** 즉각적으로 유출된 DB 비밀번호를 변경하고, AWS IAM Access Key와 S3 Bucket 정책을 전면 재발급했습니다. 이후 `.gitignore`를 재점검하여 환경변수 파일이 철저히 배제되도록 조치했습니다. 이 경험을 통해 **'보안 사고는 코딩 실수보다 치명적이다'**는 것을 뼈저리게 느끼고, 인프라 보안의 중요성을 다잡는 계기가 되었습니다.

### ⚡ 3. 365일 활동 그래프(잔디) 렌더링 쿼리 최적화
* **문제:** 사용자의 일일 활동을 보여주는 잔디 그래프 구현 초기, 프론트에서 365일 치의 데이터를 그리기 위해 날짜별로 매번 조회를 수행하여 심각한 로딩 지연이 발생했습니다. (03/11)
* **해결:** 백엔드 쿼리를 최적화하여 365번의 연산을 1번의 쿼리로 그룹화(Aggregation)하여 전달하도록 구조를 변경했습니다. 그 결과, 불필요한 DB 커넥션과 통신 비용을 획기적으로 줄여 응답 속도를 크게 개선했습니다.

### ✨ 4. AI 문체 변환기 스트리밍 응답(SSE) 도입
* **문제:** AI를 활용해 긴 글의 문체를 변환할 때, 전체 텍스트가 완성될 때까지 사용자가 빈 화면을 보며 대기해야 하는 UX 저하 문제가 있었습니다. (03/11)
* **해결:** AI API의 응답을 한 번에 받지 않고 **스트리밍(Streaming)** 방식으로 전환하여, 생성되는 텍스트를 실시간으로 프론트에 전송했습니다. 절대적인 처리 시간은 약 2초 정도 단축되었지만, 사용자가 체감하는 대기 시간(TTFB)은 거의 0에 수렴하게 만들어 **성능 개선이 단순한 수치뿐만 아니라 사용자 경험(UX) 개선과 직결됨**을 배웠습니다.
---
# 📂 프로젝트 구조

---
```text
📦 Coding Garden
├── 📂 apps                     # 도메인별 핵심 애플리케이션 모음
│   ├── 📂 ai                   # AI 관련 기능 (글 톤(Tone) 조정 및 프롬프트 관리)
│   ├── 📂 comment              # 댓글/대댓글 CRUD 및 관리 (Services 계층 분리)
│   ├── 📂 core                 # 커스텀 예외 처리, 페이지네이션 등 전역 공통 모듈
│   ├── 📂 post                 # 게시글 기능 (CRUD, 좋아요, 임시저장, 휴지통 관리)
│   ├── 📂 series               # 시리즈(연재글) 관리 및 게시글 묶음 처리
│   ├── 📂 tags                 # 태그 등록 및 게시글별 태그 카운트
│   └── 📂 user                 # 일반/소셜 로그인, 인증, 프로필 및 마이페이지 관리
├── 📂 config                   # Django 프로젝트 전역 설정 (settings, urls)
├── 📂 monitoring               # Prometheus 등 시스템 모니터링 환경 설정
├── 📂 nginx                    # Nginx 웹 서버 및 리버스 프록시 설정
├── 📂 static                   # 정적 파일 보관소 (기본 프로필 이미지 등)
├── 📂 templates                # Django 서버 사이드 렌더링(SSR) 템플릿(HTML) 모음
│   ├── 📂 post                 # 게시글 관련 화면 (작성, 조회, 휴지통, 임시저장 등)
│   ├── 📂 series               # 시리즈 관련 화면
│   └── 📂 user                 # 로그인, 회원가입, 프로필, 비밀번호 초기화 화면
├── 📄 Dockerfile               # 웹 애플리케이션 도커 빌드 설정
├── 📄 docker-compose.yml       # 로컬 개발 환경 컨테이너 오케스트레이션
├── 📄 docker-compose.prod.yml  # 운영(배포) 환경 컨테이너 오케스트레이션
├── 📄 manage.py                # Django 관리 명령어 진입점
├── 📄 poetry.lock              # 패키지 의존성 잠금 파일
└── 📄 pyproject.toml           # Poetry 기반 의존성 및 프로젝트 환경 설정