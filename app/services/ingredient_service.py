"""
재료 관련 비즈니스 로직을 처리하는 서비스 모듈
"""

from typing import List, Dict, Optional, Any
from app.utils.data_loader import data_loader


class IngredientService:
    """재료 데이터 처리를 담당하는 서비스 클래스"""

    def __init__(self):
        self.data_loader = data_loader

    def get_all_ingredients(self) -> List[Dict]:
        """모든 재료 데이터를 반환합니다."""
        return self.data_loader.get_all_ingredients()

    def get_ingredients_by_codes(self, codes: str) -> List[Dict]:
        """
        여러 코드로 재료들을 검색합니다.

        Args:
            codes: 쉼표로 구분된 재료 코드 문자열

        Returns:
            찾은 재료들의 리스트
        """
        if not codes or not codes.strip():
            return []

        # 코드들을 리스트로 변환
        code_list = [code.strip() for code in codes.split(",") if code.strip()]

        if not code_list:
            return []

        all_ingredients = self.get_all_ingredients()
        results = []

        for code in code_list:
            for ingredient in all_ingredients:
                if code == ingredient.get("code"):
                    results.append(ingredient)
                    break

        return results

    def search_by_name(self, keyword: str) -> List[Dict]:
        """
        이름으로 재료를 검색합니다.

        Args:
            keyword: 검색할 키워드

        Returns:
            검색 결과 리스트
        """
        if not keyword or not keyword.strip():
            return []

        all_ingredients = self.get_all_ingredients()
        results = []

        for ingredient in all_ingredients:
            name = ingredient.get("name", "").lower()
            if keyword.lower() in name:
                if ingredient not in results:
                    results.append(ingredient)

        return results

    def search_by_code(self, code: str) -> Optional[Dict]:
        """
        코드로 재료를 검색합니다.

        Args:
            code: 재료 코드

        Returns:
            찾은 재료 데이터 또는 None
        """
        if not code or not code.strip():
            return None

        all_ingredients = self.get_all_ingredients()

        for ingredient in all_ingredients:
            if code == ingredient.get("code"):
                return ingredient

        return None

    def search_by_category(self, category: str) -> List[Dict]:
        """
        카테고리로 재료를 검색합니다.

        Args:
            category: 재료 카테고리

        Returns:
            검색 결과 리스트
        """
        if not category or not category.strip():
            return []

        all_ingredients = self.get_all_ingredients()
        results = []

        for ingredient in all_ingredients:
            ingredient_category = ingredient.get("category", "").lower()
            if category.lower() == ingredient_category:
                results.append(ingredient)

        return results

    def get_ingredient_categories(self) -> List[str]:
        """
        사용 가능한 모든 재료 카테고리를 반환합니다.

        Returns:
            재료 카테고리 리스트
        """
        all_ingredients = self.get_all_ingredients()
        categories = set()

        for ingredient in all_ingredients:
            category = ingredient.get("category")
            if category:
                categories.add(category)

        return sorted(list(categories))

    def get_alcoholic_ingredients(self) -> List[Dict]:
        """
        알코올 재료들을 반환합니다.

        Returns:
            알코올 재료 리스트
        """
        all_ingredients = self.get_all_ingredients()
        alcoholic_ingredients = []

        for ingredient in all_ingredients:
            if ingredient.get("alcoholic", False):
                alcoholic_ingredients.append(ingredient)

        return alcoholic_ingredients

    def get_non_alcoholic_ingredients(self) -> List[Dict]:
        """
        무알코올 재료들을 반환합니다.

        Returns:
            무알코올 재료 리스트
        """
        all_ingredients = self.get_all_ingredients()
        non_alcoholic_ingredients = []

        for ingredient in all_ingredients:
            if not ingredient.get("alcoholic", True):
                non_alcoholic_ingredients.append(ingredient)

        return non_alcoholic_ingredients

    def validate_ingredient_data(self, ingredient_data: Dict) -> List[str]:
        """
        재료 데이터의 유효성을 검증합니다.

        Args:
            ingredient_data: 검증할 재료 데이터

        Returns:
            에러 메시지 리스트 (에러가 없으면 빈 리스트)
        """
        errors = []

        # 필수 필드 검증
        required_fields = ["code", "name"]
        for field in required_fields:
            if field not in ingredient_data or not ingredient_data[field]:
                errors.append(f"{field} 필드는 필수입니다.")

        # 코드 중복 검증
        if "code" in ingredient_data:
            existing_ingredient = self.search_by_code(ingredient_data["code"])
            if existing_ingredient:
                errors.append(f"코드 '{ingredient_data['code']}'는 이미 존재합니다.")

        return errors


# 전역 재료 서비스 인스턴스
ingredient_service = IngredientService()
