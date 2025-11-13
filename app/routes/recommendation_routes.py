"""
추천 관련 API 엔드포인트
"""

import json
from flask import Blueprint, request, jsonify
from app.services.persona_service import PersonaService
from app.services.recommendation_service import RecommendationService
from app.utils.response_helper import success_response, error_response
from app.utils.validators import validate_required_fields

# 블루프린트 생성
recommendation_bp = Blueprint('recommendation', __name__)

# 서비스 인스턴스
persona_service = PersonaService()
recommendation_service = RecommendationService()


@recommendation_bp.route('/persona', methods=['POST'])
def generate_persona():
    """
    사용자 페르소나를 생성합니다.
    
    Request Body:
    {
        "user_data": [{"name": "홍길동", "gender": "남성", "favoriteTaste": "단맛"}],
        "tasting_data": [{"code": "001", "drinkDate": "2024-01-01", "eval": 5, "sweetness": 4, "sourness": 2, "alcohol": 3}]
    }
    """
    try:
        data = request.get_json()
        
        # 필수 필드 검증
        required_fields = ['user_data', 'tasting_data']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return error_response(validation_error, 400)
        
        user_data = data['user_data']
        tasting_data = data['tasting_data']
        
        if not isinstance(user_data, list) or not user_data:
            return error_response("user_data는 비어있지 않은 리스트여야 합니다.", 400)
        
        if not isinstance(tasting_data, list):
            return error_response("tasting_data는 리스트여야 합니다.", 400)
        
        # 페르소나 생성
        persona = persona_service.generate_persona(user_data, tasting_data)
        
        return success_response({
            'persona': persona
        })
        
    except Exception as e:
        return error_response(f"페르소나 생성 중 오류가 발생했습니다: {str(e)}", 500)


@recommendation_bp.route('/default', methods=['POST'])
def get_default_recommendation():
    """
    기본 추천 (계절, 시간, 날씨 기반)을 가져옵니다.

    Request Body:
    {
        "persona": "사용자 페르소나",
        "cocktail_list": ["칵테일1", "칵테일2", "칵테일3"] or "칵테일1, 칵테일2, 칵테일3",
        "season": "가을",
        "time": "저녁",
        "weather": "눈"
    }
    """
    try:
        data = request.get_json()

        # 필수 필드 검증
        required_fields = ['persona', 'cocktail_list', 'season', 'time', 'weather']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return error_response(validation_error, 400)

        persona = data['persona']
        cocktail_list = data['cocktail_list']
        season = data['season']
        time = data['time']
        weather = data['weather']

        # cocktail_list가 배열이면 JSON 문자열로 변환
        if isinstance(cocktail_list, list):
            cocktail_list = json.dumps(cocktail_list)

        # 추천 생성
        recommendation = recommendation_service.get_default_recommendation(
            persona, cocktail_list, season, time, weather
        )

        return success_response({
            'recommendation': recommendation
        })

    except Exception as e:
        return error_response(f"기본 추천 생성 중 오류가 발생했습니다: {str(e)}", 500)


@recommendation_bp.route('/feeling', methods=['POST'])
def get_feeling_recommendation():
    """
    감정 기반 추천 (행복, 피곤, 화남)을 가져옵니다.

    Request Body:
    {
        "persona": "사용자 페르소나",
        "cocktail_list": ["칵테일1", "칵테일2", "칵테일3"] or "칵테일1, 칵테일2, 칵테일3"
    }
    """
    try:
        data = request.get_json()

        # 필수 필드 검증
        required_fields = ['persona', 'cocktail_list']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return error_response(validation_error, 400)

        persona = data['persona']
        cocktail_list = data['cocktail_list']

        # cocktail_list가 배열이면 JSON 문자열로 변환
        if isinstance(cocktail_list, list):
            cocktail_list = json.dumps(cocktail_list)

        # 추천 생성
        recommendation = recommendation_service.get_feeling_recommendation(persona, cocktail_list)

        return success_response({
            'recommendation': recommendation
        })

    except Exception as e:
        return error_response(f"감정 기반 추천 생성 중 오류가 발생했습니다: {str(e)}", 500)


@recommendation_bp.route('/situation', methods=['POST'])
def get_situation_recommendation():
    """
    상황 기반 추천 (바쁨, 한가, 여행)을 가져옵니다.

    Request Body:
    {
        "persona": "사용자 페르소나",
        "cocktail_list": ["칵테일1", "칵테일2", "칵테일3"] or "칵테일1, 칵테일2, 칵테일3"
    }
    """
    try:
        data = request.get_json()

        # 필수 필드 검증
        required_fields = ['persona', 'cocktail_list']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return error_response(validation_error, 400)

        persona = data['persona']
        cocktail_list = data['cocktail_list']

        # cocktail_list가 배열이면 JSON 문자열로 변환
        if isinstance(cocktail_list, list):
            cocktail_list = json.dumps(cocktail_list)

        # 추천 생성
        recommendation = recommendation_service.get_situation_recommendation(persona, cocktail_list)

        return success_response({
            'recommendation': recommendation
        })

    except Exception as e:
        return error_response(f"상황 기반 추천 생성 중 오류가 발생했습니다: {str(e)}", 500)
