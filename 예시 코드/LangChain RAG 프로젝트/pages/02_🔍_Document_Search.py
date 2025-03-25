# app/pages/02_🔍_Document_Search.py - 문서 검색 인터페이스
import streamlit as st
import pandas as pd
import plotly.express as px
from app.utils.display import set_page_config
from rag.retriever import get_retriever
from rag.vectorstore import get_vectorstore


def render_search_interface():
    # 페이지 설정
    set_page_config(
        page_title="문서 검색",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 문서 검색")

    # 검색 설정
    with st.sidebar:
        st.header("검색 설정")
        top_k = st.slider("검색 결과 수", min_value=1, max_value=20, value=10)

        st.header("필터")
        # 메타데이터 필터 (예: 문서 유형, 날짜 등)
        # 실제 데이터에 따라 필터 옵션 조정 필요
        doc_types = ["모든 유형", "PDF", "텍스트", "웹페이지"]
        selected_type = st.selectbox("문서 유형", doc_types)

        # 날짜 필터 예시
        if st.checkbox("날짜 필터 적용"):
            date_range = st.date_input(
                "날짜 범위 선택",
                value=(pd.Timestamp("2023-01-01").date(), pd.Timestamp.now().date())
            )

    # 검색 입력
    query = st.text_input("검색어를 입력하세요", key="search_query")

    col1, col2 = st.columns([1, 5])
    with col1:
        search_button = st.button("검색", use_container_width=True)
    with col2:
        st.write("")  # 빈 공간

    if search_button and query:
        with st.spinner("검색 중..."):
            # 검색 실행
            retriever = get_retriever(k=top_k)
            docs = retriever.get_relevant_documents(query)

            if not docs:
                st.warning("검색 결과가 없습니다. 다른 검색어를 시도해보세요.")
            else:
                # 검색 결과를 데이터프레임으로 변환
                results_data = []
                for doc in docs:
                    results_data.append({
                        "제목": doc.metadata.get("title", "제목 없음"),
                        "내용": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                        "유사도": doc.metadata.get("score", 0),
                        "문서 유형": doc.metadata.get("source_type", "알 수 없음"),
                        "날짜": doc.metadata.get("date", "날짜 없음"),
                        "전체 내용": doc.page_content,
                        "메타데이터": doc.metadata
                    })

                results_df = pd.DataFrame(results_data)

                # 결과 표시
                st.subheader(f"'{query}'에 대한 검색 결과")

                # 유사도 차트
                fig = px.bar(
                    results_df,
                    x="유사도",
                    y="제목",
                    orientation="h",
                    title="검색 결과 관련성",
                    color="유사도",
                    color_continuous_scale="Viridis",
                )
                fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig)

                # 결과 목록
                for i, row in results_df.iterrows():
                    with st.expander(f"{i + 1}. {row['제목']} (유사도: {row['유사도']:.2f})"):
                        st.markdown(f"**문서 유형:** {row['문서 유형']}")
                        st.markdown(f"**날짜:** {row['날짜']}")
                        st.markdown("**내용 미리보기:**")
                        st.markdown(row['내용'])

                        # 전체 내용 표시 버튼
                        if st.button(f"전체 내용 보기 #{i}", key=f"view_full_{i}"):
                            st.markdown("**전체 내용:**")
                            st.markdown(row['전체 내용'])

                        # 메타데이터 표시
                        with st.expander("메타데이터"):
                            st.json(row['메타데이터'])


def main():
    render_search_interface()


if __name__ == "__main__":
    main()