"""
음료 서비스 테스트
"""
import pytest
from app.services.drink_service import DrinkService


def _find_prefix_group_with_multiple_entries(drinks):
    """중복 prefix를 가진 음료 그룹을 찾습니다."""
    prefix_map = {}

    for drink in drinks:
        code = drink.get("code")
        if isinstance(code, str) and len(code) > 3:
            prefix = code[:-3]
            prefix_map.setdefault(prefix, []).append(drink)

    for prefix, entries in prefix_map.items():
        if len(entries) > 1:
            return prefix, entries

    raise AssertionError("중복되는 prefix를 가진 음료 데이터를 찾을 수 없습니다.")


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


def test_search_by_code_exact_match_priority(drink_service):
    """동일 prefix가 있어도 정확히 일치하는 코드를 우선 반환하는지 확인합니다."""
    drinks = drink_service.get_all_drinks()
    prefix, entries = _find_prefix_group_with_multiple_entries(drinks)

    if len(entries) < 2:
        pytest.skip("동일 prefix를 가진 충분한 데이터가 없습니다.")

    target = entries[1]
    result = drink_service.search_by_code(target["code"])

    assert result == target


def test_search_by_code_ignores_last_three_digits(drink_service):
    """코드의 뒤 3자리를 무시하고 검색하는지 확인합니다."""
    drinks = drink_service.get_all_drinks()
    prefix, entries = _find_prefix_group_with_multiple_entries(drinks)

    existing_suffixes = {
        entry["code"][-3:]
        for entry in entries
        if isinstance(entry.get("code"), str) and len(entry["code"]) > 3
    }

    fallback_code = None
    for num in range(999, -1, -1):
        candidate_suffix = f"{num:03d}"
        if candidate_suffix not in existing_suffixes:
            fallback_code = f"{prefix}{candidate_suffix}"
            break

    if fallback_code is None:
        pytest.skip("테스트용 대체 코드를 생성하지 못했습니다.")

    result = drink_service.search_by_code(fallback_code)

    assert result == entries[0]
