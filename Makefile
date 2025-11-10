# Docker 관련 명령어들
.PHONY: help build build-nocache build-standalone build-prod rebuild rebuild-fresh \
	run run-dev stop clean restart logs logs-dev shell \
	compose-up compose-down compose-dev compose-logs compose-restart \
	test test-coverage test-coverage-strict docker-test \
	init-rag init-rag-force check-env check-container-env \
	test-api-feeling test-api-situation health-check docker-stats

# .env 파일에서 환경 변수를 로드합니다
ifneq (,$(wildcard .env))
include .env
export $(shell sed -n 's/^\([A-Za-z_][A-Za-z0-9_]*\)=.*/\1/p' .env)
endif

# 기본 변수
IMAGE_NAME = mixby-be-mixby-api
TAG = latest
CONTAINER_NAME = mixby-container
API_PORT ?= 8080
DEV_HOST_PORT ?= 8081
export API_PORT
export DEV_HOST_PORT

help: ## 사용 가능한 명령어들을 보여줍니다
	@echo "사용 가능한 명령어들:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Docker Compose로 이미지를 빌드합니다 (권장)
	docker-compose build

build-nocache: ## 캐시 없이 Docker Compose로 이미지를 빌드합니다
	docker-compose build --no-cache

build-standalone: ## 독립 실행형 Docker 이미지를 빌드합니다
	docker build --build-arg API_PORT=$(API_PORT) -t $(IMAGE_NAME):$(TAG) .

build-prod: ## 프로덕션용 Docker 이미지를 빌드합니다
	docker build -f Dockerfile.prod --build-arg API_PORT=$(API_PORT) -t $(IMAGE_NAME):prod .

rebuild: build compose-restart ## 이미지를 빌드하고 서비스를 재시작합니다 (빠른 개발용)

rebuild-fresh: build-nocache compose-restart ## 캐시 없이 빌드하고 서비스를 재시작합니다 (완전 재빌드)

run: ## Docker 컨테이너를 실행합니다 (.env 파일 자동 로드)
	docker run -d --name $(CONTAINER_NAME) \
		-p $(API_PORT):$(API_PORT) \
		--env-file .env \
		-e FLASK_ENV=production \
		-e API_HOST=0.0.0.0 \
		-v $(PWD)/logs:/app/logs \
		-v $(PWD)/app/data/vector_db:/app/app/data/vector_db \
		$(IMAGE_NAME):$(TAG)

run-dev: ## 개발 모드로 Docker 컨테이너를 실행합니다 (.env 파일 자동 로드)
	docker run -d --name $(CONTAINER_NAME)-dev \
		-p $(DEV_HOST_PORT):$(API_PORT) \
		--env-file .env \
		-e FLASK_ENV=development \
		-e FLASK_DEBUG=True \
		-v $(PWD):/app \
		-v $(PWD)/app/data/vector_db:/app/app/data/vector_db \
		$(IMAGE_NAME):$(TAG)

stop: ## 실행 중인 컨테이너를 중지합니다
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker stop $(CONTAINER_NAME)-dev 2>/dev/null || true

clean: ## 중지된 컨테이너와 이미지를 제거합니다
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME)-dev 2>/dev/null || true
	@docker rmi $(IMAGE_NAME):$(TAG) 2>/dev/null || true
	@docker rmi $(IMAGE_NAME):prod 2>/dev/null || true

restart: stop clean build run ## 컨테이너를 재시작합니다

logs: ## 컨테이너 로그를 확인합니다
	docker logs -f $(CONTAINER_NAME)

logs-dev: ## 개발 컨테이너 로그를 확인합니다
	docker logs -f $(CONTAINER_NAME)-dev

shell: ## 실행 중인 컨테이너에 접속합니다
	docker exec -it $(CONTAINER_NAME) /bin/bash

compose-up: ## Docker Compose로 서비스를 시작합니다 (.env 파일 자동 로드)
	docker-compose --env-file .env up -d

compose-down: ## Docker Compose 서비스를 중지합니다
	docker-compose down

compose-dev: ## Docker Compose로 개발 환경을 시작합니다 (.env 파일 자동 로드)
	docker-compose --env-file .env --profile dev up -d

compose-logs: ## Docker Compose 로그를 확인합니다
	docker-compose logs -f

compose-restart: compose-down compose-up ## Docker Compose 서비스를 재시작합니다

test: ## 로컬에서 테스트를 실행합니다
	pytest tests/ -v

test-coverage: ## 커버리지 포함 테스트를 실행합니다
	pytest tests/ -v --cov=app --cov-report=term --cov-report=html
	@echo "\n커버리지 리포트가 htmlcov/index.html에 생성되었습니다"

test-coverage-strict: ## 커버리지 임계값(80%) 검증 포함 테스트를 실행합니다
	pytest tests/ -v --cov=app --cov-report=term --cov-report=html --cov-fail-under=80
	@echo "\n커버리지가 80% 이상입니다. 리포트: htmlcov/index.html"

docker-test: ## Docker 컨테이너 내에서 테스트를 실행합니다 (.env 파일 자동 로드)
	docker run --rm -v $(PWD):/app --env-file .env $(IMAGE_NAME):$(TAG) pytest tests/ -v

health-check: ## API 헬스체크를 수행합니다
	@echo "헬스체크 수행 중..."
	@curl -f http://localhost:$(API_PORT)/health || echo "서버가 응답하지 않습니다"

docker-stats: ## Docker 컨테이너 리소스 사용량을 확인합니다
	docker stats $(CONTAINER_NAME)

init-rag: ## RAG Vector DB를 초기화합니다
	python scripts/initialize_vector_db.py

init-rag-force: ## RAG Vector DB를 강제로 재생성합니다
	python scripts/initialize_vector_db.py --force

check-env: ## 환경변수 설정을 확인합니다
	@echo "=== 환경변수 확인 ==="
	@echo "OPENAI_API_KEY: $(if $(OPENAI_API_KEY),설정됨 ($(shell echo $(OPENAI_API_KEY) | cut -c1-20)...),❌ 미설정)"
	@echo "WEATHER_API_KEY: $(if $(WEATHER_API_KEY),설정됨,❌ 미설정)"
	@echo "USE_RAG: $(USE_RAG)"
	@echo "API_PORT: $(API_PORT)"
	@echo "FLASK_ENV: $(FLASK_ENV)"
	@echo "VECTOR_DB_PATH: $(VECTOR_DB_PATH)"
	@echo "EMBEDDING_MODEL: $(EMBEDDING_MODEL)"
	@echo "RAG_TOP_K: $(RAG_TOP_K)"

check-container-env: ## 컨테이너의 환경변수를 확인합니다
	@echo "=== 컨테이너 환경변수 ==="
	@docker exec $(CONTAINER_NAME) env | grep -E "OPENAI|USE_RAG|API_PORT|FLASK_ENV|VECTOR_DB|EMBEDDING" || echo "컨테이너가 실행중이지 않습니다"

test-api-feeling: ## Feeling 추천 API를 테스트합니다
	@echo "=== Feeling 추천 API 테스트 ==="
	@curl -X POST http://localhost:$(API_PORT)/api/recommendations/feeling \
		-H "Content-Type: application/json" \
		-d '{"user_id":"test","persona":"테스트","cocktail_list":["Mojito","Margarita","Old Fashioned"],"feeling":"행복"}' | jq

test-api-situation: ## Situation 추천 API를 테스트합니다
	@echo "=== Situation 추천 API 테스트 ==="
	@curl -X POST http://localhost:$(API_PORT)/api/recommendations/situation \
		-H "Content-Type: application/json" \
		-d '{"user_id":"test","persona":"테스트","cocktail_list":["Mojito","Margarita","Old Fashioned"],"situation":"바쁨"}' | jq
