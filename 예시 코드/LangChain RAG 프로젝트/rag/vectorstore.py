# rag/vectorstore.py - 벡터 저장소 관리
import os
from langchain.vectorstores import FAISS, Chroma

try:
    import pinecone
    from langchain.vectorstores import Pinecone

    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False

from app.config import get_settings
from rag.embeddings import get_embeddings

# 벡터 스토어 인스턴스 (싱글톤)
_vectorstore = None


def init_vectorstore():
    """벡터 스토어 초기화 (필요시)"""
    settings = get_settings()
    vector_db = settings.get("vector_db", "FAISS")

    if vector_db == "Pinecone" and PINECONE_AVAILABLE:
        # Pinecone 초기화
        pinecone.init(
            api_key=settings.get("pinecone_api_key", ""),
            environment=settings.get("pinecone_environment", "")
        )

        # 인덱스 존재 확인
        pinecone_index = settings.get("pinecone_index", "")
        if pinecone_index not in pinecone.list_indexes():
            # 차원 가져오기 - OpenAI 임베딩은 1536 차원
            dimension = 1536
            pinecone.create_index(
                name=pinecone_index,
                dimension=dimension,
                metric="cosine"
            )


def get_vectorstore():
    """벡터 스토어 인스턴스 가져오기"""
    global _vectorstore

    if _vectorstore is not None:
        return _vectorstore

    settings = get_settings()
    vector_db = settings.get("vector_db", "FAISS")
    embeddings = get_embeddings()

    # 벡터 DB 유형에 따라 다른 저장소 생성
    if vector_db == "FAISS":
        # FAISS 디렉토리 설정
        faiss_dir = os.path.join("data", "processed", "faiss_index")

        # 저장된 인덱스가 있는지 확인
        if os.path.exists(faiss_dir) and os.path.isdir(faiss_dir) and len(os.listdir(faiss_dir)) > 0:
            _vectorstore = FAISS.load_local(faiss_dir, embeddings)
        else:
            # 빈 인덱스 생성
            _vectorstore = FAISS.from_texts(["초기화 텍스트"], embeddings)

            # 디렉토리 생성
            os.makedirs(faiss_dir, exist_ok=True)

            # 저장
            _vectorstore.save_local(faiss_dir)

    elif vector_db == "Chroma":
        # Chroma 디렉토리 설정
        chroma_dir = settings.get("chroma_directory", os.path.join("data", "processed", "chroma_db"))

        # 디렉토리 확인
        os.makedirs(chroma_dir, exist_ok=True)

        # Chroma DB 생성 또는 로드
        _vectorstore = Chroma(
            persist_directory=chroma_dir,
            embedding_function=embeddings
        )

    elif vector_db == "Pinecone" and PINECONE_AVAILABLE:
        # Pinecone 초기화
        init_vectorstore()

        # Pinecone 인덱스 연결
        _vectorstore = Pinecone.from_existing_index(
            index_name=settings.get("pinecone_index", ""),
            embedding=embeddings,
            text_key="text"
        )

    else:
        # 기본값: FAISS
        faiss_dir = os.path.join("data", "processed", "faiss_index")
        os.makedirs(faiss_dir, exist_ok=True)

        _vectorstore = FAISS.from_texts(["초기화 텍스트"], embeddings)
        _vectorstore.save_local(faiss_dir)

    return _vectorstore


def add_documents(documents):
    """벡터 스토어에 문서 추가"""
    vectorstore = get_vectorstore()
    settings = get_settings()
    vector_db = settings.get("vector_db", "FAISS")

    # 문서 추가
    if vector_db == "FAISS":
        # FAISS는 기존 인덱스에 직접 추가
        vectorstore.add_documents(documents)

        # 인덱스 저장
        faiss_dir = os.path.join("data", "processed", "faiss_index")
        vectorstore.save_local(faiss_dir)

    elif vector_db == "Chroma":
        # Chroma에 문서 추가
        vectorstore.add_documents(documents)

        # 영구 저장
        if hasattr(vectorstore, "persist"):
            vectorstore.persist()

    elif vector_db == "Pinecone" and PINECONE_AVAILABLE:
        # Pinecone에 문서 추가
        vectorstore.add_documents(documents)

    return len(documents)
