"""
EmbeddingGenerator 유틸리티 테스트
"""

import pytest
from unittest.mock import Mock, MagicMock
from app.utils.embeddings import EmbeddingGenerator


class TestEmbeddingGenerator:
    """EmbeddingGenerator 클래스 테스트"""

    def test_init(self):
        """초기화 테스트"""
        # Given & When: EmbeddingGenerator 생성
        generator = EmbeddingGenerator()

        # Then: 클라이언트가 lazy initialization되어 None
        assert generator._client is None

    def test_get_client_success(self, mocker):
        """OpenAI 클라이언트 정상 초기화 테스트"""
        # Given: API 키 설정
        mocker.patch("os.getenv", return_value="test-api-key")
        mock_openai = mocker.patch("app.utils.embeddings.OpenAI")

        generator = EmbeddingGenerator()

        # When: 클라이언트 가져오기
        client = generator._get_client()

        # Then: OpenAI 클라이언트가 생성됨
        mock_openai.assert_called_once_with(api_key="test-api-key")
        assert client is not None

    def test_get_client_no_api_key(self, mocker):
        """API 키 없을 때 에러 발생 테스트"""
        # Given: API 키 미설정
        mocker.patch("os.getenv", return_value=None)

        generator = EmbeddingGenerator()

        # When & Then: ValueError 발생
        with pytest.raises(ValueError, match="OPENAI_API_KEY가 설정되지 않았습니다"):
            generator._get_client()

    def test_generate_single_text(self, mocker):
        """단일 텍스트 임베딩 생성 테스트"""
        # Given: API 키 및 모킹 설정
        mocker.patch("os.getenv", return_value="test-api-key")

        # OpenAI 응답 모킹
        mock_embedding = [0.1, 0.2, 0.3]
        mock_response = Mock()
        mock_response.data = [Mock(embedding=mock_embedding)]

        mock_client = MagicMock()
        mock_client.embeddings.create.return_value = mock_response

        mocker.patch("app.utils.embeddings.OpenAI", return_value=mock_client)

        generator = EmbeddingGenerator()

        # When: 단일 텍스트 임베딩 생성
        result = generator.generate("test text")

        # Then: 임베딩 벡터 반환
        assert result == mock_embedding
        mock_client.embeddings.create.assert_called_once_with(
            model=EmbeddingGenerator.MODEL, input="test text"
        )

    def test_generate_batch_texts(self, mocker):
        """배치 텍스트 임베딩 생성 테스트"""
        # Given: API 키 및 모킹 설정
        mocker.patch("os.getenv", return_value="test-api-key")

        # OpenAI 응답 모킹
        mock_embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        mock_response = Mock()
        mock_response.data = [Mock(embedding=emb) for emb in mock_embeddings]

        mock_client = MagicMock()
        mock_client.embeddings.create.return_value = mock_response

        mocker.patch("app.utils.embeddings.OpenAI", return_value=mock_client)

        generator = EmbeddingGenerator()

        # When: 배치 텍스트 임베딩 생성
        texts = ["text 1", "text 2"]
        result = generator.generate(texts)

        # Then: 임베딩 벡터 리스트 반환
        assert result == mock_embeddings
        mock_client.embeddings.create.assert_called_once_with(model=EmbeddingGenerator.MODEL, input=texts)

    def test_generate_batch_with_batch_size(self, mocker):
        """generate_batch 메서드 배치 크기 단위 처리 테스트"""
        # Given: API 키 및 모킹 설정
        mocker.patch("os.getenv", return_value="test-api-key")

        # OpenAI 응답 모킹 (배치마다 다른 응답)
        def create_mock_response(texts):
            embeddings = [[float(i)] * 3 for i in range(len(texts))]
            mock_response = Mock()
            mock_response.data = [Mock(embedding=emb) for emb in embeddings]
            return mock_response

        mock_client = MagicMock()
        mock_client.embeddings.create.side_effect = lambda model, input: create_mock_response(input)

        mocker.patch("app.utils.embeddings.OpenAI", return_value=mock_client)

        generator = EmbeddingGenerator()

        # When: 5개 텍스트를 batch_size=2로 처리
        texts = ["text 0", "text 1", "text 2", "text 3", "text 4"]
        result = generator.generate_batch(texts, batch_size=2)

        # Then: 모든 텍스트에 대한 임베딩 생성
        assert len(result) == 5
        # 3번의 API 호출 (2+2+1)
        assert mock_client.embeddings.create.call_count == 3

    def test_generate_api_failure(self, mocker):
        """OpenAI API 호출 실패 시 에러 전파 테스트"""
        # Given: API 키 설정 및 API 실패 모킹
        mocker.patch("os.getenv", return_value="test-api-key")

        mock_client = MagicMock()
        mock_client.embeddings.create.side_effect = Exception("API Error")

        mocker.patch("app.utils.embeddings.OpenAI", return_value=mock_client)

        generator = EmbeddingGenerator()

        # When & Then: Exception 발생
        with pytest.raises(Exception, match="API Error"):
            generator.generate("test text")

    def test_model_and_dimension_constants(self):
        """모델 및 차원 상수 테스트"""
        # Then: 상수 확인
        assert EmbeddingGenerator.MODEL == "text-embedding-3-small"
        assert EmbeddingGenerator.DIMENSION == 1536
