import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

# 제목과 간단한 설명 추가
st.set_page_config(page_title="플랫폼이름", layout="wide")
st.title('플랫폼이름')
st.write('오디오딥')

# 동영상 파일을 저장할 디렉토리
VIDEO_DIR = Path("videos")
VIDEO_DIR.mkdir(exist_ok=True)

# 딥페이크 미디어를 식별하는 함수 (예시로 2번째 영상이 딥페이크라고 가정)
def is_deepfake(index):
    return index == 1

# 업로드된 동영상을 리스트로 표시하는 함수
def list_uploaded_videos():
    video_files = [f for f in VIDEO_DIR.iterdir() if f.suffix in ['.mp4', '.mov', '.avi', '.mkv']]
    for i in range(0, len(video_files), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(video_files):
                with cols[j]:
                    video_file = video_files[i + j]
                    st.write(f"**{video_file.name}**")  # 제목 표시
                    st.video(str(video_file), format="video/mp4", start_time=0)
                    if is_deepfake(i + j):
                        st.markdown(
                            """
                            <div style="background-color:#F46760;padding:10px;border-radius:5px;text-align:center;">
                                ❎ 딥페이크 미디어입니다.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            """
                            <div style="background-color:lightgreen;padding:10px;border-radius:5px;text-align:center;">
                                ✅ 실제 미디어입니다.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

# 동영상 업로드 섹션
st.header("비디오 업로드")
uploaded_file = st.file_uploader("비디오 파일을 선택하세요", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    # 파일 저장
    video_path = VIDEO_DIR / uploaded_file.name
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Video '{uploaded_file.name}' 업로드 성공!")

# 업로드된 동영상 리스트 섹션
st.header("비디오 목록")
list_uploaded_videos()
