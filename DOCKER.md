# 🐳 MIXBY API Docker 가이드

MIXBY API를 Docker 컨테이너로 실행하는 방법을 설명합니다.

## 📋 필수 조건

- Docker Desktop이 설치되어 있어야 합니다
- Docker가 실행 중이어야 합니다

## 🔌 포트 설정

이 프로젝트는 애플리케이션과 Docker 노출 포트를 모두 `API_PORT` 환경 변수 하나로 제어합니다.
기본값은 `8080`이며, 다른 포트를 사용하려면 명령을 실행하기 전에 다음과 같이 지정하세요.

```bash
export API_PORT=9090  # 원하는 포트 번호
```

또는 프로젝트 루트의 `.env` 파일에 `API_PORT=9090`을 저장하면 모든 Makefile 및 Docker Compose 명령이 자동으로 해당 값을 사용합니다.

`Makefile`, Docker Compose, 헬스체크 명령 등은 위 값을 자동으로 사용합니다.
일시적으로만 변경하려면 `API_PORT=9090 make run`처럼 명령 앞에 붙여 사용할 수도 있습니다.
개발용 컨테이너의 호스트 포트가 필요하면 `DEV_HOST_PORT`(기본 8081)도 함께 조정할 수 있습니다.

## 🚀 빠른 시작

### 1. Docker Compose 사용 (권장)

```bash
# 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down
```

### 2. Makefile 사용

```bash
# 사용 가능한 명령어 확인
make help

# 이미지 빌드 및 실행
make build
make run

# 헬스체크
make health-check

# 로그 확인
make logs

# 정리
make clean
```

### 3. 직접 Docker 명령어 사용

```bash
# 이미지 빌드
docker build -t mixby-api:latest .

# 컨테이너 실행 (실행 전 API_PORT를 원하는 값으로 설정)
export API_PORT=8080   # 필요한 경우 다른 포트로 변경
docker run -d --name mixby-container -p $API_PORT:$API_PORT -e API_PORT=$API_PORT mixby-api:latest

# 헬스체크
curl http://localhost:$API_PORT/health
```

## 📂 환경별 실행

### 개발 환경

```bash
# 개발 모드로 실행 (코드 변경 시 자동 재시작)
make run-dev

# 또는 Docker Compose 개발 프로필 사용
docker-compose --profile dev up -d
```

### 프로덕션 환경

```bash
# 프로덕션 이미지 빌드
make build-prod

# Gunicorn으로 실행
# API_PORT가 원하는 값으로 설정되어 있다고 가정합니다
docker run -d --name mixby-prod \
  -p $API_PORT:$API_PORT \
  -e FLASK_ENV=production \
  -e API_PORT=$API_PORT \
  mixby-api:prod
```

## 🔧 환경 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `FLASK_ENV` | `production` | Flask 환경 설정 |
| `API_HOST` | `0.0.0.0` | API 서버 호스트 |
| `API_PORT` | `8080` | API 및 Docker 노출 포트 (단일 변수) |
| `LOG_LEVEL` | `INFO` | 로그 레벨 |
| `SECRET_KEY` | 자동 생성 | Flask 비밀 키 |
| `CORS_ORIGINS` | `*` | CORS 허용 도메인 |

## 📊 모니터링

### 헬스체크

```bash
# API 헬스체크
curl http://localhost:$API_PORT/health

# Docker 헬스체크 상태 확인
docker ps
```

### 로그 확인

```bash
# 실시간 로그
docker logs -f mixby-container

# 또는 Makefile 사용
make logs
```

### 리소스 사용량

```bash
# 컨테이너 리소스 사용량
make docker-stats
```

## 🧪 테스트

### 컨테이너 내 테스트

```bash
# Docker 환경에서 테스트 실행
make docker-test
```

### API 엔드포인트 테스트

```bash
# 기본 API 테스트
curl http://localhost:$API_PORT/drink/all
curl http://localhost:$API_PORT/recipe/random
curl "http://localhost:$API_PORT/drink/name=위스키"
```

## 🔄 볼륨 마운트

### 로그 파일 보존

```bash
# 로그 디렉토리 마운트
docker run -d \
  --name mixby-container \
  -p $API_PORT:$API_PORT \
  -e API_PORT=$API_PORT \
  -v $(pwd)/logs:/app/logs \
  mixby-api:latest
```

### 개발 시 코드 동기화

```bash
# 코드 변경 사항 실시간 반영
docker run -d \
  --name mixby-dev \
  -p ${DEV_HOST_PORT:-8081}:$API_PORT \
  -e FLASK_ENV=development \
  -e FLASK_DEBUG=True \
  -e API_PORT=$API_PORT \
  -v $(pwd):/app \
  mixby-api:latest
```

## 🐛 문제 해결

### 컨테이너가 시작되지 않는 경우

```bash
# 컨테이너 로그 확인
docker logs mixby-container

# 컨테이너 내부 접속
docker exec -it mixby-container /bin/bash
```

### 포트 충돌 문제

```bash
# 다른 포트로 실행 (명령 앞에 API_PORT를 지정)
API_PORT=9090 make run
# 또는
API_PORT=9090 docker-compose up -d
```

### 이미지 크기 최적화

```bash
# 프로덕션 최적화 이미지 사용
docker build -f Dockerfile.prod -t mixby-api:prod .
```

## 📝 유용한 명령어

```bash
# 모든 명령어 보기
make help

# 전체 재시작
make restart

# 개발 환경 시작
make compose-dev

# 정리 (컨테이너 + 이미지 삭제)
make clean

# Docker 시스템 정리
docker system prune -f
```

## 🚀 배포

### 이미지 레지스트리에 푸시

```bash
# 이미지 태그
docker tag mixby-api:latest your-registry/mixby-api:latest

# 푸시
docker push your-registry/mixby-api:latest
```

### Kubernetes 배포 예시

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mixby-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mixby-api
  template:
    metadata:
      labels:
        app: mixby-api
    spec:
      containers:
      - name: mixby-api
        image: mixby-api:latest
        ports:
        - containerPort: <SERVER_PORT>
        env:
        - name: FLASK_ENV
          value: "production"
        livenessProbe:
          httpGet:
            path: /health
            port: <SERVER_PORT>
          initialDelaySeconds: 30
          periodSeconds: 10
```

이제 Docker를 사용하여 MIXBY API를 어디서든 쉽게 실행할 수 있습니다! 🎉
