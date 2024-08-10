from openai import OpenAI

class NLP:
    
    def __init__(self) -> None:
        self.model = "gpt-4o-mini"
        self.client = OpenAI()

    def classifyFishing(self, question) -> None:
        thread = self.client.beta.threads.create()
        message = self.client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
        )

        run = self.client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id = 'asst_VlzcLJVSi1Lw4WWxTFcCRDJK',
        )

        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=thread.id
            )
            result = messages.data[0].content[0].text.value
        else:
            result = run.status

        return result

a = NLP()

answer = a.classifyFishing('''신문 내용의 구조는 신문사마다 천차만별이다. 그러나 기본적인 내용은 비슷하다. 맨 앞인 1면에는 신문사가 그날 가장 널리 알리고자 하는 정보를 담는다. 이 때문에 ‘신문 1면’ 이라는 위치는 상당히 영향력이 크다.[5] 현재 대부분의 신문들은 주로 종합면[6] - 정치면 - 경제면 - 사회면 - 문화면 - 과학면 등 특정 분류로 나누어 기사를 싣는다. 마지막 5면 정도에 걸쳐서는 칼럼을 싣고, 맨 마지막 면에는 매일 2~3개의 사설이 실린다. 그리고 추가적으로 날씨, 부고[7], 인사개편, 공지, 만평, 퀴즈 등 이런저런 내용을 싣는다. 신춘문예 같은 언론사 주관 대회가 있을 경우에는 2~3면 정도에 걸쳐 당선작들을 싣기도 한다.

스포츠신문의 경우, 만화를 여러 작품씩 한 번 인쇄 당 6페이지 정도 분량으로 연재하기도 했다. 김성모가 이쪽으로도 유명한데 깡비, 4인조, 스터프 166km 이런 작품들이 죄다 스포츠신문 연재작이다. 그 외에도 박인권, 고우영, 비타민, 마인드C, 이우일, 박광수, 양영순, 최훈 등이 스포츠신문에 만화를 연재한 적이 있다.

그리고 신문의 주요 기능 중 하나는 바로 광고이다. 신문은 매일매일 발행되고, 또 많은 사람이 봐야 하므로 그 정보의 양에 비해 가격이 매우 싸다.[8] 그래서 신문은 기본적으로 광고 수입을 통해 이익을 창출하게 된다.[9] 사람들이 쉽게 볼 수 있는 위치와 크기일수록 광고 단가가 높아진다. 또한 발행 부수가 많을 수록 단가는 높아진다. 제호 양 옆에 작게 나오는 광고나 밑단을 통째로 차지하는 광고도 있고, 왼편/오른편 몇 단을 차지하는 광고, 아예 한 면을 다 쓰는 전면광고, 대놓고 돈을 받고 써 주는 광고성 기사 및 인터뷰까지 종류도 많다.
''')

print(answer)