"""
레시피 관련 API 라우트
"""

from flask import Blueprint, send_from_directory, current_app
from app.services.recipe_service import recipe_service
from app.utils.response_helper import response_helper
import os

# Blueprint 생성
recipe_bp = Blueprint("recipes", __name__, url_prefix="/recipe")


@recipe_bp.route("/all")
def get_all_recipes():
    """모든 레시피 데이터를 반환합니다."""
    try:
        recipes = recipe_service.get_all_recipes()
        return response_helper.json_response(recipes)
    except Exception as e:
        return response_helper.error_response(
            message="레시피 데이터를 가져오는 중 오류가 발생했습니다.", status_code=500
        )


@recipe_bp.route("/image=<code>")
def get_recipe_image(code):
    """레시피 이미지를 반환합니다."""
    try:
        static_dir = current_app.static_folder
        image_path = os.path.join(static_dir, "recipes", f"{code}.png")

        if os.path.exists(image_path):
            return send_from_directory(os.path.join(static_dir, "recipes"), f"{code}.png")
        else:
            return response_helper.not_found_response("이미지")
    except Exception as e:
        return response_helper.error_response(message="이미지를 가져오는 중 오류가 발생했습니다.", status_code=500)


@recipe_bp.route("/name=<name>")
def get_recipe_by_name(name):
    """이름으로 레시피를 검색합니다."""
    try:
        recipes = recipe_service.search_by_name(name)
        return response_helper.search_response(results=recipes, query=name)
    except Exception as e:
        return response_helper.error_response(message="레시피 검색 중 오류가 발생했습니다.", status_code=500)


@recipe_bp.route("/code=<code>")
def get_recipe_by_code(code):
    """코드로 레시피를 검색합니다."""
    try:
        recipe = recipe_service.search_by_code(code)
        if recipe:
            return response_helper.json_response(recipe)
        else:
            return response_helper.not_found_response("레시피")
    except Exception as e:
        return response_helper.error_response(message="레시피 검색 중 오류가 발생했습니다.", status_code=500)


@recipe_bp.route("/with=<codes>")
def get_recipes_with_ingredients(codes):
    """재료 코드들로 만들 수 있는 레시피를 검색합니다."""
    try:
        recipes = recipe_service.search_by_ingredients(codes)
        return response_helper.search_response(results=recipes, query=codes)
    except Exception as e:
        return response_helper.error_response(message="레시피 검색 중 오류가 발생했습니다.", status_code=500)


@recipe_bp.route("/random")
def get_random_recipe():
    """무작위 레시피를 반환합니다."""
    try:
        recipe = recipe_service.get_random_recipe()
        if recipe:
            return response_helper.json_response(recipe)
        else:
            return response_helper.error_response(message="사용 가능한 레시피가 없습니다.", status_code=404)
    except Exception as e:
        return response_helper.error_response(
            message="무작위 레시피를 가져오는 중 오류가 발생했습니다.", status_code=500
        )


@recipe_bp.route("/categories")
def get_recipe_categories():
    """사용 가능한 모든 레시피 카테고리를 반환합니다."""
    try:
        categories = recipe_service.get_recipe_categories()
        return response_helper.json_response(categories)
    except Exception as e:
        return response_helper.error_response(
            message="레시피 카테고리를 가져오는 중 오류가 발생했습니다.", status_code=500
        )


@recipe_bp.route("/difficulty=<difficulty>")
def get_recipes_by_difficulty(difficulty):
    """난이도별 레시피를 반환합니다."""
    try:
        recipes = recipe_service.get_recipes_by_difficulty(difficulty)
        return response_helper.search_response(results=recipes, query=difficulty)
    except Exception as e:
        return response_helper.error_response(message="난이도별 레시피 검색 중 오류가 발생했습니다.", status_code=500)
