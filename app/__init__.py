"""
Flask 애플리케이션 팩토리
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
from app.config import get_config


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

    # 기본 라우트 등록
    register_basic_routes(app)

    return app


def register_blueprints(app: Flask):
    """Blueprint들을 등록합니다."""
    from app.routes.drink_routes import drink_bp
    from app.routes.recipe_routes import recipe_bp

    app.register_blueprint(drink_bp)
    app.register_blueprint(recipe_bp)


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


def register_basic_routes(app: Flask):
    """기본 라우트들을 등록합니다."""

    @app.route("/")
    def index():
        """API 문서를 반환합니다."""
        from app.utils.response_helper import response_helper
        from app.utils.data_loader import data_loader
        api_rules = data_loader.load_json("api_rules.json")
        return response_helper.json_response(api_rules)

    @app.route("/health")
    def health_check():
        """헬스 체크 엔드포인트"""
        from app.utils.response_helper import response_helper

        return response_helper.success_response(data={"status": "healthy"}, message="서버가 정상적으로 동작 중입니다.")
