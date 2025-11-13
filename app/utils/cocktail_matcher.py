"""
칵테일 이름 매칭 관련 유틸리티
"""

import json
from typing import Dict, Any, List


def match_cocktail_in_json(cocktail_list: str, response_json: str) -> Dict[str, Any]:
    """
    JSON 응답에서 칵테일 이름을 실제 보유 칵테일 목록과 매칭합니다.

    Args:
        cocktail_list: 보유한 칵테일 목록 (쉼표로 구분된 문자열 또는 JSON 배열 문자열)
        response_json: AI의 JSON 응답

    Returns:
        매칭된 칵테일 이름이 포함된 JSON
    """
    try:
        # 보유 칵테일 리스트를 파싱
        available_cocktails = []
        try:
            # JSON 배열로 파싱 시도
            cocktail_data = json.loads(cocktail_list)
            if isinstance(cocktail_data, list):
                # 각 칵테일에서 이름 추출 (korean_name, english_name, 또는 단순 문자열)
                for item in cocktail_data:
                    if isinstance(item, dict):
                        if 'korean_name' in item:
                            available_cocktails.append(item['korean_name'])
                        if 'english_name' in item:
                            available_cocktails.append(item['english_name'])
                    elif isinstance(item, str):
                        available_cocktails.append(item)
        except (json.JSONDecodeError, TypeError):
            # JSON 파싱 실패 시 쉼표로 구분된 문자열로 처리
            available_cocktails = [name.strip() for name in cocktail_list.split(",")]

        # JSON 응답 파싱
        response_data = json.loads(response_json)

        # 추천 목록에서 칵테일 이름 매칭
        if "recommendation" in response_data:
            recommendations = response_data["recommendation"]
            if isinstance(recommendations, list):
                for rec in recommendations:
                    if "name" in rec:
                        matched_name = find_best_match(rec["name"], available_cocktails)
                        if matched_name:
                            rec["name"] = matched_name

        return response_data

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error matching cocktail names: {e}")
        return {"error": "Failed to match cocktail names"}


def find_best_match(target_name: str, available_names: List[str]) -> str:
    """
    대상 이름과 가장 유사한 이름을 찾습니다.
    
    Args:
        target_name: 찾고자 하는 칵테일 이름
        available_names: 사용 가능한 칵테일 이름 목록
        
    Returns:
        가장 유사한 칵테일 이름 또는 원본 이름
    """
    # 정확히 일치하는 경우
    if target_name in available_names:
        return target_name
    
    # 대소문자 무시하고 일치하는 경우
    target_lower = target_name.lower()
    for name in available_names:
        if target_lower == name.lower():
            return name
    
    # 부분 일치하는 경우
    for name in available_names:
        if target_lower in name.lower() or name.lower() in target_lower:
            return name
    
    # 매칭되지 않으면 원본 반환
    return target_name