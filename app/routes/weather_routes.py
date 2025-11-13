"""
날씨 관련 API 라우트
"""

from flask import Blueprint, request
from app.services.weather_service import weather_service
from app.utils.response_helper import response_helper
import requests

# Blueprint 생성
weather_bp = Blueprint("weather", __name__, url_prefix="/weather")


@weather_bp.route("", methods=["POST"])
def get_weather():
    """
    위도와 경도를 기반으로 날씨 정보를 조회합니다.

    Request Body:
        {
            "latitude": float,
            "longitude": float
        }

    Returns:
        JSON 응답: 날씨 정보 (weather_description, weather_code)
    """
    try:
        # 요청 데이터 가져오기
        data = request.get_json(silent=True)

        if not data:
            return response_helper.validation_error_response("요청 본문이 비어있습니다.")

        # 필수 필드 확인
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if latitude is None or longitude is None:
            return response_helper.validation_error_response("latitude와 longitude는 필수 입력값입니다.")

        # 타입 변환 및 유효성 검증
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            return response_helper.validation_error_response("latitude와 longitude는 숫자여야 합니다.")

        # 날씨 정보 조회
        weather_info = weather_service.get_weather_by_coordinates(latitude, longitude)

        return response_helper.success_response(data=weather_info, message="날씨 정보를 성공적으로 조회했습니다.")

    except ValueError:
        return response_helper.error_response(
            message="유효하지 않은 좌표입니다.", status_code=400, error_code="VALIDATION_ERROR"
        )
    except requests.RequestException:
        return response_helper.error_response(
            message="날씨 정보를 가져오는 중 오류가 발생했습니다.", status_code=503, error_code="WEATHER_API_ERROR"
        )
    except Exception:
        return response_helper.error_response(
            message="날씨 정보 조회 중 오류가 발생했습니다.", status_code=500, error_code="INTERNAL_ERROR"
        )
