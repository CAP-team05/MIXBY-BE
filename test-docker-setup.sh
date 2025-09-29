#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
if [ -f "$SCRIPT_DIR/.env" ]; then
    set -a
    . "$SCRIPT_DIR/.env"
    set +a
fi

API_PORT=${API_PORT:-8080}

echo "🐳 MIXBY Docker 설정 검증 스크립트"
echo "=================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 체크 함수
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 파일 존재"
        return 0
    else
        echo -e "${RED}✗${NC} $1 파일 없음"
        return 1
    fi
}

check_executable() {
    if [ -x "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 실행 권한 있음"
        return 0
    else
        echo -e "${RED}✗${NC} $1 실행 권한 없음"
        return 1
    fi
}

echo -e "\n📁 Docker 파일 검증"
echo "-------------------"
check_file "Dockerfile"
check_file "Dockerfile.prod"
check_file "docker-compose.yml"
check_file ".dockerignore"
check_file "docker-entrypoint.sh"
check_file "Makefile"
check_file "DOCKER.md"
check_executable "docker-entrypoint.sh"

echo -e "\n🔧 환경 설정 검증"
echo "-------------------"
check_file "requirements.txt"
check_file "run.py"
check_file "app/__init__.py"

echo -e "\n📦 패키지 검증"
echo "---------------"
if grep -q "gunicorn" requirements.txt; then
    echo -e "${GREEN}✓${NC} Gunicorn이 requirements.txt에 포함됨"
else
    echo -e "${RED}✗${NC} Gunicorn이 requirements.txt에 없음"
fi

if grep -q "Flask-CORS" requirements.txt; then
    echo -e "${GREEN}✓${NC} Flask-CORS가 requirements.txt에 포함됨"
else
    echo -e "${RED}✗${NC} Flask-CORS가 requirements.txt에 없음"
fi

echo -e "\n🐳 Docker 데몬 상태 확인"
echo "------------------------"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker CLI 설치됨"
    
    if docker info &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker 데몬 실행 중"
        DOCKER_RUNNING=true
    else
        echo -e "${YELLOW}⚠${NC} Docker 데몬이 실행되지 않음"
        echo "  Docker Desktop을 시작해주세요"
        DOCKER_RUNNING=false
    fi
else
    echo -e "${RED}✗${NC} Docker가 설치되지 않음"
    echo "  https://docker.com에서 Docker Desktop을 다운로드하세요"
    DOCKER_RUNNING=false
fi

echo -e "\n🧪 로컬 테스트 실행"
echo "-------------------"
if python3 -c "import app" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Python 애플리케이션 import 성공"
else
    echo -e "${RED}✗${NC} Python 애플리케이션 import 실패"
    echo "  pip install -r requirements.txt 를 실행해보세요"
fi

echo -e "\n📋 Docker 사용 가이드"
echo "====================="
echo "Docker Desktop을 시작한 후, 다음 명령어를 실행하세요:"
echo ""
echo -e "${YELLOW}1. 이미지 빌드 및 실행:${NC}"
echo "   make build"
echo "   make run"
echo ""
echo -e "${YELLOW}2. 또는 Docker Compose 사용:${NC}"
echo "   docker-compose up -d"
echo ""
echo -e "${YELLOW}3. 헬스체크:${NC}"
echo "   make health-check"
echo "   또는 브라우저에서 http://localhost:${API_PORT}/health"
echo ""
echo -e "${YELLOW}4. 로그 확인:${NC}"
echo "   make logs"
echo ""
echo -e "${YELLOW}5. 정리:${NC}"
echo "   make clean"
echo ""

if [ "$DOCKER_RUNNING" = true ]; then
    echo -e "${GREEN}🎉 Docker가 실행 중입니다! 위 명령어들을 바로 사용할 수 있습니다.${NC}"
else
    echo -e "${YELLOW}⚠️  Docker Desktop을 시작한 후 위 명령어들을 사용하세요.${NC}"
fi

echo -e "\n자세한 내용은 DOCKER.md 파일을 참고하세요."
