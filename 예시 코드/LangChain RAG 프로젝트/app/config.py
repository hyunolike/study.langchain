# app/config.py - 앱 설정
import os
import json
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 기본 설정
DEFAULT_SETTINGS = {
    "llm_model": "gpt-3.5-turbo",
    "embedding_model": "text-embedding-ada-002",
    "chunk_size": 1000,
    "chunk_overlap": 100,
    "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
    "vector_db": "FAISS",  # 기본값은 로컬 FAISS 사용
}

# 설정 파일 경로
SETTINGS_FILE = "app_settings.json"


def get_settings():
    """저장된 설정 가져오기"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_SETTINGS.copy()
    else:
        return DEFAULT_SETTINGS.copy()


def update_settings(new_settings):
    """설정 업데이트 및 저장"""
    current_settings = get_settings()
    current_settings.update(new_settings)

    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(current_settings, f, indent=2)
        return True
    except Exception as e:
        print(f"설정 저장 오류: {str(e)}")
        return False