"""
RecommendationService 테스트
"""

import pytest
import json
from unittest.mock import Mock, MagicMock, patch
from app.services.recommendation_service import RecommendationService


class TestRecommendationService:
    """RecommendationService 테스트 클래스"""

    @pytest.fixture
    def mock_openai_client(self, mocker):
        """OpenAI 클라이언트 모킹"""
        mock_client = MagicMock()
        mocker.patch("app.services.recommendation_service.OpenAI", return_value=mock_client)
        return mock_client

    def test_init_without_rag(self, mocker):
        """RAG 미사용 초기화 테스트"""
        # Given: USE_RAG=false
        mocker.patch("os.getenv", side_effect=lambda key, default="false": "false" if key == "USE_RAG" else None)

        # When: RecommendationService 생성
        service = RecommendationService()

        # Then: RAG 서비스가 초기화되지 않음
        assert service.use_rag is False
        assert service.rag_service is None

    def test_init_with_rag(self, mocker):
        """RAG 사용 초기화 테스트"""
        # Given: USE_RAG=true
        def getenv_side_effect(key, default="false"):
            if key == "USE_RAG":
                return "true"
            return default

        mocker.patch("os.getenv", side_effect=getenv_side_effect)

        # RAGService 모킹 (모듈 import 레벨에서)
        mock_rag_service_class = MagicMock()
        mock_rag_service_instance = MagicMock()
        mock_rag_service_class.return_value = mock_rag_service_instance
        mocker.patch("app.services.rag_service.RAGService", mock_rag_service_class)

        # When: RecommendationService 생성
        service = RecommendationService()

        # Then: RAG 서비스가 초기화됨
        assert service.use_rag is True
        assert service.rag_service is not None

    def test_parse_cocktail_codes(self, mocker):
        """칵테일 코드 파싱 테스트"""
        # Given: USE_RAG=false로 초기화
        mocker.patch("os.getenv", return_value="false")
        service = RecommendationService()

        # When: JSON 형식의 cocktail_list 파싱
        cocktail_list = json.dumps([{"code": "300600", "name": "진토닉"}, {"code": "400600", "name": "보드카 토닉"}])
        codes = service._parse_cocktail_codes(cocktail_list)

        # Then: code 리스트 반환
        assert codes == ["300600", "400600"]

    def test_parse_cocktail_codes_invalid_json(self, mocker):
        """잘못된 JSON 파싱 테스트"""
        # Given
        mocker.patch("os.getenv", return_value="false")
        service = RecommendationService()

        # When: 잘못된 JSON
        cocktail_list = "not a valid json"
        codes = service._parse_cocktail_codes(cocktail_list)

        # Then: 빈 리스트 반환
        assert codes == []

    def test_get_feeling_recommendation_without_rag(self, mocker, mock_openai_client):
        """RAG 미사용 감정 추천 테스트"""
        # Given: USE_RAG=false
        mocker.patch("os.getenv", side_effect=lambda key, default="false": "false")
        mocker.patch("app.services.recommendation_service.match_cocktail_in_json", return_value={"matched": True})

        # OpenAI 응답 모킹
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({"recommendation": "test"})
        mock_openai_client.chat.completions.create.return_value = mock_response

        service = RecommendationService()

        # When: 감정 추천 요청
        result = service.get_feeling_recommendation(
            persona="테스트 페르소나", cocktail_list=json.dumps([{"code": "300600"}])
        )

        # Then: 추천 결과 반환
        assert result is not None
        result_data = json.loads(result)
        assert result_data["matched"] is True

        # RAG 관련 메서드 호출되지 않음
        assert service.rag_service is None

    def test_get_feeling_recommendation_with_rag(self, mocker, mock_openai_client):
        """RAG 사용 감정 추천 테스트"""
        # Given: USE_RAG=true
        def getenv_side_effect(key, default="false"):
            if key == "USE_RAG":
                return "true"
            elif key == "OPENAI_API_KEY":
                return "test-key"
            return default

        mocker.patch("os.getenv", side_effect=getenv_side_effect)

        # RAGService 모킹
        mock_rag_service_instance = MagicMock()
        mock_rag_service_instance.search_cocktails.return_value = [
            {"korean_name": "진토닉", "english_name": "Gin Tonic", "code": "300600"},
            {"korean_name": "모히또", "english_name": "Mojito", "code": "500601"},
        ]
        mock_rag_service_class = MagicMock(return_value=mock_rag_service_instance)
        mocker.patch("app.services.rag_service.RAGService", mock_rag_service_class)

        mocker.patch("app.services.recommendation_service.match_cocktail_in_json", return_value={"matched": True})

        # OpenAI 응답 모킹
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({"recommendation": "test"})
        mock_openai_client.chat.completions.create.return_value = mock_response

        service = RecommendationService()

        # When: 감정 추천 요청
        cocktail_list = json.dumps([{"code": "300600"}, {"code": "500601"}])
        result = service.get_feeling_recommendation(persona="테스트 페르소나", cocktail_list=cocktail_list)

        # Then: 추천 결과 반환
        assert result is not None
        result_data = json.loads(result)
        assert result_data["matched"] is True

        # RAG 검색이 3번 호출됨 (행복, 피곤, 화남)
        assert mock_rag_service_instance.search_cocktails.call_count == 3

        # OpenAI 호출 시 RAG 컨텍스트가 포함됨
        call_args = mock_openai_client.chat.completions.create.call_args
        system_message = call_args.kwargs["messages"][0]["content"][0]["text"]
        assert "행복에 어울리는 칵테일" in system_message or "위 목록에 있는 칵테일 중에서만" in system_message

    def test_get_feeling_recommendation_error_handling(self, mocker):
        """감정 추천 에러 처리 테스트"""
        # Given: OpenAI API 키 없음
        def getenv_side_effect(key, default="false"):
            if key == "OPENAI_API_KEY":
                return None
            return default

        mocker.patch("os.getenv", side_effect=getenv_side_effect)

        service = RecommendationService()

        # When: 감정 추천 요청
        result = service.get_feeling_recommendation(persona="테스트", cocktail_list="[]")

        # Then: 에러 메시지 반환
        result_data = json.loads(result)
        assert "error" in result_data

    def test_get_client_lazy_initialization(self, mocker, mock_openai_client):
        """OpenAI 클라이언트 지연 초기화 테스트"""
        # Given
        def getenv_side_effect(key, default="false"):
            if key == "OPENAI_API_KEY":
                return "test-key"
            return default

        mocker.patch("os.getenv", side_effect=getenv_side_effect)

        service = RecommendationService()

        # When: 첫 번째 호출
        client1 = service._get_client()

        # When: 두 번째 호출
        client2 = service._get_client()

        # Then: 동일한 클라이언트 인스턴스 반환
        assert client1 == client2
        assert service.client is not None

    def test_get_client_no_api_key(self, mocker):
        """OpenAI API 키 없을 때 에러 발생 테스트"""
        # Given: API 키 없음
        def getenv_side_effect(key, default="false"):
            if key == "OPENAI_API_KEY":
                return None
            return default

        mocker.patch("os.getenv", side_effect=getenv_side_effect)

        service = RecommendationService()

        # When & Then: ValueError 발생
        with pytest.raises(ValueError, match="OPENAI_API_KEY 환경 변수가 설정되지 않았습니다"):
            service._get_client()

    def test_get_default_recommendation(self, mocker, mock_openai_client):
        """기본 추천 테스트 (RAG 미사용)"""
        # Given
        mocker.patch("os.getenv", return_value="false")
        mocker.patch("app.services.recommendation_service.match_cocktail_in_json", return_value={"matched": True})

        # OpenAI 응답 모킹
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({"recommendation": "test"})
        mock_openai_client.chat.completions.create.return_value = mock_response

        service = RecommendationService()

        # When: 기본 추천 요청
        result = service.get_default_recommendation(
            persona="테스트 페르소나",
            cocktail_list="[]",
            season="봄",
            time="저녁",
            weather="맑음",
        )

        # Then: 추천 결과 반환
        assert result is not None
        result_data = json.loads(result)
        assert result_data["matched"] is True

    def test_get_default_recommendation_with_rag(self, mocker, mock_openai_client):
        """RAG 사용 기본 추천 테스트"""
        # Given: USE_RAG=true
        def getenv_side_effect(key, default="false"):
            if key == "USE_RAG":
                return "true"
            elif key == "OPENAI_API_KEY":
                return "test-key"
            return default

        mocker.patch("os.getenv", side_effect=getenv_side_effect)

        # RAGService 모킹
        mock_rag_service_instance = MagicMock()
        mock_rag_service_instance.search_cocktails.return_value = [
            {"korean_name": "진토닉", "english_name": "Gin Tonic", "code": "300600"},
            {"korean_name": "모히또", "english_name": "Mojito", "code": "500601"},
        ]
        mock_rag_service_class = MagicMock(return_value=mock_rag_service_instance)
        mocker.patch("app.services.rag_service.RAGService", mock_rag_service_class)

        mocker.patch("app.services.recommendation_service.match_cocktail_in_json", return_value={"matched": True})

        # OpenAI 응답 모킹
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({"recommendation": "test"})
        mock_openai_client.chat.completions.create.return_value = mock_response

        service = RecommendationService()

        # When: 기본 추천 요청
        cocktail_list = json.dumps([{"code": "300600"}, {"code": "500601"}])
        result = service.get_default_recommendation(
            persona="테스트 페르소나",
            cocktail_list=cocktail_list,
            season="봄",
            time="저녁",
            weather="맑음",
        )

        # Then: 추천 결과 반환
        assert result is not None
        result_data = json.loads(result)
        assert result_data["matched"] is True

        # RAG 검색이 3번 호출됨 (계절, 시간, 날씨)
        assert mock_rag_service_instance.search_cocktails.call_count == 3

        # OpenAI 호출 시 RAG 컨텍스트가 포함됨
        call_args = mock_openai_client.chat.completions.create.call_args
        system_message = call_args.kwargs["messages"][0]["content"][0]["text"]
        assert "위 목록에 있는 칵테일 중에서만" in system_message

    def test_get_situation_recommendation(self, mocker, mock_openai_client):
        """상황 추천 테스트 (RAG 미사용)"""
        # Given
        mocker.patch("os.getenv", return_value="false")
        mocker.patch("app.services.recommendation_service.match_cocktail_in_json", return_value={"matched": True})

        # OpenAI 응답 모킹
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({"recommendation": "test"})
        mock_openai_client.chat.completions.create.return_value = mock_response

        service = RecommendationService()

        # When: 상황 추천 요청
        result = service.get_situation_recommendation(persona="테스트 페르소나", cocktail_list="[]")

        # Then: 추천 결과 반환
        assert result is not None
        result_data = json.loads(result)
        assert result_data["matched"] is True

    def test_get_situation_recommendation_with_rag(self, mocker, mock_openai_client):
        """RAG 사용 상황 추천 테스트"""
        # Given: USE_RAG=true
        def getenv_side_effect(key, default="false"):
            if key == "USE_RAG":
                return "true"
            elif key == "OPENAI_API_KEY":
                return "test-key"
            return default

        mocker.patch("os.getenv", side_effect=getenv_side_effect)

        # RAGService 모킹
        mock_rag_service_instance = MagicMock()
        mock_rag_service_instance.search_cocktails.return_value = [
            {"korean_name": "진토닉", "english_name": "Gin Tonic", "code": "300600"},
            {"korean_name": "모히또", "english_name": "Mojito", "code": "500601"},
        ]
        mock_rag_service_class = MagicMock(return_value=mock_rag_service_instance)
        mocker.patch("app.services.rag_service.RAGService", mock_rag_service_class)

        mocker.patch("app.services.recommendation_service.match_cocktail_in_json", return_value={"matched": True})

        # OpenAI 응답 모킹
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({"recommendation": "test"})
        mock_openai_client.chat.completions.create.return_value = mock_response

        service = RecommendationService()

        # When: 상황 추천 요청
        cocktail_list = json.dumps([{"code": "300600"}, {"code": "500601"}])
        result = service.get_situation_recommendation(persona="테스트 페르소나", cocktail_list=cocktail_list)

        # Then: 추천 결과 반환
        assert result is not None
        result_data = json.loads(result)
        assert result_data["matched"] is True

        # RAG 검색이 3번 호출됨 (바쁨, 한가, 여행)
        assert mock_rag_service_instance.search_cocktails.call_count == 3

        # OpenAI 호출 시 RAG 컨텍스트가 포함됨
        call_args = mock_openai_client.chat.completions.create.call_args
        system_message = call_args.kwargs["messages"][0]["content"][0]["text"]
        assert "위 목록에 있는 칵테일 중에서만" in system_message
