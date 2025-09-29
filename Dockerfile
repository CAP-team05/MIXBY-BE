# Python 3.10 slim 이미지 사용 (경량화)
FROM python:3.10-slim

ARG SERVER_PORT=8080

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# Entrypoint 스크립트 복사 및 권한 설정 (USER 설정 전)
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# 비-root 사용자 생성 (보안)
RUN adduser --disabled-password --gecos '' --uid 1000 mixby && \
    chown -R mixby:mixby /app
USER mixby

# 환경 변수 설정
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV SERVER_PORT=${SERVER_PORT}

# 포트 노출
EXPOSE ${SERVER_PORT}

# 헬스체크 추가
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${SERVER_PORT:-8080}/health || exit 1

# 애플리케이션 실행
ENTRYPOINT ["docker-entrypoint.sh"]
