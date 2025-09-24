#!/bin/bash
set -e

# 환경 변수 기본값 설정
export FLASK_ENV=${FLASK_ENV:-production}
export API_HOST=${API_HOST:-0.0.0.0}
export API_PORT=${API_PORT:-8080}

# 로그 디렉토리 생성
mkdir -p /app/logs

# 개발 환경인지 확인
if [ "$FLASK_ENV" = "development" ]; then
    echo "Starting in development mode..."
    exec python run.py
else
    echo "Starting in production mode with Gunicorn..."
    exec gunicorn --bind $API_HOST:$API_PORT \
                  --workers 4 \
                  --timeout 120 \
                  --access-logfile /app/logs/access.log \
                  --error-logfile /app/logs/error.log \
                  --log-level info \
                  run:app
fi
