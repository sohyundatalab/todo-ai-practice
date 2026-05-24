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
너는 Python 코드리뷰어야.
아래 코드를 초보자도 이해할 수 있게 리뷰해줘.

리뷰 기준:
1. 버그 가능성
2. 가독성
3. 함수 분리
4. 예외처리
5. 보안 문제
6. 개선하면 좋은 코드 예시
7. 수정된 전체 python 코드 

아래 코드만 기준으로 리뷰해줘.

```python
{code}

"""

response = client.responses.create(
model="gpt-4o-mini", 
input=prompt
)


print(response.output_text)