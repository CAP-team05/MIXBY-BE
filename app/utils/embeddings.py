"""
OpenAI를 사용한 텍스트 임베딩 생성 유틸리티
"""
from openai import OpenAI
import os
from typing import List, Union
import logging

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """OpenAI를 사용한 임베딩 생성"""

    MODEL = "text-embedding-3-small"
    DIMENSION = 1536

    def __init__(self):
        """초기화 - OpenAI 클라이언트는 lazy initialization"""
        self._client = None

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
