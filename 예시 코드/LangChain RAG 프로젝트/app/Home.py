# app/Home.py - 메인 앱 진입점
import streamlit as st
from app.utils.session import init_session_state
from app.utils.display import set_page_config

def main():
    # 페이지 설정
    set_page_config(
        page_title="LangChain RAG 데모",
        page_icon="🤖",
        layout="wide"
    )
    
    # 세션 상태 초기화
    init_session_state()
    
    # 메인 페이지 UI
    st.title("🤖 LangChain RAG 문서 질의응답 시스템")
    
    st.markdown("""
    ## 랭체인(LangChain)과 RAG를 이용한 대화형 문서 검색 시스템
    
    이 애플리케이션은 문서 컬렉션에서 지식을 추출하고 대화형 인터페이스를 통해 정보를 검색할 수 있게 해줍니다.
    
    ### 주요 기능:
    
    - **💬 채팅 인터페이스**: 문서에 기반한 질문-답변
    - **🔍 문서 검색**: 핵심 정보 검색 및 시각화
    - **📊 문서 분석**: 문서 컬렉션에 대한 인사이트
    - **📁 문서 관리**: 데이터 업로드 및 처리
    """)
    
    # 기능 선택 카드 디스플레이
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### 💬 Chat with Documents")
        st.markdown("문서 기반 대화형 AI와 대화하세요")
        st.button("채팅 시작하기", on_click=lambda: st.switch_page("pages/01_💬_Chat.py"))
    
    with col2:
        st.info("### 🔍 Search Documents")
        st.markdown("문서 검색 및 탐색")
        st.button("검색 시작하기", on_click=lambda: st.switch_page("pages/02_🔍_Document_Search.py"))
    
    # 하단 정보
    st.markdown("---")
    st.markdown("### 📚 사용 방법")
    
    tab1, tab2, tab3 = st.tabs(["문서 업로드", "질문하기", "고급 기능"])
    with tab1:
        st.markdown("""
        1. 설정 페이지에서 문서를 업로드하세요 (.pdf, .txt, .docx, .csv 지원)
        2. 문서 처리가 완료될 때까지 기다리세요
        3. 처리된 문서를 기반으로 질문하거나 검색할 수 있습니다
        """)
    
    with tab2:
        st.markdown("""
        - 채팅 페이지에서 질문을 입력하세요
        - AI가 관련 문서를 참조하여 답변을 생성합니다
        - 답변과 함께 참조한 소스 문서를 확인할 수 있습니다
        """)
    
    with tab3:
        st.markdown("""
        - 문서 검색 페이지에서 키워드로 검색하세요
        - 유사도 점수로 관련성 높은 문서를 볼 수 있습니다
        - 설정 페이지에서 모델과 검색 매개변수를 조정할 수 있습니다
        """)

if __name__ == "__main__":
    main()
