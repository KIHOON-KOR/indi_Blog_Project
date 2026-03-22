import os
from pathlib import Path

# 환경 변수(.env) 관리를 위한 라이브러리를 가져옵니다.
import environ  # type: ignore
from datetime import (
    timedelta,
)  # 시간 간격을 계산하기 위해 가져옵니다. (JWT 만료 시간 설정용)

# 1. 기본 경로 및 환경변수 설정
BASE_DIR = (
    Path(__file__).resolve().parent.parent
)  # 현재 파일의 상위 상위 디렉토리를 프로젝트 루트(BASE_DIR)로 지정합니다.

env = environ.Env(
    DEBUG=(bool, False)
)  # 환경변수의 기본 타입과 기본값을 설정하는 객체를 생성합니다.
environ.Env.read_env(
    os.path.join(BASE_DIR, ".env")
)  # 프로젝트 루트의 .env 파일을 찾아 읽어옵니다.

SECRET_KEY = env("SECRET_KEY")  # 보안을 위해 비밀키를 환경변수에서 가져옵니다.
DEBUG = env("DEBUG")  # 디버그 모드 여부를 환경변수에서 가져옵니다.

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

AUTH_USER_MODEL = "user.User"  # 장고 기본 유저 모델 대신 커스텀 유저 모델(apps.user.User)을 사용하도록 설정합니다.

# 2. 애플리케이션 정의
DJANGO_APPS = [  # 장고 프레임워크가 기본으로 제공하는 앱 목록입니다.
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [  # 외부에서 설치한 라이브러리 앱들입니다.
    "rest_framework",  # Django Rest Framework를 사용합니다.
    "drf_spectacular",  # Swagger 문서 생성을 위한 라이브러리입니다.
    "rest_framework_simplejwt",  # JWT 인증 기능을 제공하는 라이브러리입니다.
    "storages",  # S3 연동을 위해 설치한 패키지를 활성화
]

CUSTOM_APPS = [
    "apps.user",
    "apps.post",
    "apps.series",
    "apps.tags",
    "apps.comment",
    "apps.ai",
]

INSTALLED_APPS = (
    DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS
)  # 위의 모든 앱 리스트를 하나로 합쳐 등록합니다.

MIDDLEWARE = [  # 요청과 응답 사이에서 작동하는 미들웨어 설정입니다.
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"  # 최상위 URL 설정 파일의 경로를 지정합니다.

TEMPLATES = [  # HTML 템플릿 엔진 관련 설정입니다.
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = (
    "config.wsgi.application"  # 웹 서버(WSGI)가 바라볼 애플리케이션 경로입니다.
)

# 3. 데이터베이스 (PostgreSQL)
DATABASES = {  # DB 연결 정보 설정입니다.
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # PostgreSQL 엔진을 사용합니다.
        "NAME": env("POSTGRES_DB"),  # DB 이름을 환경변수에서 가져옵니다.
        "USER": env("POSTGRES_USER"),  # 접속 계정을 환경변수에서 가져옵니다.
        "PASSWORD": env("POSTGRES_PASSWORD"),  # 비밀번호를 환경변수에서 가져옵니다.
        "HOST": os.environ.get(
            "POSTGRES_HOST", "localhost"
        ),  # 호스트 주소를 가져옵니다. (기본값 localhost)
        "PORT": env("POSTGRES_PORT"),  # 포트 번호를 환경변수에서 가져옵니다.
    }
}

# 4. 세션 설정
SESSION_ENGINE = (
    "django.contrib.sessions.backends.db"  # 세션 데이터를 데이터베이스에 저장합니다.
)
SESSION_CACHE_ALIAS = "default"  # 세션용 캐시 별칭을 지정합니다.

# 5. 패스워드 검증
AUTH_PASSWORD_VALIDATORS = [  # 유저 비밀번호 생성 시 적용될 보안 정책들입니다.
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 6. 언어 및 시간 설정
LANGUAGE_CODE = "ko-kr"  # 시스템 언어를 한국어로 설정합니다.
TIME_ZONE = "Asia/Seoul"  # 시간대를 서울로 설정합니다.
USE_I18N = True  # 국제화 기능을 사용합니다.
USE_TZ = True  # 타임존 기반 시간 처리를 활성화합니다.

# 7. 정적 파일 및 미디어 설정
STATIC_URL = "/static/"  # 웹브라우저에서 접근할 정적 파일 URL 경로입니다.
STATIC_ROOT = os.path.join(
    BASE_DIR, "staticfiles"
)  # 배포 시 정적 파일이 모이는 실제 서버 경로입니다.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]  # 개발 중 정적 파일들이 보관된 경로입니다.

MEDIA_URL = "/media/"  # 사용자가 업로드한 파일(이미지 등)에 접근할 URL 경로입니다.
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # 업로드된 파일이 저장될 실제 경로입니다.

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # 모델 생성 시 자동으로 부여되는 ID 필드 타입입니다.

# 8. DRF 설정
REST_FRAMEWORK = {  # Django Rest Framework 전역 설정입니다.
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",  # API 명세 생성을 drf-spectacular에 맡깁니다.
    "DEFAULT_PERMISSION_CLASSES": [  # 기본적으로 모든 API는 인증된 유저만 접근 가능하도록 설정합니다.
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [  # API 요청 시 사용할 인증 방식입니다. (JWT 사용)
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "EXCEPTION_HANDLER": "apps.core.exceptions.handler.custom_exception_handler",  # 에러 응답 형식을 커스텀 핸들러로 관리합니다.
}

# 9. JWT 설정
SIMPLE_JWT = {  # SimpleJWT 라이브러리 상세 설정입니다.
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=60
    ),  # 액세스 토큰의 유효 기간을 60분으로 설정합니다.
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=7
    ),  # 리프레시 토큰의 유효 기간을 7일로 설정합니다.
    "ROTATE_REFRESH_TOKENS": False,  # 리프레시 토큰 사용 시 새 토큰 발급 여부입니다.
    "BLACKLIST_AFTER_ROTATION": False,  # 토큰 로테이션 후 이전 토큰을 블랙리스트에 넣을지 여부입니다.
    "ALGORITHM": "HS256",  # 토큰 암호화 알고리즘입니다.
    "SIGNING_KEY": SECRET_KEY,  # 서명에 사용할 키입니다.
}

# 10. Swagger (drf-spectacular) 설정
SPECTACULAR_SETTINGS = {
    "TITLE": "김기훈의 개인 블로그 제작 스웨거 입니다.",  # 문서 페이지 상단 제목입니다.
    "DESCRIPTION": "김기훈의 웹 사이트 개발을 위한 API입니다.",  # 문서에 대한 설명 문구입니다.
    "VERSION": "1.0.0",  # API 버전 정보입니다.
    "SERVE_INCLUDE_SCHEMA": False,  # 스키마(YAML) 자체를 API 엔드포인트로 보여줄지 여부입니다.
    "COMPONENT_SPLIT_REQUEST": True,  # 요청과 응답 스키마를 분리해 가독성을 높입니다.
    "SWAGGER_UI_SETTINGS": {  # Swagger UI 내부 설정입니다.
        "deepLinking": True,  # 특정 API를 고유 URL로 공유 가능하게 합니다.
        "persistAuthorization": True,  # 토큰 정보를 페이지가 닫히기 전까지 유지합니다.
        "displayOperationId": True,  # 함수 고유 ID를 표시합니다.
        "filter": True,  # 검색 창을 활성화합니다.
    },
    # 이렇게 하면 DRF 설정의 JWTAuthentication을 보고 자동으로 'jwtAuth'를 만드는 것을 방지합니다.
    "AUTHENTICATION_WHITELIST": [],
    "SERVE_PERMISSIONS": [
        "rest_framework.permissions.AllowAny"
    ],  # 스웨거 문서는 누구나 볼 수 있게 합니다.
    "SECURITY": [  # 전역 보안 설정으로 아래 정의한 'BearerAuth'를 사용합니다.
        {
            "BearerAuth": [],
        }
    ],
    "APPEND_COMPONENTS": {  # 수동으로 보안 컴포넌트를 추가합니다.
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",  # HTTP 방식 인증입니다.
                "scheme": "bearer",  # 헤더 형식을 Bearer로 지정합니다.
                "bearerFormat": "JWT",  # 포맷 힌트로 JWT를 보여줍니다.
            }
        }
    },
}

# 11. 기타 설정
APPEND_SLASH = True  # URL 끝에 슬래시가 없으면 자동으로 붙여줍니다.
USE_X_FORWARDED_HOST = (
    True  # 프록시(Nginx 등) 뒤에 있을 때 호스트 주소를 올바르게 인식하도록 합니다.
)

# 커스텀 앱 설정 (인증 코드 유효시간 등)
VERIFICATION_DEFAULT_TTL_SECONDS = int(
    os.getenv("VERIFICATION_DEFAULT_TTL_SECONDS", "300")
)
VERIFICATION_TOKEN_GENERATE_MAX_ATTEMPTS = int(
    os.getenv("VERIFICATION_TOKEN_GENERATE_MAX_ATTEMPTS", "5")
)
VERIFICATION_CODE_LENGTH = int(os.getenv("VERIFICATION_CODE_LENGTH", "6"))
VERIFICATION_TOKEN_BYTES = int(os.getenv("VERIFICATION_TOKEN_BYTES", "32"))
VERIFICATION_CODE_CHARS = os.getenv("VERIFICATION_CODE_CHARS", "1234567890")


# AWS S3 기본 설정

AWS_ACCESS_KEY_ID = env(
    "AWS_ACCESS_KEY_ID"
)  # .env 파일에서 'AWS_ACCESS_KEY_ID' 값을 엄격하게 가져옵니다. 값이 누락되면 서버 실행 시 즉시 에러를 띄워줍니다.

AWS_SECRET_ACCESS_KEY = env(
    "AWS_SECRET_ACCESS_KEY"
)  # S3 접근을 위한 '비밀 액세스 키'를 가져옵니다. 외부에 절대 노출되면 안 되는 값이므로 확실하게 검증합니다.

AWS_STORAGE_BUCKET_NAME = env(
    "AWS_STORAGE_BUCKET_NAME"
)  # 이미지가 저장될 실제 '버킷 이름'을 가져옵니다.

AWS_S3_REGION_NAME = env(
    "AWS_REGION", default="ap-northeast-2"
)  # 버킷이 위치한 '리전 코드'를 가져옵니다. default 값을 설정해두면 .env에 값이 없을 때 기본값(서울 리전)으로 동작하게 하여 안정성을 높일 수 있습니다.

# 추가 옵션 설정
AWS_DEFAULT_ACL = "public-read"  # S3에 업로드된 파일에 접근할 수 있는 기본 권한을 '누구나 읽기 가능'으로 설정(블로그 썸네일이기 때문)
AWS_S3_FILE_OVERWRITE = False  # 동일한 이름의 파일이 올라오면, 기존 파일을 덮어쓰지 않고 파일명 뒤에 랜덤한 문자를 붙여서 저장 (안전성 확보)
# S3 주소 체계를 설정 (boto3가 이 형식에 맞춰 이미지 URL을 만들어줌)
AWS_S3_CUSTOM_DOMAIN = (
    f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
)

# Django 미디어 파일 저장소 변경
STORAGES = {
    # 1. 미디어 파일 (유저가 업로드하는 파일, 썸네일 등) -> S3로 보냄
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    # 2. 정적 파일 (CSS, JS 등) -> 일단 기존처럼 서버 로컬에서 처리
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# 소셜로그인
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")

# Ai 설정
GEMINI_API_KEY = env("GEMINI_API_KEY", default="")


# 배포 환경(Nginx + HTTPS)을 위한 보안 설정

# Nginx 같은 프록시 서버가 클라이언트의 HTTPS 접속을 받아서 HTTP로 넘겨줄 때,
# Django가 원래 요청이 HTTPS였음을 파악할 수 있게 헤더를 지정합니다.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# 배포 환경(DEBUG=False)일 때만 엄격한 쿠키 보안 정책을 적용합니다.
if not DEBUG:
    # 세션 쿠키를 HTTPS 연결에서만 전송하도록 강제합니다. (해커가 쿠키를 가로채는 것을 방지)
    SESSION_COOKIE_SECURE = True

    # CSRF 보안 쿠키도 HTTPS 연결에서만 전송하도록 강제합니다.
    CSRF_COOKIE_SECURE = True

    # 브라우저가 XSS 공격을 통해 쿠키(세션 등)에 접근하는 것을 자바스크립트 레벨에서 차단합니다.
    SESSION_COOKIE_HTTPONLY = True


# ==========================================
# 이메일 발송 설정 (SMTP) - Gmail

# Django에서 기본 제공하는 SMTP 이메일 발송 엔진 사용
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# 구글의 메일 서버 주소를 지정
EMAIL_HOST = "smtp.gmail.com"
# 구글 SMTP 서버와 통신하기 위한 권장 포트 번호(587)
EMAIL_PORT = 587
# 메일 전송 과정의 보안을 위해 TLS 암호화를 사용
EMAIL_USE_TLS = True

# 이메일을 발송할 구글 계정 주소
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", default="")
# 구글 계정의 '앱 비밀번호'(일반 비밀번호 아님)
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", default="")
# 수신자에게 보여질 '보내는 사람'의 기본 주소
DEFAULT_FROM_EMAIL = "블로그 관리자 <nike57793254@gmail.com>"


# 2. 캐시(Cache) 설정
CACHES = {
    "default": {  # 기본으로 사용할 캐시 설정의 이름
        "BACKEND": "django_redis.cache.RedisCache",  # django-redis 패키지의 캐시 엔진을 사용한다고 선언
        # docker-compose.yml에 적어둔 컨테이너 이름(blog_redis)을 사용
        "LOCATION": env("REDIS_URL", default=""),
        "OPTIONS": {  # Redis 연결에 필요한 세부 옵션들을 설정
            # Django와 Redis를 이어주는 기본 클라이언트 객체를 지정
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# ==========================================
# DEBUG가 True일 때(즉, 로컬 개발 환경일 때)만 Silk를 활성화
if DEBUG:
    INSTALLED_APPS.append("silk")
    MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")
