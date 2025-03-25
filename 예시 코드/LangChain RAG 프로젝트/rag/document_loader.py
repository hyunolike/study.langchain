# rag/document_loader.py - 문서 로드 및 처리
import os
from typing import List, Optional
from langchain.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    UnstructuredMarkdownLoader,
    Docx2txtLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import get_settings

# 지원하는 확장자 및 로더 매핑
LOADER_MAPPING = {
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
    ".csv": CSVLoader,
    ".md": UnstructuredMarkdownLoader,
    ".docx": Docx2txtLoader,
}


def load_document(file_path: str) -> List:
    """단일 문서 로드"""
    ext = os.path.splitext(file_path)[1].lower()

    if ext not in LOADER_MAPPING:
        raise ValueError(f"지원하지 않는 파일 형식입니다: {ext}")

    try:
        loader = LOADER_MAPPING[ext](file_path)
        documents = loader.load()

        # 메타데이터 추가
        for doc in documents:
            if "source" not in doc.metadata:
                doc.metadata["source"] = file_path
            if "title" not in doc.metadata:
                doc.metadata["title"] = os.path.basename(file_path)

        return documents
    except Exception as e:
        raise Exception(f"문서 로드 중 오류가 발생했습니다: {str(e)}")


def split_documents(documents: List, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None) -> List:
    """문서를 청크로 분할"""
    settings = get_settings()

    # 설정에서 청크 크기와 겹침 가져오기 (지정된 값이 없는 경우)
    if chunk_size is None:
        chunk_size = settings.get("chunk_size", 1000)

    if chunk_overlap is None:
        chunk_overlap = settings.get("chunk_overlap", 100)

    # 텍스트 분할기 생성
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    # 문서 분할
    chunks = text_splitter.split_documents(documents)
    return chunks