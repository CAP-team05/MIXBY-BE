"""
입력 검증을 위한 유틸리티 모듈
"""

import re
from typing import List, Dict, Any, Optional, Union


class InputValidator:
    """입력 검증을 위한 클래스"""

    @staticmethod
    def validate_string(
        value: Any, min_length: int = 1, max_length: int = 255, pattern: str = None, field_name: str = "값"
    ) -> List[str]:
        """
        문자열 입력을 검증합니다.

        Args:
            value: 검증할 값
            min_length: 최소 길이
            max_length: 최대 길이
            pattern: 정규식 패턴
            field_name: 필드명

        Returns:
            에러 메시지 리스트
        """
        errors = []

        # None 또는 빈 값 체크
        if value is None or value == "":
            if min_length > 0:
                errors.append(f"{field_name}은(는) 필수입니다.")
            return errors

        # 문자열 타입 체크
        if not isinstance(value, str):
            value = str(value)

        # 길이 체크
        if len(value) < min_length:
            errors.append(f"{field_name}은(는) 최소 {min_length}자 이상이어야 합니다.")

        if len(value) > max_length:
            errors.append(f"{field_name}은(는) 최대 {max_length}자 이하여야 합니다.")

        # 패턴 체크
        if pattern and not re.match(pattern, value):
            errors.append(f"{field_name}의 형식이 올바르지 않습니다.")

        return errors

    @staticmethod
    def validate_code(code: Any, field_name: str = "코드") -> List[str]:
        """
        코드 형식을 검증합니다.

        Args:
            code: 검증할 코드
            field_name: 필드명

        Returns:
            에러 메시지 리스트
        """
        # 알파벳, 숫자, 하이픈, 언더스코어만 허용
        pattern = r"^[a-zA-Z0-9_-]+$"
        return InputValidator.validate_string(code, min_length=1, max_length=50, pattern=pattern, field_name=field_name)

    @staticmethod
    def validate_coordinates(lat: Any, lng: Any) -> List[str]:
        """
        위도/경도 좌표를 검증합니다.

        Args:
            lat: 위도
            lng: 경도

        Returns:
            에러 메시지 리스트
        """
        errors = []

        try:
            lat_float = float(lat)
            lng_float = float(lng)

            if not (-90 <= lat_float <= 90):
                errors.append("위도는 -90과 90 사이의 값이어야 합니다.")

            if not (-180 <= lng_float <= 180):
                errors.append("경도는 -180과 180 사이의 값이어야 합니다.")

        except (ValueError, TypeError):
            errors.append("위도와 경도는 숫자여야 합니다.")

        return errors

    @staticmethod
    def validate_json_data(data: Any, required_fields: List[str] = None) -> List[str]:
        """
        JSON 데이터를 검증합니다.

        Args:
            data: 검증할 JSON 데이터
            required_fields: 필수 필드 리스트

        Returns:
            에러 메시지 리스트
        """
        errors = []

        if data is None:
            errors.append("요청 데이터가 없습니다.")
            return errors

        if not isinstance(data, dict):
            errors.append("요청 데이터는 JSON 객체여야 합니다.")
            return errors

        # 필수 필드 체크
        if required_fields:
            for field in required_fields:
                if field not in data or data[field] is None:
                    errors.append(f"'{field}' 필드는 필수입니다.")

        return errors

    @staticmethod
    def sanitize_string(value: str, max_length: int = 255) -> str:
        """
        문자열을 안전하게 정제합니다.

        Args:
            value: 정제할 문자열
            max_length: 최대 길이

        Returns:
            정제된 문자열
        """
        if not isinstance(value, str):
            value = str(value)

        # HTML 태그 제거
        value = re.sub(r"<[^>]+>", "", value)

        # 특수 문자 이스케이프
        value = value.replace("<", "&lt;").replace(">", "&gt;")

        # 길이 제한
        if len(value) > max_length:
            value = value[:max_length]

        # 앞뒤 공백 제거
        return value.strip()

    @staticmethod
    def validate_ingredient_codes(codes: str) -> List[str]:
        """
        재료 코드 문자열을 검증합니다.

        Args:
            codes: 쉼표로 구분된 재료 코드 문자열

        Returns:
            에러 메시지 리스트
        """
        errors = []

        if not codes or not codes.strip():
            errors.append("재료 코드는 필수입니다.")
            return errors

        # 쉼표로 분리하여 각 코드 검증
        code_list = [code.strip() for code in codes.split(",")]

        for code in code_list:
            if not code:
                errors.append("빈 재료 코드는 허용되지 않습니다.")
                continue

            code_errors = InputValidator.validate_code(code, "재료 코드")
            errors.extend(code_errors)

        return errors

    @staticmethod
    def validate_search_query(query: str, field_name: str = "검색어") -> List[str]:
        """
        검색 쿼리를 검증합니다.

        Args:
            query: 검색 쿼리
            field_name: 필드명

        Returns:
            에러 메시지 리스트
        """
        errors = []

        if not query or not query.strip():
            errors.append(f"{field_name}를 입력해주세요.")
            return errors

        # 길이 제한
        if len(query) > 100:
            errors.append(f"{field_name}는 100자 이하여야 합니다.")

        # 특수 문자 제한 (기본적인 검색어만 허용)
        if re.search(r'[<>"\']', query):
            errors.append(f"{field_name}에 허용되지 않는 문자가 포함되어 있습니다.")

        return errors


# 전역 검증기 인스턴스
validator = InputValidator()
