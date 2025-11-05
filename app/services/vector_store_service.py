"""
ChromaDB를 사용한 벡터 저장소 서비스
"""
import chromadb
from typing import List, Dict, Any, Optional
import os
import logging

logger = logging.getLogger(__name__)


class VectorStoreService:
    """ChromaDB를 사용한 벡터 저장소 서비스"""

    def __init__(self, persist_directory: str = "./app/data/vector_db"):
        """초기화

        Args:
            persist_directory: ChromaDB 데이터 저장 경로
        """
        self.persist_directory = persist_directory
        # PersistentClient 사용 (ChromaDB 최신 버전)
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = None

    def initialize_collection(self, collection_name: str = "cocktails"):
        """컬렉션 초기화 또는 로드

        Args:
            collection_name: 컬렉션 이름 (기본값: "cocktails")

        Returns:
            초기화된 컬렉션 객체
        """
        self.collection = self.client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}  # 코사인 유사도 사용
        )
        return self.collection

    def is_initialized(self) -> bool:
        """벡터 DB가 이미 초기화되어 데이터가 있는지 확인

        Returns:
            True if 벡터 DB 파일이 존재하고 데이터가 있음, False otherwise
        """
        # ChromaDB 데이터 디렉토리 존재 확인
        if not os.path.exists(self.persist_directory):
            return False

        # ChromaDB SQLite 파일 확인 (chroma.sqlite3)
        db_file = os.path.join(self.persist_directory, "chroma.sqlite3")
        if not os.path.exists(db_file):
            return False

        # 컬렉션이 초기화되어 있고 데이터가 있는지 확인
        if self.collection is None:
            return False

        return self.count() > 0

    def add_documents(
        self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str], embeddings: List[List[float]]
    ):
        """문서를 벡터 DB에 추가

        Args:
            documents: 문서 텍스트 리스트
            metadatas: 메타데이터 딕셔너리 리스트
            ids: 문서 ID 리스트
            embeddings: 임베딩 벡터 리스트
        """
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings)

    def search(
        self, query_embedding: List[float], n_results: int = 10, where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """유사도 검색

        Args:
            query_embedding: 쿼리 벡터
            n_results: 반환할 결과 수 (기본값: 10)
            where: 메타데이터 필터링 조건 (선택사항)

        Returns:
            검색 결과 딕셔너리 (ids, distances, metadatas, documents)
        """
        results = self.collection.query(query_embeddings=[query_embedding], n_results=n_results, where=where)
        return results

    def count(self) -> int:
        """저장된 문서 수 반환

        Returns:
            컬렉션 내 문서 수
        """
        return self.collection.count()

    def clear(self):
        """컬렉션 내 모든 데이터 삭제 및 재초기화"""
        collection_name = self.collection.name
        self.client.delete_collection(collection_name)
        self.initialize_collection(collection_name)
