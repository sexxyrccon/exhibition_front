from openai import OpenAI
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt

class Detect:
    def __init__(self) -> None:
        self.client = OpenAI()
        self.model = joblib.load('./pages/voice_fraud_detection_model_with_weights.pkl')
        self.okt = Okt()
        self.tfidf = joblib.load('/tfidf_vectorizer.pkl')

    def classifyFishing(self, question) -> None:
        thread = self.client.beta.threads.create()
        message = self.client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
        )

        run = self.client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id = 'asst_V4GTqXZJvC6SqyJmEyWb2Sm8',
        )

        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=thread.id
            )
            result = json.loads(messages.data[0].content[0].text.value)
        else:
            result = run.status

        return result
    
    def predict_fraud(self, sentence):
        sentence_tokenized = ' '.join(self.okt.morphs(sentence))

        # 전처리된 문장을 TF-IDF로 변환
        sentence_tfidf = self.tfidf.transform([sentence_tokenized])

        # 예측
        prediction = self.model.predict_proba(sentence_tfidf)
        isfraud = prediction[0][0]

        if isfraud >= 0.8:
            return 0
        elif isfraud <= 0.2:
            return 1
        else:
            return None
    
    def evaluate(self, sentence):
        confidence = self.predict_fraud(sentence = sentence)
        llm = self.classifyFishing(question = sentence)

        gpt = 1 in llm['labels']

        if gpt != confidence:
            frauds = []
            for words in llm['groups']:
                frauds.append(self.predict_fraud(sentence = words))
            ifFraud = 1 in frauds

            if gpt == ifFraud:
                return gpt, llm
            else:
                return ifFraud, ''
        else:
            if gpt:
                return gpt, llm
            else:
                return gpt, 'not physhing'

a = Detect()

print(a.evaluate('안녕하세요 중국인 권해정입니다'))