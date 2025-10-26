"""
레시피 관련 비즈니스 로직을 처리하는 서비스 모듈
"""

from typing import List, Dict, Optional, Any
from app.utils.data_loader import data_loader
import random


class RecipeService:
    """레시피 데이터 처리를 담당하는 서비스 클래스"""

    def __init__(self):
        self.data_loader = data_loader

    def get_all_recipes(self) -> List[Dict]:
        """모든 레시피 데이터를 반환합니다."""
        return self.data_loader.get_all_recipes()

    def search_by_name(self, keyword: str) -> List[Dict]:
        """
        이름으로 레시피를 검색합니다.

        Args:
            keyword: 검색할 키워드

        Returns:
            검색 결과 리스트
        """
        if not keyword or not keyword.strip():
            return []

        all_recipes = self.get_all_recipes()
        results = []

        for recipe in all_recipes:
            english_name = recipe.get("english_name", "").lower()
            korean_name = recipe.get("korean_name", "").lower()
            keyword_lower = keyword.lower()

            if (keyword_lower in english_name or keyword_lower in korean_name):
                if recipe not in results:
                    results.append(recipe)

        return results

    def search_by_code(self, code: str) -> Optional[Dict]:
        """
        코드로 레시피를 검색합니다.

        Args:
            code: 레시피 코드

        Returns:
            찾은 레시피 데이터 또는 None
        """
        if not code or not code.strip():
            return None

        all_recipes = self.get_all_recipes()

        for recipe in all_recipes:
            if code == recipe.get("code"):
                return recipe

        return None

    def get_code_by_name(self, name: str) -> Optional[str]:
        """
        레시피 이름으로 코드를 찾습니다.
        
        정확히 일치하는 이름을 우선적으로 찾고, 없으면 부분 일치하는 첫 번째 레시피의 코드를 반환합니다.
        대소문자를 구분하지 않습니다.
        한국어 이름(korean_name)과 영어 이름(english_name) 모두에서 검색합니다.

        Args:
            name: 레시피 이름

        Returns:
            레시피 코드 또는 None (찾지 못한 경우)
        """
        if not name or not name.strip():
            return None

        all_recipes = self.get_all_recipes()
        name_lower = name.strip().lower()
        
        # 1단계: 정확히 일치하는 이름 찾기 (대소문자 구분 없음)
        for recipe in all_recipes:
            korean_name = recipe.get("korean_name", "")
            english_name = recipe.get("english_name", "")
            
            if korean_name.lower() == name_lower or english_name.lower() == name_lower:
                return recipe.get("code")
        
        # 2단계: 부분 일치하는 첫 번째 레시피 찾기
        for recipe in all_recipes:
            korean_name = recipe.get("korean_name", "")
            english_name = recipe.get("english_name", "")
            
            if name_lower in korean_name.lower() or name_lower in english_name.lower():
                return recipe.get("code")
        
        # 찾지 못한 경우
        return None

    def search_by_ingredients(self, ingredient_codes: str) -> List[Dict]:
        """
        재료 코드들로 만들 수 있는 레시피를 검색합니다.

        Args:
            ingredient_codes: 쉼표로 구분된 재료 코드 문자열

        Returns:
            만들 수 있는 레시피 리스트
        """
        if not ingredient_codes or not ingredient_codes.strip():
            return []

        # 입력된 재료 코드들을 리스트로 변환
        available_codes = [code.strip() for code in ingredient_codes.split(",") if code.strip()]

        if not available_codes:
            return []

        all_recipes = self.get_all_recipes()
        available_recipes = []

        for recipe in all_recipes:
            recipe_ingredients = recipe.get("ingredients", [])

            # 레시피의 모든 재료가 사용 가능한 재료에 포함되는지 확인
            can_make = True
            for ingredient in recipe_ingredients:
                ingredient_code = ingredient.get("code")
                if ingredient_code not in available_codes:
                    can_make = False
                    break

            if can_make:
                available_recipes.append(recipe)

        return available_recipes

    def get_random_recipe(self) -> Optional[Dict]:
        """
        무작위 레시피를 반환합니다.

        Returns:
            무작위 레시피 또는 None
        """
        all_recipes = self.get_all_recipes()

        if not all_recipes:
            return None

        return random.choice(all_recipes)

    def get_recipe_categories(self) -> List[str]:
        """
        사용 가능한 모든 레시피 카테고리를 반환합니다.

        Returns:
            레시피 카테고리 리스트
        """
        all_recipes = self.get_all_recipes()
        categories = set()

        for recipe in all_recipes:
            category = recipe.get("category")
            if category:
                categories.add(category)

        return sorted(list(categories))

    def get_recipes_by_difficulty(self, difficulty: str) -> List[Dict]:
        """
        난이도별 레시피를 반환합니다.

        Args:
            difficulty: 난이도 (easy, medium, hard)

        Returns:
            해당 난이도의 레시피 리스트
        """
        if not difficulty:
            return []

        all_recipes = self.get_all_recipes()
        results = []

        for recipe in all_recipes:
            recipe_difficulty = recipe.get("difficulty", "").lower()
            if difficulty.lower() == recipe_difficulty:
                results.append(recipe)

        return results

    def validate_recipe_data(self, recipe_data: Dict) -> List[str]:
        """
        레시피 데이터의 유효성을 검증합니다.

        Args:
            recipe_data: 검증할 레시피 데이터

        Returns:
            에러 메시지 리스트 (에러가 없으면 빈 리스트)
        """
        errors = []

        # 필수 필드 검증
        required_fields = ["code", "name", "ingredients"]
        for field in required_fields:
            if field not in recipe_data or not recipe_data[field]:
                errors.append(f"{field} 필드는 필수입니다.")

        # 재료 데이터 검증
        if "ingredients" in recipe_data:
            ingredients = recipe_data["ingredients"]
            if not isinstance(ingredients, list):
                errors.append("ingredients는 리스트 형태여야 합니다.")
            elif len(ingredients) == 0:
                errors.append("최소 하나의 재료가 필요합니다.")

        # 코드 중복 검증
        if "code" in recipe_data:
            existing_recipe = self.search_by_code(recipe_data["code"])
            if existing_recipe:
                errors.append(f"코드 '{recipe_data['code']}'는 이미 존재합니다.")

        return errors


# 전역 레시피 서비스 인스턴스
recipe_service = RecipeService()
