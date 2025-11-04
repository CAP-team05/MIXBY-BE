"""
재료 관련 라우트
"""

import json
import os
from flask import Blueprint
from app.utils.response_helper import response_helper

ingredient_bp = Blueprint("ingredient", __name__)


def load_ingredients():
    """
    allIngredients.json 파일에서 재료 데이터를 로드합니다.

    Returns:
        list: 재료 목록
    """
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        'allIngredients.json'
    )

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"재료 데이터 파일을 찾을 수 없습니다: {json_path}")
    except json.JSONDecodeError:
        raise ValueError("재료 데이터 파일의 형식이 올바르지 않습니다.")


@ingredient_bp.route("/ingredient/")
def get_ingredients():
    """
    모든 재료 목록을 반환합니다.

    Returns:
        JSON 응답: 재료 목록
    """
    try:
        ingredients = load_ingredients()
        return response_helper.success_response(
            data={"ingredients": ingredients},
            message="재료 목록을 성공적으로 조회했습니다."
        )
    except Exception as e:
        return response_helper.error_response(
            message=f"재료 목록 조회 중 오류가 발생했습니다: {str(e)}",
            status_code=500,
            error_code="INGREDIENT_LOAD_ERROR"
        )


@ingredient_bp.route("/ingredient/all")
def get_all_ingredients():
    """
    모든 재료 목록을 반환합니다. (/ingredient/와 동일)

    Returns:
        JSON 응답: 재료 목록
    """
    try:
        ingredients = load_ingredients()
        return response_helper.success_response(
            data={"ingredients": ingredients},
            message="재료 목록을 성공적으로 조회했습니다."
        )
    except Exception as e:
        return response_helper.error_response(
            message=f"재료 목록 조회 중 오류가 발생했습니다: {str(e)}",
            status_code=500,
            error_code="INGREDIENT_LOAD_ERROR"
        )
