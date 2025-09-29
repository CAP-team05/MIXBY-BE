"""
Flask 애플리케이션 실행 파일
"""

import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()

# 환경 변수에서 설정 이름 가져오기 (기본값: development)
config_name = os.environ.get("FLASK_ENV", "development")

# Flask 애플리케이션 생성
app = create_app(config_name)

if __name__ == "__main__":
    # 개발 서버 실행
    app.run(host=app.config["API_HOST"], port=app.config["API_PORT"], debug=app.config["DEBUG"])
