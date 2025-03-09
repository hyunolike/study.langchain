# streamlit_app.py (Streamlit 프론트엔드)
import streamlit as st
import requests
import json
import time

# 페이지 설정
st.set_page_config(
    page_title="문서 QA 시스템",
    page_icon="🤖",
    layout="centered",
)

# 타이틀 및 설명
st.title("📚 문서 기반 질의응답 시스템")
st.markdown("문서 데이터베이스에 질문하고 AI 답변을 받아보세요.")

# 사이드바 설정
st.sidebar.header("About")
st.sidebar.info(
    "이 애플리케이션은 LangChain과 LangServe를 사용하여 "
    "문서 데이터에 대한 질의응답을 제공합니다."
)

# API 엔드포인트 설정
API_URL = "http://localhost:8000/api/qa/invoke"

# 사용자 입력 필드
query = st.text_input("질문을 입력하세요:", placeholder="문서에 대한 질문을 입력하세요...")

if query:
    # 사용자가 질문을 입력했을 때
    with st.spinner("AI가 답변을 생성 중입니다..."):
        try:
            # LangServe API 호출
            payload = json.dumps(query)
            headers = {
                'Content-Type': 'application/json'
            }
            
            # API 요청 전송
            response = requests.post(API_URL, headers=headers, data=payload)
            
            if response.status_code == 200:
                # 응답 처리
                result = response.json()
                
                # 결과 표시
                st.subheader("답변:")
                st.write(result)
                
                # 메타데이터 표시
                st.subheader("메타데이터")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="응답 시간", value=f"{response.elapsed.total_seconds():.2f}초")
                with col2:
                    st.metric(label="신뢰도", value="높음" if len(result) > 100 else "중간")
                
            else:
                st.error(f"API 오류: {response.status_code}")
                st.error(response.text)
                
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# 사용자 피드백 섹션
with st.expander("피드백 남기기"):
    st.write("답변이 도움이 되었나요?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("👍 좋아요")
    with col2:
        st.button("👎 별로에요")
    with col3:
        st.button("🤔 모르겠어요")
    
    feedback = st.text_area("추가 피드백:", placeholder="추가 의견이 있으시면 남겨주세요...")
    if st.button("제출"):
        st.success("피드백이 제출되었습니다. 감사합니다!")

# 푸터
st.markdown("---")
st.markdown("© 2025 LLM 문서 QA 시스템")
