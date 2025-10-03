"""
CocktailMatcher 유틸리티 테스트
"""

import pytest
import json
from app.utils.cocktail_matcher import match_cocktail_in_json, find_best_match


class TestMatchCocktailInJson:
    """match_cocktail_in_json 함수 테스트"""

    def test_match_cocktail_in_json_exact_match(self):
        """정확히 일치하는 칵테일 이름이 있을 때 매칭되는지 테스트"""
        # Given
        cocktail_list = "Mojito, Margarita, Old Fashioned"
        response_json = json.dumps({
            "recommendation": [
                {"name": "Mojito", "description": "상쾌한 칵테일"},
                {"name": "Margarita", "description": "시원한 칵테일"}
            ]
        })

        # When
        result = match_cocktail_in_json(cocktail_list, response_json)

        # Then
        assert "recommendation" in result
        assert len(result["recommendation"]) == 2
        assert result["recommendation"][0]["name"] == "Mojito"
        assert result["recommendation"][1]["name"] == "Margarita"

    def test_match_cocktail_in_json_no_match(self):
        """매칭되는 칵테일이 없을 때 원본 이름을 유지하는지 테스트"""
        # Given
        cocktail_list = "Mojito, Margarita"
        response_json = json.dumps({
            "recommendation": [
                {"name": "Unknown Cocktail", "description": "알 수 없는 칵테일"}
            ]
        })

        # When
        result = match_cocktail_in_json(cocktail_list, response_json)

        # Then
        assert "recommendation" in result
        assert result["recommendation"][0]["name"] == "Unknown Cocktail"


    def test_match_cocktail_in_json_invalid_json(self):
        """잘못된 JSON 형식일 때 에러를 처리하는지 테스트"""
        # Given
        cocktail_list = "Mojito, Margarita"
        invalid_json = "This is not a valid JSON"

        # When
        result = match_cocktail_in_json(cocktail_list, invalid_json)

        # Then
        assert "error" in result
        assert result["error"] == "Failed to match cocktail names"


class TestFindBestMatch:
    """find_best_match 함수 테스트"""

    def test_find_best_match_exact(self):
        """정확히 일치하는 이름을 찾는지 테스트"""
        # Given
        target_name = "Mojito"
        available_names = ["Mojito", "Margarita", "Old Fashioned"]

        # When
        result = find_best_match(target_name, available_names)

        # Then
        assert result == "Mojito"

    def test_find_best_match_case_insensitive(self):
        """대소문자 무시하고 일치하는 이름을 찾는지 테스트"""
        # Given
        target_name = "mojito"
        available_names = ["Mojito", "Margarita", "Old Fashioned"]

        # When
        result = find_best_match(target_name, available_names)

        # Then
        assert result == "Mojito"

    def test_find_best_match_partial(self):
        """부분 일치하는 이름을 찾는지 테스트"""
        # Given
        target_name = "Classic Mojito"
        available_names = ["Mojito", "Margarita", "Old Fashioned"]

        # When
        result = find_best_match(target_name, available_names)

        # Then
        assert result == "Mojito"

    def test_find_best_match_no_match(self):
        """매칭되는 이름이 없을 때 원본을 반환하는지 테스트"""
        # Given
        target_name = "Unknown Cocktail"
        available_names = ["Mojito", "Margarita", "Old Fashioned"]

        # When
        result = find_best_match(target_name, available_names)

        # Then
        assert result == "Unknown Cocktail"
