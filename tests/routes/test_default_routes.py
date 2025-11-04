"""
DefaultRoutes 통합 테스트
"""

import pytest
from unittest.mock import patch


class TestDefaultRoutes:
    """DefaultRoutes 엔드포인트 테스트"""

    def test_index_returns_api_documentation(self, client):
        """
        GET / 엔드포인트 테스트
        API 문서를 정상적으로 반환하는지 검증
        """
        # Given: API 문서 데이터가 존재함
        mock_api_rules = {
            "title": "Mixby API Documentation",
            "version": "1.0.0",
            "endpoints": [
                {
                    "path": "/health",
                    "method": "GET",
                    "description": "헬스 체크"
                },
                {
                    "path": "/drink/all",
                    "method": "GET",
                    "description": "전체 주류 조회"
                }
            ]
        }

        with patch('app.utils.data_loader.data_loader.load_json') as mock_load:
            mock_load.return_value = mock_api_rules

            # When: / 엔드포인트 호출
            response = client.get('/')

            # Then: 200 상태 코드와 API 문서 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data == mock_api_rules
            assert data["title"] == "Mixby API Documentation"
            assert data["version"] == "1.0.0"
            assert "endpoints" in data
            mock_load.assert_called_once_with("api_rules.json")

    def test_index_response_format(self, client):
        """
        GET / 엔드포인트 응답 형식 테스트
        응답이 JSON 형식인지 검증
        """
        # Given: API 문서 데이터가 존재함
        mock_api_rules = {
            "title": "Test API",
            "endpoints": []
        }

        with patch('app.utils.data_loader.data_loader.load_json') as mock_load:
            mock_load.return_value = mock_api_rules

            # When: / 엔드포인트 호출
            response = client.get('/')

            # Then: JSON 응답 반환
            assert response.status_code == 200
            assert response.content_type == "application/json"
            data = response.get_json()
            assert isinstance(data, dict)

    def test_index_loads_correct_file(self, client):
        """
        GET / 엔드포인트 파일 로딩 테스트
        api_rules.json 파일을 올바르게 로드하는지 검증
        """
        # Given: data_loader가 정상 동작함
        mock_api_rules = {"test": "data"}

        with patch('app.utils.data_loader.data_loader.load_json') as mock_load:
            mock_load.return_value = mock_api_rules

            # When: / 엔드포인트 호출
            response = client.get('/')

            # Then: api_rules.json 파일을 로드함
            assert response.status_code == 200
            mock_load.assert_called_once_with("api_rules.json")

    def test_index_handles_empty_api_rules(self, client):
        """
        GET / 엔드포인트 빈 데이터 처리 테스트
        API 문서가 비어있어도 정상 응답하는지 검증
        """
        # Given: API 문서가 비어있음
        mock_api_rules = {}

        with patch('app.utils.data_loader.data_loader.load_json') as mock_load:
            mock_load.return_value = mock_api_rules

            # When: / 엔드포인트 호출
            response = client.get('/')

            # Then: 200 상태 코드와 빈 객체 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data == {}
