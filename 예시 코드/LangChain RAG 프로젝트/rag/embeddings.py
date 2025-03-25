# rag/embeddings.py - 임베딩 모듈
from langchain_openai import OpenAIEmbeddings
from app.config import get_settings


def get_embeddings():
    """OpenAI 임베딩 모델 인스턴스 반환"""
    settings = get_settings()

    return OpenAIEmbeddings(
        model=settings.get("embedding_model", "text-embedding-ada-002"),
        api_key=settings.get("openai_api_key", "")
    )
