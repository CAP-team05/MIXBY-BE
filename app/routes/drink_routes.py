"""
음료 관련 API 라우트
"""

from flask import Blueprint, send_from_directory, current_app
from app.services.drink_service import drink_service
from app.utils.response_helper import response_helper
from app.utils.validators import validator
import os

# Blueprint 생성
drink_bp = Blueprint("drinks", __name__, url_prefix="/drink")


@drink_bp.route("/all")
def get_all_drinks():
    """모든 음료 데이터를 반환합니다."""
    try:
        drinks = drink_service.get_all_drinks()
        return response_helper.json_response(drinks)
    except Exception as e:
        return response_helper.error_response(message="음료 데이터를 가져오는 중 오류가 발생했습니다.", status_code=500)


@drink_bp.route("/image=<code>")
def get_drink_image(code):
    """음료 이미지를 반환합니다."""
    try:
        static_dir = current_app.static_folder
        image_path = os.path.join(static_dir, "drinks", f"{code}.png")

        if os.path.exists(image_path):
            return send_from_directory(os.path.join(static_dir, "drinks"), f"{code}.png")
        else:
            return response_helper.not_found_response("이미지")
    except Exception as e:
        return response_helper.error_response(message="이미지를 가져오는 중 오류가 발생했습니다.", status_code=500)


@drink_bp.route("/code=<code>")
def get_drink_by_code(code):
    """코드로 음료를 검색합니다."""
    try:
        # 입력 검증
        validation_errors = validator.validate_code(code, "음료 코드")
        if validation_errors:
            return response_helper.validation_error_response(validation_errors)

        # 코드 정제
        sanitized_code = validator.sanitize_string(code, 50)

        drink = drink_service.search_by_code(sanitized_code)
        if drink:
            return response_helper.json_response(drink)
        else:
            return response_helper.not_found_response("음료")
    except Exception as e:
        return response_helper.error_response(message="음료 검색 중 오류가 발생했습니다.", status_code=500)


@drink_bp.route("/name=<name>")
def get_drink_by_name(name):
    """이름으로 음료를 검색합니다."""
    try:
        # 입력 검증
        validation_errors = validator.validate_search_query(name, "음료명")
        if validation_errors:
            return response_helper.validation_error_response(validation_errors)

        # 검색어 정제
        sanitized_name = validator.sanitize_string(name, 100)

        drinks = drink_service.search_by_name(sanitized_name)
        return response_helper.search_response(results=drinks, query=sanitized_name)
    except Exception as e:
        return response_helper.error_response(message="음료 검색 중 오류가 발생했습니다.", status_code=500)


@drink_bp.route("/type=<drink_type>")
def get_drink_by_type(drink_type):
    """타입으로 음료를 검색합니다."""
    try:
        drinks = drink_service.search_by_type(drink_type)
        return response_helper.search_response(results=drinks, query=drink_type)
    except Exception as e:
        return response_helper.error_response(message="음료 검색 중 오류가 발생했습니다.", status_code=500)


@drink_bp.route("/types")
def get_drink_types():
    """사용 가능한 모든 음료 타입을 반환합니다."""
    try:
        types = drink_service.get_drink_types()
        return response_helper.json_response(types)
    except Exception as e:
        return response_helper.error_response(message="음료 타입을 가져오는 중 오류가 발생했습니다.", status_code=500)
