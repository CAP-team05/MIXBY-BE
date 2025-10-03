"""
RecommendationRoutes 통합 테스트
"""

import pytest
from unittest.mock import patch, MagicMock


class TestRecommendationRoutes:
    """RecommendationRoutes 엔드포인트 테스트"""

    def test_generate_persona_success(self, client, sample_user_data, sample_tasting_data):
        """
        POST /api/recommendations/persona 엔드포인트 테스트 (성공)
        유효한 데이터로 페르소나 생성 요청 시 페르소나를 정상적으로 반환하는지 검증
        """
        # Given: 유효한 사용자 데이터와 테이스팅 데이터가 존재함
        mock_persona = {
            "summary": "단맛을 선호하는 남성 사용자",
            "preferences": {
                "sweetness": 4,
                "sourness": 2,
                "alcohol": 3
            }
        }

        with patch('app.services.persona_service.PersonaService.generate_persona') as mock_generate:
            mock_generate.return_value = mock_persona

            # When: /api/recommendations/persona 엔드포인트 호출
            response = client.post(
                '/api/recommendations/persona',
                json={
                    'user_data': sample_user_data,
                    'tasting_data': sample_tasting_data
                }
            )

            # Then: 200 상태 코드와 페르소나 데이터 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert "persona" in data["data"]
            assert data["data"]["persona"] == mock_persona
            assert data["data"]["persona"]["summary"] == "단맛을 선호하는 남성 사용자"
            mock_generate.assert_called_once_with(sample_user_data, sample_tasting_data)

    def test_generate_persona_missing_fields(self, client):
        """
        POST /api/recommendations/persona 엔드포인트 테스트 (필수 필드 누락)
        필수 필드가 누락된 경우 400 에러를 반환하는지 검증
        """
        # Test 1: user_data 누락
        # Given: user_data가 누락된 요청 데이터
        # When: /api/recommendations/persona 엔드포인트 호출
        response = client.post(
            '/api/recommendations/persona',
            json={
                'tasting_data': []
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "user_data" in data["message"]

        # Test 2: tasting_data 누락
        # Given: tasting_data가 누락된 요청 데이터
        # When: /api/recommendations/persona 엔드포인트 호출
        response = client.post(
            '/api/recommendations/persona',
            json={
                'user_data': [{"name": "테스트"}]
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "tasting_data" in data["message"]

        # Test 3: 모든 필드 누락
        # Given: 빈 요청 데이터
        # When: /api/recommendations/persona 엔드포인트 호출
        response = client.post(
            '/api/recommendations/persona',
            json={}
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False

    def test_generate_persona_invalid_data_types(self, client):
        """
        POST /api/recommendations/persona 엔드포인트 테스트 (잘못된 데이터 타입)
        잘못된 데이터 타입이 전달된 경우 400 에러를 반환하는지 검증
        """
        # Test 1: user_data가 리스트가 아닌 경우
        # Given: user_data가 문자열인 요청 데이터
        # When: /api/recommendations/persona 엔드포인트 호출
        response = client.post(
            '/api/recommendations/persona',
            json={
                'user_data': "not a list",
                'tasting_data': []
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "리스트" in data["message"]

        # Test 2: user_data가 빈 리스트인 경우
        # Given: user_data가 빈 리스트인 요청 데이터
        # When: /api/recommendations/persona 엔드포인트 호출
        response = client.post(
            '/api/recommendations/persona',
            json={
                'user_data': [],
                'tasting_data': []
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "비어있지 않은" in data["message"]

        # Test 3: tasting_data가 리스트가 아닌 경우
        # Given: tasting_data가 딕셔너리인 요청 데이터
        # When: /api/recommendations/persona 엔드포인트 호출
        response = client.post(
            '/api/recommendations/persona',
            json={
                'user_data': [{"name": "테스트"}],
                'tasting_data': {"invalid": "data"}
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "리스트" in data["message"]

    def test_get_default_recommendation_success(self, client):
        """
        POST /api/recommendations/default 엔드포인트 테스트 (성공)
        유효한 데이터로 기본 추천 요청 시 추천 결과를 정상적으로 반환하는지 검증
        """
        # Given: 유효한 페르소나와 칵테일 리스트가 존재함
        mock_recommendation = {
            "recommended_cocktail": "진토닉",
            "reason": "상쾌한 가을 저녁에 어울리는 칵테일입니다.",
            "season": "가을",
            "time": "저녁",
            "weather": "눈"
        }

        with patch('app.services.recommendation_service.RecommendationService.get_default_recommendation') as mock_recommend:
            mock_recommend.return_value = mock_recommendation

            # When: /api/recommendations/default 엔드포인트 호출
            response = client.post(
                '/api/recommendations/default',
                json={
                    'persona': '단맛을 선호하는 사용자',
                    'cocktail_list': '진토닉, 모히또, 마가리타',
                    'season': '가을',
                    'time': '저녁',
                    'weather': '눈'
                }
            )

            # Then: 200 상태 코드와 추천 데이터 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert "recommendation" in data["data"]
            assert data["data"]["recommendation"] == mock_recommendation
            assert data["data"]["recommendation"]["recommended_cocktail"] == "진토닉"
            assert data["data"]["recommendation"]["season"] == "가을"
            mock_recommend.assert_called_once_with(
                '단맛을 선호하는 사용자',
                '진토닉, 모히또, 마가리타',
                '가을',
                '저녁',
                '눈'
            )

    def test_get_default_recommendation_missing_fields(self, client):
        """
        POST /api/recommendations/default 엔드포인트 테스트 (필수 필드 누락)
        필수 필드가 누락된 경우 400 에러를 반환하는지 검증
        """
        # Test 1: persona 누락
        # Given: persona가 누락된 요청 데이터
        # When: /api/recommendations/default 엔드포인트 호출
        response = client.post(
            '/api/recommendations/default',
            json={
                'cocktail_list': '진토닉, 모히또',
                'season': '가을',
                'time': '저녁',
                'weather': '눈'
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "persona" in data["message"]

        # Test 2: cocktail_list 누락
        # Given: cocktail_list가 누락된 요청 데이터
        # When: /api/recommendations/default 엔드포인트 호출
        response = client.post(
            '/api/recommendations/default',
            json={
                'persona': '단맛을 선호하는 사용자',
                'season': '가을',
                'time': '저녁',
                'weather': '눈'
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "cocktail_list" in data["message"]

        # Test 3: season 누락
        # Given: season이 누락된 요청 데이터
        # When: /api/recommendations/default 엔드포인트 호출
        response = client.post(
            '/api/recommendations/default',
            json={
                'persona': '단맛을 선호하는 사용자',
                'cocktail_list': '진토닉, 모히또',
                'time': '저녁',
                'weather': '눈'
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "season" in data["message"]

        # Test 4: time 누락
        # Given: time이 누락된 요청 데이터
        # When: /api/recommendations/default 엔드포인트 호출
        response = client.post(
            '/api/recommendations/default',
            json={
                'persona': '단맛을 선호하는 사용자',
                'cocktail_list': '진토닉, 모히또',
                'season': '가을',
                'weather': '눈'
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "time" in data["message"]

        # Test 5: weather 누락
        # Given: weather가 누락된 요청 데이터
        # When: /api/recommendations/default 엔드포인트 호출
        response = client.post(
            '/api/recommendations/default',
            json={
                'persona': '단맛을 선호하는 사용자',
                'cocktail_list': '진토닉, 모히또',
                'season': '가을',
                'time': '저녁'
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "weather" in data["message"]

        # Test 6: 모든 필드 누락
        # Given: 빈 요청 데이터
        # When: /api/recommendations/default 엔드포인트 호출
        response = client.post(
            '/api/recommendations/default',
            json={}
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False

    def test_get_feeling_recommendation_success(self, client):
        """
        POST /api/recommendations/feeling 엔드포인트 테스트 (성공)
        유효한 데이터로 감정 기반 추천 요청 시 추천 결과를 정상적으로 반환하는지 검증
        """
        # Given: 유효한 페르소나와 칵테일 리스트가 존재함
        mock_recommendation = {
            "happy": {
                "cocktail": "모히또",
                "reason": "행복한 기분에 어울리는 상쾌한 칵테일입니다."
            },
            "tired": {
                "cocktail": "위스키 사워",
                "reason": "피곤할 때 기분을 전환시켜주는 칵테일입니다."
            },
            "angry": {
                "cocktail": "마가리타",
                "reason": "화난 기분을 달래주는 칵테일입니다."
            }
        }

        with patch('app.services.recommendation_service.RecommendationService.get_feeling_recommendation') as mock_recommend:
            mock_recommend.return_value = mock_recommendation

            # When: /api/recommendations/feeling 엔드포인트 호출
            response = client.post(
                '/api/recommendations/feeling',
                json={
                    'persona': '단맛을 선호하는 사용자',
                    'cocktail_list': '진토닉, 모히또, 마가리타, 위스키 사워'
                }
            )

            # Then: 200 상태 코드와 추천 데이터 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert "recommendation" in data["data"]
            assert data["data"]["recommendation"] == mock_recommendation
            assert "happy" in data["data"]["recommendation"]
            assert "tired" in data["data"]["recommendation"]
            assert "angry" in data["data"]["recommendation"]
            assert data["data"]["recommendation"]["happy"]["cocktail"] == "모히또"
            mock_recommend.assert_called_once_with(
                '단맛을 선호하는 사용자',
                '진토닉, 모히또, 마가리타, 위스키 사워'
            )

    def test_get_feeling_recommendation_missing_fields(self, client):
        """
        POST /api/recommendations/feeling 엔드포인트 테스트 (필수 필드 누락)
        필수 필드가 누락된 경우 400 에러를 반환하는지 검증
        """
        # Test 1: persona 누락
        # Given: persona가 누락된 요청 데이터
        # When: /api/recommendations/feeling 엔드포인트 호출
        response = client.post(
            '/api/recommendations/feeling',
            json={
                'cocktail_list': '진토닉, 모히또'
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "persona" in data["message"]

        # Test 2: cocktail_list 누락
        # Given: cocktail_list가 누락된 요청 데이터
        # When: /api/recommendations/feeling 엔드포인트 호출
        response = client.post(
            '/api/recommendations/feeling',
            json={
                'persona': '단맛을 선호하는 사용자'
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "cocktail_list" in data["message"]

        # Test 3: 모든 필드 누락
        # Given: 빈 요청 데이터
        # When: /api/recommendations/feeling 엔드포인트 호출
        response = client.post(
            '/api/recommendations/feeling',
            json={}
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False

    def test_get_situation_recommendation_success(self, client):
        """
        POST /api/recommendations/situation 엔드포인트 테스트 (성공)
        유효한 데이터로 상황 기반 추천 요청 시 추천 결과를 정상적으로 반환하는지 검증
        """
        # Given: 유효한 페르소나와 칵테일 리스트가 존재함
        mock_recommendation = {
            "busy": {
                "cocktail": "진토닉",
                "reason": "바쁜 일상에서 간단하게 즐길 수 있는 칵테일입니다."
            },
            "relaxed": {
                "cocktail": "모히또",
                "reason": "여유로운 시간에 천천히 즐기기 좋은 칵테일입니다."
            },
            "travel": {
                "cocktail": "마가리타",
                "reason": "여행지에서 즐기기 좋은 이국적인 칵테일입니다."
            }
        }

        with patch('app.services.recommendation_service.RecommendationService.get_situation_recommendation') as mock_recommend:
            mock_recommend.return_value = mock_recommendation

            # When: /api/recommendations/situation 엔드포인트 호출
            response = client.post(
                '/api/recommendations/situation',
                json={
                    'persona': '단맛을 선호하는 사용자',
                    'cocktail_list': '진토닉, 모히또, 마가리타'
                }
            )

            # Then: 200 상태 코드와 추천 데이터 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert "recommendation" in data["data"]
            assert data["data"]["recommendation"] == mock_recommendation
            assert "busy" in data["data"]["recommendation"]
            assert "relaxed" in data["data"]["recommendation"]
            assert "travel" in data["data"]["recommendation"]
            assert data["data"]["recommendation"]["busy"]["cocktail"] == "진토닉"
            mock_recommend.assert_called_once_with(
                '단맛을 선호하는 사용자',
                '진토닉, 모히또, 마가리타'
            )

    def test_get_situation_recommendation_missing_fields(self, client):
        """
        POST /api/recommendations/situation 엔드포인트 테스트 (필수 필드 누락)
        필수 필드가 누락된 경우 400 에러를 반환하는지 검증
        """
        # Test 1: persona 누락
        # Given: persona가 누락된 요청 데이터
        # When: /api/recommendations/situation 엔드포인트 호출
        response = client.post(
            '/api/recommendations/situation',
            json={
                'cocktail_list': '진토닉, 모히또'
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "persona" in data["message"]

        # Test 2: cocktail_list 누락
        # Given: cocktail_list가 누락된 요청 데이터
        # When: /api/recommendations/situation 엔드포인트 호출
        response = client.post(
            '/api/recommendations/situation',
            json={
                'persona': '단맛을 선호하는 사용자'
            }
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "cocktail_list" in data["message"]

        # Test 3: 모든 필드 누락
        # Given: 빈 요청 데이터
        # When: /api/recommendations/situation 엔드포인트 호출
        response = client.post(
            '/api/recommendations/situation',
            json={}
        )

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
