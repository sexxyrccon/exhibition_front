import streamlit as st
from nlpmodel import NLP

st.title("보이스 피싱 감지 모델")
st.markdown(":gray[*NLP기술을 활용한 보이스 피싱 감지*]")

txt = st.text_area("의심되는 보이스피싱 문구", height= 200)

import time
import numpy as np
import pandas as pd
import streamlit as st

model = NLP()

text = model.classifyFishing(txt)

def stream_data():
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

st.write_stream(stream_data)