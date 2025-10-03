"""
ResponseHelper 유틸리티 테스트
"""

import json
import pytest
from flask import Flask
from app.utils.response_helper import ResponseHelper


@pytest.fixture
def app():
    """Flask 애플리케이션 fixture"""
    app = Flask(__name__)
    return app


class TestResponseHelper:
    """ResponseHelper 클래스 테스트"""

    def test_json_response(self, app):
        """json_response 메서드 테스트"""
        with app.app_context():
            # Given: 테스트 데이터
            test_data = {"key": "value", "number": 123}
            
            # When: json_response 호출
            response = ResponseHelper.json_response(test_data, status_code=200)
            
            # Then: 응답 검증
            assert response.status_code == 200
            assert "application/json" in response.mimetype
            
            response_data = json.loads(response.data)
            assert response_data == test_data

    def test_json_response_with_custom_status_code(self, app):
        """json_response 커스텀 상태 코드 테스트"""
        with app.app_context():
            # Given: 테스트 데이터와 커스텀 상태 코드
            test_data = {"error": "test"}
            
            # When: json_response 호출
            response = ResponseHelper.json_response(test_data, status_code=404)
            
            # Then: 상태 코드 검증
            assert response.status_code == 404

    def test_success_response(self, app):
        """success_response 메서드 테스트"""
        with app.app_context():
            # Given: 성공 데이터
            test_data = {"result": "success"}
            
            # When: success_response 호출
            response = ResponseHelper.success_response(test_data, message="작업 완료")
            
            # Then: 응답 검증
            assert response.status_code == 200
            
            response_data = json.loads(response.data)
            assert response_data["success"] is True
            assert response_data["message"] == "작업 완료"
            assert response_data["data"] == test_data

    def test_success_response_default_message(self, app):
        """success_response 기본 메시지 테스트"""
        with app.app_context():
            # Given: 성공 데이터
            test_data = {"result": "success"}
            
            # When: success_response 호출 (메시지 생략)
            response = ResponseHelper.success_response(test_data)
            
            # Then: 기본 메시지 검증
            response_data = json.loads(response.data)
            assert response_data["message"] == "성공"

    def test_success_response_with_custom_status_code(self, app):
        """success_response 커스텀 상태 코드 테스트"""
        with app.app_context():
            # Given: 성공 데이터
            test_data = {"created": True}
            
            # When: success_response 호출 (201 상태 코드)
            response = ResponseHelper.success_response(test_data, message="생성됨", status_code=201)
            
            # Then: 상태 코드 검증
            assert response.status_code == 201

    def test_error_response(self, app):
        """error_response 메서드 테스트"""
        with app.app_context():
            # Given: 에러 메시지
            error_message = "잘못된 요청입니다"
            
            # When: error_response 호출
            response = ResponseHelper.error_response(error_message)
            
            # Then: 응답 검증
            assert response.status_code == 400
            
            response_data = json.loads(response.data)
            assert response_data["success"] is False
            assert response_data["message"] == error_message
            assert "error_code" not in response_data

    def test_error_response_with_code(self, app):
        """error_response error_code 포함 테스트"""
        with app.app_context():
            # Given: 에러 메시지와 코드
            error_message = "인증 실패"
            error_code = "AUTH_FAILED"
            
            # When: error_response 호출
            response = ResponseHelper.error_response(
                error_message, 
                status_code=401, 
                error_code=error_code
            )
            
            # Then: 응답 검증
            assert response.status_code == 401
            
            response_data = json.loads(response.data)
            assert response_data["success"] is False
            assert response_data["message"] == error_message
            assert response_data["error_code"] == error_code

    def test_error_response_with_custom_status_code(self, app):
        """error_response 커스텀 상태 코드 테스트"""
        with app.app_context():
            # Given: 에러 메시지와 500 상태 코드
            error_message = "서버 오류"
            
            # When: error_response 호출
            response = ResponseHelper.error_response(error_message, status_code=500)
            
            # Then: 상태 코드 검증
            assert response.status_code == 500

    def test_not_found_response(self, app):
        """not_found_response 메서드 테스트"""
        with app.app_context():
            # Given: 리소스명
            resource = "레시피"
            
            # When: not_found_response 호출
            response = ResponseHelper.not_found_response(resource)
            
            # Then: 응답 검증
            assert response.status_code == 404
            
            response_data = json.loads(response.data)
            assert response_data["success"] is False
            assert resource in response_data["message"]
            assert response_data["error_code"] == "NOT_FOUND"

    def test_not_found_response_default_resource(self, app):
        """not_found_response 기본 리소스명 테스트"""
        with app.app_context():
            # When: not_found_response 호출 (리소스명 생략)
            response = ResponseHelper.not_found_response()
            
            # Then: 기본 리소스명 검증
            response_data = json.loads(response.data)
            assert "리소스" in response_data["message"]

    def test_search_response(self, app):
        """search_response 메서드 테스트"""
        with app.app_context():
            # Given: 검색 결과
            results = [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"},
                {"id": 3, "name": "Item 3"}
            ]
            
            # When: search_response 호출
            response = ResponseHelper.search_response(results)
            
            # Then: 응답 검증
            assert response.status_code == 200
            
            response_data = json.loads(response.data)
            assert response_data["success"] is True
            assert response_data["total_count"] == 3
            assert response_data["results"] == results
            assert "query" not in response_data

    def test_search_response_with_query(self, app):
        """search_response 쿼리 포함 테스트"""
        with app.app_context():
            # Given: 검색 결과와 쿼리
            results = [{"id": 1, "name": "Test"}]
            query = "test keyword"
            
            # When: search_response 호출
            response = ResponseHelper.search_response(results, query=query)
            
            # Then: 응답 검증
            response_data = json.loads(response.data)
            assert response_data["query"] == query
            assert response_data["total_count"] == 1

    def test_search_response_with_custom_total_count(self, app):
        """search_response 커스텀 total_count 테스트"""
        with app.app_context():
            # Given: 검색 결과와 커스텀 total_count
            results = [{"id": 1}, {"id": 2}]
            total_count = 100  # 실제 결과보다 큰 값 (페이징 시나리오)
            
            # When: search_response 호출
            response = ResponseHelper.search_response(results, total_count=total_count)
            
            # Then: total_count 검증
            response_data = json.loads(response.data)
            assert response_data["total_count"] == 100
            assert len(response_data["results"]) == 2

    def test_search_response_empty_results(self, app):
        """search_response 빈 결과 테스트"""
        with app.app_context():
            # Given: 빈 검색 결과
            results = []
            
            # When: search_response 호출
            response = ResponseHelper.search_response(results)
            
            # Then: 응답 검증
            response_data = json.loads(response.data)
            assert response_data["total_count"] == 0
            assert response_data["results"] == []

    def test_validation_error_response_string(self, app):
        """validation_error_response 문자열 에러 테스트"""
        with app.app_context():
            # Given: 문자열 에러 메시지
            error = "필수 필드가 누락되었습니다"
            
            # When: validation_error_response 호출
            response = ResponseHelper.validation_error_response(error)
            
            # Then: 응답 검증
            assert response.status_code == 400
            
            response_data = json.loads(response.data)
            assert response_data["success"] is False
            assert response_data["message"] == error
            assert response_data["error_code"] == "VALIDATION_ERROR"
            assert "errors" not in response_data

    def test_validation_error_response_list(self, app):
        """validation_error_response 리스트 에러 테스트"""
        with app.app_context():
            # Given: 리스트 에러 메시지
            errors = [
                "이름은 필수입니다",
                "이메일 형식이 올바르지 않습니다",
                "비밀번호는 8자 이상이어야 합니다"
            ]
            
            # When: validation_error_response 호출
            response = ResponseHelper.validation_error_response(errors)
            
            # Then: 응답 검증
            assert response.status_code == 400
            
            response_data = json.loads(response.data)
            assert response_data["success"] is False
            assert response_data["message"] == "; ".join(errors)
            assert response_data["error_code"] == "VALIDATION_ERROR"
            assert response_data["errors"] == errors

    def test_validation_error_response_dict(self, app):
        """validation_error_response 딕셔너리 에러 테스트"""
        with app.app_context():
            # Given: 딕셔너리 에러 메시지
            errors = {
                "name": "이름은 필수입니다",
                "email": "이메일 형식이 올바르지 않습니다",
                "password": "비밀번호는 8자 이상이어야 합니다"
            }
            
            # When: validation_error_response 호출
            response = ResponseHelper.validation_error_response(errors)
            
            # Then: 응답 검증
            assert response.status_code == 400
            
            response_data = json.loads(response.data)
            assert response_data["success"] is False
            assert response_data["message"] == "입력 데이터가 유효하지 않습니다."
            assert response_data["error_code"] == "VALIDATION_ERROR"
            assert response_data["errors"] == errors
