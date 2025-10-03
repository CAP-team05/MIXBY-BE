"""
테스트 공통 fixture 정의
"""

import pytest
from app import create_app


@pytest.fixture
def app():
    """Flask 애플리케이션 fixture"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Flask 테스트 클라이언트 fixture"""
    return app.test_client()


@pytest.fixture
def sample_recipe():
    """테스트용 레시피 데이터"""
    return {
        "english_name": "Test Cocktail",
        "korean_name": "테스트 칵테일",
        "code": "TEST001",
        "ingredients": [
            {
                "name": "진",
                "code": "300",
                "amount": "45",
                "unit": "ml"
            },
            {
                "name": "토닉워터",
                "code": "600",
                "amount": "120",
                "unit": "ml"
            }
        ],
        "instructions": [
            "하이볼 글라스에 얼음을 채운다.",
            "진을 붓는다.",
            "토닉워터를 천천히 부어 섞는다.",
            "라임 웨지로 장식한다."
        ],
        "difficulty": "쉬움",
        "category": "롱 드링크",
        "tag1": "상쾌함",
        "tag2": "클래식",
        "glass": "하이볼",
        "garnish": "라임 웨지"
    }


@pytest.fixture
def sample_ingredient():
    """테스트용 재료 데이터"""
    return {
        "name": "진",
        "code": "300"
    }


@pytest.fixture
def sample_challenge():
    """테스트용 챌린지 데이터"""
    return {
        "code": 1,
        "name": "여정의 시작",
        "description": "앱 실행"
    }


@pytest.fixture
def sample_user_data():
    """테스트용 사용자 데이터"""
    return [{
        "name": "테스트유저",
        "gender": "남성",
        "prefer": "단맛"
    }]


@pytest.fixture
def sample_tasting_data():
    """테스트용 테이스팅 데이터"""
    return [{
        "id": 1,
        "name": "진토닉",
        "date": "2024-01-15",
        "tag1": "상쾌함",
        "tag2": "클래식",
        "eval": "매우 만족",
        "sweetness": "보통",
        "sourness": "만족",
        "alcohol": "만족"
    }]


@pytest.fixture
def sample_recipes_list():
    """테스트용 레시피 리스트"""
    return [
        {
            "english_name": "Gin Tonic",
            "korean_name": "진토닉",
            "code": "300600",
            "ingredients": [
                {"name": "진", "code": "300", "amount": "45", "unit": "ml"},
                {"name": "토닉워터", "code": "600", "amount": "120", "unit": "ml"}
            ],
            "difficulty": "쉬움",
            "category": "롱 드링크",
            "tag1": "상쾌함",
            "tag2": "클래식"
        },
        {
            "english_name": "Mojito",
            "korean_name": "모히또",
            "code": "500601",
            "ingredients": [
                {"name": "럼", "code": "500", "amount": "50", "unit": "ml"},
                {"name": "탄산수", "code": "601", "amount": "100", "unit": "ml"}
            ],
            "difficulty": "보통",
            "category": "롱 드링크",
            "tag1": "청량",
            "tag2": "민트"
        }
    ]


@pytest.fixture
def sample_ingredients_list():
    """테스트용 재료 리스트"""
    return [
        {"name": "진", "code": "300"},
        {"name": "보드카", "code": "400"},
        {"name": "럼", "code": "500"},
        {"name": "토닉워터", "code": "600"},
        {"name": "탄산수", "code": "601"}
    ]


@pytest.fixture
def sample_challenges_list():
    """테스트용 챌린지 리스트"""
    return [
        {"code": 1, "name": "여정의 시작", "description": "앱 실행"},
        {"code": 2, "name": "너의 눈동자에 치얼스", "description": "달콤한 칵테일 제조"},
        {"code": 3, "name": "정말~ 달콤해", "description": "달콤한 칵테일 3종 완성"}
    ]
