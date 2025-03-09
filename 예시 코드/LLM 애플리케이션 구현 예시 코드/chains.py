# chains.py (LangChain 고급 체인 구현)
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class DocumentQAChain:
    """문서 검색 및 질의응답을 위한 고급 체인 클래스"""
    
    def __init__(self, docs_path, openai_api_key):
        """체인 초기화"""
        self.openai_api_key = openai_api_key
        self.docs_path = docs_path
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 스트리밍 콜백 설정
        self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        
        # 벡터 스토어 및 검색기 초기화
        self.vectorstore = self._setup_vectorstore()
        self.retriever = self._setup_advanced_retriever()
        
        # QA 체인 설정
        self.qa_chain = self._setup_qa_chain()
    
    def _setup_vectorstore(self):
        """벡터 저장소 설정"""
        # 이미 생성된 벡터 스토어가 있는지 확인
        try:
            return Chroma(
                persist_directory=f"{self.docs_path}/chroma_db",
                embedding_function=OpenAIEmbeddings(openai_api_key=self.openai_api_key)
            )
        except:
            # 새로운 벡터 스토어 생성 로직 (실제 구현에서는 더 상세하게)
            print("기존 벡터 스토어를 찾을 수 없습니다. 새로 생성이 필요합니다.")
            return None
    
    def _setup_advanced_retriever(self):
        """고급 검색기 설정 (컨텍스트 압축 포함)"""
        base_retriever = self.vectorstore.as_retriever(
            search_type="mmr",  # Maximum Marginal Relevance
            search_kwargs={"k": 5, "fetch_k": 10}
        )
        
        # LLM 기반 추출기로 검색 결과 압축
        llm = ChatOpenAI(temperature=0, openai_api_key=self.openai_api_key)
        compressor = LLMChainExtractor.from_llm(llm)
        
        # 컨텍스트 압축 검색기
        return ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )
    
    def _setup_qa_chain(self):
        """QA 체인 설정"""
        # 프롬프트 템플릿
        prompt_template = """
        다음 대화 및 질문을 고려하여, 제공된 컨텍스트를 바탕으로 질문에 답변해주세요.
        
        대화 내역: {chat_history}
        컨텍스트: {context}
        질문: {question}
        
        답변:
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["chat_history", "context", "question"]
        )
        
        # LLM 설정
        llm = ChatOpenAI(
            temperature=0.2,
            openai_api_key=self.openai_api_key,
            streaming=True,
            callback_manager=self.callback_manager
        )
        
        # QA 체인 구성
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": PROMPT,
                "memory": self.memory
            }
        )
    
    def query(self, question):
        """질문에 대한 응답 생성"""
        try:
            result = self.qa_chain({"query": question})
            return {
                "answer": result["result"],
                "sources": [doc.metadata for doc in result["source_documents"]],
                "success": True
            }
        except Exception as e:
            return {
                "answer": f"오류가 발생했습니다: {str(e)}",
                "sources": [],
                "success": False
            }
    
    def reset_memory(self):
        """대화 기록 초기화"""
        self.memory.clear()
        return {"status": "memory_cleared"}
