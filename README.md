# Mixby
Mixby로 자신의 퍼스널라이징 바텐더를 만들어보세요!

![image](https://github.com/user-attachments/assets/747107a7-f835-4cd7-a6db-80dd297e0a8a)

## Introduction
이 repository는 mixby의 **백엔드**를 다룹니다.  
> [Swift Mixby](https://github.com/CAP-team05/Swift_Mixby)에서 프론트앤드 코드를 참고하세요!  
> 해당 백엔드 코드는 자체 서버에서 돌아가고 있습니다..!
> 따라서 swift mixby repository에서는 localhost가 아닌 다른 api address를 사용하고 있습니다.  

## How to test
1. 이 repository를 clone 해주세요.
```bash
git clone https://github.com/CAP-team05/MIXBY-BE
```
2. clone 받은 폴더로 이동합니다.
```bash
cd Mixby
```
3. 프로젝트 root에 `.env`파일을 만들고 안에 내용을 채워주세요.
```python
OPENAI_API_KEY=sk-proj-***************
OPENWEATHER_API_KEY=cf790*************
```
> openai api, openweathermap api 키를 발급받고 해당 부분을 채우면 됩니다.
4. 프로젝트 root에서 실행하면 됩니다.
```bash
code .
```
이후 `run.py` 실행합니다.

5. library가 설치되어 있지 않다면 해당되는 library를 install 해주세요.
```bash
pip install flask
.
.
.
etc.
```

## Directory Structure
### app/
서버에서 실행하는 주요 코드와 관련된 모든 파일이 포함됩니다.
1.  `data/`  
    레시피 정보, 주류 정보 등 데이터베이스를 저장해두는 폴더입니다. 데이터의 양이 대단히 많진 않기 때문에 json으로 구현했습니다.
2.  `static/`  
    이미지 파일과 같이 정적인 resource를 보관하는 폴더입니다.
3.  `models/`  
    데이터 모델 정의를 포함합니다.
4.  `routes/`  
    API 엔드포인트 및 라우팅 로직을 처리합니다.
5.  `services/`  
    비즈니스 로직 및 데이터 처리를 담당하는 서비스 계층입니다.
6.  `utils/`  
    다양한 유틸리티 함수 및 헬퍼 모듈을 포함합니다.

### .env
api키와 같이 보안이 필요한 key 값들을 저장해두었습니다.  

## API Endpoints

### 추천 API

#### 1. 페르소나 생성 API
사용자의 기본 정보와 테이스팅 이력을 바탕으로 페르소나를 생성합니다.

**Endpoint:** `POST /api/recommendations/persona`

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

#### 2. 기본 추천 API (계절, 시간, 날씨 기반)
**Endpoint:** `POST /api/recommendations/default`

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

#### 3. 감정 기반 추천 API
**Endpoint:** `POST /api/recommendations/feeling`

**Request Body:**
```json
{
    "persona": "생성된 사용자 페르소나",
    "cocktail_list": "스크류 드라이버, 보드카토닉, 모스크뮬, 마티니"
}
```

#### 4. 상황 기반 추천 API
**Endpoint:** `POST /api/recommendations/situation`

**Request Body:**
```json
{
    "persona": "생성된 사용자 페르소나", 
    "cocktail_list": "스크류 드라이버, 보드카토닉, 모스크뮬, 마티니"
}
```
