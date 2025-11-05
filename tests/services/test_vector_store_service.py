"""
VectorStoreService 테스트 모듈
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from app.services.vector_store_service import VectorStoreService


class TestVectorStoreService:
    """VectorStoreService 클래스 테스트"""

    @pytest.fixture
    def mock_chromadb_client(self, mocker):
        """ChromaDB 클라이언트 모킹"""
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mocker.patch("app.services.vector_store_service.chromadb.PersistentClient", return_value=mock_client)
        return mock_client, mock_collection

    def test_init(self, mock_chromadb_client):
        """초기화 테스트"""
        # Given: ChromaDB 클라이언트 모킹
        mock_client, _ = mock_chromadb_client

        # When: VectorStoreService 생성
        service = VectorStoreService(persist_directory="./test_db")

        # Then: 속성이 올바르게 설정됨
        assert service.persist_directory == "./test_db"
        assert service.client == mock_client
        assert service.collection is None

    def test_initialize_collection(self, mock_chromadb_client):
        """컬렉션 초기화 테스트"""
        # Given: ChromaDB 클라이언트 모킹
        mock_client, mock_collection = mock_chromadb_client

        service = VectorStoreService()

        # When: 컬렉션 초기화
        result = service.initialize_collection("test_collection")

        # Then: 컬렉션이 생성되고 반환됨
        mock_client.get_or_create_collection.assert_called_once_with(
            name="test_collection", metadata={"hnsw:space": "cosine"}
        )
        assert result == mock_collection
        assert service.collection == mock_collection

    def test_initialize_collection_default_name(self, mock_chromadb_client):
        """컬렉션 기본 이름으로 초기화 테스트"""
        # Given: ChromaDB 클라이언트 모킹
        mock_client, mock_collection = mock_chromadb_client

        service = VectorStoreService()

        # When: 기본 이름으로 컬렉션 초기화
        service.initialize_collection()

        # Then: "cocktails" 이름으로 생성됨
        mock_client.get_or_create_collection.assert_called_once_with(
            name="cocktails", metadata={"hnsw:space": "cosine"}
        )

    def test_is_initialized_directory_not_exists(self, mock_chromadb_client, mocker):
        """디렉토리가 없을 때 is_initialized 테스트"""
        # Given: 디렉토리가 존재하지 않음
        mocker.patch("os.path.exists", return_value=False)

        service = VectorStoreService()
        service.initialize_collection()

        # When: is_initialized 호출
        result = service.is_initialized()

        # Then: False 반환
        assert result is False

    def test_is_initialized_db_file_not_exists(self, mock_chromadb_client, mocker):
        """DB 파일이 없을 때 is_initialized 테스트"""
        # Given: 디렉토리는 있지만 DB 파일이 없음
        def exists_side_effect(path):
            if "chroma.sqlite3" in path:
                return False
            return True

        mocker.patch("os.path.exists", side_effect=exists_side_effect)

        service = VectorStoreService()
        service.initialize_collection()

        # When: is_initialized 호출
        result = service.is_initialized()

        # Then: False 반환
        assert result is False

    def test_is_initialized_collection_not_initialized(self, mock_chromadb_client, mocker):
        """컬렉션이 초기화되지 않았을 때 테스트"""
        # Given: 디렉토리와 DB 파일은 있지만 컬렉션이 None
        mocker.patch("os.path.exists", return_value=True)

        service = VectorStoreService()
        # 컬렉션을 초기화하지 않음

        # When: is_initialized 호출
        result = service.is_initialized()

        # Then: False 반환
        assert result is False

    def test_is_initialized_no_data(self, mock_chromadb_client, mocker):
        """데이터가 없을 때 is_initialized 테스트"""
        # Given: 모든 조건은 충족하지만 데이터가 없음
        mocker.patch("os.path.exists", return_value=True)
        _, mock_collection = mock_chromadb_client
        mock_collection.count.return_value = 0

        service = VectorStoreService()
        service.initialize_collection()

        # When: is_initialized 호출
        result = service.is_initialized()

        # Then: False 반환 (데이터가 없음)
        assert result is False

    def test_is_initialized_success(self, mock_chromadb_client, mocker):
        """정상적으로 초기화되어 데이터가 있을 때 테스트"""
        # Given: 모든 조건 충족 및 데이터 존재
        mocker.patch("os.path.exists", return_value=True)
        _, mock_collection = mock_chromadb_client
        mock_collection.count.return_value = 100

        service = VectorStoreService()
        service.initialize_collection()

        # When: is_initialized 호출
        result = service.is_initialized()

        # Then: True 반환
        assert result is True

    def test_add_documents(self, mock_chromadb_client):
        """문서 추가 테스트"""
        # Given: 테스트 데이터
        _, mock_collection = mock_chromadb_client

        service = VectorStoreService()
        service.initialize_collection()

        documents = ["doc1", "doc2"]
        metadatas = [{"key": "value1"}, {"key": "value2"}]
        ids = ["id1", "id2"]
        embeddings = [[0.1, 0.2], [0.3, 0.4]]

        # When: 문서 추가
        service.add_documents(documents, metadatas, ids, embeddings)

        # Then: collection.add가 호출됨
        mock_collection.add.assert_called_once_with(
            documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings
        )

    def test_search(self, mock_chromadb_client):
        """검색 테스트"""
        # Given: ChromaDB 검색 결과 모킹
        _, mock_collection = mock_chromadb_client
        mock_results = {"ids": [["id1", "id2"]], "distances": [[0.1, 0.2]], "metadatas": [[{}, {}]]}
        mock_collection.query.return_value = mock_results

        service = VectorStoreService()
        service.initialize_collection()

        query_embedding = [0.5, 0.6]

        # When: 검색 실행
        result = service.search(query_embedding, n_results=5)

        # Then: 검색 결과가 반환됨
        mock_collection.query.assert_called_once_with(
            query_embeddings=[query_embedding], n_results=5, where=None
        )
        assert result == mock_results

    def test_search_with_filter(self, mock_chromadb_client):
        """필터링 검색 테스트"""
        # Given: 필터링 조건 설정
        _, mock_collection = mock_chromadb_client
        mock_results = {"ids": [["id1"]], "distances": [[0.1]]}
        mock_collection.query.return_value = mock_results

        service = VectorStoreService()
        service.initialize_collection()

        query_embedding = [0.5, 0.6]
        where_filter = {"category": "롱 드링크"}

        # When: 필터링 검색 실행
        result = service.search(query_embedding, n_results=10, where=where_filter)

        # Then: 필터가 적용된 검색이 실행됨
        mock_collection.query.assert_called_once_with(
            query_embeddings=[query_embedding], n_results=10, where=where_filter
        )
        assert result == mock_results

    def test_count(self, mock_chromadb_client):
        """문서 수 카운트 테스트"""
        # Given: 컬렉션에 문서가 있음
        _, mock_collection = mock_chromadb_client
        mock_collection.count.return_value = 42

        service = VectorStoreService()
        service.initialize_collection()

        # When: count 호출
        result = service.count()

        # Then: 문서 수가 반환됨
        assert result == 42

    def test_clear(self, mock_chromadb_client):
        """데이터 삭제 및 재초기화 테스트"""
        # Given: 컬렉션이 존재
        mock_client, mock_collection = mock_chromadb_client
        mock_collection.name = "test_collection"

        service = VectorStoreService()
        service.initialize_collection("test_collection")

        # When: clear 호출
        service.clear()

        # Then: 컬렉션이 삭제되고 재생성됨
        mock_client.delete_collection.assert_called_once_with("test_collection")
        # get_or_create_collection이 2번 호출됨 (initialize + clear)
        assert mock_client.get_or_create_collection.call_count == 2
