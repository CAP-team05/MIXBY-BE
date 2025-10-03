"""
RecipeRoutes 통합 테스트
"""

import pytest
from unittest.mock import patch, MagicMock


class TestRecipeRoutes:
    """RecipeRoutes 엔드포인트 테스트"""

    def test_get_all_recipes(self, client, sample_recipes_list):
        """
        GET /recipe/all 엔드포인트 테스트
        모든 레시피 데이터를 정상적으로 반환하는지 검증
        """
        # Given: 레시피 데이터가 존재함
        with patch('app.services.recipe_service.recipe_service.get_all_recipes') as mock_get_all:
            mock_get_all.return_value = sample_recipes_list

            # When: /recipe/all 엔드포인트 호출
            response = client.get('/recipe/all')

            # Then: 200 상태 코드와 레시피 데이터 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data == sample_recipes_list
            assert len(data) == 2
            assert data[0]["korean_name"] == "진토닉"
            assert data[1]["korean_name"] == "모히또"

    def test_get_recipe_categories(self, client):
        """
        GET /recipe/categories 엔드포인트 테스트
        사용 가능한 모든 레시피 카테고리를 정상적으로 반환하는지 검증
        """
        # Given: 레시피 카테고리 데이터가 존재함
        mock_categories = ["롱 드링크", "숏 드링크", "샷", "핫 드링크"]

        with patch('app.services.recipe_service.recipe_service.get_recipe_categories') as mock_get_categories:
            mock_get_categories.return_value = mock_categories

            # When: /recipe/categories 엔드포인트 호출
            response = client.get('/recipe/categories')

            # Then: 200 상태 코드와 카테고리 리스트 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data == mock_categories
            assert len(data) == 4
            assert "롱 드링크" in data
            assert "숏 드링크" in data

    def test_get_random_recipe(self, client, sample_recipe):
        """
        GET /recipe/random 엔드포인트 테스트
        무작위 레시피를 정상적으로 반환하는지 검증
        """
        # Given: 레시피 데이터가 존재함
        with patch('app.services.recipe_service.recipe_service.get_random_recipe') as mock_get_random:
            mock_get_random.return_value = sample_recipe

            # When: /recipe/random 엔드포인트 호출
            response = client.get('/recipe/random')

            # Then: 200 상태 코드와 레시피 데이터 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data == sample_recipe
            assert data["korean_name"] == "테스트 칵테일"
            assert data["code"] == "TEST001"


    def test_get_recipe_by_name(self, client, sample_recipes_list):
        """
        GET /recipe/name=<name> 엔드포인트 테스트
        이름으로 레시피를 검색하면 검색 결과를 반환하는지 검증
        """
        # Given: 검색어에 해당하는 레시피들이 존재함
        search_results = [sample_recipes_list[0]]  # 진토닉만 반환

        with patch('app.services.recipe_service.recipe_service.search_by_name') as mock_search:
            mock_search.return_value = search_results

            # When: /recipe/name=진토닉 엔드포인트 호출
            response = client.get('/recipe/name=진토닉')

            # Then: 200 상태 코드와 검색 결과 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["total_count"] == 1
            assert data["query"] == "진토닉"
            assert len(data["results"]) == 1
            assert data["results"][0]["korean_name"] == "진토닉"
            mock_search.assert_called_once_with("진토닉")

    def test_get_recipe_by_code_valid(self, client, sample_recipe):
        """
        GET /recipe/code=<code> 엔드포인트 테스트 (유효한 코드)
        유효한 코드로 레시피를 검색하면 해당 레시피 데이터를 반환하는지 검증
        """
        # Given: 특정 코드의 레시피가 존재함
        with patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search:
            mock_search.return_value = sample_recipe

            # When: /recipe/code=TEST001 엔드포인트 호출
            response = client.get('/recipe/code=TEST001')

            # Then: 200 상태 코드와 레시피 데이터 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data == sample_recipe
            assert data["code"] == "TEST001"
            assert data["korean_name"] == "테스트 칵테일"
            mock_search.assert_called_once_with("TEST001")

    def test_get_recipe_by_code_not_found(self, client):
        """
        GET /recipe/code=<code> 엔드포인트 테스트 (존재하지 않는 코드)
        존재하지 않는 코드로 검색하면 404 에러를 반환하는지 검증
        """
        # Given: 해당 코드의 레시피가 존재하지 않음
        with patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search:
            mock_search.return_value = None

            # When: /recipe/code=INVALID_CODE 엔드포인트 호출
            response = client.get('/recipe/code=INVALID_CODE')

            # Then: 404 상태 코드와 에러 메시지 반환
            assert response.status_code == 404
            data = response.get_json()
            assert data["success"] is False
            assert "레시피" in data["message"]
            assert data["error_code"] == "NOT_FOUND"
            mock_search.assert_called_once_with("INVALID_CODE")


    def test_get_recipes_with_ingredients(self, client, sample_recipes_list):
        """
        GET /recipe/with=<codes> 엔드포인트 테스트
        재료 코드들로 만들 수 있는 레시피를 검색하면 검색 결과를 반환하는지 검증
        """
        # Given: 특정 재료들로 만들 수 있는 레시피들이 존재함
        ingredient_codes = "300,600"  # 진, 토닉워터
        search_results = [sample_recipes_list[0]]  # 진토닉

        with patch('app.services.recipe_service.recipe_service.search_by_ingredients') as mock_search:
            mock_search.return_value = search_results

            # When: /recipe/with=300,600 엔드포인트 호출
            response = client.get(f'/recipe/with={ingredient_codes}')

            # Then: 200 상태 코드와 검색 결과 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["total_count"] == 1
            assert data["query"] == ingredient_codes
            assert len(data["results"]) == 1
            assert data["results"][0]["korean_name"] == "진토닉"
            mock_search.assert_called_once_with(ingredient_codes)

    def test_get_recipes_by_difficulty(self, client, sample_recipes_list):
        """
        GET /recipe/difficulty=<difficulty> 엔드포인트 테스트
        난이도별 레시피를 검색하면 해당 난이도의 레시피들을 반환하는지 검증
        """
        # Given: 특정 난이도의 레시피들이 존재함
        difficulty = "쉬움"
        easy_recipes = [sample_recipes_list[0]]  # 진토닉 (쉬움)

        with patch('app.services.recipe_service.recipe_service.get_recipes_by_difficulty') as mock_get_by_difficulty:
            mock_get_by_difficulty.return_value = easy_recipes

            # When: /recipe/difficulty=쉬움 엔드포인트 호출
            response = client.get(f'/recipe/difficulty={difficulty}')

            # Then: 200 상태 코드와 검색 결과 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["total_count"] == 1
            assert data["query"] == difficulty
            assert len(data["results"]) == 1
            assert data["results"][0]["difficulty"] == "쉬움"
            mock_get_by_difficulty.assert_called_once_with(difficulty)


    def test_get_recipe_image_exists(self, client):
        """
        GET /recipe/image=<code> 엔드포인트 테스트 (이미지 존재)
        이미지 파일이 존재하면 이미지를 정상적으로 반환하는지 검증
        """
        # Given: 특정 코드의 이미지 파일이 존재함
        test_code = "300600"
        
        with patch('app.routes.recipe_routes.os.path.exists') as mock_exists, \
             patch('app.routes.recipe_routes.send_from_directory') as mock_send:
            mock_exists.return_value = True
            mock_send.return_value = MagicMock()

            # When: /recipe/image=300600 엔드포인트 호출
            response = client.get(f'/recipe/image={test_code}')

            # Then: send_from_directory가 호출되어 이미지 반환
            assert mock_exists.called
            assert mock_send.called
            # send_from_directory의 두 번째 인자가 올바른 파일명인지 확인
            call_args = mock_send.call_args
            assert f"{test_code}.png" in str(call_args)

    def test_get_recipe_image_not_found(self, client):
        """
        GET /recipe/image=<code> 엔드포인트 테스트 (이미지 없음)
        이미지 파일이 존재하지 않으면 404 에러를 반환하는지 검증
        """
        # Given: 특정 코드의 이미지 파일이 존재하지 않음
        test_code = "NONEXISTENT_CODE"
        
        with patch('app.routes.recipe_routes.os.path.exists') as mock_exists:
            mock_exists.return_value = False

            # When: /recipe/image=NONEXISTENT_CODE 엔드포인트 호출
            response = client.get(f'/recipe/image={test_code}')

            # Then: 404 상태 코드와 에러 메시지 반환
            assert response.status_code == 404
            data = response.get_json()
            assert data["success"] is False
            assert "이미지" in data["message"]
            assert data["error_code"] == "NOT_FOUND"
            mock_exists.assert_called()
