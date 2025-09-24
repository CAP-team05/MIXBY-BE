"""
입력 검증기 테스트
"""
import pytest
from app.utils.validators import InputValidator


def test_validate_string_valid():
    """유효한 문자열 검증 테스트"""
    errors = InputValidator.validate_string("test", min_length=1, max_length=10)
    assert len(errors) == 0


def test_validate_string_too_short():
    """너무 짧은 문자열 검증 테스트"""
    errors = InputValidator.validate_string("", min_length=1, max_length=10)
    assert len(errors) > 0
    assert "필수입니다" in errors[0]


def test_validate_string_too_long():
    """너무 긴 문자열 검증 테스트"""
    long_string = "a" * 300
    errors = InputValidator.validate_string(long_string, min_length=1, max_length=255)
    assert len(errors) > 0
    assert "최대" in errors[0]


def test_validate_code_valid():
    """유효한 코드 검증 테스트"""
    errors = InputValidator.validate_code("test123")
    assert len(errors) == 0


def test_validate_code_invalid():
    """무효한 코드 검증 테스트"""
    errors = InputValidator.validate_code("test@#$")
    assert len(errors) > 0
    assert "형식이 올바르지 않습니다" in errors[0]


def test_validate_coordinates_valid():
    """유효한 좌표 검증 테스트"""
    errors = InputValidator.validate_coordinates(37.5665, 126.9780)
    assert len(errors) == 0


def test_validate_coordinates_invalid_lat():
    """무효한 위도 검증 테스트"""
    errors = InputValidator.validate_coordinates(91, 126.9780)
    assert len(errors) > 0
    assert "위도" in errors[0]


def test_validate_coordinates_invalid_lng():
    """무효한 경도 검증 테스트"""
    errors = InputValidator.validate_coordinates(37.5665, 181)
    assert len(errors) > 0
    assert "경도" in errors[0]


def test_validate_coordinates_non_numeric():
    """숫자가 아닌 좌표 검증 테스트"""
    errors = InputValidator.validate_coordinates("abc", "def")
    assert len(errors) > 0
    assert "숫자여야 합니다" in errors[0]


def test_validate_json_data_valid():
    """유효한 JSON 데이터 검증 테스트"""
    data = {"name": "test", "code": "123"}
    errors = InputValidator.validate_json_data(data, ["name", "code"])
    assert len(errors) == 0


def test_validate_json_data_missing_fields():
    """필수 필드가 누락된 JSON 데이터 검증 테스트"""
    data = {"name": "test"}
    errors = InputValidator.validate_json_data(data, ["name", "code"])
    assert len(errors) > 0
    assert "code" in errors[0]


def test_validate_json_data_none():
    """None 데이터 검증 테스트"""
    errors = InputValidator.validate_json_data(None)
    assert len(errors) > 0
    assert "요청 데이터가 없습니다" in errors[0]


def test_sanitize_string():
    """문자열 정제 테스트"""
    dirty_string = "<script>alert('xss')</script>hello"
    clean_string = InputValidator.sanitize_string(dirty_string)
    assert "<script>" not in clean_string
    assert "&lt;" in clean_string or "alert" in clean_string


def test_validate_ingredient_codes_valid():
    """유효한 재료 코드 검증 테스트"""
    errors = InputValidator.validate_ingredient_codes("code1,code2,code3")
    assert len(errors) == 0


def test_validate_ingredient_codes_empty():
    """빈 재료 코드 검증 테스트"""
    errors = InputValidator.validate_ingredient_codes("")
    assert len(errors) > 0
    assert "필수입니다" in errors[0]


def test_validate_search_query_valid():
    """유효한 검색 쿼리 검증 테스트"""
    errors = InputValidator.validate_search_query("test query")
    assert len(errors) == 0


def test_validate_search_query_with_special_chars():
    """특수 문자가 포함된 검색 쿼리 검증 테스트"""
    errors = InputValidator.validate_search_query("test<script>")
    assert len(errors) > 0
    assert "허용되지 않는 문자" in errors[0]
