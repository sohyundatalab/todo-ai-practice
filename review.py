from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일 불러오기
load_dotenv()

# OpenAI 클라이언트 생성
client = OpenAI()

# 리뷰받을 코드 파일 이름
target_file = "main.py"

# main.py 코드 읽기
code = Path(target_file).read_text(encoding="utf-8")

# LLM에게 보낼 프롬프트
prompt = f"""
너는 Python 초급자를 지도하는 코드 리뷰어야.

아래 코드는 콘솔 기반 할 일 관리 프로그램이야.
코드는 실행되지만, 구조적으로 개선할 부분이 있는지 리뷰해줘.

리뷰 기준:
1. 버그 가능성
2. 함수 분리
3. 중복 코드
4. 예외처리
5. 가독성
6. 초급자가 이해하기 쉬운 개선 방향

리뷰 결과는 아래 형식으로 정리해줘.

| 번호 | 문제 유형 | 문제 설명 | 개선 방향 | 우선순위 |
|---|---|---|---|---|

그리고 바로 전체 코드를 고치지 말고,
먼저 개선 항목만 제안해줘.

아래는 main.py 코드야.
```python
{code}

"""

response = client.responses.create(
model="gpt-4o-mini", 
input=prompt
)


print(response.output_text)