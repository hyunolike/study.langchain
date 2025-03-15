## MCP (Model Context Protocol)
> [!NOTE]
> Anthropic 2024년 11월 말에 공개한 오픈소스 표준 프로토콜 \n
> AI 모델, 특히 대규모 언어 모델 (LLM)을 외부 데이터 소스 및 도구와 연결하기 위한 범용 방법 제공

### 기본 개념
- MCP는 앤트로픽이 개발한 오픈소스 표준 프로토콜로, AI 모델이 다양한 외부 데이터나 툴과 손쉽게 연결되어 정보를 가져오거나 작업을 수행할 수 있게 하는 기술
- 쉽게 말하면, MCP는 다양한 기기를 하나의 USB 포트에 연결하는 것과 비슷


```
기존에는 AI가 새로운 서비스를 활용하려면 그때마다 각 서비스 전용 API를 따로 개발하고 연동해야 했습니다.
MCP를 사용하면 AI가 데이터나 도구에 연결할 때마다 별도의 코드 작성 없이도 하나의 표준된 방식으로 쉽게 연결할 수 있습니다.
```

### 기본 아키텍처
- <img width="953" alt="image" src="https://github.com/user-attachments/assets/eb43a489-2d59-48df-9e9a-354f3a047bd9" />
- ![image](https://github.com/user-attachments/assets/f68caba5-e1aa-4d9b-a0e9-730264d9564a)
- MCP는 호스트 애플리케이션, 클라이언트, 서버 간의 표준화된 통신을 위한 프로토콜입니다. 이 구조는 JSON-RPC를 기반으로 하며, 안전하고 효율적인 데이터 및 기능 교환을 가능하게 합니다.

### AI 생태계의 새로운 연결 표준
<img width="1301" alt="image" src="https://github.com/user-attachments/assets/c79897c9-458c-43e9-9867-72a33cd68b37" />


### 참고자료
- [공식 자료](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)
- [Model Context Protocol (MCP) Anthropic 개발 방법](https://wikidocs.net/book/17027)
