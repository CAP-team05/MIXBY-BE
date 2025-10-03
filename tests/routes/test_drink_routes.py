"""
DrinkRoutes 통합 테스트
"""

import pytest
from unittest.mock import patch, MagicMock


class TestDrinkRoutes:
    """DrinkRoutes 엔드포인트 테스트"""

    def test_get_all_drinks(self, client):
        """
        GET /drink/all 엔드포인트 테스트
        모든 음료 데이터를 정상적으로 반환하는지 검증
        """
        # Given: 음료 데이터가 존재함
        mock_drinks = [
            {
                "code": "0000088001159",
                "name": "Absolut Vodka",
                "type": "Vodka"
            },
            {
                "code": "0000088001166",
                "name": "Absolut Citron",
                "type": "Vodka"
            }
        ]

        with patch('app.services.drink_service.drink_service.get_all_drinks') as mock_get_all:
            mock_get_all.return_value = mock_drinks

            # When: /drink/all 엔드포인트 호출
            response = client.get('/drink/all')

            # Then: 200 상태 코드와 음료 데이터 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data == mock_drinks
            assert len(data) == 2
            assert data[0]["name"] == "Absolut Vodka"

    def test_get_drink_types(self, client):
        """
        GET /drink/types 엔드포인트 테스트
        사용 가능한 모든 음료 타입을 정상적으로 반환하는지 검증
        """
        # Given: 음료 타입 데이터가 존재함
        mock_types = ["Vodka", "Gin", "Rum", "Whiskey", "Tequila"]

        with patch('app.services.drink_service.drink_service.get_drink_types') as mock_get_types:
            mock_get_types.return_value = mock_types

            # When: /drink/types 엔드포인트 호출
            response = client.get('/drink/types')

            # Then: 200 상태 코드와 타입 리스트 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data == mock_types
            assert len(data) == 5
            assert "Vodka" in data
            assert "Gin" in data

    def test_get_drink_by_code_valid(self, client):
        """
        GET /drink/code=<code> 엔드포인트 테스트 (유효한 코드)
        유효한 코드로 음료를 검색하면 해당 음료 데이터를 반환하는지 검증
        """
        # Given: 특정 코드의 음료가 존재함
        mock_drink = {
            "code": "0000088001159",
            "name": "Absolut Vodka",
            "type": "Vodka",
            "alcohol": 40.0
        }

        with patch('app.services.drink_service.drink_service.search_by_code') as mock_search:
            mock_search.return_value = mock_drink

            # When: /drink/code=0000088001159 엔드포인트 호출
            response = client.get('/drink/code=0000088001159')

            # Then: 200 상태 코드와 음료 데이터 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data == mock_drink
            assert data["code"] == "0000088001159"
            assert data["name"] == "Absolut Vodka"
            mock_search.assert_called_once_with("0000088001159")

    def test_get_drink_by_code_invalid(self, client):
        """
        GET /drink/code=<code> 엔드포인트 테스트 (존재하지 않는 코드)
        존재하지 않는 코드로 검색하면 404 에러를 반환하는지 검증
        """
        # Given: 해당 코드의 음료가 존재하지 않음
        with patch('app.services.drink_service.drink_service.search_by_code') as mock_search:
            mock_search.return_value = None

            # When: /drink/code=INVALID_CODE 엔드포인트 호출
            response = client.get('/drink/code=INVALID_CODE')

            # Then: 404 상태 코드와 에러 메시지 반환
            assert response.status_code == 404
            data = response.get_json()
            assert data["success"] is False
            assert "음료" in data["message"]
            assert data["error_code"] == "NOT_FOUND"
            mock_search.assert_called_once_with("INVALID_CODE")

    def test_get_drink_by_name(self, client):
        """
        GET /drink/name=<name> 엔드포인트 테스트
        이름으로 음료를 검색하면 검색 결과를 반환하는지 검증
        """
        # Given: 검색어에 해당하는 음료들이 존재함
        mock_drinks = [
            {
                "code": "0000088001159",
                "name": "Absolut Vodka",
                "type": "Vodka"
            },
            {
                "code": "0000088001166",
                "name": "Absolut Citron",
                "type": "Vodka"
            }
        ]

        with patch('app.services.drink_service.drink_service.search_by_name') as mock_search:
            mock_search.return_value = mock_drinks

            # When: /drink/name=Absolut 엔드포인트 호출
            response = client.get('/drink/name=Absolut')

            # Then: 200 상태 코드와 검색 결과 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["total_count"] == 2
            assert data["query"] == "Absolut"
            assert len(data["results"]) == 2
            assert data["results"][0]["name"] == "Absolut Vodka"
            mock_search.assert_called_once_with("Absolut")

    def test_get_drink_by_type(self, client):
        """
        GET /drink/type=<drink_type> 엔드포인트 테스트
        타입으로 음료를 검색하면 해당 타입의 음료들을 반환하는지 검증
        """
        # Given: 특정 타입의 음료들이 존재함
        mock_drinks = [
            {
                "code": "0000088001159",
                "name": "Absolut Vodka",
                "type": "Vodka"
            },
            {
                "code": "0000088001166",
                "name": "Absolut Citron",
                "type": "Vodka"
            },
            {
                "code": "5010314003807",
                "name": "Smirnoff Vodka",
                "type": "Vodka"
            }
        ]

        with patch('app.services.drink_service.drink_service.search_by_type') as mock_search:
            mock_search.return_value = mock_drinks

            # When: /drink/type=Vodka 엔드포인트 호출
            response = client.get('/drink/type=Vodka')

            # Then: 200 상태 코드와 검색 결과 반환
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["total_count"] == 3
            assert data["query"] == "Vodka"
            assert len(data["results"]) == 3
            assert all(drink["type"] == "Vodka" for drink in data["results"])
            mock_search.assert_called_once_with("Vodka")

    def test_get_drink_image_exists(self, client):
        """
        GET /drink/image=<code> 엔드포인트 테스트 (이미지 존재)
        이미지 파일이 존재하면 이미지를 정상적으로 반환하는지 검증
        """
        # Given: 특정 코드의 이미지 파일이 존재함
        test_code = "0000088001159"
        
        with patch('app.routes.drink_routes.os.path.exists') as mock_exists, \
             patch('app.routes.drink_routes.send_from_directory') as mock_send:
            mock_exists.return_value = True
            mock_send.return_value = MagicMock()

            # When: /drink/image=0000088001159 엔드포인트 호출
            response = client.get(f'/drink/image={test_code}')

            # Then: send_from_directory가 호출되어 이미지 반환
            assert mock_exists.called
            assert mock_send.called
            # send_from_directory의 두 번째 인자가 올바른 파일명인지 확인
            call_args = mock_send.call_args
            assert f"{test_code}.png" in str(call_args)

    def test_get_drink_image_not_found(self, client):
        """
        GET /drink/image=<code> 엔드포인트 테스트 (이미지 없음)
        이미지 파일이 존재하지 않으면 404 에러를 반환하는지 검증
        """
        # Given: 특정 코드의 이미지 파일이 존재하지 않음
        test_code = "NONEXISTENT_CODE"
        
        with patch('app.routes.drink_routes.os.path.exists') as mock_exists:
            mock_exists.return_value = False

            # When: /drink/image=NONEXISTENT_CODE 엔드포인트 호출
            response = client.get(f'/drink/image={test_code}')

            # Then: 404 상태 코드와 에러 메시지 반환
            assert response.status_code == 404
            data = response.get_json()
            assert data["success"] is False
            assert "이미지" in data["message"]
            assert data["error_code"] == "NOT_FOUND"
            mock_exists.assert_called()

    def test_validation_errors(self, client):
        """
        입력 검증 테스트
        잘못된 입력에 대해 적절한 에러 응답을 반환하는지 검증
        """
        # Test 1: 공백 코드로 검색
        # Given: 공백 코드가 전달됨
        # When: /drink/code=%20 엔드포인트 호출 (URL 인코딩된 공백)
        response = client.get('/drink/code=%20')
        
        # Then: 400 상태 코드와 검증 에러 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["error_code"] == "VALIDATION_ERROR"
        assert "errors" in data
        
        # Test 2: 특수 문자가 포함된 코드로 검색
        # Given: 특수 문자가 포함된 코드가 전달됨
        # When: /drink/code=test@code! 엔드포인트 호출
        response = client.get('/drink/code=test@code!')
        
        # Then: 400 상태 코드와 검증 에러 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["error_code"] == "VALIDATION_ERROR"
        assert "errors" in data
        errors = data["errors"]
        assert any("형식" in error for error in errors)
        
        # Test 3: 너무 긴 코드로 검색
        # Given: 50자를 초과하는 코드가 전달됨
        long_code = "A" * 51
        # When: /drink/code={long_code} 엔드포인트 호출
        response = client.get(f'/drink/code={long_code}')
        
        # Then: 400 상태 코드와 검증 에러 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["error_code"] == "VALIDATION_ERROR"
        assert "errors" in data
        errors = data["errors"]
        assert any("50자" in error for error in errors)
        
        # Test 4: 공백 이름으로 검색
        # Given: 공백 검색어가 전달됨
        # When: /drink/name=%20 엔드포인트 호출 (URL 인코딩된 공백)
        response = client.get('/drink/name=%20')
        
        # Then: 400 상태 코드와 검증 에러 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["error_code"] == "VALIDATION_ERROR"
        assert "errors" in data
        
        # Test 5: 특수 문자가 포함된 이름으로 검색
        # Given: 허용되지 않는 특수 문자가 포함된 검색어가 전달됨
        # When: /drink/name=<script> 엔드포인트 호출
        response = client.get('/drink/name=<script>')
        
        # Then: 400 상태 코드와 검증 에러 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["error_code"] == "VALIDATION_ERROR"
        assert "errors" in data
        errors = data["errors"]
        assert any("허용되지 않는 문자" in error for error in errors)
        
        # Test 6: 너무 긴 이름으로 검색
        # Given: 100자를 초과하는 검색어가 전달됨
        long_name = "A" * 101
        # When: /drink/name={long_name} 엔드포인트 호출
        response = client.get(f'/drink/name={long_name}')
        
        # Then: 400 상태 코드와 검증 에러 반환
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["error_code"] == "VALIDATION_ERROR"
        assert "errors" in data
        errors = data["errors"]
        assert any("100자" in error for error in errors)
