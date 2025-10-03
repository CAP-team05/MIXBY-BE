"""
추천 서비스 테스트
"""

import pytest
import json
from unittest.mock import Mock, patch
from app.services.recommendation_service import RecommendationService


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