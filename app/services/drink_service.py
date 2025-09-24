"""
음료 관련 비즈니스 로직을 처리하는 서비스 모듈
"""

from typing import List, Dict, Optional, Any
from app.utils.data_loader import data_loader


class DrinkService:
    """음료 데이터 처리를 담당하는 서비스 클래스"""

    def __init__(self):
        self.data_loader = data_loader

    def get_all_drinks(self) -> List[Dict]:
        """모든 음료 데이터를 반환합니다."""
        return self.data_loader.get_all_drinks()

    def search_by_name(self, keyword: str) -> List[Dict]:
        """
        이름으로 음료를 검색합니다.

        Args:
            keyword: 검색할 키워드

        Returns:
            검색 결과 리스트
        """
        if not keyword or not keyword.strip():
            return []

        all_drinks = self.get_all_drinks()
        results = []

        for drink in all_drinks:
            if keyword.lower() in drink.get("name", "").lower():
                if drink not in results:
                    results.append(drink)

        return results

    def search_by_type(self, drink_type: str) -> List[Dict]:
        """
        타입으로 음료를 검색합니다.

        Args:
            drink_type: 음료 타입

        Returns:
            검색 결과 리스트
        """
        if not drink_type or not drink_type.strip():
            return []

        all_drinks = self.get_all_drinks()
        results = []

        for drink in all_drinks:
            if drink_type.lower() in drink.get("type", "").lower():
                if drink not in results:
                    results.append(drink)

        return results

    def search_by_code(self, code: str) -> Optional[Dict]:
        """
        코드로 음료를 검색합니다.

        Args:
            code: 음료 코드

        Returns:
            찾은 음료 데이터 또는 None
        """
        if not code or not code.strip():
            return None

        all_drinks = self.get_all_drinks()

        for drink in all_drinks:
            if code == drink.get("code"):
                return drink

        return None

    def get_drink_by_codes(self, codes: List[str]) -> List[Dict]:
        """
        여러 코드로 음료들을 검색합니다.

        Args:
            codes: 음료 코드 리스트

        Returns:
            찾은 음료들의 리스트
        """
        if not codes:
            return []

        all_drinks = self.get_all_drinks()
        results = []

        for code in codes:
            for drink in all_drinks:
                if code == drink.get("code"):
                    results.append(drink)
                    break

        return results

    def get_drink_types(self) -> List[str]:
        """
        사용 가능한 모든 음료 타입을 반환합니다.

        Returns:
            음료 타입 리스트
        """
        all_drinks = self.get_all_drinks()
        types = set()

        for drink in all_drinks:
            drink_type = drink.get("type")
            if drink_type:
                types.add(drink_type)

        return sorted(list(types))

    def validate_drink_data(self, drink_data: Dict) -> List[str]:
        """
        음료 데이터의 유효성을 검증합니다.

        Args:
            drink_data: 검증할 음료 데이터

        Returns:
            에러 메시지 리스트 (에러가 없으면 빈 리스트)
        """
        errors = []

        # 필수 필드 검증
        required_fields = ["code", "name", "type"]
        for field in required_fields:
            if field not in drink_data or not drink_data[field]:
                errors.append(f"{field} 필드는 필수입니다.")

        # 코드 중복 검증
        if "code" in drink_data:
            existing_drink = self.search_by_code(drink_data["code"])
            if existing_drink:
                errors.append(f"코드 '{drink_data['code']}'는 이미 존재합니다.")

        return errors


# 전역 음료 서비스 인스턴스
drink_service = DrinkService()
