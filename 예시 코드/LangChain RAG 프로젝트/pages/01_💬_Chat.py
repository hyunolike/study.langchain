# app/pages/01_💬_Chat.py - 채팅 인터페이스
import streamlit as st
import time
from app.utils.session import get_session_state
from app.utils.display import set_page_config, display_message, display_source
from langchain_modules.chains import get_qa_chain
from rag.retriever import get_retriever


def render_chat_interface():
    # 페이지 설정
    set_page_config(page_title="대화형 문서 검색", page_icon="💬")

    st.title("💬 문서 기반 채팅")

    # 사이드바 설정
    with st.sidebar:
        st.header("설정")
        use_rag = st.toggle("RAG 활성화", value=True, help="검색 증강 생성을 사용하여 문서 기반 답변을 생성합니다")

        if use_rag:
            st.subheader("검색 설정")
            top_k = st.slider("참조 문서 수", min_value=1, max_value=10, value=4)
            st.subheader("모델 설정")
            temperature = st.slider("창의성 수준", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

        st.markdown("---")
        if st.button("대화 초기화"):
            st.session_state.messages = []
            st.rerun()

    # 채팅 메시지 표시
    messages = get_session_state("messages", [])
    for message in messages:
        display_message(
            role=message["role"],
            content=message["content"],
            sources=message.get("sources")
        )

    # 메시지 입력
    if prompt := st.chat_input("질문을 입력하세요..."):
        # 사용자 메시지 추가 및 표시
        messages.append({"role": "user", "content": prompt})
        display_message(role="user", content=prompt)

        with st.status("답변 생성 중...") as status:
            try:
                # 채팅 기록 구성
                chat_history = []
                for m in st.session_state.messages[:-1]:  # 마지막 메시지 제외
                    if m["role"] != "system":  # 시스템 메시지 제외
                        chat_history.append(f"{m['role']}: {m['content']}")

                # RAG 활성화 여부에 따라 검색기 가져오기
                retriever = get_retriever(k=top_k) if use_rag else None

                # QA 체인 가져오기
                chain = get_qa_chain(
                    use_retrieval=use_rag,
                    retriever=retriever,
                    temperature=temperature
                )

                status.update(label="문서 검색 중...")

                # 응답 생성
                start_time = time.time()
                result = chain.invoke({
                    "question": prompt,
                    "chat_history": "\n".join(chat_history) if chat_history else ""
                })

                status.update(label="답변 생성 중...")

                # 소스 정보 추출
                sources = []
                if hasattr(result, 'source_documents') and result.source_documents:
                    for doc in result.source_documents:
                        sources.append({
                            "title": doc.metadata.get("title", "문서"),
                            "content": doc.page_content,
                            "score": doc.metadata.get("score", 0.0)
                        })

                # 답변 추출
                answer = result.answer if hasattr(result, 'answer') else result

                # 실행 시간 계산
                execution_time = time.time() - start_time

                status.update(label=f"완료! ({execution_time:.2f}초)")
                time.sleep(0.5)  # UI 상태 업데이트를 위한 짧은 대기

            except Exception as e:
                # 오류 처리
                error_message = f"오류가 발생했습니다: {str(e)}"
                messages.append({
                    "role": "assistant",
                    "content": error_message
                })
                display_message(role="assistant", content=error_message)
                status.update(label="오류 발생", state="error")
                return

        # 어시스턴트 메시지 추가 및 표시
        assistant_message = {
            "role": "assistant",
            "content": answer,
            "sources": sources if sources else None
        }
        messages.append(assistant_message)
        display_message(
            role="assistant",
            content=answer,
            sources=sources
        )

        # 세션 상태 업데이트
        st.session_state.messages = messages


def main():
    render_chat_interface()


if __name__ == "__main__":
    main()
