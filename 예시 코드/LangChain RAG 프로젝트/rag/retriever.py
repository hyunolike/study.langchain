# rag/retriever.py - 문서 검색기
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from rag.vectorstore import get_vectorstore
from langchain_modules.chains import get_llm


def get_retriever(k=4, use_compression=False):
    """문서 검색기 생성

    Args:
        k: 검색할 문서 수
        use_compression: 컨텍스트 압축 사용 여부

    Returns:
        검색기 인스턴스
    """
    # 벡터 스토어에서 기본 검색기 가져오기
    vectorstore = get_vectorstore()
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    if not use_compression:
        return base_retriever

    # 컨텍스트 압축 검색기 설정
    llm = get_llm(temperature=0.0)  # 압축에는 낮은 온도 사용
    compressor = LLMChainExtractor.from_llm(llm)

    # 압축 검색기 반환
    return ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )

