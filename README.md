# Mixby
Mixby로 자신의 퍼스널라이징 바텐더를 만들어보세요!

![image](https://github.com/user-attachments/assets/747107a7-f835-4cd7-a6db-80dd297e0a8a)

## Introduction
이 repository는 mixby의 **백엔드**를 다룹니다.  
> [Swift Mixby](https://github.com/CAP-team05/Swift_Mixby)에서 프론트엔드 코드를 참고하세요!  
> 해당 백엔드 코드는 자체 서버에서 돌아가고 있습니다.
> 따라서 swift mixby repository에서는 localhost가 아닌 다른 api address를 사용하고 있습니다.

## 핵심 기능
- **AI 기반 페르소나 생성**: 사용자의 기본 정보와 테이스팅 이력을 바탕으로 개인화된 페르소나 생성
- **상황별 칵테일 추천**: 계절, 시간, 날씨, 감정, 상황에 따른 맞춤형 칵테일 추천
- **레시피 검색 및 관리**: 이름, 코드, 재료, 난이도별 레시피 검색 및 조회
- **주류 정보 제공**: 주류 데이터베이스 검색 및 이미지 제공
- **이미지 서빙**: 레시피 및 주류 이미지 제공

## 기술 스택
- **Flask 2.3.3**: 웹 프레임워크
- **OpenAI GPT-4o-mini**: AI 기반 페르소나 생성 및 추천 엔진
- **OpenWeatherMap API**: 날씨 기반 추천
- **pytest**: 테스트 프레임워크 (커버리지 80% 이상 유지)
- **Docker & docker-compose**: 컨테이너화 및 배포

## 빠른 시작

### 로컬 환경 설정

1. 이 repository를 clone 해주세요.
```bash
git clone https://github.com/CAP-team05/MIXBY-BE
cd MIXBY-BE
```

2. 의존성을 설치합니다.
```bash
pip install -r requirements.txt
```

3. 프로젝트 root에 `.env` 파일을 만들고 API 키를 설정합니다.
```bash
OPENAI_API_KEY=sk-proj-***************
OPENWEATHER_API_KEY=cf790*************
FLASK_ENV=development
API_PORT=8080
```
> OpenAI API와 OpenWeatherMap API 키를 발급받아 설정해야 합니다.

4. 애플리케이션을 실행합니다.
```bash
python run.py
```

서버가 `http://localhost:8080`에서 실행됩니다.

### Docker 환경 설정

```bash
# 이미지 빌드 및 컨테이너 실행
make build
make run

# 또는 docker-compose 사용
make compose-up

# 로그 확인
make logs

# 컨테이너 중지 및 정리
make clean
```

## 프로젝트 구조

```
MIXBY-BE/
├── app/                    # 메인 애플리케이션 패키지
│   ├── __init__.py        # Flask 앱 팩토리
│   ├── config.py          # 환경별 설정 (development, production, testing)
│   ├── data/              # JSON 데이터베이스 파일들
│   │   ├── allRecipes.json
│   │   ├── allProducts.json
│   │   ├── allIngredients.json
│   │   └── api_rules.json
│   ├── models/            # 데이터 모델 정의
│   ├── routes/            # API 엔드포인트 (Blueprint)
│   │   ├── drink_routes.py
│   │   ├── recipe_routes.py
│   │   └── recommendation_routes.py
│   ├── services/          # 비즈니스 로직 계층
│   │   ├── persona_service.py
│   │   ├── recommendation_service.py
│   │   ├── recipe_service.py
│   │   ├── drink_service.py
│   │   ├── ingredient_service.py
│   │   └── challenge_service.py
│   ├── static/            # 정적 리소스 (이미지)
│   │   ├── recipes/
│   │   ├── drinks/
│   │   └── ingredients/
│   └── utils/             # 유틸리티 함수 및 헬퍼
│       ├── response_helper.py
│       ├── data_loader.py
│       ├── validators.py
│       └── cocktail_matcher.py
├── tests/                 # 테스트 코드
│   ├── routes/
│   ├── services/
│   └── utils/
├── run.py                 # 애플리케이션 진입점
├── requirements.txt       # Python 의존성
├── pyproject.toml        # 도구 설정 (black, pytest)
├── Makefile              # 빌드 자동화
├── Dockerfile            # Docker 이미지 정의
├── docker-compose.yml    # Docker Compose 설정
└── .env                  # 환경 변수 (git 제외)
```

### 아키텍처 패턴

프로젝트는 명확한 계층 분리를 따릅니다:

1. **Routes (라우트 계층)**: API 엔드포인트 정의, 요청/응답 처리
   - Blueprint 패턴 사용
   - URL prefix로 API 그룹화
   - 입력 검증 및 에러 핸들링

2. **Services (서비스 계층)**: 비즈니스 로직 구현
   - 외부 API 호출 (OpenAI, OpenWeatherMap)
   - 데이터 처리 및 변환
   - 재사용 가능한 로직 캡슐화

3. **Utils (유틸리티 계층)**: 공통 기능 제공
   - 응답 포맷팅 (`response_helper.py`)
   - 데이터 로딩 (`data_loader.py`)
   - 입력 검증 (`validators.py`)

### 주요 디렉토리 설명

#### `app/routes/`
API 엔드포인트를 Blueprint로 구성:
- `drink_routes.py`: 주류 정보 API (`/drink`)
- `recipe_routes.py`: 레시피 검색 및 조회 API (`/recipe`)
- `recommendation_routes.py`: 추천 API (`/api/recommendations`)

#### `app/services/`
비즈니스 로직 서비스:
- `persona_service.py`: 사용자 페르소나 생성
- `recommendation_service.py`: AI 기반 칵테일 추천
- `recipe_service.py`: 레시피 검색 및 필터링
- `drink_service.py`: 주류 정보 관리
- `ingredient_service.py`: 재료 정보 관리
- `challenge_service.py`: 챌린지 관련 로직

#### `app/data/`
JSON 파일 기반 데이터 저장소:
- `allRecipes.json`: 전체 레시피 데이터
- `allProducts.json`: 주류 제품 정보
- `allIngredients.json`: 재료 정보
- `api_rules.json`: API 문서

#### `app/static/`
정적 파일 (이미지):
- `recipes/`: 레시피 이미지
- `drinks/`: 주류 이미지
- `ingredients/`: 재료 이미지  

## 테스트

### 테스트 실행

프로젝트는 pytest를 사용하여 테스트를 실행합니다.

```bash
# 기본 테스트 실행
make test
# 또는
pytest tests/ -v

# 커버리지 포함 테스트 실행
make test-coverage
# 또는
pytest tests/ -v --cov=app --cov-report=term --cov-report=html

# 커버리지 임계값(80%) 검증 포함 테스트
make test-coverage-strict
# 또는
pytest tests/ -v --cov=app --cov-report=term --cov-report=html --cov-fail-under=80

# Docker 환경에서 테스트
make docker-test

# 특정 테스트 파일만 실행
pytest tests/services/test_recipe_service.py -v

# 특정 테스트 함수만 실행
pytest tests/services/test_recipe_service.py::test_get_all_recipes -v

# 키워드로 테스트 필터링
pytest tests/ -k "recipe" -v
```

### 커버리지 리포트

테스트 커버리지 리포트는 다음 위치에 생성됩니다:
- **HTML 리포트**: `htmlcov/index.html` (브라우저에서 열어서 확인)
- **터미널 리포트**: 테스트 실행 후 콘솔에 출력

### 커버리지 요구사항

- **최소 커버리지**: 전체 코드의 80% 이상
- **PR 제출 전**: 반드시 `make test-coverage-strict` 실행하여 커버리지 확인
- **새로운 코드**: 테스트 없이 커버리지를 낮추는 코드는 리뷰 거부 대상

### 테스트 작성 규칙

모든 새로운 코드는 테스트와 함께 작성되어야 합니다:

- **서비스 클래스**: `tests/services/test_{service_name}.py`
- **API 엔드포인트**: `tests/routes/test_{route_name}.py`
- **유틸리티 함수**: `tests/utils/test_{util_name}.py`

테스트는 Given-When-Then 패턴을 따르며, 외부 API 호출은 모킹(mocking)해야 합니다.

자세한 테스트 작성 가이드는 `.kiro/steering/testing.md`를 참고하세요.

## API Endpoints

### 기본 엔드포인트

#### 헬스 체크
```
GET /health
```
서버 상태를 확인합니다.

**응답 예시:**
```json
{
    "success": true,
    "message": "서버가 정상적으로 동작 중입니다.",
    "data": {
        "status": "healthy"
    }
}
```

#### API 문서
```
GET /
```
전체 API 문서를 반환합니다.

---

### 추천 API (`/api/recommendations`)

#### 1. 페르소나 생성
사용자의 기본 정보와 테이스팅 이력을 바탕으로 AI 페르소나를 생성합니다.

```
POST /api/recommendations/persona
```

**Request Body:**
```json
{
    "user_data": [
        {
            "name": "홍길동",
            "gender": "남성", 
            "favoriteTaste": "단맛"
        }
    ],
    "tasting_data": [
        {
            "code": "001",
            "drinkDate": "2024-01-01",
            "eval": 5,
            "sweetness": 4,
            "sourness": 2,
            "alcohol": 3
        }
    ]
}
```

**응답 예시:**
```json
{
    "success": true,
    "data": {
        "persona": "사용자는 단맛을 선호하며..."
    }
}
```

#### 2. 기본 추천 (계절, 시간, 날씨 기반)
현재 계절, 시간, 날씨를 고려한 칵테일을 추천합니다.

```
POST /api/recommendations/default
```

**Request Body:**
```json
{
    "persona": "생성된 사용자 페르소나",
    "cocktail_list": "스크류 드라이버, 보드카토닉, 모스크뮬, 마티니",
    "season": "가을",
    "time": "저녁", 
    "weather": "눈"
}
```

#### 3. 감정 기반 추천
사용자의 현재 감정 상태에 맞는 칵테일을 추천합니다.

```
POST /api/recommendations/feeling
```

**Request Body:**
```json
{
    "persona": "생성된 사용자 페르소나",
    "cocktail_list": "스크류 드라이버, 보드카토닉, 모스크뮬, 마티니"
}
```

#### 4. 상황 기반 추천
사용자의 현재 상황에 맞는 칵테일을 추천합니다.

```
POST /api/recommendations/situation
```

**Request Body:**
```json
{
    "persona": "생성된 사용자 페르소나", 
    "cocktail_list": "스크류 드라이버, 보드카토닉, 모스크뮬, 마티니"
}
```

---

### 레시피 API (`/recipe`)

#### 전체 레시피 조회
```
GET /recipe/all
```
모든 레시피 데이터를 반환합니다.

#### 레시피 이름 검색
```
GET /recipe/name=<name>
```
이름으로 레시피를 검색합니다.

**예시:** `GET /recipe/name=모히또`

#### 레시피 코드 조회
```
GET /recipe/code=<code>
```
코드로 특정 레시피를 조회합니다.

**예시:** `GET /recipe/code=001`

#### 재료 기반 레시피 검색
```
GET /recipe/with=<codes>
```
보유한 재료 코드들로 만들 수 있는 레시피를 검색합니다.

**예시:** `GET /recipe/with=001,002,003`

#### 난이도별 레시피 조회
```
GET /recipe/difficulty=<difficulty>
```
난이도별로 레시피를 필터링합니다.

**예시:** `GET /recipe/difficulty=쉬움`

#### 무작위 레시피 조회
```
GET /recipe/random
```
무작위로 하나의 레시피를 반환합니다.

#### 레시피 카테고리 조회
```
GET /recipe/categories
```
사용 가능한 모든 레시피 카테고리를 반환합니다.

#### 레시피 이미지 조회 (코드)
```
GET /recipe/image/code=<code>
```
레시피 코드로 이미지를 반환합니다.

**예시:** `GET /recipe/image/code=001`

#### 레시피 이미지 조회 (이름)
```
GET /recipe/image/name=<name>
```
레시피 이름으로 이미지를 반환합니다.

**예시:** `GET /recipe/image/name=모히또`

---

### 주류 API (`/drink`)

#### 전체 주류 조회
```
GET /drink/all
```
모든 주류 데이터를 반환합니다.

#### 주류 이름 검색
```
GET /drink/name=<name>
```
이름으로 주류를 검색합니다.

**예시:** `GET /drink/name=보드카`

#### 주류 코드 조회
```
GET /drink/code=<code>
```
코드로 특정 주류를 조회합니다.

**예시:** `GET /drink/code=0080480004699`

#### 주류 타입별 조회
```
GET /drink/type=<type>
```
타입별로 주류를 필터링합니다.

**예시:** `GET /drink/type=위스키`

#### 주류 타입 목록 조회
```
GET /drink/types
```
사용 가능한 모든 주류 타입을 반환합니다.

#### 주류 이미지 조회
```
GET /drink/image=<code>
```
주류 코드로 이미지를 반환합니다.

**예시:** `GET /drink/image=0080480004699`

---

### 응답 형식

모든 API는 일관된 JSON 응답 형식을 사용합니다.

**성공 응답:**
```json
{
    "success": true,
    "message": "성공 메시지",
    "data": { ... }
}
```

**에러 응답:**
```json
{
    "success": false,
    "message": "에러 메시지",
    "error_code": "ERROR_CODE"
}
```

**검색 응답:**
```json
{
    "success": true,
    "message": "검색 완료",
    "data": {
        "results": [ ... ],
        "count": 10,
        "query": "검색어"
    }
}
```


## 개발 가이드

### 코딩 규칙

#### 네이밍 컨벤션
- **파일명**: `snake_case` (예: `recommendation_service.py`)
- **클래스명**: `PascalCase` (예: `RecommendationService`)
- **함수/변수명**: `snake_case` (예: `get_default_recommendation`)
- **상수**: `UPPER_SNAKE_CASE` (예: `API_PORT`)

#### 코드 스타일
- **Black 포매터** 사용 (line-length: 120)
- **Docstring**은 Google 스타일
- **타입 힌트** 사용 권장

```bash
# 코드 포매팅
black app/ tests/

# 린팅
flake8 app/ tests/
```

### 에러 처리

모든 API는 일관된 에러 처리를 따릅니다:

```python
try:
    # 비즈니스 로직
    result = service.do_something()
    return response_helper.json_response(result)
except Exception as e:
    return response_helper.error_response(
        message="에러 메시지",
        status_code=500
    )
```

### 입력 검증

`validators.py`의 유틸리티 함수를 사용하여 입력을 검증합니다:

```python
from app.utils.validators import validator

# 필수 필드 검증
validation_errors = validator.validate_required_fields(data, ['field1', 'field2'])
if validation_errors:
    return response_helper.validation_error_response(validation_errors)

# 검색어 정제
sanitized_query = validator.sanitize_string(query, max_length=100)
```

## Makefile 명령어

프로젝트는 Makefile을 통해 다양한 작업을 자동화합니다:

### Docker 명령어
```bash
make build              # Docker 이미지 빌드
make run                # 컨테이너 실행
make run-dev            # 개발 모드로 실행
make logs               # 로그 확인
make clean              # 컨테이너 중지 및 정리
```

### Docker Compose 명령어
```bash
make compose-up         # 서비스 시작
make compose-dev        # 개발 환경 시작
make compose-down       # 서비스 중지
make compose-logs       # 로그 확인
```

### 테스트 명령어
```bash
make test               # 기본 테스트 실행
make test-coverage      # 커버리지 포함 테스트
make docker-test        # Docker 내 테스트
```

### 유틸리티 명령어
```bash
make health-check       # API 헬스체크
```

## 환경 변수

`.env` 파일에 다음 환경 변수를 설정해야 합니다:

```bash
# OpenAI API 키 (필수)
OPENAI_API_KEY=sk-proj-***************

# OpenWeatherMap API 키 (필수)
OPENWEATHER_API_KEY=cf790*************

# Flask 환경 설정
FLASK_ENV=development

# API 포트
API_PORT=8080
```

## 외부 API 의존성

### OpenAI API
- **모델**: GPT-4o-mini
- **용도**: 페르소나 생성 및 칵테일 추천
- **발급**: [OpenAI Platform](https://platform.openai.com/)

### OpenWeatherMap API
- **용도**: 날씨 기반 추천
- **발급**: [OpenWeatherMap](https://openweathermap.org/api)

## 배포

프로젝트는 자체 서버에서 운영 중입니다. Docker를 사용하여 배포됩니다.

```bash
# 프로덕션 빌드
docker build -f Dockerfile.prod -t mixby-backend:latest .

# 프로덕션 실행
docker run -d -p 8080:8080 --env-file .env mixby-backend:latest
```

## 기여하기

1. 이 저장소를 Fork 합니다
2. 새로운 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 Push 합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

### PR 체크리스트
- [ ] 코드가 Black으로 포매팅되었는가?
- [ ] 모든 테스트가 통과하는가?
- [ ] 커버리지가 80% 이상인가?
- [ ] 새로운 기능에 대한 테스트가 작성되었는가?
- [ ] API 문서가 업데이트되었는가?

## 라이선스

이 프로젝트는 CAP-team05의 소유입니다.

## 팀

- **프론트엔드**: [Swift Mixby](https://github.com/CAP-team05/Swift_Mixby)
- **백엔드**: [MIXBY-BE](https://github.com/CAP-team05/MIXBY-BE)

## 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.
