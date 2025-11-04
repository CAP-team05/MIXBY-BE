"""
헬스 체크 관련 라우트
"""

from flask import Blueprint
from app.utils.response_helper import response_helper

health_bp = Blueprint("health", __name__)


@health_bp.route("/health")
def health_check():
    """
    헬스 체크 엔드포인트

    서버의 상태를 확인합니다.

    Returns:
        JSON 응답: 서버 상태 정보
    """
    return response_helper.success_response(
        data={"status": "healthy"},
        message="서버가 정상적으로 동작 중입니다."
    )
