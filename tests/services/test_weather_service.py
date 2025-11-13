"""
WeatherService 단위 테스트
"""

import pytest
from unittest.mock import patch, MagicMock
from app.services.weather_service import WeatherService
import requests


class TestWeatherService:
    """WeatherService 테스트"""

    @pytest.fixture
    def weather_service(self, app):
        """WeatherService 인스턴스 생성"""
        with app.app_context():
            return WeatherService()

    @pytest.fixture
    def mock_weather_response(self):
        """모의 OpenWeather API 응답"""
        return {
            "weather": [{"id": 800, "main": "Clear", "description": "clear sky"}],
            "main": {"temp": 293.15},
        }

    def test_validate_coordinates_valid(self, weather_service):
        """유효한 좌표 검증 테스트"""
        # Given: 유효한 좌표
        latitude = 37.5665
        longitude = 126.9780

        # When: 좌표 검증
        result = weather_service._validate_coordinates(latitude, longitude)

        # Then: 검증 성공
        assert result is True

    def test_validate_coordinates_invalid_latitude(self, weather_service):
        """위도가 범위를 벗어난 경우 테스트"""
        # Given: 유효하지 않은 위도
        latitude = 91.0
        longitude = 126.9780

        # When: 좌표 검증
        result = weather_service._validate_coordinates(latitude, longitude)

        # Then: 검증 실패
        assert result is False

    def test_validate_coordinates_invalid_longitude(self, weather_service):
        """경도가 범위를 벗어난 경우 테스트"""
        # Given: 유효하지 않은 경도
        latitude = 37.5665
        longitude = 181.0

        # When: 좌표 검증
        result = weather_service._validate_coordinates(latitude, longitude)

        # Then: 검증 실패
        assert result is False

    def test_validate_coordinates_non_numeric(self, weather_service):
        """숫자가 아닌 좌표 테스트"""
        # Given: 숫자가 아닌 좌표
        latitude = "invalid"
        longitude = "invalid"

        # When: 좌표 검증
        result = weather_service._validate_coordinates(latitude, longitude)

        # Then: 검증 실패
        assert result is False

    @patch("requests.get")
    def test_get_weather_by_coordinates_success(self, mock_get, app, mock_weather_response):
        """날씨 정보 조회 성공 테스트"""
        # Given: 유효한 좌표와 API 키
        latitude = 37.5665
        longitude = 126.9780

        mock_response = MagicMock()
        mock_response.json.return_value = mock_weather_response
        mock_get.return_value = mock_response

        with app.app_context():
            app.config["WEATHER_API_KEY"] = "test_api_key"
            app.config["WEATHER_API_URL"] = "https://api.openweathermap.org/data/2.5/weather"
            weather_service = WeatherService()

            # When: 날씨 정보 조회
            result = weather_service.get_weather_by_coordinates(latitude, longitude)

            # Then: 날씨 정보 반환
            assert result["weather_description"] == "sunny"
            assert result["weather_code"] == 800
            mock_get.assert_called_once()

    def test_get_weather_by_coordinates_no_api_key(self, app):
        """API 키가 없는 경우 테스트"""
        with app.app_context():
            app.config["WEATHER_API_KEY"] = None
            weather_service = WeatherService()

            # When & Then: ValueError 발생
            with pytest.raises(ValueError, match="WEATHER_API_KEY가 설정되지 않았습니다"):
                weather_service.get_weather_by_coordinates(37.5665, 126.9780)

    def test_get_weather_by_coordinates_invalid_coordinates(self, app):
        """유효하지 않은 좌표 테스트"""
        with app.app_context():
            app.config["WEATHER_API_KEY"] = "test_api_key"
            weather_service = WeatherService()

            # When & Then: ValueError 발생
            with pytest.raises(ValueError, match="유효하지 않은 좌표입니다"):
                weather_service.get_weather_by_coordinates(91.0, 126.9780)

    @patch("requests.get")
    def test_get_weather_by_coordinates_api_timeout(self, mock_get, app):
        """API 요청 타임아웃 테스트"""
        # Given: API 요청이 타임아웃
        mock_get.side_effect = requests.Timeout()

        with app.app_context():
            app.config["WEATHER_API_KEY"] = "test_api_key"
            app.config["WEATHER_API_URL"] = "https://api.openweathermap.org/data/2.5/weather"
            weather_service = WeatherService()

            # When & Then: RequestException 발생
            with pytest.raises(requests.RequestException, match="날씨 API 요청 시간이 초과되었습니다"):
                weather_service.get_weather_by_coordinates(37.5665, 126.9780)

    @patch("requests.get")
    def test_get_weather_by_coordinates_api_error(self, mock_get, app):
        """API 요청 실패 테스트"""
        # Given: API 요청이 실패
        mock_get.side_effect = requests.RequestException("API Error")

        with app.app_context():
            app.config["WEATHER_API_KEY"] = "test_api_key"
            app.config["WEATHER_API_URL"] = "https://api.openweathermap.org/data/2.5/weather"
            weather_service = WeatherService()

            # When & Then: RequestException 발생
            with pytest.raises(requests.RequestException):
                weather_service.get_weather_by_coordinates(37.5665, 126.9780)

    @patch("requests.get")
    def test_get_weather_by_coordinates_cloudy(self, mock_get, app):
        """흐린 날씨 매핑 테스트"""
        # Given: 흐린 날씨 응답
        mock_response = MagicMock()
        mock_response.json.return_value = {"weather": [{"id": 803}]}
        mock_get.return_value = mock_response

        with app.app_context():
            app.config["WEATHER_API_KEY"] = "test_api_key"
            app.config["WEATHER_API_URL"] = "https://api.openweathermap.org/data/2.5/weather"
            weather_service = WeatherService()

            # When: 날씨 정보 조회
            result = weather_service.get_weather_by_coordinates(37.5665, 126.9780)

            # Then: 흐림으로 매핑
            assert result["weather_description"] == "cloudy"
            assert result["weather_code"] == 803

    @patch("requests.get")
    def test_get_weather_by_coordinates_rainy(self, mock_get, app):
        """비오는 날씨 매핑 테스트"""
        # Given: 비오는 날씨 응답
        mock_response = MagicMock()
        mock_response.json.return_value = {"weather": [{"id": 500}]}
        mock_get.return_value = mock_response

        with app.app_context():
            app.config["WEATHER_API_KEY"] = "test_api_key"
            app.config["WEATHER_API_URL"] = "https://api.openweathermap.org/data/2.5/weather"
            weather_service = WeatherService()

            # When: 날씨 정보 조회
            result = weather_service.get_weather_by_coordinates(37.5665, 126.9780)

            # Then: 비오는 날씨로 매핑
            assert result["weather_description"] == "rainy"
            assert result["weather_code"] == 500

    @patch("requests.get")
    def test_get_weather_by_coordinates_unknown_code(self, mock_get, app):
        """알 수 없는 날씨 코드 테스트"""
        # Given: 매핑되지 않은 날씨 코드
        mock_response = MagicMock()
        mock_response.json.return_value = {"weather": [{"id": 9999}]}
        mock_get.return_value = mock_response

        with app.app_context():
            app.config["WEATHER_API_KEY"] = "test_api_key"
            app.config["WEATHER_API_URL"] = "https://api.openweathermap.org/data/2.5/weather"
            weather_service = WeatherService()

            # When: 날씨 정보 조회
            result = weather_service.get_weather_by_coordinates(37.5665, 126.9780)

            # Then: unknown으로 매핑
            assert result["weather_description"] == "unknown"
            assert result["weather_code"] == 9999
