"""
API 응답을 위한 유틸리티 모듈
일관된 JSON 응답 형식을 제공합니다.
"""

import json
from flask import Response, jsonify
from typing import Any, Dict, List, Optional, Union


class ResponseHelper:
    """API 응답을 생성하는 헬퍼 클래스"""

    @staticmethod
    def json_response(data: Any, status_code: int = 200, ensure_ascii: bool = False) -> Response:
        """
        JSON 응답을 생성합니다.

        Args:
            data: 응답 데이터
            status_code: HTTP 상태 코드
            ensure_ascii: ASCII 인코딩 강제 여부

        Returns:
            Flask Response 객체
        """
        response_data = json.dumps(data, indent=4, ensure_ascii=ensure_ascii)
        return Response(response=response_data, status=status_code, mimetype="application/json; charset=utf-8")

    @staticmethod
    def success_response(data: Any, message: str = "성공", status_code: int = 200) -> Response:
        """
        성공 응답을 생성합니다.

        Args:
            data: 응답 데이터
            message: 성공 메시지
            status_code: HTTP 상태 코드

        Returns:
            Flask Response 객체
        """
        response_data = {"success": True, "message": message, "data": data}
        return ResponseHelper.json_response(response_data, status_code)

    @staticmethod
    def error_response(message: str, status_code: int = 400, error_code: str = None) -> Response:
        """
        에러 응답을 생성합니다.

        Args:
            message: 에러 메시지
            status_code: HTTP 상태 코드
            error_code: 에러 코드

        Returns:
            Flask Response 객체
        """
        response_data = {"success": False, "message": message}

        if error_code:
            response_data["error_code"] = error_code

        return ResponseHelper.json_response(response_data, status_code)

    @staticmethod
    def search_response(results: List[Any], total_count: int = None, query: str = None) -> Response:
        """
        검색 결과 응답을 생성합니다.

        Args:
            results: 검색 결과 리스트
            total_count: 전체 결과 수 (None인 경우 results의 길이 사용)
            query: 검색 쿼리

        Returns:
            Flask Response 객체
        """
        if total_count is None:
            total_count = len(results)

        response_data = {"success": True, "total_count": total_count, "results": results}

        if query:
            response_data["query"] = query

        return ResponseHelper.json_response(response_data)

    @staticmethod
    def not_found_response(resource: str = "리소스") -> Response:
        """
        404 Not Found 응답을 생성합니다.

        Args:
            resource: 찾을 수 없는 리소스명

        Returns:
            Flask Response 객체
        """
        return ResponseHelper.error_response(
            message=f"{resource}를 찾을 수 없습니다.", status_code=404, error_code="NOT_FOUND"
        )

    @staticmethod
    def validation_error_response(errors: Union[str, List[str], Dict[str, str]]) -> Response:
        """
        유효성 검증 에러 응답을 생성합니다.

        Args:
            errors: 에러 메시지 (문자열, 리스트 또는 딕셔너리)

        Returns:
            Flask Response 객체
        """
        if isinstance(errors, str):
            message = errors
        elif isinstance(errors, list):
            message = "; ".join(errors)
        else:
            message = "입력 데이터가 유효하지 않습니다."

        response_data = {"success": False, "message": message, "error_code": "VALIDATION_ERROR"}

        if isinstance(errors, (list, dict)):
            response_data["errors"] = errors

        return ResponseHelper.json_response(response_data, 400)


# 전역 응답 헬퍼 인스턴스
response_helper = ResponseHelper()
