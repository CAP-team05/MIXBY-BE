# Docker 관련 명령어들
.PHONY: help build run stop clean dev test docker-test

# .env 파일 자동 로드
ifneq (,$(wildcard .env))
include .env
export $(shell sed -n 's/^\([A-Za-z_][A-Za-z0-9_]*\)=.*/\1/p' .env)
endif

# 기본 변수
IMAGE_NAME = mixby-api
TAG = latest
CONTAINER_NAME = mixby-container
SERVER_PORT ?= 8080
DEV_HOST_PORT ?= 8081

help: ## 사용 가능한 명령어들을 보여줍니다
	@echo "사용 가능한 명령어들:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Docker 이미지를 빌드합니다
	docker build -t $(IMAGE_NAME):$(TAG) .

build-prod: ## 프로덕션용 Docker 이미지를 빌드합니다
	docker build -f Dockerfile.prod -t $(IMAGE_NAME):prod .

run: ## Docker 컨테이너를 실행합니다
	docker run -d --name $(CONTAINER_NAME) \
		-p $(SERVER_PORT):$(SERVER_PORT) \
		-e SERVER_PORT=$(SERVER_PORT) \
		-e API_PORT=$(SERVER_PORT) \
		$(IMAGE_NAME):$(TAG)

run-dev: ## 개발 모드로 Docker 컨테이너를 실행합니다
	docker run -d --name $(CONTAINER_NAME)-dev \
		-p $(DEV_HOST_PORT):$(SERVER_PORT) \
		-e FLASK_ENV=development \
		-e FLASK_DEBUG=True \
		-e SERVER_PORT=$(SERVER_PORT) \
		-e API_PORT=$(SERVER_PORT) \
		-v $(PWD):/app \
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

compose-up: ## Docker Compose로 서비스를 시작합니다
	docker-compose up -d

compose-down: ## Docker Compose 서비스를 중지합니다
	docker-compose down

compose-dev: ## Docker Compose로 개발 환경을 시작합니다
	docker-compose --profile dev up -d

compose-logs: ## Docker Compose 로그를 확인합니다
	docker-compose logs -f

test: ## 로컬에서 테스트를 실행합니다
	pytest tests/ -v

docker-test: ## Docker 컨테이너 내에서 테스트를 실행합니다
	docker run --rm -v $(PWD):/app $(IMAGE_NAME):$(TAG) pytest tests/ -v

health-check: ## API 헬스체크를 수행합니다
	@echo "헬스체크 수행 중..."
	@curl -f http://localhost:$(SERVER_PORT)/health || echo "서버가 응답하지 않습니다"

docker-stats: ## Docker 컨테이너 리소스 사용량을 확인합니다
	docker stats $(CONTAINER_NAME)
