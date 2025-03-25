# scripts/ingest.py - 데이터 인제스트 스크립트
import os
import glob
from typing import List, Optional
from rag.document_loader import load_document, split_documents
from rag.vectorstore import add_documents, get_vectorstore
from app.config import get_settings

def process_file(file_path: str, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None) -> int:
    """단일 파일 처리 및 벡터 스토어에 인제스트"""
    # 문서 로드
    documents = load_document(file_path)

    # 문서 분할
    chunks = split_documents(documents, chunk_size, chunk_overlap)

    # 벡터 스토어에 추가
    return add_documents(chunks)


def process_directory(directory: str, recursive: bool = True) -> int:
    """디렉토리의 모든 파일 처리"""
    total_chunks = 0

    # 파일 패턴
    file_pattern = os.path.join(directory, "**/*.*" if recursive else "*.*")

    # 모든 파일 반복
    for file_path in glob.glob(file_pattern, recursive=recursive):
        ext = os.path.splitext(file_path)[1].lower()

        # 지원하는 파일 형식인 경우 처리
        if ext in {".txt", ".pdf", ".csv", ".md", ".docx"}:
            try:
                chunks_added = process_file(file_path)
                total_chunks += chunks_added
                print(f"처리 완료: {file_path} ({chunks_added} 청크)")
            except Exception as e:
                print(f"처리 오류: {file_path} - {str(e)}")

    return total_chunks


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(description="문서 처리 및 벡터 스토어 인제스트")
    parser.add_argument("--dir", help="처리할 디렉토리 경로", default="./data/raw/documents")
    parser.add_argument("--file", help="처리할 단일 파일 경로")
    parser.add_argument("--chunk-size", type=int, help="청크 크기")
    parser.add_argument("--chunk-overlap", type=int, help="청크 겹침")

    args = parser.parse_args()

    # 벡터 스토어 초기화 (필요 시)
    get_vectorstore()

    if args.file:
        # 단일 파일 처리
        chunks = process_file(args.file, args.chunk_size, args.chunk_overlap)
        print(f"파일 처리 완료: {chunks} 청크 추가됨")
    elif args.dir:
        # 디렉토리 처리
        chunks = process_directory(args.dir)
        print(f"디렉토리 처리 완료: {chunks} 청크 추가됨")
    else:
        print("처리할 파일이나 디렉토리를 지정해주세요.")


if __name__ == "__main__":
    main()
