# app.py (LangServe 백엔드)
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langserve import add_routes

# FastAPI 앱 생성
app = FastAPI(
    title="LLM 애플리케이션 API",
    version="1.0",
    description="LangChain을 사용한 문서 QA 시스템"
)

# 문서 로딩 및 벡터 DB 설정
loader = TextLoader("./documents/data.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
splits = text_splitter.split_documents(documents)

# 벡터 저장소 생성
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# 프롬프트 템플릿 생성
template = """
당신은 지식이 풍부한 비서입니다. 다음 지식을 바탕으로 질문에 답변해주세요.
컨텍스트: {context}
질문: {question}
답변:
"""
prompt = ChatPromptTemplate.from_template(template)

# 체인 구성
model = ChatOpenAI(model="gpt-4")
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# LangServe로 API 엔드포인트 추가
add_routes(
    app,
    {"qa": chain},
    path="/api"
)

# CORS 설정
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포시 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
