"""
IngredientService 테스트 모듈
"""

import pytest
from app.services.ingredient_service import IngredientService


class TestIngredientService:
    """IngredientService 클래스 테스트"""

    @pytest.fixture
    def ingredient_service(self):
        """IngredientService 인스턴스 fixture"""
        return IngredientService()

    def test_get_all_ingredients(self, ingredient_service):
        """
        Given: IngredientService 인스턴스가 존재할 때
        When: get_all_ingredients() 메서드를 호출하면
        Then: 모든 재료 데이터가 리스트로 반환되어야 함
        """
        # When
        result = ingredient_service.get_all_ingredients()

        # Then
        assert isinstance(result, list)
        assert len(result) > 0
        # 첫 번째 재료가 필수 필드를 가지고 있는지 확인
        if result:
            first_ingredient = result[0]
            assert "name" in first_ingredient
            assert "code" in first_ingredient

    def test_get_ingredients_by_codes_valid(self, ingredient_service):
        """
        Given: 유효한 재료 코드들이 주어졌을 때
        When: get_ingredients_by_codes() 메서드를 호출하면
        Then: 해당 코드들에 맞는 재료들이 반환되어야 함
        """
        # Given
        all_ingredients = ingredient_service.get_all_ingredients()
        # 실제 존재하는 코드 2개를 가져옴
        if len(all_ingredients) >= 2:
            code1 = all_ingredients[0].get("code")
            code2 = all_ingredients[1].get("code")
            codes = f"{code1},{code2}"

            # When
            result = ingredient_service.get_ingredients_by_codes(codes)

            # Then
            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0].get("code") == code1
            assert result[1].get("code") == code2

    def test_get_ingredients_by_codes_empty(self, ingredient_service):
        """
        Given: 빈 문자열이나 공백만 있는 코드가 주어졌을 때
        When: get_ingredients_by_codes() 메서드를 호출하면
        Then: 빈 리스트가 반환되어야 함
        """
        # When & Then
        assert ingredient_service.get_ingredients_by_codes("") == []
        assert ingredient_service.get_ingredients_by_codes("   ") == []
        assert ingredient_service.get_ingredients_by_codes(",,,") == []

    def test_search_by_name_valid(self, ingredient_service):
        """
        Given: 유효한 검색 키워드가 주어졌을 때
        When: search_by_name() 메서드를 호출하면
        Then: 키워드를 포함하는 재료들이 반환되어야 함
        """
        # Given
        all_ingredients = ingredient_service.get_all_ingredients()
        # 실제 존재하는 재료의 이름 일부를 검색어로 사용
        if all_ingredients:
            first_ingredient = all_ingredients[0]
            ingredient_name = first_ingredient.get("name", "")
            # 이름의 일부를 검색어로 사용 (최소 3글자)
            if len(ingredient_name) >= 3:
                keyword = ingredient_name[:3]

                # When
                result = ingredient_service.search_by_name(keyword)

                # Then
                assert isinstance(result, list)
                assert len(result) > 0
                # 결과에 검색한 재료가 포함되어 있는지 확인
                assert any(keyword.lower() in ing.get("name", "").lower() for ing in result)

    def test_search_by_name_empty(self, ingredient_service):
        """
        Given: 빈 문자열이나 공백만 있는 키워드가 주어졌을 때
        When: search_by_name() 메서드를 호출하면
        Then: 빈 리스트가 반환되어야 함
        """
        # When & Then
        assert ingredient_service.search_by_name("") == []
        assert ingredient_service.search_by_name("   ") == []
        assert ingredient_service.search_by_name(None) == []

    def test_search_by_code_valid(self, ingredient_service):
        """
        Given: 유효한 재료 코드가 주어졌을 때
        When: search_by_code() 메서드를 호출하면
        Then: 해당 코드의 재료 데이터가 반환되어야 함
        """
        # Given
        all_ingredients = ingredient_service.get_all_ingredients()
        if all_ingredients:
            expected_ingredient = all_ingredients[0]
            code = expected_ingredient.get("code")

            # When
            result = ingredient_service.search_by_code(code)

            # Then
            assert result is not None
            assert isinstance(result, dict)
            assert result.get("code") == code
            assert result.get("name") == expected_ingredient.get("name")

    def test_search_by_code_invalid(self, ingredient_service):
        """
        Given: 존재하지 않는 재료 코드가 주어졌을 때
        When: search_by_code() 메서드를 호출하면
        Then: None이 반환되어야 함
        """
        # Given
        invalid_code = "INVALID_CODE_12345"

        # When
        result = ingredient_service.search_by_code(invalid_code)

        # Then
        assert result is None

        # 빈 문자열과 공백도 테스트
        assert ingredient_service.search_by_code("") is None
        assert ingredient_service.search_by_code("   ") is None
        assert ingredient_service.search_by_code(None) is None

    def test_search_by_category(self, ingredient_service):
        """
        Given: 유효한 카테고리가 주어졌을 때
        When: search_by_category() 메서드를 호출하면
        Then: 해당 카테고리의 재료들이 반환되어야 함
        """
        # Given
        all_ingredients = ingredient_service.get_all_ingredients()
        
        # 실제 데이터에 category 필드가 있는 재료를 찾음
        ingredient_with_category = None
        for ingredient in all_ingredients:
            if ingredient.get("category"):
                ingredient_with_category = ingredient
                break
        
        if ingredient_with_category:
            category = ingredient_with_category.get("category")
            
            # When
            result = ingredient_service.search_by_category(category)

            # Then
            assert isinstance(result, list)
            assert len(result) > 0
            # 모든 결과가 해당 카테고리를 가지고 있는지 확인
            for ingredient in result:
                assert ingredient.get("category", "").lower() == category.lower()

        # 빈 문자열 테스트
        assert ingredient_service.search_by_category("") == []
        assert ingredient_service.search_by_category("   ") == []

    def test_get_ingredient_categories(self, ingredient_service):
        """
        Given: IngredientService 인스턴스가 존재할 때
        When: get_ingredient_categories() 메서드를 호출하면
        Then: 모든 재료 카테고리가 정렬된 리스트로 반환되어야 함
        """
        # When
        result = ingredient_service.get_ingredient_categories()

        # Then
        assert isinstance(result, list)
        # 데이터에 category 필드가 없을 수 있으므로 빈 리스트도 허용
        # 정렬되어 있는지 확인
        assert result == sorted(result)
        # 중복이 없는지 확인
        assert len(result) == len(set(result))

    def test_get_alcoholic_ingredients(self, ingredient_service):
        """
        Given: IngredientService 인스턴스가 존재할 때
        When: get_alcoholic_ingredients() 메서드를 호출하면
        Then: 알코올 재료들만 반환되어야 함
        """
        # When
        result = ingredient_service.get_alcoholic_ingredients()

        # Then
        assert isinstance(result, list)
        # 모든 결과가 알코올 재료인지 확인
        for ingredient in result:
            assert ingredient.get("alcoholic") is True

    def test_get_non_alcoholic_ingredients(self, ingredient_service):
        """
        Given: IngredientService 인스턴스가 존재할 때
        When: get_non_alcoholic_ingredients() 메서드를 호출하면
        Then: 무알코올 재료들만 반환되어야 함
        """
        # When
        result = ingredient_service.get_non_alcoholic_ingredients()

        # Then
        assert isinstance(result, list)
        # 모든 결과가 무알코올 재료인지 확인
        for ingredient in result:
            assert ingredient.get("alcoholic") is False

    def test_validate_ingredient_data_valid(self, ingredient_service):
        """
        Given: 유효한 재료 데이터가 주어졌을 때
        When: validate_ingredient_data() 메서드를 호출하면
        Then: 빈 에러 리스트가 반환되어야 함
        """
        # Given - 존재하지 않는 새로운 코드로 유효한 재료 데이터 생성
        valid_ingredient = {
            "code": "NEW_TEST_INGREDIENT_12345",
            "name": "테스트 재료"
        }

        # When
        errors = ingredient_service.validate_ingredient_data(valid_ingredient)

        # Then
        assert isinstance(errors, list)
        assert len(errors) == 0

    def test_validate_ingredient_data_missing_code(self, ingredient_service):
        """
        Given: code 필드가 누락된 재료 데이터가 주어졌을 때
        When: validate_ingredient_data() 메서드를 호출하면
        Then: code 필드 누락 에러가 반환되어야 함
        """
        # Given
        invalid_ingredient = {
            "name": "테스트 재료"
        }

        # When
        errors = ingredient_service.validate_ingredient_data(invalid_ingredient)

        # Then
        assert isinstance(errors, list)
        assert len(errors) > 0
        assert any("code" in error.lower() for error in errors)

    def test_validate_ingredient_data_missing_name(self, ingredient_service):
        """
        Given: name 필드가 누락된 재료 데이터가 주어졌을 때
        When: validate_ingredient_data() 메서드를 호출하면
        Then: name 필드 누락 에러가 반환되어야 함
        """
        # Given
        invalid_ingredient = {
            "code": "TEST001"
        }

        # When
        errors = ingredient_service.validate_ingredient_data(invalid_ingredient)

        # Then
        assert isinstance(errors, list)
        assert len(errors) > 0
        assert any("name" in error.lower() for error in errors)

    def test_validate_ingredient_data_empty_code(self, ingredient_service):
        """
        Given: code 필드가 빈 문자열인 재료 데이터가 주어졌을 때
        When: validate_ingredient_data() 메서드를 호출하면
        Then: code 필드 누락 에러가 반환되어야 함
        """
        # Given
        invalid_ingredient = {
            "code": "",
            "name": "테스트 재료"
        }

        # When
        errors = ingredient_service.validate_ingredient_data(invalid_ingredient)

        # Then
        assert isinstance(errors, list)
        assert len(errors) > 0
        assert any("code" in error.lower() for error in errors)

    def test_validate_ingredient_data_empty_name(self, ingredient_service):
        """
        Given: name 필드가 빈 문자열인 재료 데이터가 주어졌을 때
        When: validate_ingredient_data() 메서드를 호출하면
        Then: name 필드 누락 에러가 반환되어야 함
        """
        # Given
        invalid_ingredient = {
            "code": "TEST001",
            "name": ""
        }

        # When
        errors = ingredient_service.validate_ingredient_data(invalid_ingredient)

        # Then
        assert isinstance(errors, list)
        assert len(errors) > 0
        assert any("name" in error.lower() for error in errors)

    def test_validate_ingredient_data_duplicate_code(self, ingredient_service):
        """
        Given: 이미 존재하는 코드를 가진 재료 데이터가 주어졌을 때
        When: validate_ingredient_data() 메서드를 호출하면
        Then: 코드 중복 에러가 반환되어야 함
        """
        # Given - 실제 존재하는 재료의 코드를 사용
        all_ingredients = ingredient_service.get_all_ingredients()
        if all_ingredients:
            existing_code = all_ingredients[0].get("code")
            duplicate_ingredient = {
                "code": existing_code,
                "name": "중복 테스트 재료"
            }

            # When
            errors = ingredient_service.validate_ingredient_data(duplicate_ingredient)

            # Then
            assert isinstance(errors, list)
            assert len(errors) > 0
            assert any("이미 존재" in error for error in errors)
            assert any(existing_code in error for error in errors)

    def test_validate_ingredient_data_multiple_errors(self, ingredient_service):
        """
        Given: 여러 필드가 누락된 재료 데이터가 주어졌을 때
        When: validate_ingredient_data() 메서드를 호출하면
        Then: 모든 에러가 리스트로 반환되어야 함
        """
        # Given
        invalid_ingredient = {}

        # When
        errors = ingredient_service.validate_ingredient_data(invalid_ingredient)

        # Then
        assert isinstance(errors, list)
        assert len(errors) >= 2  # code와 name 필드 누락
        assert any("code" in error.lower() for error in errors)
        assert any("name" in error.lower() for error in errors)
