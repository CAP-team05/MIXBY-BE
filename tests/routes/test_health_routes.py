"""
HealthRoutes 통합 테스트
"""

import pytest


class TestHealthRoutes:
    """HealthRoutes 엔드포인트 테스트"""

    def test_health_check(self, client):
        """
        GET /health 엔드포인트 테스트
        헬스 체크가 정상적으로 동작하는지 검증
        """
        # Given: 서버가 실행 중임

        # When: /health 엔드포인트 호출
        response = client.get('/health')

        # Then: 200 상태 코드와 healthy 상태 반환
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["message"] == "서버가 정상적으로 동작 중입니다."
        assert data["data"]["status"] == "healthy"

    def test_health_check_response_format(self, client):
        """
        GET /health 엔드포인트 응답 형식 테스트
        응답이 표준 형식을 따르는지 검증
        """
        # Given: 서버가 실행 중임

        # When: /health 엔드포인트 호출
        response = client.get('/health')

        # Then: 표준 응답 형식 검증
        assert response.status_code == 200
        data = response.get_json()
        assert "success" in data
        assert "message" in data
        assert "data" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["message"], str)
        assert isinstance(data["data"], dict)

    def test_health_check_content_type(self, client):
        """
        GET /health 엔드포인트 Content-Type 테스트
        응답이 JSON 형식인지 검증
        """
        # Given: 서버가 실행 중임

        # When: /health 엔드포인트 호출
        response = client.get('/health')

        # Then: Content-Type이 JSON임
        assert response.status_code == 200
        assert response.content_type == "application/json"
