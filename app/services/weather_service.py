"""
날씨 정보 조회 서비스
OpenWeatherMap API를 사용하여 날씨 정보를 제공합니다.
"""

import requests
import logging
from typing import Dict
from flask import current_app

logger = logging.getLogger(__name__)


class WeatherService:
    """날씨 정보를 관리하는 서비스 클래스"""

    # OpenWeather API 날씨 코드를 영문 날씨 상태로 매핑
    WEATHER_CODE_MAPPING = {
        # Thunderstorm
        200: "thunderstorm",
        201: "thunderstorm",
        202: "thunderstorm",
        210: "thunderstorm",
        211: "thunderstorm",
        212: "thunderstorm",
        221: "thunderstorm",
        230: "thunderstorm",
        231: "thunderstorm",
        232: "thunderstorm",
        # Drizzle
        300: "drizzle",
        301: "drizzle",
        302: "drizzle",
        310: "drizzle",
        311: "drizzle",
        312: "drizzle",
        313: "drizzle",
        314: "drizzle",
        321: "drizzle",
        # Rain
        500: "rainy",
        501: "rainy",
        502: "rainy",
        503: "rainy",
        504: "rainy",
        511: "rainy",
        520: "rainy",
        521: "rainy",
        522: "rainy",
        531: "rainy",
        # Snow
        600: "snowy",
        601: "snowy",
        602: "snowy",
        611: "snowy",
        612: "snowy",
        613: "snowy",
        615: "snowy",
        616: "snowy",
        620: "snowy",
        621: "snowy",
        622: "snowy",
        # Atmosphere
        701: "foggy",
        711: "foggy",
        721: "foggy",
        731: "foggy",
        741: "foggy",
        751: "foggy",
        761: "foggy",
        762: "foggy",
        771: "foggy",
        781: "foggy",
        # Clear
        800: "sunny",
        # Clouds
        801: "cloudy",
        802: "cloudy",
        803: "cloudy",
        804: "cloudy",
    }

    def get_weather_by_coordinates(self, latitude: float, longitude: float) -> Dict:
        """
        위도와 경도를 기반으로 날씨 정보를 조회합니다.

        Args:
            latitude: 위도
            longitude: 경도

        Returns:
            날씨 정보 딕셔너리 (weather_description, weather_code)

        Raises:
            ValueError: API 키가 설정되지 않았거나 좌표가 유효하지 않은 경우
            requests.RequestException: API 요청 실패 시
        """
        # API 키 확인
        api_key = current_app.config.get("WEATHER_API_KEY")
        if not api_key:
            raise ValueError("WEATHER_API_KEY가 설정되지 않았습니다.")

        # 좌표 유효성 검증
        if not self._validate_coordinates(latitude, longitude):
            raise ValueError("유효하지 않은 좌표입니다. 위도는 -90 ~ 90, 경도는 -180 ~ 180 사이여야 합니다.")

        # API 요청
        api_url = current_app.config.get("WEATHER_API_URL")
        params = {"lat": latitude, "lon": longitude, "appid": api_key}

        try:
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # 날씨 코드 추출
            weather_code = data.get("weather", [{}])[0].get("id")
            if not weather_code:
                raise ValueError("날씨 정보를 찾을 수 없습니다.")

            # 날씨 설명 매핑
            weather_description = self.WEATHER_CODE_MAPPING.get(weather_code, "unknown")

            return {"weather_description": weather_description, "weather_code": weather_code}

        except requests.Timeout:
            logger.error(f"날씨 API 요청 타임아웃: lat={latitude}, lon={longitude}")
            raise requests.RequestException("날씨 API 요청 시간이 초과되었습니다.")
        except requests.RequestException as e:
            logger.error(f"날씨 API 요청 실패: {str(e)}")
            raise

    def _validate_coordinates(self, latitude: float, longitude: float) -> bool:
        """
        위도와 경도의 유효성을 검증합니다.

        Args:
            latitude: 위도
            longitude: 경도

        Returns:
            유효 여부
        """
        try:
            lat = float(latitude)
            lon = float(longitude)
            return -90 <= lat <= 90 and -180 <= lon <= 180
        except (TypeError, ValueError):
            return False


# 전역 서비스 인스턴스
weather_service = WeatherService()
