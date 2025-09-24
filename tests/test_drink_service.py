"""
음료 서비스 테스트
"""
import pytest
from app.services.drink_service import DrinkService


@pytest.fixture
def drink_service():
    """테스트용 음료 서비스 인스턴스를 생성합니다."""
    return DrinkService()


def test_get_all_drinks(drink_service):
    """모든 음료 데이터를 가져오는 기능을 테스트합니다."""
    drinks = drink_service.get_all_drinks()
    assert isinstance(drinks, list)


def test_search_by_name_empty_keyword(drink_service):
    """빈 키워드로 검색할 때를 테스트합니다."""
    results = drink_service.search_by_name("")
    assert results == []
    
    results = drink_service.search_by_name(None)
    assert results == []


def test_search_by_code_empty_code(drink_service):
    """빈 코드로 검색할 때를 테스트합니다."""
    result = drink_service.search_by_code("")
    assert result is None
    
    result = drink_service.search_by_code(None)
    assert result is None


def test_get_drink_types(drink_service):
    """음료 타입을 가져오는 기능을 테스트합니다."""
    types = drink_service.get_drink_types()
    assert isinstance(types, list)


def test_validate_drink_data_missing_fields(drink_service):
    """필수 필드가 누락된 음료 데이터 검증을 테스트합니다."""
    incomplete_data = {"name": "Test Drink"}
    errors = drink_service.validate_drink_data(incomplete_data)
    assert len(errors) > 0
    assert any("code" in error for error in errors)
    assert any("type" in error for error in errors)
