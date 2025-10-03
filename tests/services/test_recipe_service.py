"""
RecipeService 테스트 모듈
"""

import pytest
from unittest.mock import patch, MagicMock
from app.services.recipe_service import RecipeService, recipe_service


class TestRecipeService:
    """RecipeService 클래스 테스트"""

    @pytest.fixture
    def service(self):
        """RecipeService 인스턴스 fixture"""
        return RecipeService()

    def test_get_all_recipes(self, service, sample_recipes_list):
        """모든 레시피를 반환하는지 테스트"""
        # Given: 데이터 로더가 레시피 리스트를 반환하도록 모킹
        with patch.object(service.data_loader, 'get_all_recipes', return_value=sample_recipes_list):
            # When: 모든 레시피를 조회
            result = service.get_all_recipes()

            # Then: 전체 레시피 리스트가 반환됨
            assert result == sample_recipes_list
            assert len(result) == 2
            assert result[0]["korean_name"] == "진토닉"

    def test_search_by_name_valid(self, service):
        """유효한 키워드로 레시피를 검색하는지 테스트"""
        # Given: name 필드를 포함한 레시피 리스트
        recipes_with_name = [
            {
                "name": "Gin Tonic",
                "korean_name": "진토닉",
                "code": "300600",
                "ingredients": [
                    {"name": "진", "code": "300", "amount": "45", "unit": "ml"},
                    {"name": "토닉워터", "code": "600", "amount": "120", "unit": "ml"}
                ],
                "difficulty": "쉬움"
            },
            {
                "name": "Mojito",
                "korean_name": "모히또",
                "code": "500601",
                "ingredients": [
                    {"name": "럼", "code": "500", "amount": "50", "unit": "ml"}
                ],
                "difficulty": "보통"
            }
        ]
        with patch.object(service.data_loader, 'get_all_recipes', return_value=recipes_with_name):
            # When: "Gin"으로 검색
            result = service.search_by_name("Gin")

            # Then: 진토닉 레시피가 반환됨
            assert len(result) == 1
            assert result[0]["korean_name"] == "진토닉"
            assert result[0]["code"] == "300600"

    def test_search_by_name_empty(self, service, sample_recipes_list):
        """빈 키워드로 검색 시 빈 리스트를 반환하는지 테스트"""
        # Given: 데이터 로더가 레시피 리스트를 반환하도록 모킹
        with patch.object(service.data_loader, 'get_all_recipes', return_value=sample_recipes_list):
            # When: 빈 문자열로 검색
            result_empty = service.search_by_name("")
            result_whitespace = service.search_by_name("   ")

            # Then: 빈 리스트가 반환됨
            assert result_empty == []
            assert result_whitespace == []

    def test_search_by_code_valid(self, service, sample_recipes_list):
        """유효한 코드로 레시피를 검색하는지 테스트"""
        # Given: 데이터 로더가 레시피 리스트를 반환하도록 모킹
        with patch.object(service.data_loader, 'get_all_recipes', return_value=sample_recipes_list):
            # When: "300600" 코드로 검색
            result = service.search_by_code("300600")

            # Then: 진토닉 레시피가 반환됨
            assert result is not None
            assert result["korean_name"] == "진토닉"
            assert result["code"] == "300600"

    def test_search_by_code_invalid(self, service, sample_recipes_list):
        """존재하지 않는 코드로 검색 시 None을 반환하는지 테스트"""
        # Given: 데이터 로더가 레시피 리스트를 반환하도록 모킹
        with patch.object(service.data_loader, 'get_all_recipes', return_value=sample_recipes_list):
            # When: 존재하지 않는 코드로 검색
            result_invalid = service.search_by_code("999999")
            result_empty = service.search_by_code("")
            result_whitespace = service.search_by_code("   ")

            # Then: None이 반환됨
            assert result_invalid is None
            assert result_empty is None
            assert result_whitespace is None

    def test_search_by_ingredients_valid(self, service, sample_recipes_list):
        """유효한 재료 코드로 레시피를 검색하는지 테스트"""
        # Given: 데이터 로더가 레시피 리스트를 반환하도록 모킹
        with patch.object(service.data_loader, 'get_all_recipes', return_value=sample_recipes_list):
            # When: 진토닉을 만들 수 있는 재료 코드로 검색
            result = service.search_by_ingredients("300,600")

            # Then: 진토닉 레시피가 반환됨
            assert len(result) == 1
            assert result[0]["korean_name"] == "진토닉"
            assert result[0]["code"] == "300600"

    def test_search_by_ingredients_empty(self, service, sample_recipes_list):
        """빈 재료 코드로 검색 시 빈 리스트를 반환하는지 테스트"""
        # Given: 데이터 로더가 레시피 리스트를 반환하도록 모킹
        with patch.object(service.data_loader, 'get_all_recipes', return_value=sample_recipes_list):
            # When: 빈 문자열로 검색
            result_empty = service.search_by_ingredients("")
            result_whitespace = service.search_by_ingredients("   ")
            result_commas_only = service.search_by_ingredients(",,,")

            # Then: 빈 리스트가 반환됨
            assert result_empty == []
            assert result_whitespace == []
            assert result_commas_only == []

    def test_get_random_recipe(self, service, sample_recipes_list):
        """무작위 레시피를 반환하는지 테스트"""
        # Given: 데이터 로더가 레시피 리스트를 반환하도록 모킹
        with patch.object(service.data_loader, 'get_all_recipes', return_value=sample_recipes_list):
            # When: 무작위 레시피 조회
            result = service.get_random_recipe()

            # Then: 레시피 리스트 중 하나가 반환됨
            assert result is not None
            assert result in sample_recipes_list

    def test_get_random_recipe_empty_list(self, service):
        """레시피가 없을 때 None을 반환하는지 테스트"""
        # Given: 데이터 로더가 빈 리스트를 반환하도록 모킹
        with patch.object(service.data_loader, 'get_all_recipes', return_value=[]):
            # When: 무작위 레시피 조회
            result = service.get_random_recipe()

            # Then: None이 반환됨
            assert result is None

    def test_get_recipe_categories(self, service, sample_recipes_list):
        """모든 레시피 카테고리를 반환하는지 테스트"""
        # Given: 데이터 로더가 레시피 리스트를 반환하도록 모킹
        with patch.object(service.data_loader, 'get_all_recipes', return_value=sample_recipes_list):
            # When: 카테고리 조회
            result = service.get_recipe_categories()

            # Then: 정렬된 카테고리 리스트가 반환됨
            assert result == ["롱 드링크"]
            assert isinstance(result, list)

    def test_get_recipes_by_difficulty(self, service, sample_recipes_list):
        """난이도별 레시피를 반환하는지 테스트"""
        # Given: 데이터 로더가 레시피 리스트를 반환하도록 모킹
        with patch.object(service.data_loader, 'get_all_recipes', return_value=sample_recipes_list):
            # When: "쉬움" 난이도로 검색
            result_easy = service.get_recipes_by_difficulty("쉬움")
            # When: "보통" 난이도로 검색
            result_medium = service.get_recipes_by_difficulty("보통")
            # When: 존재하지 않는 난이도로 검색
            result_invalid = service.get_recipes_by_difficulty("어려움")

            # Then: 해당 난이도의 레시피만 반환됨
            assert len(result_easy) == 1
            assert result_easy[0]["korean_name"] == "진토닉"
            assert len(result_medium) == 1
            assert result_medium[0]["korean_name"] == "모히또"
            assert result_invalid == []

    def test_validate_recipe_data_valid(self, service):
        """유효한 레시피 데이터 검증 테스트"""
        # Given: 유효한 레시피 데이터와 빈 레시피 리스트
        valid_recipe = {
            "code": "NEW001",
            "name": "새로운 칵테일",
            "ingredients": [
                {"name": "진", "code": "300", "amount": "45", "unit": "ml"}
            ]
        }
        with patch.object(service.data_loader, 'get_all_recipes', return_value=[]):
            # When: 데이터 검증
            errors = service.validate_recipe_data(valid_recipe)

            # Then: 에러가 없음
            assert errors == []

    def test_validate_recipe_data_invalid(self, service):
        """유효하지 않은 레시피 데이터 검증 테스트"""
        # Given: 데이터 로더가 빈 리스트를 반환하도록 모킹
        with patch.object(service.data_loader, 'get_all_recipes', return_value=[]):
            # When: 필수 필드 누락 - code 없음
            invalid_recipe_no_code = {
                "name": "테스트",
                "ingredients": [{"name": "진", "code": "300"}]
            }
            errors_no_code = service.validate_recipe_data(invalid_recipe_no_code)

            # Then: code 필드 에러 발생
            assert len(errors_no_code) > 0
            assert any("code" in error for error in errors_no_code)

            # When: 필수 필드 누락 - name 없음
            invalid_recipe_no_name = {
                "code": "TEST001",
                "ingredients": [{"name": "진", "code": "300"}]
            }
            errors_no_name = service.validate_recipe_data(invalid_recipe_no_name)

            # Then: name 필드 에러 발생
            assert len(errors_no_name) > 0
            assert any("name" in error for error in errors_no_name)

            # When: 필수 필드 누락 - ingredients 없음
            invalid_recipe_no_ingredients = {
                "code": "TEST001",
                "name": "테스트"
            }
            errors_no_ingredients = service.validate_recipe_data(invalid_recipe_no_ingredients)

            # Then: ingredients 필드 에러 발생
            assert len(errors_no_ingredients) > 0
            assert any("ingredients" in error for error in errors_no_ingredients)

            # When: ingredients가 리스트가 아님
            invalid_recipe_wrong_type = {
                "code": "TEST001",
                "name": "테스트",
                "ingredients": "not a list"
            }
            errors_wrong_type = service.validate_recipe_data(invalid_recipe_wrong_type)

            # Then: 타입 에러 발생
            assert len(errors_wrong_type) > 0
            assert any("리스트" in error for error in errors_wrong_type)

            # When: ingredients가 빈 리스트
            invalid_recipe_empty_ingredients = {
                "code": "TEST001",
                "name": "테스트",
                "ingredients": []
            }
            errors_empty = service.validate_recipe_data(invalid_recipe_empty_ingredients)

            # Then: 재료 필요 에러 발생
            assert len(errors_empty) > 0
            assert any("재료" in error for error in errors_empty)

    def test_validate_recipe_data_duplicate_code(self, service, sample_recipes_list):
        """중복된 코드 검증 테스트"""
        # Given: 기존 레시피가 있는 상태
        with patch.object(service.data_loader, 'get_all_recipes', return_value=sample_recipes_list):
            # When: 기존 코드와 동일한 코드로 레시피 생성 시도
            duplicate_recipe = {
                "code": "300600",  # 이미 존재하는 코드
                "name": "중복 테스트",
                "ingredients": [{"name": "진", "code": "300"}]
            }
            errors = service.validate_recipe_data(duplicate_recipe)

            # Then: 중복 코드 에러 발생
            assert len(errors) > 0
            assert any("이미 존재" in error for error in errors)
