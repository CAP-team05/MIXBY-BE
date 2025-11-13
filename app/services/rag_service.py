"""
RAG (Retrieval-Augmented Generation) 파이프라인 서비스
"""
from typing import List, Dict, Any, Optional
from app.services.vector_store_service import VectorStoreService
from app.utils.embeddings import EmbeddingGenerator
from app.utils.data_loader import data_loader
import logging

logger = logging.getLogger(__name__)


class RAGService:
    """RAG 파이프라인 서비스"""

    def __init__(self, persist_directory: str = None):
        """초기화

        Args:
            persist_directory: 벡터 DB 저장 경로 (None이면 기본값 사용)
        """
        if persist_directory:
            self.vector_store = VectorStoreService(persist_directory=persist_directory)
        else:
            self.vector_store = VectorStoreService()
        self.embedding_gen = EmbeddingGenerator()
        self.vector_store.initialize_collection()

    def initialize_vector_db(self, force_rebuild: bool = False):
        """칵테일 데이터를 벡터 DB에 로드

        Args:
            force_rebuild: True인 경우 기존 데이터 삭제 후 재구축

        Note:
            - 벡터 DB 파일이 이미 존재하고 데이터가 있으면 로딩만 하고 스킵 (효율성)
            - 파일이 없거나 비어있으면 임베딩 생성 및 저장
            - 앱 시작 시마다 호출되어도 효율적으로 동작
        """
        # force_rebuild가 True면 기존 데이터 삭제
        if force_rebuild:
            logger.info("벡터 DB 강제 재구축 시작")
            self.vector_store.clear()

        # 벡터 DB가 이미 초기화되어 있고 데이터가 있으면 스킵
        if self.vector_store.is_initialized():
            count = self.vector_store.count()
            logger.info(f"벡터 DB 로드 완료: {count}개의 칵테일이 이미 존재합니다. 임베딩 생성 스킵.")
            return

        # 벡터 DB가 비어있거나 존재하지 않으면 임베딩 생성
        logger.info("벡터 DB가 존재하지 않거나 비어있습니다. 임베딩 생성을 시작합니다...")

        # JSON에서 칵테일 데이터 로드
        recipes = data_loader.get_all_recipes()
        logger.info(f"{len(recipes)}개의 칵테일 데이터 로드 완료")

        # 임베딩할 텍스트 생성
        documents = []
        metadatas = []
        ids = []

        for recipe in recipes:
            # 칵테일 정보를 텍스트로 변환
            doc_text = self._recipe_to_text(recipe)
            documents.append(doc_text)

            # 메타데이터 저장 (필터링 및 결과 반환용)
            metadatas.append(
                {
                    "code": recipe.get("code"),
                    "korean_name": recipe.get("korean_name", ""),
                    "english_name": recipe.get("english_name", ""),
                    "tag1": recipe.get("tag1", ""),
                    "tag2": recipe.get("tag2", ""),
                }
            )

            ids.append(str(recipe.get("code")))

        # 임베딩 생성
        logger.info("임베딩 생성 시작")
        embeddings = self.embedding_gen.generate_batch(documents)

        # 벡터 DB에 저장
        logger.info("벡터 DB에 저장 시작")
        self.vector_store.add_documents(documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings)

        logger.info(f"벡터 DB 초기화 완료: {len(recipes)}개 칵테일 저장")

    def search_cocktails(
        self, query: str, n_results: int = 10, cocktail_list: Optional[List[str]] = None, use_mmr: bool = True
    ) -> List[Dict[str, Any]]:
        """유사도 기반 칵테일 검색 (MMR 지원)

        Args:
            query: 검색 쿼리 (예: "상큼하고 달콤한 여름 칵테일")
            n_results: 반환할 결과 수 (기본값: 10)
            cocktail_list: 사용자가 접근 가능한 칵테일 code 리스트 (필터링용)
            use_mmr: MMR(다양성) 사용 여부 (기본값: True)

        Returns:
            검색된 칵테일 메타데이터 리스트 (similarity_score 포함)
        """
        # 쿼리 벡터화 (캐싱 사용 - 자주 사용되는 쿼리 최적화)
        query_embedding = self.embedding_gen.generate_cached(query)

        # 필터 조건 설정
        where = None
        if cocktail_list:
            where = {"code": {"$in": cocktail_list}}

        # MMR 사용 여부에 따라 검색 방식 선택
        if use_mmr:
            # MMR을 사용하여 다양성 있는 검색 결과 반환
            results = self.vector_store.search_with_mmr(
                query_embedding=query_embedding,
                n_results=n_results,
                where=where,
                lambda_mult=0.5,  # 관련성과 다양성의 균형
                fetch_k=min(n_results * 3, 20)  # 초기 검색 결과 수
            )
        else:
            # 기본 유사도 검색
            results = self.vector_store.search(query_embedding=query_embedding, n_results=n_results, where=where)

        # 결과 포매팅
        cocktails = []
        for i, metadata in enumerate(results["metadatas"][0]):
            cocktails.append(
                {
                    **metadata,
                    "similarity_score": 1 - results["distances"][0][i],  # distance를 similarity로 변환
                }
            )

        return cocktails

    def _recipe_to_text(self, recipe: Dict[str, Any]) -> str:
        """칵테일 레시피를 임베딩용 텍스트로 변환

        Args:
            recipe: 칵테일 레시피 딕셔너리

        Returns:
            임베딩용 텍스트 문자열
        """
        # 칵테일의 주요 정보를 자연어 문장으로 구성
        parts = [
            f"칵테일 이름: {recipe.get('korean_name', '')}",
            f"영문명: {recipe.get('english_name', '')}",
            f"태그: {recipe.get('tag1', '')}, {recipe.get('tag2', '')}",
        ]

        # 재료 정보
        ingredients = recipe.get("ingredients", [])
        if ingredients:
            ingredient_names = [ing.get("name", "") for ing in ingredients]
            parts.append(f"재료: {', '.join(ingredient_names)}")

        # 만드는 방법
        instructions = recipe.get("instructions", [])
        if instructions:
            parts.append(f"만드는 방법: {' '.join(instructions)}")

        return " | ".join(parts)
