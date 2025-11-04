"""
IngredientRoutes 통합 테스트
"""

import pytest
import json


class TestIngredientRoutes:
    """IngredientRoutes 엔드포인트 테스트"""

    def test_get_ingredients(self, client):
        """
        GET /ingredient/ 엔드포인트 테스트
        재료 목록이 정상적으로 반환되는지 검증
        """
        # Given: 서버가 실행 중이고 재료 데이터가 존재함

        # When: /ingredient/ 엔드포인트 호출
        response = client.get('/ingredient/')

        # Then: 200 상태 코드와 재료 목록 반환
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["message"] == "재료 목록을 성공적으로 조회했습니다."
        assert "ingredients" in data["data"]
        assert isinstance(data["data"]["ingredients"], list)
        assert len(data["data"]["ingredients"]) > 0

    def test_get_all_ingredients(self, client):
        """
        GET /ingredient/all 엔드포인트 테스트
        재료 목록이 정상적으로 반환되는지 검증
        """
        # Given: 서버가 실행 중이고 재료 데이터가 존재함

        # When: /ingredient/all 엔드포인트 호출
        response = client.get('/ingredient/all')

        # Then: 200 상태 코드와 재료 목록 반환
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["message"] == "재료 목록을 성공적으로 조회했습니다."
        assert "ingredients" in data["data"]
        assert isinstance(data["data"]["ingredients"], list)
        assert len(data["data"]["ingredients"]) > 0

    def test_ingredients_endpoints_return_same_data(self, client):
        """
        /ingredient/와 /ingredient/all이 같은 데이터를 반환하는지 검증
        """
        # Given: 서버가 실행 중임

        # When: 두 엔드포인트 모두 호출
        response1 = client.get('/ingredient/')
        response2 = client.get('/ingredient/all')

        # Then: 두 응답의 데이터가 동일함
        data1 = response1.get_json()
        data2 = response2.get_json()
        assert data1["data"]["ingredients"] == data2["data"]["ingredients"]

    def test_ingredients_data_structure(self, client):
        """
        재료 데이터 구조가 올바른지 검증
        각 재료가 name과 code 필드를 가지고 있는지 확인
        """
        # Given: 서버가 실행 중임

        # When: /ingredient/ 엔드포인트 호출
        response = client.get('/ingredient/')

        # Then: 각 재료가 올바른 구조를 가짐
        data = response.get_json()
        ingredients = data["data"]["ingredients"]

        for ingredient in ingredients:
            assert "name" in ingredient
            assert "code" in ingredient
            assert isinstance(ingredient["name"], str)
            assert isinstance(ingredient["code"], str)
            assert len(ingredient["name"]) > 0
            assert len(ingredient["code"]) > 0

    def test_ingredients_response_format(self, client):
        """
        GET /ingredient/ 엔드포인트 응답 형식 테스트
        응답이 표준 형식을 따르는지 검증
        """
        # Given: 서버가 실행 중임

        # When: /ingredient/ 엔드포인트 호출
        response = client.get('/ingredient/')

        # Then: 표준 응답 형식 검증
        assert response.status_code == 200
        data = response.get_json()
        assert "success" in data
        assert "message" in data
        assert "data" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["message"], str)
        assert isinstance(data["data"], dict)

    def test_ingredients_content_type(self, client):
        """
        GET /ingredient/ 엔드포인트 Content-Type 테스트
        응답이 JSON 형식인지 검증
        """
        # Given: 서버가 실행 중임

        # When: /ingredient/ 엔드포인트 호출
        response = client.get('/ingredient/')

        # Then: Content-Type이 JSON임
        assert response.status_code == 200
        assert response.content_type == "application/json"

    def test_ingredients_known_items(self, client):
        """
        재료 목록에 알려진 재료들이 포함되어 있는지 검증
        """
        # Given: 서버가 실행 중임

        # When: /ingredient/ 엔드포인트 호출
        response = client.get('/ingredient/')

        # Then: 알려진 재료들이 포함됨
        data = response.get_json()
        ingredients = data["data"]["ingredients"]
        ingredient_names = [ing["name"] for ing in ingredients]

        # allIngredients.json에 있는 일부 재료들 확인
        assert "위스키" in ingredient_names
        assert "진" in ingredient_names
        assert "보드카" in ingredient_names
        assert "럼" in ingredient_names

    def test_ingredients_code_format(self, client):
        """
        재료 코드가 올바른 형식인지 검증
        코드는 숫자 문자열이어야 함
        """
        # Given: 서버가 실행 중임

        # When: /ingredient/ 엔드포인트 호출
        response = client.get('/ingredient/')

        # Then: 모든 코드가 숫자로만 구성됨
        data = response.get_json()
        ingredients = data["data"]["ingredients"]

        for ingredient in ingredients:
            code = ingredient["code"]
            assert code.isdigit(), f"재료 '{ingredient['name']}'의 코드 '{code}'가 숫자가 아닙니다"
