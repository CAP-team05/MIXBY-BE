"""
Flask 애플리케이션 팩토리
"""

import os
import time
import logging
from flask import Flask, send_from_directory
from flask_cors import CORS
from app.config import get_config

logger = logging.getLogger(__name__)


def create_app(config_name: str = None) -> Flask:
    """
    Flask 애플리케이션을 생성하고 설정합니다.

    Args:
        config_name: 설정 환경 이름

    Returns:
        설정된 Flask 애플리케이션 인스턴스
    """
    app = Flask(__name__)

    # 설정 로드
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # 설정 초기화
    config_class.init_app(app)

    # CORS 설정
    CORS(app, origins=app.config["CORS_ORIGINS"])

    # Blueprint 등록
    register_blueprints(app)

    # 에러 핸들러 등록
    register_error_handlers(app)

    # RAG 벡터 DB 자동 초기화
    initialize_rag(app)

    return app


def register_blueprints(app: Flask):
    """Blueprint들을 등록합니다."""
    from app.routes.default_routes import default_bp
    from app.routes.health_routes import health_bp
    from app.routes.drink_routes import drink_bp
    from app.routes.recipe_routes import recipe_bp
    from app.routes.recommendation_routes import recommendation_bp
    from app.routes.ingredient_routes import ingredient_bp

    app.register_blueprint(default_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(drink_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(recommendation_bp, url_prefix='/api/recommendations')
    app.register_blueprint(ingredient_bp)


def register_error_handlers(app: Flask):
    """에러 핸들러를 등록합니다."""
    from app.utils.response_helper import response_helper

    @app.errorhandler(404)
    def not_found_error(error):
        return response_helper.error_response(
            message="요청한 리소스를 찾을 수 없습니다.", status_code=404, error_code="NOT_FOUND"
        )

    @app.errorhandler(500)
    def internal_error(error):
        return response_helper.error_response(
            message="서버 내부 오류가 발생했습니다.", status_code=500, error_code="INTERNAL_ERROR"
        )

    @app.errorhandler(400)
    def bad_request_error(error):
        return response_helper.error_response(message="잘못된 요청입니다.", status_code=400, error_code="BAD_REQUEST")


def initialize_rag(app: Flask):
    """RAG 벡터 DB를 자동 초기화합니다.

    Args:
        app: Flask 애플리케이션 인스턴스

    Note:
        - USE_RAG 환경 변수가 'true'인 경우에만 초기화
        - 벡터 DB가 이미 존재하면 로드만 하고 스킵 (<1초)
        - 벡터 DB가 없으면 임베딩 생성 (2-5분)
        - 초기화 실패 시 경고 로그만 출력하고 앱은 정상 시작
    """
    use_rag = os.getenv("USE_RAG", "false").lower() == "true"

    if not use_rag:
        logger.info("RAG 기능이 비활성화되어 있습니다 (USE_RAG=false)")
        return

    logger.info("RAG 벡터 DB 초기화 시작...")
    start_time = time.time()

    try:
        from app.services.rag_service import RAGService

        # RAG 서비스 생성 및 초기화
        rag_service = RAGService()
        rag_service.initialize_vector_db(force_rebuild=False)

        elapsed_time = time.time() - start_time
        logger.info(f"RAG 벡터 DB 초기화 완료 (소요 시간: {elapsed_time:.2f}초)")

    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.warning(f"RAG 벡터 DB 초기화 실패 (소요 시간: {elapsed_time:.2f}초): {e}")
        logger.warning("RAG 기능을 사용할 수 없지만 앱은 정상적으로 시작됩니다.")
        logger.warning("RAG 초기화를 수동으로 실행하려면: python scripts/initialize_vector_db.py")


