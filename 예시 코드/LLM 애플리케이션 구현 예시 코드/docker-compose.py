# docker-compose.yml
version: '3'

services:
  # 백엔드 서비스: LangServe
  langserve:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
    volumes:
      - ./data:/app/data
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # 프론트엔드 서비스: Streamlit
  streamlit:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    environment:
      - BACKEND_API_URL=http://langserve:8000
    depends_on:
      - langserve
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501"]
      interval: 30s
      timeout: 10s
      retries: 3

  # 벡터 데이터베이스: Chroma
  chroma:
    image: ghcr.io/chroma-core/chroma:latest
    ports:
      - "8080:8000"
    volumes:
      - ./chroma_data:/chroma/chroma
    environment:
      - ALLOW_RESET=true
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000
    restart: always

  # 모니터링: LangSmith (LangChain 모니터링 도구)
  langsmith:
    image: langchain/langchainplus-backend:latest
    ports:
      - "4173:4173"
    environment:
      - PORT=4173
      - NODE_ENV=production
    restart: always
