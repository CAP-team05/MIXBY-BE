#!/usr/bin/env python
"""벡터 DB 초기화 스크립트

사용법:
  python scripts/initialize_vector_db.py          # 기존 DB 있으면 스킵
  python scripts/initialize_vector_db.py --force  # 강제 재구축
"""
import sys
import os

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.services.rag_service import RAGService


def main():
    """벡터 DB 초기화 메인 함수"""
    force = "--force" in sys.argv

    print("=" * 60)
    print("MIXBY RAG 벡터 DB 초기화 스크립트")
    print("=" * 60)
    print(f"모드: {'강제 재구축' if force else '스마트 초기화 (기존 DB 재사용)'}")
    print()

    # Flask 앱 생성
    app = create_app()

    with app.app_context():
        # RAG 서비스 초기화
        rag_service = RAGService()

        print(f"벡터 DB 초기화 시작 (force_rebuild={force})...")
        print()

        try:
            # 벡터 DB 초기화
            rag_service.initialize_vector_db(force_rebuild=force)

            print()
            print("=" * 60)
            print("✓ 벡터 DB 초기화 완료!")
            print("=" * 60)
            print(f"  저장 위치: {rag_service.vector_store.persist_directory}")
            print(f"  칵테일 수: {rag_service.vector_store.count()}개")
            print()

        except Exception as e:
            print()
            print("=" * 60)
            print("✗ 벡터 DB 초기화 실패!")
            print("=" * 60)
            print(f"  에러: {str(e)}")
            print()
            sys.exit(1)


if __name__ == "__main__":
    main()
