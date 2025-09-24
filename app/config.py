"""
애플리케이션 설정 모듈
환경 변수와 설정값을 관리합니다.
"""

import os
from typing import Dict, Any


class Config:
    """기본 설정 클래스"""

    # Flask 설정
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    JSON_AS_ASCII = False  # 한글 지원

    # 데이터 디렉토리 설정
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    STATIC_DIR = os.path.join(BASE_DIR, "static")

    # API 설정
    API_HOST = os.environ.get("API_HOST") or "0.0.0.0"
    API_PORT = int(os.environ.get("API_PORT") or 8080)
    DEBUG = os.environ.get("FLASK_DEBUG") == "True"

    # CORS 설정
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")

    # 로깅 설정
    LOG_LEVEL = os.environ.get("LOG_LEVEL") or "INFO"
    LOG_FILE = os.environ.get("LOG_FILE") or "app.log"

    # 외부 API 설정
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
    WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

    # 파일 업로드 설정
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    @staticmethod
    def init_app(app):
        """Flask 앱 초기화"""
        pass


class DevelopmentConfig(Config):
    """개발 환경 설정"""

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """프로덕션 환경 설정"""

    DEBUG = False
    LOG_LEVEL = "WARNING"

    @staticmethod
    def init_app(app):
        Config.init_app(app)

        # 프로덕션 환경에서 필요한 추가 설정
        if not app.config.get("SECRET_KEY"):
            raise ValueError("SECRET_KEY must be set in production")


class TestingConfig(Config):
    """테스트 환경 설정"""

    TESTING = True
    DEBUG = True
    LOG_LEVEL = "DEBUG"


# 환경별 설정 매핑
config: Dict[str, Any] = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


def get_config(env_name: str = None) -> Config:
    """
    환경 이름에 따른 설정 클래스를 반환합니다.

    Args:
        env_name: 환경 이름 (development, production, testing)

    Returns:
        해당 환경의 설정 클래스
    """
    if env_name is None:
        env_name = os.environ.get("FLASK_ENV", "default")

    return config.get(env_name, config["default"])
