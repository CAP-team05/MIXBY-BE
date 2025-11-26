# Recommendation API Documentation

## Base URL
```
http://snsn.kr:5050
```

---

## 1. 페르소나 생성 (Generate Persona)

### Endpoint
```
POST /api/recommendations/persona
```

### Description
사용자의 기본 정보와 테이스팅 데이터를 기반으로 개인화된 페르소나를 생성합니다.

### Request

#### Headers
```
Content-Type: application/json
```

#### Body
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

#### Parameters
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| user_data | Array | Yes | 사용자 기본 정보 배열 (비어있지 않아야 함) |
| tasting_data | Array | Yes | 사용자의 칵테일 테이스팅 데이터 배열 |

### Response

#### Success (200 OK)
```json
{
  "success": true,
  "message": "성공",
  "data": {
    "persona": "홍길동은 남성으로, 단맛을 선호하는 칵테일 애호가입니다. 달콤한 맛을 가진 음료를 즐기는 편입니다."
  }
}
```

#### Error (400 Bad Request)
```json
{
  "success": false,
  "message": "user_data 필드가 필요합니다."
}
```

### Example
```bash
curl -X POST http://snsn.kr:5050/api/recommendations/persona \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## 2. 기본 추천 (Default Recommendation)

### Endpoint
```
POST /api/recommendations/default
```

### Description
계절, 시간대, 날씨를 기반으로 칵테일을 추천합니다. 각 요소(계절, 시간, 날씨)에 대해 1종씩 총 3종을 추천합니다.

### Request

#### Headers
```
Content-Type: application/json
```

#### Body
```json
{
  "persona": "단맛을 선호하는 남성 사용자",
  "cocktail_list": ["진토닉", "모히또", "마가리타"],
  "season": "가을",
  "time": "저녁",
  "weather": "눈"
}
```

또는 문자열 형태:
```json
{
  "persona": "단맛을 선호하는 남성 사용자",
  "cocktail_list": "진토닉, 모히또, 마가리타",
  "season": "가을",
  "time": "저녁",
  "weather": "눈"
}
```

#### Parameters
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| persona | String | Yes | 사용자 페르소나 |
| cocktail_list | Array/String | Yes | 보유한 칵테일 목록 (배열 또는 쉼표로 구분된 문자열) |
| season | String | Yes | 계절 (예: 봄, 여름, 가을, 겨울) |
| time | String | Yes | 시간대 (예: 아침, 점심, 저녁, 밤) |
| weather | String | Yes | 날씨 (예: 맑음, 흐림, 비, 눈) |

### Response

#### Success (200 OK)
```json
{
  "success": true,
  "message": "성공",
  "data": {
    "recommendation": "{\n    \"recommendation\": [\n        {\n            \"name\": \"골든 드림\",\n            \"tag\": \"가을\",\n            \"reason\": \"가을의 풍미를 느낄 수 있는 달콤한 음료!\"\n        },\n        {\n            \"name\": \"스위트 드림\",\n            \"tag\": \"저녁\",\n            \"reason\": \"달콤한 맛이 매력적인 저녁의 완벽한 선택!\"\n        },\n        {\n            \"name\": \"윈터 선\",\n            \"tag\": \"눈\",\n            \"reason\": \"눈 내리는 날, 따뜻하고 달콤한 기분을 주는 칵테일!\"\n        }\n    ]\n}"
  }
}
```

#### Error (400 Bad Request)
```json
{
  "success": false,
  "message": "season 필드가 필요합니다."
}
```

### Example
```bash
curl -X POST http://snsn.kr:5050/api/recommendations/default \
  -H "Content-Type: application/json" \
  -d '{
    "persona": "단맛을 선호하는 남성 사용자",
    "cocktail_list": ["진토닉", "모히또", "마가리타"],
    "season": "가을",
    "time": "저녁",
    "weather": "눈"
  }'
```

---

## 3. 감정 기반 추천 (Feeling-based Recommendation)

### Endpoint
```
POST /api/recommendations/feeling
```

### Description
사용자의 감정(행복, 피곤, 화남)에 기반하여 칵테일을 추천합니다. 각 감정에 대해 1종씩 총 3종을 추천합니다.

### Request

#### Headers
```
Content-Type: application/json
```

#### Body
```json
{
  "persona": "단맛을 선호하는 남성 사용자",
  "cocktail_list": ["모히또", "마가리타", "위스키 사워", "진토닉"]
}
```

또는 문자열 형태:
```json
{
  "persona": "단맛을 선호하는 남성 사용자",
  "cocktail_list": "모히또, 마가리타, 위스키 사워, 진토닉"
}
```

#### Parameters
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| persona | String | Yes | 사용자 페르소나 |
| cocktail_list | Array/String | Yes | 보유한 칵테일 목록 (배열 또는 쉼표로 구분된 문자열) |

### Response

#### Success (200 OK)
```json
{
  "success": true,
  "message": "성공",
  "data": {
    "recommendation": "{\n    \"recommendation\": [\n        {\n            \"name\": \"스위트 드림\",\n            \"tag\": \"달콤함\",\n            \"reason\": \"홍길동님처럼 단맛을 좋아하는 분에게 완벽해요!\"\n        },\n        {\n            \"name\": \"골든 드림\",\n            \"tag\": \"부드러움\",\n            \"reason\": \"부드러운 단맛으로 행복감을 제공합니다.\"\n        },\n        {\n            \"name\": \"스위트 드림\",\n            \"tag\": \"편안함\",\n            \"reason\": \"편안하면서도 달콤한 맛이 피로를 잊게 해줍니다.\"\n        }\n    ]\n}"
  }
}
```

#### Error (400 Bad Request)
```json
{
  "success": false,
  "message": "persona 필드가 필요합니다."
}
```

### Example
```bash
curl -X POST http://snsn.kr:5050/api/recommendations/feeling \
  -H "Content-Type: application/json" \
  -d '{
    "persona": "단맛을 선호하는 남성 사용자",
    "cocktail_list": ["모히또", "마가리타", "위스키 사워", "진토닉"]
  }'
```

---

## 4. 상황 기반 추천 (Situation-based Recommendation)

### Endpoint
```
POST /api/recommendations/situation
```

### Description
사용자의 상황(바쁨, 한가, 여행)에 기반하여 칵테일을 추천합니다. 각 상황에 대해 1종씩 총 3종을 추천합니다.

### Request

#### Headers
```
Content-Type: application/json
```

#### Body
```json
{
  "persona": "단맛을 선호하는 남성 사용자",
  "cocktail_list": ["진토닉", "모히또", "마가리타"]
}
```

또는 문자열 형태:
```json
{
  "persona": "단맛을 선호하는 남성 사용자",
  "cocktail_list": "진토닉, 모히또, 마가리타"
}
```

#### Parameters
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| persona | String | Yes | 사용자 페르소나 |
| cocktail_list | Array/String | Yes | 보유한 칵테일 목록 (배열 또는 쉼표로 구분된 문자열) |

### Response

#### Success (200 OK)
```json
{
  "success": true,
  "message": "성공",
  "data": {
    "recommendation": "{\n    \"recommendation\": [\n        {\n            \"name\": \"골든 드림\",\n            \"tag\": \"바쁨\",\n            \"reason\": \"달콤하고 부드러워 빠르게 마시기 좋아요.\"\n        },\n        {\n            \"name\": \"비스 니즈\",\n            \"tag\": \"한가\",\n            \"reason\": \"꿀의 달콤한 맛이 여유로운 한과 잘 어울려요.\"\n        },\n        {\n            \"name\": \"골든 드림\",\n            \"tag\": \"여행\",\n            \"reason\": \"여행의 기분을 잘 느낄 수 있는 달콤한 칵테일입니다.\"\n        }\n    ]\n}"
  }
}
```

#### Error (400 Bad Request)
```json
{
  "success": false,
  "message": "cocktail_list 필드가 필요합니다."
}
```

### Example
```bash
curl -X POST http://snsn.kr:5050/api/recommendations/situation \
  -H "Content-Type: application/json" \
  -d '{
    "persona": "단맛을 선호하는 남성 사용자",
    "cocktail_list": ["진토닉", "모히또", "마가리타"]
  }'
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | 성공 |
| 400 | 잘못된 요청 (필수 필드 누락 또는 잘못된 데이터 타입) |
| 500 | 서버 내부 오류 |

## Notes

1. **cocktail_list 형식**: 배열 형태와 쉼표로 구분된 문자열 형태를 모두 지원합니다.
2. **페르소나**: `/api/recommendations/persona` 엔드포인트를 통해 생성된 페르소나를 사용하는 것을 권장합니다.
3. **추천 개수**: 각 API는 요청된 카테고리별로 1종씩, 총 3종의 칵테일을 추천합니다.
4. **추천 이유**: 모든 추천에는 50자 내외의 추천 이유가 포함됩니다.
5. **RAG 지원**: `USE_RAG` 환경 변수가 `true`로 설정되면 벡터 검색 기반 추천을 사용합니다.
