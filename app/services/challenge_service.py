"""
챌린지 관련 비즈니스 로직을 처리하는 서비스 모듈
"""

from typing import List, Dict, Optional, Any
from app.utils.data_loader import data_loader


class ChallengeService:
    """챌린지 데이터 처리를 담당하는 서비스 클래스"""

    def __init__(self):
        self.data_loader = data_loader

    def get_all_challenges(self) -> List[Dict]:
        """모든 챌린지 데이터를 반환합니다."""
        return self.data_loader.get_all_challenges()

    def get_challenge_by_id(self, challenge_id: str) -> Optional[Dict]:
        """
        ID로 챌린지를 검색합니다.

        Args:
            challenge_id: 챌린지 ID

        Returns:
            찾은 챌린지 데이터 또는 None
        """
        if not challenge_id or not challenge_id.strip():
            return None

        all_challenges = self.get_all_challenges()

        for challenge in all_challenges:
            if str(challenge.get("id")) == str(challenge_id):
                return challenge

        return None

    def search_by_title(self, keyword: str) -> List[Dict]:
        """
        제목으로 챌린지를 검색합니다.

        Args:
            keyword: 검색할 키워드

        Returns:
            검색 결과 리스트
        """
        if not keyword or not keyword.strip():
            return []

        all_challenges = self.get_all_challenges()
        results = []

        for challenge in all_challenges:
            # 'title' 또는 'name' 필드를 확인
            title = challenge.get("title", challenge.get("name", "")).lower()
            if keyword.lower() in title:
                if challenge not in results:
                    results.append(challenge)

        return results

    def search_by_difficulty(self, difficulty: str) -> List[Dict]:
        """
        난이도로 챌린지를 검색합니다.

        Args:
            difficulty: 난이도

        Returns:
            검색 결과 리스트
        """
        if not difficulty or not difficulty.strip():
            return []

        all_challenges = self.get_all_challenges()
        results = []

        for challenge in all_challenges:
            challenge_difficulty = challenge.get("difficulty", "").lower()
            if difficulty.lower() == challenge_difficulty:
                results.append(challenge)

        return results

    def get_challenge_categories(self) -> List[str]:
        """
        사용 가능한 모든 챌린지 카테고리를 반환합니다.

        Returns:
            챌린지 카테고리 리스트
        """
        all_challenges = self.get_all_challenges()
        categories = set()

        for challenge in all_challenges:
            category = challenge.get("category")
            if category:
                categories.add(category)

        return sorted(list(categories))

    def get_challenge_difficulties(self) -> List[str]:
        """
        사용 가능한 모든 챌린지 난이도를 반환합니다.

        Returns:
            챌린지 난이도 리스트
        """
        all_challenges = self.get_all_challenges()
        difficulties = set()

        for challenge in all_challenges:
            difficulty = challenge.get("difficulty")
            if difficulty:
                difficulties.add(difficulty)

        return sorted(list(difficulties))

    def validate_challenge_data(self, challenge_data: Dict) -> List[str]:
        """
        챌린지 데이터의 유효성을 검증합니다.

        Args:
            challenge_data: 검증할 챌린지 데이터

        Returns:
            에러 메시지 리스트 (에러가 없으면 빈 리스트)
        """
        errors = []

        # 필수 필드 검증
        required_fields = ["id", "title", "description"]
        for field in required_fields:
            if field not in challenge_data or not challenge_data[field]:
                errors.append(f"{field} 필드는 필수입니다.")

        # ID 중복 검증
        if "id" in challenge_data:
            existing_challenge = self.get_challenge_by_id(challenge_data["id"])
            if existing_challenge:
                errors.append(f"ID '{challenge_data['id']}'는 이미 존재합니다.")

        return errors


# 전역 챌린지 서비스 인스턴스
challenge_service = ChallengeService()
