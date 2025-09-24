"""
Flask 애플리케이션 테스트
"""
import pytest
from app import create_app


@pytest.fixture
def app():
    """테스트용 Flask 애플리케이션 인스턴스를 생성합니다."""
    app = create_app("testing")
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """테스트 클라이언트를 생성합니다."""
    return app.test_client()


def test_app_creation():
    """애플리케이션이 정상적으로 생성되는지 테스트합니다."""
    app = create_app("testing")
    assert app is not None
    assert app.config["TESTING"] is True


def test_health_check(client):
    """헬스 체크 엔드포인트를 테스트합니다."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"
    assert "서버가 정상적으로 동작 중입니다." in data["message"]


def test_index_route(client):
    """인덱스 라우트를 테스트합니다."""
    response = client.get("/")
    assert response.status_code == 200
