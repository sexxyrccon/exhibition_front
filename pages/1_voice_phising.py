import streamlit as st
from openai import OpenAI
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt

client = OpenAI()
model = joblib.load('./pages/utils/voice_fraud_detection_model_with_weights.pkl')
okt = Okt()
tfidf = joblib.load('./pages/utils/tfidf_vectorizer.pkl')

def classifyFishing(question):
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=question
    )

    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id = 'asst_V4GTqXZJvC6SqyJmEyWb2Sm8',
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        result = json.loads(messages.data[0].content[0].text.value)
    else:
        result = run.status

    return result
    
def predict_fraud(sentence):
    sentence_tokenized = ' '.join(okt.morphs(sentence))

    # 전처리된 문장을 TF-IDF로 변환
    sentence_tfidf = tfidf.transform([sentence_tokenized])

    # 예측
    prediction = model.predict_proba(sentence_tfidf)
    isfraud = prediction[0][0]
    print(prediction[0][0] + prediction[0][1])

    if isfraud >= 0.8:
        return 0
    elif isfraud <= 0.2:
        return 1
    else:
        return None

def evaluate(sentence):
    confidence = predict_fraud(sentence)
    llm = classifyFishing(sentence)

    gpt = 1 in llm['labels']
    
    if confidence != None:
        if gpt != confidence:
            frauds = []
            for words in llm['groups']:
                frauds.append(predict_fraud(words))
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
    else: return gpt, llm



st.title("보이스 피싱 감지 모델")
st.markdown(":gray[*NLP기술을 활용한 보이스 피싱 감지*]")

txt = st.text_area("의심되는 보이스피싱 문구", height= 200)

if txt != '':
    isPhishing, data = evaluate(txt)
    st.write(data)
    st.write(isPhishing)

    if isPhishing and data != '':
        st.divider()
        st.subheader('본 문장은 보이스피싱으로 의심됩니다')
        st.markdown('보이스피싱으로 의심되는 문장과 어휘들')
        marks = ''

        reasons = data['reason']
        for i in range(len(reasons['text'])):
            marks += f"* {reasons['text'][i]}\n  - {reasons['why'][i]}\n"
        print(marks)
        st.markdown(marks)
    elif isPhishing and data == '':
        st.divider()
        st.subheader('본 문장은 보이스피싱으로 의심됩니다')
    else:
        st.divider()
        st.subheader('본 문장은 보이스피싱이 아닙니다')

# if isPhishing:
#     if data == '':
#         st.header('본 문장은 보이스피싱으로 의심됩니다')
#     else:
#         st.header('본 문장은 보이스피싱으로 의심됩니다')
#         st.subheader('보이스피싱으로 의심되는 문장')
# else:
#     st.markdown("### 아닌듯")
