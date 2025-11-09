"""
RAGService 테스트 모듈
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from app.services.rag_service import RAGService


class TestRAGService:
    """RAGService 클래스 테스트"""

    @pytest.fixture
    def mock_dependencies(self, mocker):
        """RAGService 의존성 모킹"""
        # VectorStoreService 모킹
        mock_vector_store = MagicMock()
        mocker.patch("app.services.rag_service.VectorStoreService", return_value=mock_vector_store)

        # EmbeddingGenerator 모킹
        mock_embedding_gen = MagicMock()
        mocker.patch("app.services.rag_service.EmbeddingGenerator", return_value=mock_embedding_gen)

        return mock_vector_store, mock_embedding_gen

    def test_init(self, mock_dependencies):
        """초기화 테스트"""
        # Given: 모킹된 의존성
        mock_vector_store, mock_embedding_gen = mock_dependencies

        # When: RAGService 생성
        service = RAGService()

        # Then: 의존성이 올바르게 초기화됨
        assert service.vector_store == mock_vector_store
        assert service.embedding_gen == mock_embedding_gen
        mock_vector_store.initialize_collection.assert_called_once()

    def test_init_with_custom_directory(self, mocker):
        """커스텀 디렉토리로 초기화 테스트"""
        # Given: 커스텀 디렉토리 설정
        mock_vector_store_class = mocker.patch("app.services.rag_service.VectorStoreService")
        mocker.patch("app.services.rag_service.EmbeddingGenerator")

        custom_dir = "/custom/path/vector_db"

        # When: 커스텀 디렉토리로 RAGService 생성
        service = RAGService(persist_directory=custom_dir)

        # Then: VectorStoreService가 커스텀 디렉토리로 초기화됨
        mock_vector_store_class.assert_called_once_with(persist_directory=custom_dir)

    def test_recipe_to_text(self, mock_dependencies):
        """레시피를 텍스트로 변환하는 테스트"""
        # Given: 테스트 레시피 데이터
        recipe = {
            "korean_name": "진토닉",
            "english_name": "Gin Tonic",
            "tag1": "상쾌함",
            "tag2": "클래식",
            "ingredients": [{"name": "진", "code": "300"}, {"name": "토닉워터", "code": "600"}],
            "instructions": ["하이볼 글라스에 얼음을 채운다.", "진을 붓는다."],
        }

        service = RAGService()

        # When: 레시피를 텍스트로 변환
        result = service._recipe_to_text(recipe)

        # Then: 주요 정보가 텍스트로 변환됨
        assert "칵테일 이름: 진토닉" in result
        assert "영문명: Gin Tonic" in result
        assert "태그: 상쾌함, 클래식" in result
        assert "재료: 진, 토닉워터" in result
        assert "만드는 방법: 하이볼 글라스에 얼음을 채운다. 진을 붓는다." in result

    def test_recipe_to_text_minimal_data(self, mock_dependencies):
        """최소 데이터로 레시피 텍스트 변환 테스트"""
        # Given: 최소한의 레시피 데이터
        recipe = {"korean_name": "테스트 칵테일"}

        service = RAGService()

        # When: 레시피를 텍스트로 변환
        result = service._recipe_to_text(recipe)

        # Then: 있는 정보만 포함됨
        assert "칵테일 이름: 테스트 칵테일" in result
        assert "영문명: " in result  # 빈 값
        assert "태그: , " in result  # 빈 값

    def test_initialize_vector_db_already_initialized(self, mock_dependencies):
        """이미 초기화된 벡터 DB 테스트"""
        # Given: 이미 초기화된 벡터 DB
        mock_vector_store, _ = mock_dependencies
        mock_vector_store.is_initialized.return_value = True
        mock_vector_store.count.return_value = 100

        service = RAGService()

        # When: 초기화 시도
        service.initialize_vector_db()

        # Then: 스킵되고 로드만 수행됨
        mock_vector_store.is_initialized.assert_called_once()
        mock_vector_store.count.assert_called_once()
        # clear나 add_documents가 호출되지 않음
        mock_vector_store.clear.assert_not_called()
        mock_vector_store.add_documents.assert_not_called()

    def test_initialize_vector_db_force_rebuild(self, mock_dependencies, mocker):
        """강제 재구축 테스트"""
        # Given: force_rebuild=True 및 모킹 데이터
        mock_vector_store, mock_embedding_gen = mock_dependencies

        # is_initialized는 clear 후에 False 반환 (재구축 필요)
        mock_vector_store.is_initialized.return_value = False

        # 테스트 레시피 데이터
        mock_recipes = [
            {
                "code": "300600",
                "korean_name": "진토닉",
                "english_name": "Gin Tonic",
                "tag1": "상쾌함",
                "tag2": "클래식",
                "ingredients": [{"name": "진"}, {"name": "토닉워터"}],
            }
        ]
        mocker.patch("app.services.rag_service.data_loader.get_all_recipes", return_value=mock_recipes)

        # 임베딩 생성 모킹
        mock_embeddings = [[0.1, 0.2, 0.3]]
        mock_embedding_gen.generate_batch.return_value = mock_embeddings

        service = RAGService()

        # When: force_rebuild=True로 초기화
        service.initialize_vector_db(force_rebuild=True)

        # Then: clear가 호출되고 재구축됨
        mock_vector_store.clear.assert_called_once()
        mock_embedding_gen.generate_batch.assert_called_once()
        mock_vector_store.add_documents.assert_called_once()

    def test_initialize_vector_db_new_database(self, mock_dependencies, mocker):
        """새 데이터베이스 생성 테스트"""
        # Given: 초기화되지 않은 벡터 DB
        mock_vector_store, mock_embedding_gen = mock_dependencies
        mock_vector_store.is_initialized.return_value = False

        # 테스트 레시피 데이터
        mock_recipes = [
            {
                "code": "300600",
                "korean_name": "진토닉",
                "english_name": "Gin Tonic",
                "tag1": "상쾌함",
                "tag2": "클래식",
                "ingredients": [{"name": "진"}, {"name": "토닉워터"}],
                "instructions": ["글라스에 얼음을 채운다."],
            },
            {
                "code": "500601",
                "korean_name": "모히또",
                "english_name": "Mojito",
                "tag1": "청량",
                "tag2": "민트",
                "ingredients": [{"name": "럼"}, {"name": "민트"}],
                "instructions": ["민트를 으깬다."],
            },
        ]
        mocker.patch("app.services.rag_service.data_loader.get_all_recipes", return_value=mock_recipes)

        # 임베딩 생성 모킹
        mock_embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        mock_embedding_gen.generate_batch.return_value = mock_embeddings

        service = RAGService()

        # When: 초기화 실행
        service.initialize_vector_db()

        # Then: 임베딩 생성 및 저장됨
        mock_embedding_gen.generate_batch.assert_called_once()

        # add_documents 호출 검증
        call_args = mock_vector_store.add_documents.call_args
        assert len(call_args.kwargs["documents"]) == 2
        assert len(call_args.kwargs["metadatas"]) == 2
        assert len(call_args.kwargs["ids"]) == 2
        assert call_args.kwargs["ids"] == ["300600", "500601"]
        assert call_args.kwargs["embeddings"] == mock_embeddings

    def test_search_cocktails(self, mock_dependencies):
        """칵테일 검색 테스트"""
        # Given: 검색 결과 모킹
        mock_vector_store, mock_embedding_gen = mock_dependencies

        # 쿼리 임베딩 모킹
        query_embedding = [0.7, 0.8, 0.9]
        mock_embedding_gen.generate.return_value = query_embedding

        # 검색 결과 모킹
        mock_results = {
            "metadatas": [
                [
                    {"code": "300600", "korean_name": "진토닉", "english_name": "Gin Tonic"},
                    {"code": "500601", "korean_name": "모히또", "english_name": "Mojito"},
                ]
            ],
            "distances": [[0.2, 0.3]],
        }
        mock_vector_store.search.return_value = mock_results

        service = RAGService()

        # When: 칵테일 검색
        results = service.search_cocktails(query="상쾌한 칵테일", n_results=5)

        # Then: 검색이 수행되고 결과가 반환됨
        mock_embedding_gen.generate.assert_called_once_with("상쾌한 칵테일")
        mock_vector_store.search.assert_called_once_with(query_embedding=query_embedding, n_results=5, where=None)

        assert len(results) == 2
        assert results[0]["code"] == "300600"
        assert results[0]["korean_name"] == "진토닉"
        assert "similarity_score" in results[0]
        assert results[0]["similarity_score"] == 0.8  # 1 - 0.2

    def test_search_cocktails_with_filter(self, mock_dependencies):
        """필터링 적용 검색 테스트"""
        # Given: 필터링 조건 및 검색 결과 모킹
        mock_vector_store, mock_embedding_gen = mock_dependencies

        query_embedding = [0.7, 0.8, 0.9]
        mock_embedding_gen.generate.return_value = query_embedding

        mock_results = {"metadatas": [[{"code": "300600", "korean_name": "진토닉"}]], "distances": [[0.15]]}
        mock_vector_store.search.return_value = mock_results

        service = RAGService()

        # When: cocktail_list 필터링 적용하여 검색
        cocktail_list = ["300600", "400600", "500600"]
        results = service.search_cocktails(query="상쾌한 칵테일", n_results=10, cocktail_list=cocktail_list)

        # Then: 필터가 적용되어 검색됨
        call_args = mock_vector_store.search.call_args
        assert call_args.kwargs["where"] == {"code": {"$in": cocktail_list}}

        assert len(results) == 1
        assert results[0]["similarity_score"] == 0.85  # 1 - 0.15
