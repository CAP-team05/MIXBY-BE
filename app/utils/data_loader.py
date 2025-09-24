"""
데이터 로딩을 위한 유틸리티 모듈
JSON 파일들을 로드하고 캐싱하는 기능을 제공합니다.
"""

import json
import os
from collections import OrderedDict
from typing import Dict, List, Any, Optional


class DataLoader:
    """JSON 데이터 파일을 로드하고 캐싱하는 클래스"""

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # 현재 파일의 위치를 기준으로 data 디렉토리 경로 설정
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.data_dir = os.path.join(os.path.dirname(current_dir), "data")
        else:
            self.data_dir = data_dir

        self._cache: Dict[str, Any] = {}

    def load_json(self, filename: str, use_ordered_dict: bool = True) -> Any:
        """
        JSON 파일을 로드합니다.

        Args:
            filename: JSON 파일명 (확장자 포함)
            use_ordered_dict: OrderedDict 사용 여부

        Returns:
            로드된 JSON 데이터
        """
        if filename in self._cache:
            return self._cache[filename]

        file_path = os.path.join(self.data_dir, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"JSON 파일을 찾을 수 없습니다: {file_path}")

        try:
            with open(file_path, "r", encoding="UTF-8") as json_file:
                if use_ordered_dict:
                    data = json.load(json_file, object_pairs_hook=OrderedDict)
                else:
                    data = json.load(json_file)

                self._cache[filename] = data
                return data
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 파일 파싱 오류: {filename} - {str(e)}")
        except Exception as e:
            raise Exception(f"파일 로드 오류: {filename} - {str(e)}")

    def get_all_challenges(self) -> List[Dict]:
        """모든 챌린지 데이터를 반환합니다."""
        return self.load_json("allChallenges.json")

    def get_all_drinks(self) -> List[Dict]:
        """모든 음료 데이터를 반환합니다."""
        return self.load_json("allProducts.json")

    def get_all_ingredients(self) -> List[Dict]:
        """모든 재료 데이터를 반환합니다."""
        return self.load_json("allIngredients.json")

    def get_all_recipes(self) -> List[Dict]:
        """모든 레시피 데이터를 반환합니다."""
        return self.load_json("allRecipes.json")

    def get_bases(self) -> List[Dict]:
        """베이스 음료 데이터를 반환합니다."""
        return self.load_json("bases.json")

    def get_recipe_names(self) -> List[Dict]:
        """레시피 이름 데이터를 반환합니다."""
        return self.load_json("recipe_names.json")

    def clear_cache(self):
        """캐시를 초기화합니다."""
        self._cache.clear()

    def reload_data(self, filename: str = None):
        """
        데이터를 다시 로드합니다.

        Args:
            filename: 특정 파일만 다시 로드할 경우 파일명 지정
        """
        if filename:
            if filename in self._cache:
                del self._cache[filename]
        else:
            self.clear_cache()


# 전역 데이터 로더 인스턴스
data_loader = DataLoader()
