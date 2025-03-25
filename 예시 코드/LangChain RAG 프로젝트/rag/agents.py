# langchain_modules/agents.py - LangChain 에이전트
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.config import get_settings
from rag.retriever import get_retriever
from typing import List, Dict, Any, Optional


class DocumentSearchTool(BaseTool):
    """문서 검색 도구"""
    name = "document_search"
    description = "문서 컬렉션에서 정보를 검색합니다. 질문이나 키워드를 입력하세요."

    def _run(self, query: str) -> str:
        """검색 실행"""
        retriever = get_retriever(k=3)
        docs = retriever.get_relevant_documents(query)

        if not docs:
            return "관련 정보를 찾을 수 없습니다."

        # 검색 결과 포맷팅
        result = "검색 결과:\n\n"
        for i, doc in enumerate(docs, 1):
            result += f"--- 문서 {i} ---\n"
            result += f"출처: {doc.metadata.get('source', '알 수 없음')}\n"
            result += f"내용: {doc.page_content}\n\n"

        return result

    def _arun(self, query: str) -> str:
        """비동기 실행 (현재는 동기 버전 호출)"""
        return self._run(query)


def create_document_agent():
    """문서 기반 에이전트 생성"""
    settings = get_settings()

    # 도구 정의
    tools = [
        DocumentSearchTool(),
    ]

    # LLM 정의
    llm = ChatOpenAI(
        model=settings.get("llm_model", "gpt-3.5-turbo"),
        temperature=0.5,
        api_key=settings.get("openai_api_key", "")
    )

    # 에이전트 프롬프트
    prompt = PromptTemplate.from_template(
        """
        당신은 문서 검색 AI 비서입니다. 사용자의 질문에 답하기 위해 주어진 도구를 사용하세요.

        {tools}

        질문에 답하기 위해 다음 단계를 따르세요:
        1. 사용자 질문을 이해합니다.
        2. 필요한 정보가 있다면 document_search 도구를 사용하여 검색합니다.
        3. 검색 결과를 기반으로 답변을 작성합니다.
        4. 검색 결과에서 명확한 답을 찾을 수 없는 경우, 정직하게 정보가 부족하다고 말합니다.

        사용자 질문: {input}

        {agent_scratchpad}
        """
    )

    # 에이전트 생성
    agent = create_react_agent(llm, tools, prompt)

    # 에이전트 실행기 반환
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5
    )


# 에이전트를 직접 실행하는 함수
def run_document_agent(query: str) -> Dict[str, Any]:
    """문서 에이전트 실행"""
    agent_executor = create_document_agent()
    return agent_executor.invoke({"input": query})