"""
기본 라우트
"""

from flask import Blueprint
from app.utils.response_helper import response_helper
from app.utils.data_loader import data_loader

default_bp = Blueprint("default", __name__)


@default_bp.route("/")
def index():
    """
    API 문서 엔드포인트

    전체 API 문서를 반환합니다.

    Returns:
        JSON 응답: API 문서
    """
    api_rules = data_loader.load_json("api_rules.json")
    return response_helper.json_response(api_rules)
