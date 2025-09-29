"""
추천 서비스 테스트
"""

import pytest
import json
from unittest.mock import Mock, patch
from app.services.persona_service import PersonaService
from app.services.recommendation_service import RecommendationService


class TestPersonaService:
    """PersonaService 테스트 클래스"""
    
    def test_to_eval_string(self):
        """평점을 문자열로 변환하는 함수 테스트"""
        service = PersonaService()
        
        assert service._to_eval_string(0) == "매우 불만"
        assert service._to_eval_string(3) == "보통"
        assert service._to_eval_string(6) == "매우 만족"
        assert service._to_eval_string(7) == "7"  # 범위 밖 값
    
    def test_get_drink_list_string_empty(self):
        """빈 테이스팅 데이터로 드링크 리스트 문자열 생성 테스트"""
        service = PersonaService()
        result = service.get_drink_list_string([])
        assert result == ""
    
    @patch('app.services.persona_service.RecipeService')
    def test_get_drink_list_string_with_data(self, mock_recipe_service):
        """테이스팅 데이터로 드링크 리스트 문자열 생성 테스트"""
        # Mock 설정
        mock_recipe_service.return_value.search_by_code.return_value = {
            "korean_name": "진토닉",
            "tag1": "상쾌함",
            "tag2": "클래식"
        }
        
        service = PersonaService()
        tasting_data = [{
            "code": "001",
            "drinkDate": "2024-01-01",
            "eval": 5,
            "sweetness": 3,
            "sourness": 2,
            "alcohol": 4
        }]
        
        result = service.get_drink_list_string(tasting_data)
        expected = "[진토닉, 2024-01-01, 상쾌함, 클래식, 대체로 만족, 보통, 조금 불만, 조금 만족]"
        assert result == expected


class TestRecommendationService:
    """RecommendationService 테스트 클래스"""
    
    @patch('app.services.recommendation_service.OpenAI')
    @patch('app.services.recommendation_service.match_cocktail_in_json')
    def test_get_default_recommendation(self, mock_matcher, mock_openai):
        """기본 추천 생성 테스트"""
        # Mock 설정
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"recommendation": "test"}'
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        mock_matcher.return_value = {"recommendation": "matched"}
        
        service = RecommendationService()
        result = service.get_default_recommendation(
            "테스트 페르소나", "진토닉, 마티니", "가을", "저녁", "맑음"
        )
        
        assert "matched" in result
        mock_openai.return_value.chat.completions.create.assert_called_once()
        mock_matcher.assert_called_once()
    
    @patch('app.services.recommendation_service.OpenAI')
    def test_get_default_recommendation_error(self, mock_openai):
        """기본 추천 생성 에러 처리 테스트"""
        # Mock에서 예외 발생 설정
        mock_openai.return_value.chat.completions.create.side_effect = Exception("API Error")
        
        service = RecommendationService()
        result = service.get_default_recommendation(
            "테스트 페르소나", "진토닉, 마티니", "가을", "저녁", "맑음"
        )
        
        assert "error" in result
        assert "추천 생성에 실패했습니다" in result