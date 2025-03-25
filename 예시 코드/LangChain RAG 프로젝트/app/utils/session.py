# app/utils/session.py - 세션 관리
import streamlit as st


def init_session_state():
    """세션 상태 초기화"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "settings" not in st.session_state:
        # 기본 설정 로드
        from app.config import get_settings
        st.session_state.settings = get_settings()


def get_session_state(key, default=None):
    """세션 상태 값 가져오기"""
    return st.session_state.get(key, default)


def set_session_state(key, value):
    """세션 상태 값 설정"""
    st.session_state[key] = value