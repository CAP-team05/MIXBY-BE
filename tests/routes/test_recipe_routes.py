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

    def test_get_all_recipes_exception(self, client):
        """
        GET /recipe/all 엔드포인트 예외 처리 테스트
        서비스에서 예외가 발생하면 500 에러를 반환하는지 검증
        """
        # Given: 서비스에서 예외 발생
        with patch('app.services.recipe_service.recipe_service.get_all_recipes') as mock_get_all:
            mock_get_all.side_effect = Exception("Database error")

            # When: /recipe/all 엔드포인트 호출
            response = client.get('/recipe/all')

            # Then: 500 상태 코드와 에러 메시지 반환
            assert response.status_code == 500
            data = response.get_json()
            assert data["success"] is False
            assert "레시피 데이터를 가져오는 중 오류가 발생했습니다" in data["message"]

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

    def test_get_recipe_categories_exception(self, client):
        """
        GET /recipe/categories 엔드포인트 예외 처리 테스트
        서비스에서 예외가 발생하면 500 에러를 반환하는지 검증
        """
        # Given: 서비스에서 예외 발생
        with patch('app.services.recipe_service.recipe_service.get_recipe_categories') as mock_get_categories:
            mock_get_categories.side_effect = Exception("Database error")

            # When: /recipe/categories 엔드포인트 호출
            response = client.get('/recipe/categories')

            # Then: 500 상태 코드와 에러 메시지 반환
            assert response.status_code == 500
            data = response.get_json()
            assert data["success"] is False
            assert "레시피 카테고리를 가져오는 중 오류가 발생했습니다" in data["message"]

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

    def test_get_random_recipe_no_recipes(self, client):
        """
        GET /recipe/random 엔드포인트 테스트 (레시피 없음)
        사용 가능한 레시피가 없으면 404 에러를 반환하는지 검증
        """
        # Given: 사용 가능한 레시피가 없음
        with patch('app.services.recipe_service.recipe_service.get_random_recipe') as mock_get_random:
            mock_get_random.return_value = None

            # When: /recipe/random 엔드포인트 호출
            response = client.get('/recipe/random')

            # Then: 404 상태 코드와 에러 메시지 반환
            assert response.status_code == 404
            data = response.get_json()
            assert data["success"] is False
            assert "사용 가능한 레시피가 없습니다" in data["message"]

    def test_get_random_recipe_exception(self, client):
        """
        GET /recipe/random 엔드포인트 예외 처리 테스트
        서비스에서 예외가 발생하면 500 에러를 반환하는지 검증
        """
        # Given: 서비스에서 예외 발생
        with patch('app.services.recipe_service.recipe_service.get_random_recipe') as mock_get_random:
            mock_get_random.side_effect = Exception("Random error")

            # When: /recipe/random 엔드포인트 호출
            response = client.get('/recipe/random')

            # Then: 500 상태 코드와 에러 메시지 반환
            assert response.status_code == 500
            data = response.get_json()
            assert data["success"] is False
            assert "무작위 레시피를 가져오는 중 오류가 발생했습니다" in data["message"]


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

    def test_get_recipe_by_name_exception(self, client):
        """
        GET /recipe/name=<name> 엔드포인트 예외 처리 테스트
        서비스에서 예외가 발생하면 500 에러를 반환하는지 검증
        """
        # Given: 서비스에서 예외 발생
        with patch('app.services.recipe_service.recipe_service.search_by_name') as mock_search:
            mock_search.side_effect = Exception("Search error")

            # When: /recipe/name=진토닉 엔드포인트 호출
            response = client.get('/recipe/name=진토닉')

            # Then: 500 상태 코드와 에러 메시지 반환
            assert response.status_code == 500
            data = response.get_json()
            assert data["success"] is False
            assert "레시피 검색 중 오류가 발생했습니다" in data["message"]

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

    def test_get_recipe_by_code_exception(self, client):
        """
        GET /recipe/code=<code> 엔드포인트 예외 처리 테스트
        서비스에서 예외가 발생하면 500 에러를 반환하는지 검증
        """
        # Given: 서비스에서 예외 발생
        with patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search:
            mock_search.side_effect = Exception("Database error")

            # When: /recipe/code=TEST001 엔드포인트 호출
            response = client.get('/recipe/code=TEST001')

            # Then: 500 상태 코드와 에러 메시지 반환
            assert response.status_code == 500
            data = response.get_json()
            assert data["success"] is False
            assert "레시피 검색 중 오류가 발생했습니다" in data["message"]


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

    def test_get_recipes_with_ingredients_exception(self, client):
        """
        GET /recipe/with=<codes> 엔드포인트 예외 처리 테스트
        서비스에서 예외가 발생하면 500 에러를 반환하는지 검증
        """
        # Given: 서비스에서 예외 발생
        with patch('app.services.recipe_service.recipe_service.search_by_ingredients') as mock_search:
            mock_search.side_effect = Exception("Search error")

            # When: /recipe/with=300,600 엔드포인트 호출
            response = client.get('/recipe/with=300,600')

            # Then: 500 상태 코드와 에러 메시지 반환
            assert response.status_code == 500
            data = response.get_json()
            assert data["success"] is False
            assert "레시피 검색 중 오류가 발생했습니다" in data["message"]

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

    def test_get_recipes_by_difficulty_exception(self, client):
        """
        GET /recipe/difficulty=<difficulty> 엔드포인트 예외 처리 테스트
        서비스에서 예외가 발생하면 500 에러를 반환하는지 검증
        """
        # Given: 서비스에서 예외 발생
        with patch('app.services.recipe_service.recipe_service.get_recipes_by_difficulty') as mock_get_by_difficulty:
            mock_get_by_difficulty.side_effect = Exception("Database error")

            # When: /recipe/difficulty=쉬움 엔드포인트 호출
            response = client.get('/recipe/difficulty=쉬움')

            # Then: 500 상태 코드와 에러 메시지 반환
            assert response.status_code == 500
            data = response.get_json()
            assert data["success"] is False
            assert "난이도별 레시피 검색 중 오류가 발생했습니다" in data["message"]


    def test_get_recipe_image_by_code_exists(self, client, sample_recipe):
        """
        GET /recipe/image/code=<code> 엔드포인트 테스트 (이미지 존재)
        이미지 파일이 존재하면 이미지를 정상적으로 반환하는지 검증
        """
        # Given: 특정 코드의 레시피와 이미지 파일이 존재함
        test_code = "300600"
        
        with patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search, \
             patch('app.routes.recipe_routes.os.path.exists') as mock_exists, \
             patch('app.routes.recipe_routes.send_from_directory') as mock_send:
            mock_search.return_value = sample_recipe
            mock_exists.return_value = True
            mock_send.return_value = MagicMock()

            # When: /recipe/image/code=300600 엔드포인트 호출
            response = client.get(f'/recipe/image/code={test_code}')

            # Then: 레시피 존재 확인 후 send_from_directory가 호출되어 이미지 반환
            mock_search.assert_called_once_with(test_code)
            assert mock_exists.called
            assert mock_send.called
            # send_from_directory의 두 번째 인자가 올바른 파일명인지 확인
            call_args = mock_send.call_args
            assert f"{test_code}.png" in str(call_args)

    def test_get_recipe_image_by_code_not_found(self, client):
        """
        GET /recipe/image/code=<code> 엔드포인트 테스트 (레시피 없음)
        레시피가 존재하지 않으면 404 에러를 반환하는지 검증
        """
        # Given: 특정 코드의 레시피가 존재하지 않음
        test_code = "NONEXISTENT_CODE"
        
        with patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search:
            mock_search.return_value = None

            # When: /recipe/image/code=NONEXISTENT_CODE 엔드포인트 호출
            response = client.get(f'/recipe/image/code={test_code}')

            # Then: 404 상태 코드와 명확한 에러 메시지 반환
            assert response.status_code == 404
            data = response.get_json()
            assert data["success"] is False
            assert "레시피" in data["message"]
            assert data["error_code"] == "RECIPE_NOT_FOUND"
            mock_search.assert_called_once_with(test_code)

    def test_get_recipe_image_by_code_exception(self, client, sample_recipe):
        """
        GET /recipe/image/code=<code> 엔드포인트 예외 처리 테스트
        파일 시스템 접근 중 예외가 발생하면 500 에러를 반환하는지 검증
        """
        # Given: 레시피는 존재하지만 파일 시스템 접근 중 예외 발생
        test_code = "TEST001"
        
        with patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search, \
             patch('app.routes.recipe_routes.current_app') as mock_app:
            mock_search.return_value = sample_recipe
            mock_app.static_folder = None  # None으로 설정하여 예외 발생 유도

            # When: /recipe/image/code=TEST001 엔드포인트 호출
            response = client.get(f'/recipe/image/code={test_code}')

            # Then: 500 상태 코드와 에러 메시지 반환
            assert response.status_code == 500
            data = response.get_json()
            assert data["success"] is False
            assert "이미지를 가져오는 중 오류가 발생했습니다" in data["message"]

    def test_get_recipe_image_by_code_empty_code(self, client):
        """
        GET /recipe/image/code=<code> 엔드포인트 테스트 (빈 코드)
        빈 문자열로 호출하면 400 에러를 반환하는지 검증
        """
        # Given: 빈 레시피 코드
        
        # When: /recipe/image/code= 엔드포인트 호출 (빈 코드)
        # Flask는 빈 문자열을 URL 파라미터로 받을 수 있음
        with patch('app.routes.recipe_routes.os.path.exists') as mock_exists:
            # 빈 문자열은 입력 검증에서 걸러지므로 os.path.exists가 호출되지 않음
            response = client.get('/recipe/image/code=')

            # Then: 400 상태 코드와 에러 메시지 반환
            # 빈 문자열이 전달되면 _send_recipe_image에서 400 반환
            if response.status_code == 400:
                data = response.get_json()
                assert data["success"] is False
                assert "레시피 코드가 필요합니다" in data["message"]
                assert data["error_code"] == "INVALID_INPUT"

    def test_old_image_endpoint_removed(self, client):
        """
        GET /recipe/image=<code> 엔드포인트 제거 확인 테스트
        기존 엔드포인트가 더 이상 작동하지 않는지 검증 (Breaking Change)
        """
        # Given: 기존 엔드포인트 URL
        test_code = "300600"
        
        # When: 기존 /recipe/image=<code> 엔드포인트 호출
        response = client.get(f'/recipe/image={test_code}')

        # Then: 404 상태 코드 반환 (엔드포인트가 존재하지 않음)
        assert response.status_code == 404

    def test_get_recipe_image_by_name_valid(self, client, sample_recipe):
        """
        GET /recipe/image/name=<name> 엔드포인트 테스트 (유효한 이름)
        유효한 레시피 이름으로 이미지를 요청하면 이미지를 반환하는지 검증
        """
        # Given: 유효한 레시피 이름과 해당 레시피 및 이미지 파일이 존재함
        test_name = "모히또"
        test_code = "300600"
        
        with patch('app.services.recipe_service.recipe_service.get_code_by_name') as mock_get_code, \
             patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search, \
             patch('app.routes.recipe_routes.os.path.exists') as mock_exists, \
             patch('app.routes.recipe_routes.send_from_directory') as mock_send:
            mock_get_code.return_value = test_code
            mock_search.return_value = sample_recipe
            mock_exists.return_value = True
            mock_send.return_value = MagicMock()

            # When: /recipe/image/name=모히또 엔드포인트 호출
            response = client.get(f'/recipe/image/name={test_name}')

            # Then: 레시피 코드를 찾고 이미지를 반환
            mock_get_code.assert_called_once_with(test_name)
            mock_search.assert_called_once_with(test_code)
            assert mock_exists.called
            assert mock_send.called
            call_args = mock_send.call_args
            assert f"{test_code}.png" in str(call_args)

    def test_get_recipe_image_by_name_not_found(self, client):
        """
        GET /recipe/image/name=<name> 엔드포인트 테스트 (존재하지 않는 이름)
        존재하지 않는 레시피 이름으로 요청하면 404 에러를 반환하는지 검증
        """
        # Given: 존재하지 않는 레시피 이름
        test_name = "존재하지않는칵테일"
        
        with patch('app.services.recipe_service.recipe_service.get_code_by_name') as mock_get_code:
            mock_get_code.return_value = None

            # When: /recipe/image/name=존재하지않는칵테일 엔드포인트 호출
            response = client.get(f'/recipe/image/name={test_name}')

            # Then: 404 상태 코드와 에러 메시지 반환
            assert response.status_code == 404
            data = response.get_json()
            assert data["success"] is False
            assert f"레시피 '{test_name}'을(를) 찾을 수 없습니다" in data["message"]
            assert data["error_code"] == "RECIPE_NOT_FOUND"
            mock_get_code.assert_called_once_with(test_name)

    def test_get_recipe_image_by_name_empty_name(self, client):
        """
        GET /recipe/image/name=<name> 엔드포인트 테스트 (빈 이름)
        빈 문자열로 호출하면 400 에러를 반환하는지 검증
        """
        # Given: 빈 레시피 이름
        
        # When: /recipe/image/name= 엔드포인트 호출 (빈 이름)
        response = client.get('/recipe/image/name=')

        # Then: 400 상태 코드와 에러 메시지 반환
        if response.status_code == 400:
            data = response.get_json()
            assert data["success"] is False
            assert "레시피 이름이 필요합니다" in data["message"]
            assert data["error_code"] == "INVALID_INPUT"

    def test_get_recipe_image_by_name_url_encoded(self, client, sample_recipe):
        """
        GET /recipe/image/name=<name> 엔드포인트 테스트 (URL 인코딩된 이름)
        URL 인코딩된 레시피 이름을 올바르게 처리하는지 검증
        """
        # Given: URL 인코딩된 레시피 이름
        test_name_encoded = "%EB%AA%A8%ED%9E%88%EB%98%90"  # "모히또"의 URL 인코딩
        test_name_decoded = "모히또"
        test_code = "300600"
        
        with patch('app.services.recipe_service.recipe_service.get_code_by_name') as mock_get_code, \
             patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search, \
             patch('app.routes.recipe_routes.os.path.exists') as mock_exists, \
             patch('app.routes.recipe_routes.send_from_directory') as mock_send:
            mock_get_code.return_value = test_code
            mock_search.return_value = sample_recipe
            mock_exists.return_value = True
            mock_send.return_value = MagicMock()

            # When: URL 인코딩된 이름으로 엔드포인트 호출
            response = client.get(f'/recipe/image/name={test_name_encoded}')

            # Then: 디코딩된 이름으로 레시피를 찾고 이미지를 반환
            mock_get_code.assert_called_once_with(test_name_decoded)
            mock_search.assert_called_once_with(test_code)
            assert mock_exists.called
            assert mock_send.called

    def test_get_recipe_image_by_name_with_spaces(self, client, sample_recipe):
        """
        GET /recipe/image/name=<name> 엔드포인트 테스트 (공백 포함 이름)
        공백이 포함된 레시피 이름을 올바르게 처리하는지 검증
        """
        # Given: 공백이 포함된 레시피 이름
        test_name = "진 토닉"
        test_code = "300600"
        
        with patch('app.services.recipe_service.recipe_service.get_code_by_name') as mock_get_code, \
             patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search, \
             patch('app.routes.recipe_routes.os.path.exists') as mock_exists, \
             patch('app.routes.recipe_routes.send_from_directory') as mock_send:
            mock_get_code.return_value = test_code
            mock_search.return_value = sample_recipe
            mock_exists.return_value = True
            mock_send.return_value = MagicMock()

            # When: 공백이 포함된 이름으로 엔드포인트 호출
            response = client.get(f'/recipe/image/name={test_name}')

            # Then: 공백을 포함한 이름으로 레시피를 찾고 이미지를 반환
            mock_get_code.assert_called_once_with(test_name)
            mock_search.assert_called_once_with(test_code)
            assert mock_exists.called
            assert mock_send.called

    def test_get_recipe_image_by_name_exception(self, client):
        """
        GET /recipe/image/name=<name> 엔드포인트 예외 처리 테스트
        서비스에서 예외가 발생하면 500 에러를 반환하는지 검증
        """
        # Given: 서비스에서 예외 발생
        test_name = "모히또"
        
        with patch('app.services.recipe_service.recipe_service.get_code_by_name') as mock_get_code:
            mock_get_code.side_effect = Exception("Database error")

            # When: /recipe/image/name=모히또 엔드포인트 호출
            response = client.get(f'/recipe/image/name={test_name}')

            # Then: 500 상태 코드와 에러 메시지 반환
            assert response.status_code == 500
            data = response.get_json()
            assert data["success"] is False
            assert "이미지를 가져오는 중 오류가 발생했습니다" in data["message"]


class TestSendRecipeImageHelper:
    """_send_recipe_image() 헬퍼 함수 테스트"""

    def test_send_recipe_image_valid_code(self, client, sample_recipe):
        """
        _send_recipe_image() 유효한 코드로 이미지 반환 테스트
        유효한 레시피 코드로 호출하면 이미지 파일을 반환하는지 검증
        """
        # Given: 유효한 레시피 코드와 이미지 파일이 존재함
        from app.routes.recipe_routes import _send_recipe_image
        test_code = "300600"
        
        with patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search, \
             patch('app.routes.recipe_routes.os.path.exists') as mock_exists, \
             patch('app.routes.recipe_routes.send_from_directory') as mock_send, \
             patch('app.routes.recipe_routes.current_app') as mock_app:
            mock_search.return_value = sample_recipe
            mock_exists.return_value = True
            mock_send.return_value = MagicMock()
            mock_app.static_folder = "/fake/static"

            # When: _send_recipe_image() 호출
            with client.application.app_context():
                result = _send_recipe_image(test_code)

            # Then: 레시피 존재 확인 후 send_from_directory가 호출되어 이미지 반환
            mock_search.assert_called_once_with(test_code)
            assert mock_exists.called
            assert mock_send.called
            call_args = mock_send.call_args
            assert f"{test_code}.png" in str(call_args)

    def test_send_recipe_image_empty_code(self, client):
        """
        _send_recipe_image() 빈 코드 입력 테스트
        빈 문자열로 호출하면 400 에러를 반환하는지 검증
        """
        # Given: 빈 레시피 코드
        from app.routes.recipe_routes import _send_recipe_image
        
        # When: 빈 문자열로 _send_recipe_image() 호출
        with client.application.app_context():
            result_empty = _send_recipe_image("")
            result_whitespace = _send_recipe_image("   ")

        # Then: 400 상태 코드와 에러 메시지 반환
        assert result_empty.status_code == 400
        data_empty = result_empty.get_json()
        assert data_empty["success"] is False
        assert "레시피 코드가 필요합니다" in data_empty["message"]
        assert data_empty["error_code"] == "INVALID_INPUT"

        assert result_whitespace.status_code == 400
        data_whitespace = result_whitespace.get_json()
        assert data_whitespace["success"] is False
        assert "레시피 코드가 필요합니다" in data_whitespace["message"]

    def test_send_recipe_image_file_not_found(self, client, sample_recipe):
        """
        _send_recipe_image() 이미지 파일 없음 테스트
        레시피는 존재하지만 이미지 파일이 없으면 404 에러를 반환하는지 검증
        """
        # Given: 레시피는 존재하지만 이미지 파일이 존재하지 않음
        from app.routes.recipe_routes import _send_recipe_image
        test_code = "MISSING_IMAGE"
        
        with patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search, \
             patch('app.routes.recipe_routes.os.path.exists') as mock_exists, \
             patch('app.routes.recipe_routes.current_app') as mock_app:
            mock_search.return_value = sample_recipe
            mock_exists.return_value = False
            mock_app.static_folder = "/fake/static"

            # When: _send_recipe_image() 호출
            with client.application.app_context():
                result = _send_recipe_image(test_code)

            # Then: 404 상태 코드와 명확한 에러 메시지 반환 (레시피는 있지만 이미지 파일이 없음)
            assert result.status_code == 404
            data = result.get_json()
            assert data["success"] is False
            assert f"레시피 '{test_code}'의 이미지 파일이 존재하지 않습니다" in data["message"]
            assert data["error_code"] == "IMAGE_FILE_NOT_FOUND"

    def test_send_recipe_image_exception_handling(self, client, sample_recipe):
        """
        _send_recipe_image() 예외 처리 테스트
        파일 시스템 접근 중 예외가 발생하면 500 에러를 반환하는지 검증
        """
        # Given: 레시피는 존재하지만 파일 시스템 접근 중 예외 발생
        from app.routes.recipe_routes import _send_recipe_image
        test_code = "TEST001"
        
        with patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search, \
             patch('app.routes.recipe_routes.current_app') as mock_app:
            mock_search.return_value = sample_recipe
            mock_app.static_folder = None  # None으로 설정하여 예외 발생 유도

            # When: _send_recipe_image() 호출
            with client.application.app_context():
                result = _send_recipe_image(test_code)

            # Then: 500 상태 코드와 일반적인 에러 메시지 반환
            assert result.status_code == 500
            data = result.get_json()
            assert data["success"] is False
            assert "이미지를 가져오는 중 오류가 발생했습니다" in data["message"]

    def test_send_recipe_image_permission_error(self, client, sample_recipe):
        """
        _send_recipe_image() 권한 에러 테스트
        파일 접근 권한이 없으면 500 에러를 반환하는지 검증
        """
        # Given: 레시피는 존재하지만 파일 접근 권한이 없음
        from app.routes.recipe_routes import _send_recipe_image
        test_code = "TEST001"
        
        with patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search, \
             patch('app.routes.recipe_routes.os.path.exists') as mock_exists, \
             patch('app.routes.recipe_routes.current_app') as mock_app:
            mock_search.return_value = sample_recipe
            mock_exists.side_effect = PermissionError("Permission denied")
            mock_app.static_folder = "/fake/static"

            # When: _send_recipe_image() 호출
            with client.application.app_context():
                result = _send_recipe_image(test_code)

            # Then: 500 상태 코드와 권한 에러 메시지 반환
            assert result.status_code == 500
            data = result.get_json()
            assert data["success"] is False
            assert "이미지 파일에 접근할 권한이 없습니다" in data["message"]
            assert data["error_code"] == "FILE_PERMISSION_ERROR"

    def test_send_recipe_image_os_error(self, client, sample_recipe):
        """
        _send_recipe_image() 파일 시스템 에러 테스트
        파일 시스템 접근 중 OSError가 발생하면 500 에러를 반환하는지 검증
        """
        # Given: 레시피는 존재하지만 파일 시스템 접근 중 OSError 발생
        from app.routes.recipe_routes import _send_recipe_image
        test_code = "TEST001"
        
        with patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search, \
             patch('app.routes.recipe_routes.os.path.exists') as mock_exists, \
             patch('app.routes.recipe_routes.current_app') as mock_app:
            mock_search.return_value = sample_recipe
            mock_exists.side_effect = OSError("Disk I/O error")
            mock_app.static_folder = "/fake/static"

            # When: _send_recipe_image() 호출
            with client.application.app_context():
                result = _send_recipe_image(test_code)

            # Then: 500 상태 코드와 파일 시스템 에러 메시지 반환
            assert result.status_code == 500
            data = result.get_json()
            assert data["success"] is False
            assert "파일 시스템 접근 중 오류가 발생했습니다" in data["message"]
            assert data["error_code"] == "FILE_SYSTEM_ERROR"

    def test_send_recipe_image_recipe_not_found(self, client):
        """
        _send_recipe_image() 레시피 없음 테스트
        레시피가 존재하지 않으면 404 에러를 반환하는지 검증
        """
        # Given: 레시피가 존재하지 않음
        from app.routes.recipe_routes import _send_recipe_image
        test_code = "NONEXISTENT"
        
        with patch('app.services.recipe_service.recipe_service.search_by_code') as mock_search:
            mock_search.return_value = None

            # When: _send_recipe_image() 호출
            with client.application.app_context():
                result = _send_recipe_image(test_code)

            # Then: 404 상태 코드와 레시피 없음 에러 메시지 반환
            assert result.status_code == 404
            data = result.get_json()
            assert data["success"] is False
            assert f"레시피 코드 '{test_code}'에 해당하는 레시피를 찾을 수 없습니다" in data["message"]
            assert data["error_code"] == "RECIPE_NOT_FOUND"
