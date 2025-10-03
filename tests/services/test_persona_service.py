"""
PersonaService 테스트
"""

import pytest
import json
from unittest.mock import Mock, patch
from app.services.persona_service import PersonaService


class TestPersonaService:
    """PersonaService 테스트 클래스"""
    
    def test_to_eval_string(self):
        """평점을 문자열로 변환하는 함수 테스트"""
        service = PersonaService()
        
        assert service._to_eval_string(0) == "매우 불만"
        assert service._to_eval_string(3) == "보통"
        assert service._to_eval_string(6) == "매우 만족"
        assert service._to_eval_string(7) == "7"  # 범위 밖 값
    
    def test_to_eval_string_all_values(self):
        """모든 평점 값에 대한 문자열 변환 테스트"""
        service = PersonaService()
        
        # 모든 유효한 평점 값 테스트
        assert service._to_eval_string(0) == "매우 불만"
        assert service._to_eval_string(1) == "대체로 불만"
        assert service._to_eval_string(2) == "조금 불만"
        assert service._to_eval_string(3) == "보통"
        assert service._to_eval_string(4) == "조금 만족"
        assert service._to_eval_string(5) == "대체로 만족"
        assert service._to_eval_string(6) == "매우 만족"
        
        # 범위 밖 값 테스트
        assert service._to_eval_string(-1) == "-1"
        assert service._to_eval_string(7) == "7"
        assert service._to_eval_string(10) == "10"
    
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
    
    @patch('app.services.persona_service.RecipeService')
    def test_get_drink_list_string_with_multiple_items(self, mock_recipe_service):
        """여러 테이스팅 데이터로 드링크 리스트 문자열 생성 테스트"""
        # Mock 설정 - 여러 레시피 반환
        def mock_search_by_code(code):
            recipes = {
                "001": {
                    "korean_name": "모히또",
                    "tag1": "상쾌함",
                    "tag2": "민트향"
                },
                "002": {
                    "korean_name": "마티니",
                    "tag1": "드라이",
                    "tag2": "클래식"
                },
                "003": {
                    "korean_name": "마가리타",
                    "tag1": "새콤함",
                    "tag2": "데킬라"
                }
            }
            return recipes.get(code)
        
        mock_recipe_service.return_value.search_by_code.side_effect = mock_search_by_code
        
        service = PersonaService()
        tasting_data = [
            {
                "code": "001",
                "drinkDate": "2024-01-01",
                "eval": 5,
                "sweetness": 4,
                "sourness": 2,
                "alcohol": 3
            },
            {
                "code": "002",
                "drinkDate": "2024-01-15",
                "eval": 4,
                "sweetness": 1,
                "sourness": 1,
                "alcohol": 5
            },
            {
                "code": "003",
                "drinkDate": "2024-02-01",
                "eval": 6,
                "sweetness": 2,
                "sourness": 5,
                "alcohol": 4
            }
        ]
        
        result = service.get_drink_list_string(tasting_data)
        
        # 검증 - 세 개의 칵테일 정보가 쉼표로 구분되어 있어야 함
        assert "[모히또, 2024-01-01, 상쾌함, 민트향, 대체로 만족, 조금 만족, 조금 불만, 보통]" in result
        assert "[마티니, 2024-01-15, 드라이, 클래식, 조금 만족, 대체로 불만, 대체로 불만, 대체로 만족]" in result
        assert "[마가리타, 2024-02-01, 새콤함, 데킬라, 매우 만족, 조금 불만, 대체로 만족, 조금 만족]" in result
        
        # 전체 문자열 검증
        expected = (
            "[모히또, 2024-01-01, 상쾌함, 민트향, 대체로 만족, 조금 만족, 조금 불만, 보통], "
            "[마티니, 2024-01-15, 드라이, 클래식, 조금 만족, 대체로 불만, 대체로 불만, 대체로 만족], "
            "[마가리타, 2024-02-01, 새콤함, 데킬라, 매우 만족, 조금 불만, 대체로 만족, 조금 만족]"
        )
        assert result == expected
    
    @patch('app.services.persona_service.OpenAI')
    @patch('app.services.persona_service.RecipeService')
    def test_generate_persona_success(self, mock_recipe_service, mock_openai):
        """OpenAI API를 모킹하여 페르소나 생성 성공 테스트"""
        # RecipeService Mock 설정
        mock_recipe_service.return_value.search_by_code.return_value = {
            "korean_name": "모히또",
            "tag1": "상쾌함",
            "tag2": "민트향"
        }
        
        # OpenAI Mock 설정
        mock_response = Mock()
        mock_message = Mock()
        mock_message.content = json.dumps({"summary": "단맛을 좋아하는 사용자로, 상쾌한 칵테일을 선호합니다."})
        mock_response.choices = [Mock(message=mock_message)]
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # 테스트 실행
        service = PersonaService()
        user_data = [{
            "name": "홍길동",
            "gender": "남성",
            "favoriteTaste": "단맛"
        }]
        tasting_data = [{
            "code": "001",
            "drinkDate": "2024-01-01",
            "eval": 5,
            "sweetness": 4,
            "sourness": 2,
            "alcohol": 3
        }]
        
        result = service.generate_persona(user_data, tasting_data)
        
        # 검증
        assert result == "단맛을 좋아하는 사용자로, 상쾌한 칵테일을 선호합니다."
        mock_client.chat.completions.create.assert_called_once()
    
    def test_generate_persona_no_user_data(self):
        """사용자 데이터가 없을 때 에러 발생 테스트"""
        service = PersonaService()
        
        with pytest.raises(ValueError, match="사용자 데이터가 필요합니다"):
            service.generate_persona([], [])
    
    @patch('app.services.persona_service.OpenAI')
    @patch('app.services.persona_service.RecipeService')
    def test_generate_persona_api_error(self, mock_recipe_service, mock_openai):
        """OpenAI API 호출 실패 시 에러 처리 테스트"""
        # RecipeService Mock 설정
        mock_recipe_service.return_value.search_by_code.return_value = {
            "korean_name": "마티니",
            "tag1": "드라이",
            "tag2": "클래식"
        }
        
        # OpenAI Mock 설정 - API 에러 발생
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API 호출 실패")
        mock_openai.return_value = mock_client
        
        # 테스트 실행
        service = PersonaService()
        user_data = [{
            "name": "김철수",
            "gender": "남성",
            "favoriteTaste": "쓴맛"
        }]
        tasting_data = [{
            "code": "002",
            "drinkDate": "2024-01-15",
            "eval": 4,
            "sweetness": 1,
            "sourness": 2,
            "alcohol": 5
        }]
        
        result = service.generate_persona(user_data, tasting_data)
        
        # 검증 - 에러 발생 시 기본 메시지 반환
        assert result == "페르소나 생성에 실패했습니다."
