# langchain_modules/chains.py - LangChain 체인 구현
from typing import List, Dict, Any
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.config import get_settings
from langchain_modules.prompts import qa_prompt, condense_question_prompt


def get_llm(temperature=None):
    """LLM 인스턴스 생성"""
    settings = get_settings()

    if temperature is None:
        temperature = 0.7  # 기본값

    return ChatOpenAI(
        model=settings.get("llm_model", "gpt-3.5-turbo"),
        temperature=temperature,
        api_key=settings.get("openai_api_key", "")
    )


def get_qa_chain(use_retrieval=True, retriever=None, temperature=None):
    """QA 체인 생성 - RAG 사용 여부에 따라 다른 체인 반환"""
    llm = get_llm(temperature=temperature)

    if use_retrieval and retriever:
        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            condense_question_prompt=condense_question_prompt,
            combine_docs_chain_kwargs={"prompt": qa_prompt},
            return_source_documents=True,
        )
    else:
        # RAG 없이 일반 대화형 체인
        prompt = PromptTemplate(
            input_variables=["chat_history", "question"],
            template="""
            다음은 사용자와의 대화입니다:
            {chat_history}

            사용자 질문: {question}

            정보와 사실에 기반하여 답변해주세요:
            """
        )
        return LLMChain(llm=llm, prompt=prompt)