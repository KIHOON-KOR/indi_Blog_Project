import os  # 운영체제와 상호작용하기 위한 표준 라이브러리를 가져옵니다.
from pathlib import Path  # 파일 경로를 객체 단위로 편리하게 다루기 위해 가져옵니다.
import environ  # 환경 변수(.env) 관리를 위한 라이브러리를 가져옵니다.
from datetime import timedelta  # 시간 간격을 계산하기 위해 가져옵니다. (JWT 만료 시간 설정용)

# 1. 기본 경로 및 환경변수 설정
BASE_DIR = Path(__file__).resolve().parent.parent  # 현재 파일의 상위 상위 디렉토리를 프로젝트 루트(BASE_DIR)로 지정합니다.

env = environ.Env(DEBUG=(bool, False))  # 환경변수의 기본 타입과 기본값을 설정하는 객체를 생성합니다.
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))  # 프로젝트 루트의 .env 파일을 찾아 읽어옵니다.

SECRET_KEY = env("SECRET_KEY")  # 보안을 위해 비밀키를 환경변수에서 가져옵니다.
DEBUG = env("DEBUG")  # 디버그 모드 여부를 환경변수에서 가져옵니다.

ALLOWED_HOSTS = ["*"]  # 모든 호스트에서의 접속을 허용합니다. (개발 환경용 설정)

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
]

CUSTOM_APPS = [  # 기훈 님이 직접 만드신 비즈니스 로직 앱들입니다.
    "apps.user",
    "apps.post",
    "apps.series",
    "apps.tags",
    "apps.comment",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS  # 위의 모든 앱 리스트를 하나로 합쳐 등록합니다.

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
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"  # 웹 서버(WSGI)가 바라볼 애플리케이션 경로입니다.

# 3. 데이터베이스 (PostgreSQL)
DATABASES = {  # DB 연결 정보 설정입니다.
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # PostgreSQL 엔진을 사용합니다.
        "NAME": env("POSTGRES_DB"),  # DB 이름을 환경변수에서 가져옵니다.
        "USER": env("POSTGRES_USER"),  # 접속 계정을 환경변수에서 가져옵니다.
        "PASSWORD": env("POSTGRES_PASSWORD"),  # 비밀번호를 환경변수에서 가져옵니다.
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),  # 호스트 주소를 가져옵니다. (기본값 localhost)
        "PORT": env("POSTGRES_PORT"),  # 포트 번호를 환경변수에서 가져옵니다.
    }
}

# 4. 세션 설정
SESSION_ENGINE = "django.contrib.sessions.backends.db"  # 세션 데이터를 데이터베이스에 저장합니다.
SESSION_CACHE_ALIAS = "default"  # 세션용 캐시 별칭을 지정합니다.

# 5. 패스워드 검증
AUTH_PASSWORD_VALIDATORS = [  # 유저 비밀번호 생성 시 적용될 보안 정책들입니다.
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
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
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # 배포 시 정적 파일이 모이는 실제 서버 경로입니다.
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  # 개발 중 정적 파일들이 보관된 경로입니다.

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
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),  # 액세스 토큰의 유효 기간을 60분으로 설정합니다.
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # 리프레시 토큰의 유효 기간을 7일로 설정합니다.
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

    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],  # 스웨거 문서는 누구나 볼 수 있게 합니다.

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
USE_X_FORWARDED_HOST = True  # 프록시(Nginx 등) 뒤에 있을 때 호스트 주소를 올바르게 인식하도록 합니다.

# 커스텀 앱 설정 (인증 코드 유효시간 등)
VERIFICATION_DEFAULT_TTL_SECONDS = int(os.getenv("VERIFICATION_DEFAULT_TTL_SECONDS", "300"))
VERIFICATION_TOKEN_GENERATE_MAX_ATTEMPTS = int(os.getenv("VERIFICATION_TOKEN_GENERATE_MAX_ATTEMPTS", "5"))
VERIFICATION_CODE_LENGTH = int(os.getenv("VERIFICATION_CODE_LENGTH", "6"))
VERIFICATION_TOKEN_BYTES = int(os.getenv("VERIFICATION_TOKEN_BYTES", "32"))
VERIFICATION_CODE_CHARS = os.getenv("VERIFICATION_CODE_CHARS", "1234567890")

# Celery 설정 (비동기 작업용)
CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")  # 메시지 브로커 주소입니다.
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "redis://localhost:6379/0")  # 작업 결과 저장소입니다.
CELERY_ACCEPT_CONTENT = ["json"]  # 데이터 교환 시 JSON 형식을 허용합니다.
CELERY_TASK_SERIALIZER = "json"  # 작업 데이터 직렬화 방식입니다.
CELERY_RESULT_SERIALIZER = "json"  # 결과 데이터 직렬화 방식입니다.