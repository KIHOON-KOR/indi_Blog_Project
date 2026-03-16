# 파이썬 3.13의 가벼운(slim) 버전을 기반 이미지로 사용하여 컨테이너 용량을 줄입니다.
FROM python:3.13-slim

# 파이썬 출력을 버퍼링하지 않고 콘솔에 즉시 출력하도록 설정하여 로그 확인을 쉽게 합니다.
ENV PYTHONUNBUFFERED=1

# 파이썬이 불필요한 .pyc(바이트코드) 파일을 생성하지 않도록 설정하여 용량을 아낍니다.
ENV PYTHONDONTWRITEBYTECODE=1

# 컨테이너 내부에서 작업이 이루어질 기본 디렉토리를 /app으로 지정합니다.
WORKDIR /app

# 운영체제 패키지 목록을 업데이트하고 필요한 필수 시스템 패키지들을 설치합니다.
RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    gcc \
    # [최적화] 설치가 끝난 후 불필요해진 apt 캐시를 삭제하여 도커 이미지 크기를 대폭 줄입니다.
    && rm -rf /var/lib/apt/lists/*

# Poetry 패키지 관리자를 pip를 통해 설치합니다.
RUN pip install poetry

# Poetry가 가상환경(virtualenv)을 생성하지 않고 시스템(컨테이너) 전역에 패키지를 설치하도록 설정합니다. (도커 자체가 이미 격리된 환경이므로 불필요)
RUN poetry config virtualenvs.create false

# 의존성 설치에 필요한 pyproject.toml 파일과 poetry.lock 파일을 먼저 복사합니다. (캐시 활용을 위해 소스 코드보다 먼저 복사)
COPY pyproject.toml poetry.lock* /app/

# Poetry를 사용하여 의존성 패키지들을 설치합니다. (--no-root: 현재 프로젝트 자체는 설치 제외, --no-interaction: 사용자 입력 무시, --no-ansi: 색상 출력 무시)
RUN poetry install --no-root --no-interaction --no-ansi

# 나머지 모든 프로젝트 소스 코드를 도커 컨테이너 내부의 /app 디렉토리로 복사합니다.
COPY . /app/