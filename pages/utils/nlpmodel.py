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