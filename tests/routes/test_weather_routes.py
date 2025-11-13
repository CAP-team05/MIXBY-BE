"""
WeatherRoutes 통합 테스트
"""

from unittest.mock import patch
import requests


class TestWeatherRoutes:
    """WeatherRoutes 엔드포인트 테스트"""

    def test_get_weather_success(self, client):
        """
        POST /weather 엔드포인트 성공 테스트
        정상적으로 날씨 정보를 조회하는지 검증
        """
        # Given: 유효한 위도와 경도
        payload = {"latitude": 37.5665, "longitude": 126.9780}

        # Mock weather service
        with patch("app.routes.weather_routes.weather_service.get_weather_by_coordinates") as mock_weather:
            mock_weather.return_value = {"weather_description": "sunny", "weather_code": 800}

            # When: POST /weather 엔드포인트 호출
            response = client.post("/weather", json=payload)

            # Then: 200 상태 코드와 날씨 정보 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["message"] == "날씨 정보를 성공적으로 조회했습니다."
            assert data["data"]["weather_description"] == "sunny"
            assert data["data"]["weather_code"] == 800

    def test_get_weather_missing_latitude(self, client):
        """
        POST /weather 엔드포인트 latitude 누락 테스트
        latitude가 없는 경우 에러를 반환하는지 검증
        """
        # Given: longitude만 있는 요청
        payload = {"longitude": 126.9780}

        # When: POST /weather 엔드포인트 호출
        response = client.post("/weather", json=payload)

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "latitude와 longitude는 필수 입력값입니다" in data["message"]

    def test_get_weather_missing_longitude(self, client):
        """
        POST /weather 엔드포인트 longitude 누락 테스트
        longitude가 없는 경우 에러를 반환하는지 검증
        """
        # Given: latitude만 있는 요청
        payload = {"latitude": 37.5665}

        # When: POST /weather 엔드포인트 호출
        response = client.post("/weather", json=payload)

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "latitude와 longitude는 필수 입력값입니다" in data["message"]

    def test_get_weather_empty_body(self, client):
        """
        POST /weather 엔드포인트 빈 요청 본문 테스트
        요청 본문이 비어있는 경우 에러를 반환하는지 검증
        """
        # Given: 빈 요청 본문

        # When: POST /weather 엔드포인트 호출
        response = client.post("/weather", json=None)

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "요청 본문이 비어있습니다" in data["message"]

    def test_get_weather_invalid_latitude_type(self, client):
        """
        POST /weather 엔드포인트 latitude 타입 오류 테스트
        latitude가 숫자가 아닌 경우 에러를 반환하는지 검증
        """
        # Given: latitude가 문자열인 요청
        payload = {"latitude": "invalid", "longitude": 126.9780}

        # When: POST /weather 엔드포인트 호출
        response = client.post("/weather", json=payload)

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "latitude와 longitude는 숫자여야 합니다" in data["message"]

    def test_get_weather_invalid_longitude_type(self, client):
        """
        POST /weather 엔드포인트 longitude 타입 오류 테스트
        longitude가 숫자가 아닌 경우 에러를 반환하는지 검증
        """
        # Given: longitude가 문자열인 요청
        payload = {"latitude": 37.5665, "longitude": "invalid"}

        # When: POST /weather 엔드포인트 호출
        response = client.post("/weather", json=payload)

        # Then: 400 상태 코드와 에러 메시지 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "latitude와 longitude는 숫자여야 합니다" in data["message"]

    def test_get_weather_invalid_coordinates(self, client):
        """
        POST /weather 엔드포인트 유효하지 않은 좌표 테스트
        좌표가 유효 범위를 벗어난 경우 에러를 반환하는지 검증
        """
        # Given: 유효하지 않은 좌표
        payload = {"latitude": 91.0, "longitude": 126.9780}

        # Mock weather service to raise ValueError
        with patch("app.routes.weather_routes.weather_service.get_weather_by_coordinates") as mock_weather:
            mock_weather.side_effect = ValueError(
                "유효하지 않은 좌표입니다. 위도는 -90 ~ 90, 경도는 -180 ~ 180 사이여야 합니다."
            )

            # When: POST /weather 엔드포인트 호출
            response = client.post("/weather", json=payload)

            # Then: 400 상태 코드와 에러 메시지 반환
            assert response.status_code == 400
            data = response.get_json()
            assert data["success"] is False
            assert "유효하지 않은 좌표입니다" in data["message"]

    def test_get_weather_api_error(self, client):
        """
        POST /weather 엔드포인트 API 오류 테스트
        날씨 API 호출 실패 시 에러를 반환하는지 검증
        """
        # Given: 유효한 위도와 경도
        payload = {"latitude": 37.5665, "longitude": 126.9780}

        # Mock weather service to raise RequestException
        with patch("app.routes.weather_routes.weather_service.get_weather_by_coordinates") as mock_weather:
            mock_weather.side_effect = requests.RequestException("API Error")

            # When: POST /weather 엔드포인트 호출
            response = client.post("/weather", json=payload)

            # Then: 503 상태 코드와 에러 메시지 반환
            assert response.status_code == 503
            data = response.get_json()
            assert data["success"] is False
            assert data["error_code"] == "WEATHER_API_ERROR"

    def test_get_weather_internal_error(self, client):
        """
        POST /weather 엔드포인트 내부 오류 테스트
        예상치 못한 오류 발생 시 에러를 반환하는지 검증
        """
        # Given: 유효한 위도와 경도
        payload = {"latitude": 37.5665, "longitude": 126.9780}

        # Mock weather service to raise generic Exception
        with patch("app.routes.weather_routes.weather_service.get_weather_by_coordinates") as mock_weather:
            mock_weather.side_effect = Exception("Unexpected Error")

            # When: POST /weather 엔드포인트 호출
            response = client.post("/weather", json=payload)

            # Then: 500 상태 코드와 에러 메시지 반환
            assert response.status_code == 500
            data = response.get_json()
            assert data["success"] is False
            assert data["error_code"] == "INTERNAL_ERROR"

    def test_get_weather_cloudy(self, client):
        """
        POST /weather 엔드포인트 흐린 날씨 테스트
        흐린 날씨 정보를 정상적으로 반환하는지 검증
        """
        # Given: 유효한 위도와 경도
        payload = {"latitude": 37.5665, "longitude": 126.9780}

        # Mock weather service
        with patch("app.routes.weather_routes.weather_service.get_weather_by_coordinates") as mock_weather:
            mock_weather.return_value = {"weather_description": "cloudy", "weather_code": 803}

            # When: POST /weather 엔드포인트 호출
            response = client.post("/weather", json=payload)

            # Then: 200 상태 코드와 흐린 날씨 정보 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["data"]["weather_description"] == "cloudy"
            assert data["data"]["weather_code"] == 803

    def test_get_weather_rainy(self, client):
        """
        POST /weather 엔드포인트 비오는 날씨 테스트
        비오는 날씨 정보를 정상적으로 반환하는지 검증
        """
        # Given: 유효한 위도와 경도
        payload = {"latitude": 37.5665, "longitude": 126.9780}

        # Mock weather service
        with patch("app.routes.weather_routes.weather_service.get_weather_by_coordinates") as mock_weather:
            mock_weather.return_value = {"weather_description": "rainy", "weather_code": 500}

            # When: POST /weather 엔드포인트 호출
            response = client.post("/weather", json=payload)

            # Then: 200 상태 코드와 비오는 날씨 정보 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["data"]["weather_description"] == "rainy"
            assert data["data"]["weather_code"] == 500

    def test_get_weather_response_format(self, client):
        """
        POST /weather 엔드포인트 응답 형식 테스트
        응답이 표준 형식을 따르는지 검증
        """
        # Given: 유효한 위도와 경도
        payload = {"latitude": 37.5665, "longitude": 126.9780}

        # Mock weather service
        with patch("app.routes.weather_routes.weather_service.get_weather_by_coordinates") as mock_weather:
            mock_weather.return_value = {"weather_description": "sunny", "weather_code": 800}

            # When: POST /weather 엔드포인트 호출
            response = client.post("/weather", json=payload)

            # Then: 표준 응답 형식 검증
            assert response.status_code == 200
            data = response.get_json()
            assert "success" in data
            assert "message" in data
            assert "data" in data
            assert isinstance(data["success"], bool)
            assert isinstance(data["message"], str)
            assert isinstance(data["data"], dict)
            assert "weather_description" in data["data"]
            assert "weather_code" in data["data"]
