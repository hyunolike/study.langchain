# app/utils/display.py - UI 표시 유틸리티
import streamlit as st


def set_page_config(page_title="LangChain RAG", page_icon="📚", layout="wide"):
    """페이지 설정"""
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state="expanded"
    )


def display_message(role, content, sources=None):
    """채팅 메시지 표시"""
    avatar = "🧑‍💻" if role == "user" else "🤖"

    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

        # 소스 표시 (있는 경우)
        if sources:
            display_sources(sources)


def display_sources(sources):
    """참조 소스 표시"""
    with st.expander("참조 문서"):
        for i, source in enumerate(sources):
            st.markdown(f"**출처 {i + 1}:** {source.get('title', '문서')}")
            st.markdown(f"**관련성:** {source.get('score', 0.0):.2f}")
            st.markdown("**내용:**")
            st.markdown(source.get('content', '내용 없음'))
            st.markdown("---")