from pydantic import BaseModel
from openai import OpenAI
import time



class Groups(BaseModel):
    groups: list[str]
    labels: list[int]

model = "gpt-4o"
client = OpenAI()

question = "그때 지냈 그런 얘길 많이 지금 아니 초딩 진짜 그런 얘기 니까 얘길 절대 얘기 하나 그냥 질문 정말 질문 대한 그리고 그냥 얘긴 절대 무슨 얘기 그런 얘기 하나 으니까 재미 별로 굳이 마실 구나 마이크"

thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=question,
)

# response_format은 "auto" 또는 API에서 허용하는 다른 형식을 사용해야 합니다.
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id='asst_VlzcLJVSi1Lw4WWxTFcCRDJK',
    response_format="json",
)

while run.status != "completed":
    time.sleep(0.5)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

messages = client.beta.threads.messages.list(
    thread_id=thread.id
)
print(messages)
# if run.status == 'completed':
#     messages = client.beta.threads.messages.list(
#         thread_id=thread.id
#     )
#     # 메시지 내용을 가져와서 Groups 모델로 변환합니다.
#     data = messages[0].content  # 응답 데이터가 포함된 메시지를 가정
#     groups_result = Groups(**data)
# else:
#     groups_result = None

# print(groups_result)
