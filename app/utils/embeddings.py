"""
OpenAI를 사용한 텍스트 임베딩 생성 유틸리티
"""
from openai import OpenAI
import os
from typing import List, Union
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """OpenAI를 사용한 임베딩 생성"""

    MODEL = "text-embedding-3-small"
    DIMENSION = 1536

    def __init__(self):
        """초기화 - OpenAI 클라이언트는 lazy initialization"""
        self._client = None
        self._cache = {}  # 수동 캐시 (LRU 스타일)
        self._cache_max_size = 128

    def _get_client(self) -> OpenAI:
        """OpenAI 클라이언트 lazy initialization

        Returns:
            OpenAI 클라이언트 인스턴스

        Raises:
            ValueError: OPENAI_API_KEY가 설정되지 않은 경우
        """
        if self._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")
            self._client = OpenAI(api_key=api_key)
        return self._client

    def generate(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """텍스트를 임베딩 벡터로 변환

        Args:
            text: 단일 문자열 또는 문자열 리스트

        Returns:
            단일 텍스트의 경우 임베딩 벡터 (List[float])
            리스트의 경우 임베딩 벡터 리스트 (List[List[float]])

        Raises:
            ValueError: API 키가 설정되지 않은 경우
            Exception: OpenAI API 호출 실패 시
        """
        client = self._get_client()

        # 단일 텍스트 처리
        if isinstance(text, str):
            response = client.embeddings.create(model=self.MODEL, input=text)
            return response.data[0].embedding

        # 배치 처리 (리스트)
        response = client.embeddings.create(model=self.MODEL, input=text)
        return [item.embedding for item in response.data]

    def generate_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """대량의 텍스트를 배치 단위로 임베딩 생성

        Args:
            texts: 텍스트 리스트
            batch_size: 배치 크기 (OpenAI API 제한 고려, 기본값 100)

        Returns:
            임베딩 벡터 리스트

        Raises:
            ValueError: API 키가 설정되지 않은 경우
            Exception: OpenAI API 호출 실패 시
        """
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            logger.info(f"임베딩 생성 중: {i}/{len(texts)}")
            embeddings = self.generate(batch)
            all_embeddings.extend(embeddings)

        return all_embeddings

    def generate_cached(self, text: str) -> List[float]:
        """캐싱을 사용하여 텍스트를 임베딩 벡터로 변환

        자주 사용되는 쿼리(감정, 상황, 계절 등)를 캐싱하여 API 호출 감소

        Args:
            text: 문자열 (리스트는 지원하지 않음)

        Returns:
            임베딩 벡터 (List[float])

        Raises:
            ValueError: API 키가 설정되지 않거나, 텍스트가 문자열이 아닌 경우
            Exception: OpenAI API 호출 실패 시
        """
        if not isinstance(text, str):
            raise ValueError("generate_cached()는 문자열만 지원합니다")

        # 캐시 확인
        if text in self._cache:
            logger.debug(f"캐시 히트: {text[:50]}...")
            return self._cache[text]

        # 캐시 미스 - API 호출
        logger.debug(f"캐시 미스: {text[:50]}...")
        embedding = self.generate(text)

        # 캐시 크기 제한 (LRU 방식: 가장 오래된 항목 삭제)
        if len(self._cache) >= self._cache_max_size:
            # 첫 번째 키 삭제 (FIFO - 간단한 구현)
            first_key = next(iter(self._cache))
            del self._cache[first_key]
            logger.debug(f"캐시 용량 초과 - 항목 삭제: {first_key[:50]}...")

        # 캐시에 저장
        self._cache[text] = embedding
        return embedding

    def clear_cache(self):
        """캐시 초기화"""
        self._cache.clear()
        logger.info("임베딩 캐시 초기화 완료")

    def get_cache_info(self) -> dict:
        """캐시 정보 반환

        Returns:
            캐시 크기 및 최대 크기 정보
        """
        return {
            "size": len(self._cache),
            "max_size": self._cache_max_size,
            "hit_rate": "N/A (히트 카운터 미구현)"
        }
