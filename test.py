from pydantic import BaseModel
from openai import OpenAI

class Groups(BaseModel):
    groups: list[str]
    labels: list[int]
    

class NLP:
    
    def __init__(self) -> None:
        self.model = "gpt-4o"
        self.client = OpenAI()

    def classifyFishing(self, question) -> None:
        thread = self.client.beta.threads.create()
        message = self.client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question,
        )

        run = self.client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id = 'asst_VlzcLJVSi1Lw4WWxTFcCRDJK',
        response_format = Groups,
        )

        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=thread.id
            )
            result = messages
        else:
            result = run.status

        return result

new = NLP()

answer = new.classifyFishing('그때 지냈 그런 얘길 많이 지금 아니 초딩 진짜 그런 얘기 니까 얘길 절대 얘기 하나 그냥 질문 정말 질문 대한 그리고 그냥 얘긴 절대 무슨 얘기 그런 얘기 하나 으니까 재미 별로 굳이 마실 구나 마이크')

from pprint import pprint

pprint(answer)