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
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        return results

    def search_with_mmr(
        self,
        query_embedding: List[float],
        n_results: int = 10,
        where: Optional[Dict[str, Any]] = None,
        lambda_mult: float = 0.5,
        fetch_k: int = 20
    ) -> Dict[str, Any]:
        """MMR(Maximal Marginal Relevance)을 사용한 다양성 검색

        Args:
            query_embedding: 쿼리 벡터
            n_results: 최종 반환할 결과 수
            where: 메타데이터 필터링 조건
            lambda_mult: 관련성과 다양성의 균형 (0=최대 다양성, 1=최대 관련성, 기본값=0.5)
            fetch_k: 초기 검색할 문서 수 (n_results보다 커야 함)

        Returns:
            MMR 알고리즘이 적용된 검색 결과
        """
        import numpy as np

        # 더 많은 결과를 먼저 가져옴
        initial_results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(fetch_k, self.count()),
            where=where,
            include=["metadatas", "documents", "distances", "embeddings"]
        )

        if (not initial_results.get("embeddings") or
            not initial_results["embeddings"] or
            len(initial_results["embeddings"][0]) == 0):
            return initial_results

        # MMR 알고리즘 적용
        embeddings = np.array(initial_results["embeddings"][0])
        query_emb = np.array(query_embedding)

        # 쿼리와의 유사도 계산 (코사인 유사도)
        query_similarities = 1 - np.array(initial_results["distances"][0])

        selected_indices = []
        remaining_indices = list(range(len(embeddings)))

        # 첫 번째 문서: 쿼리와 가장 유사한 것 선택
        first_idx = remaining_indices[np.argmax(query_similarities)]
        selected_indices.append(first_idx)
        remaining_indices.remove(first_idx)

        # 나머지 문서 선택
        while len(selected_indices) < min(n_results, len(embeddings)) and remaining_indices:
            selected_embeddings = embeddings[selected_indices]

            mmr_scores = []
            for idx in remaining_indices:
                # 쿼리와의 관련성
                relevance = query_similarities[idx]

                # 이미 선택된 문서들과의 최대 유사도 (다양성의 역)
                similarities_to_selected = []
                for selected_emb in selected_embeddings:
                    # 코사인 유사도 계산
                    sim = np.dot(embeddings[idx], selected_emb) / (
                        np.linalg.norm(embeddings[idx]) * np.linalg.norm(selected_emb)
                    )
                    similarities_to_selected.append(sim)

                max_similarity = max(similarities_to_selected) if similarities_to_selected else 0

                # MMR 점수 계산
                mmr_score = lambda_mult * relevance - (1 - lambda_mult) * max_similarity
                mmr_scores.append(mmr_score)

            # 최고 MMR 점수를 가진 문서 선택
            best_idx = remaining_indices[np.argmax(mmr_scores)]
            selected_indices.append(best_idx)
            remaining_indices.remove(best_idx)

        # 선택된 인덱스에 해당하는 결과만 반환
        mmr_results = {
            "ids": [[initial_results["ids"][0][i] for i in selected_indices]],
            "distances": [[initial_results["distances"][0][i] for i in selected_indices]],
            "metadatas": [[initial_results["metadatas"][0][i] for i in selected_indices]],
            "documents": [[initial_results["documents"][0][i] for i in selected_indices]]
        }

        return mmr_results

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
