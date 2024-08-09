import os

KEY = os.environ.get("OPENAI_API_KEY")

from openai import OpenAI

class NLP:
    
    def __init__(self) -> None:
        self.model = "gpt-4o-mini"
        self.client = OpenAI(api_key = KEY)

    def classifyFishing(self, question) -> None:
        completion = self.client.chat.completions.create(
        model = self.model,
        messages=[
            {"role": "system",
            "content": '''너는 어떤 문장이 들어오면 해당 문장이 보이스피싱 사기로 볼 수 있는지 아님 평소 문장인지 판단해줘 대답은 보이스피싱 사기 문장이 많은 정도를 0부터 100사이 숫자를 이용해서 나타내줘 만약에 50%정도이면 50 이렇게, 보이스피싱으로 볼 수 있는 단어마다 중요도를 정해서 좀더 세부적으로 의심도를 나누어봐'''},
            {"role": "user", "content": question}
        ]
        )
        return completion.choices[0].message.content

fishing = NLP()
answer = fishing.classifyFishing("우리 기억 마신다 말씀 어디 사람 부동산 운영 면서 실적 으로 불법 도박 사이트 운영 혐의 상태 입니다 에게 연락 사람 공부 과정 에서 명의 농협 국민은행 통장 불법 용도 사용 압수수색 하고 적응력 연락 드렸 습니다 연락 주세요 저녁 모르 고요 국민은행 농협 그래서 저희 연락 드린 본인 께서 통장 직접 개설 통장 으로 판매 거나 양도 사실 으신 건지 아니 면은 본인 에게 명의 도용 저런 보험 때문 연락 드린 건데 지금 제일 중요 대해서 지금 새끼 때문 연락 드린 고요 혹시 김민철 연관 으신지 또한 아니면 명의 도용 당하 연락 드린 겁니다 치킨 전화")
print(answer)