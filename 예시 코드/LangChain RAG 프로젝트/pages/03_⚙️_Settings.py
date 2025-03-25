# app/pages/03_⚙️_Settings.py - 설정 페이지
import streamlit as st
import os
from app.utils.display import set_page_config
from app.config import update_settings, get_settings
from scripts.ingest import process_file


def render_settings_interface():
    # 페이지 설정
    set_page_config(page_title="설정", page_icon="⚙️")

    st.title("⚙️ 애플리케이션 설정")

    # 설정 값 로드
    settings = get_settings()

    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["일반 설정", "문서 관리", "API 설정"])

    with tab1:
        st.header("일반 설정")

        # 모델 설정
        st.subheader("AI 모델 설정")

        model = st.selectbox(
            "LLM 모델",
            options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            index=0 if settings.get("llm_model") == "gpt-3.5-turbo" else
            1 if settings.get("llm_model") == "gpt-4" else 2
        )

        embedding_model = st.selectbox(
            "임베딩 모델",
            options=["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"],
            index=0 if settings.get("embedding_model") == "text-embedding-ada-002" else
            1 if settings.get("embedding_model") == "text-embedding-3-small" else 2
        )

        # RAG 설정
        st.subheader("RAG 설정")

        chunk_size = st.number_input(
            "청크 크기",
            min_value=100,
            max_value=4000,
            value=settings.get("chunk_size", 1000),
            help="문서를 분할할 때 사용할 청크 크기입니다. 더 작은 값은 정밀한 검색에 유리합니다."
        )

        chunk_overlap = st.number_input(
            "청크 겹침",
            min_value=0,
            max_value=1000,
            value=settings.get("chunk_overlap", 100),
            help="청크 간 겹치는 문자 수입니다. 문맥 유지에 도움이 됩니다."
        )

        if st.button("설정 저장", key="save_general"):
            # 설정 업데이트
            new_settings = {
                "llm_model": model,
                "embedding_model": embedding_model,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap
            }
            update_settings(new_settings)
            st.success("설정이 저장되었습니다!")

    with tab2:
        st.header("문서 관리")

        # 문서 업로드
        st.subheader("문서 업로드")

        uploaded_files = st.file_uploader(
            "문서 파일을 업로드하세요",
            accept_multiple_files=True,
            type=["pdf", "txt", "docx", "csv", "md"]
        )

        if uploaded_files:
            if st.button("업로드된 파일 처리", key="process_files"):
                with st.status("파일 처리 중...") as status:
                    for uploaded_file in uploaded_files:
                        # 파일 저장 경로
                        upload_dir = os.path.join("data", "upload")
                        os.makedirs(upload_dir, exist_ok=True)
                        file_path = os.path.join(upload_dir, uploaded_file.name)

                        # 파일 저장
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        status.update(label=f"{uploaded_file.name} 처리 중...")

                        # 파일 처리 및 인덱싱
                        try:
                            process_file(file_path, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                            st.success(f"{uploaded_file.name} 처리 완료!")
                        except Exception as e:
                            st.error(f"{uploaded_file.name} 처리 실패: {str(e)}")

                status.update(label="모든 파일 처리 완료!", state="complete")

        # 인덱스된 문서 관리
        st.subheader("인덱스된 문서")

        # 여기에서는 예시로 정적 데이터를 표시합니다.
        # 실제 구현에서는 벡터 스토어나 메타데이터 저장소에서 문서 정보를 가져와야 합니다.
        if st.button("인덱스된 문서 조회"):
            # 예시 데이터
            st.info("이 기능은 실제 구현에서 벡터 스토어에서 문서 목록을 가져와야 합니다.")
            sample_docs = [
                {"name": "example.pdf", "chunks": 15, "date": "2023-10-15"},
                {"name": "documentation.txt", "chunks": 8, "date": "2023-10-14"},
                {"name": "data.csv", "chunks": 5, "date": "2023-10-13"},
            ]

            # 문서 목록 표시
            st.dataframe(
                sample_docs,
                use_container_width=True,
                column_config={
                    "name": "파일명",
                    "chunks": "청크 수",
                    "date": "업로드 날짜"
                }
            )

    with tab3:
        st.header("API 설정")

        # API 키 설정
        st.subheader("API 키")

        openai_api_key = st.text_input(
            "OpenAI API 키",
            type="password",
            value=settings.get("openai_api_key", ""),
            help="OpenAI API 키를 입력하세요."
        )

        # 벡터 DB 설정
        st.subheader("벡터 DB 설정")

        vector_db = st.selectbox(
            "벡터 데이터베이스",
            options=["FAISS", "Chroma", "Pinecone"],
            index=0 if settings.get("vector_db") == "FAISS" else
            1 if settings.get("vector_db") == "Chroma" else 2
        )

        if vector_db == "Pinecone":
            pinecone_api_key = st.text_input(
                "Pinecone API 키",
                type="password",
                value=settings.get("pinecone_api_key", "")
            )

            pinecone_environment = st.text_input(
                "Pinecone 환경",
                value=settings.get("pinecone_environment", "")
            )

            pinecone_index = st.text_input(
                "Pinecone 인덱스",
                value=settings.get("pinecone_index", "")
            )

        elif vector_db == "Chroma":
            chroma_directory = st.text_input(
                "Chroma 디렉토리",
                value=settings.get("chroma_directory", "./data/chroma_db")
            )

        if st.button("API 설정 저장", key="save_api"):
            # 설정 업데이트
            new_settings = {
                "openai_api_key": openai_api_key,
                "vector_db": vector_db
            }

            if vector_db == "Pinecone":
                new_settings.update({
                    "pinecone_api_key": pinecone_api_key,
                    "pinecone_environment": pinecone_environment,
                    "pinecone_index": pinecone_index
                })
            elif vector_db == "Chroma":
                new_settings.update({
                    "chroma_directory": chroma_directory
                })

            update_settings(new_settings)
            st.success("API 설정이 저장되었습니다!")


def main():
    render_settings_interface()


if __name__ == "__main__":
    main()
