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
            "content": '''너는 어떤 문장이 들어오면 해당 문장이 보이스피싱 사기로 볼 수 있는지 아님 평소 문장인지 판단해줘 대답은 보이스피싱 사기 문장이 맞으면 True 아니면 False로 답해줘'''},
            {"role": "user", "content": question}
        ]
        )
        return completion.choices[0].message.content

fishing = NLP()
answer = fishing.classifyFishing("습니까 지내 계시 지요 고요 그리고 계좌 번호 모른다고 계좌 번호 알려 고요 괜찮 으세요 계좌 번호 모르 습니까 습니다 지금 화면 어떤")
print(answer)