import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
import subprocess  # FFmpeg 사용
from model.model1 import analyze_audio, extract_mfcc_features

st.set_page_config(page_title="플랫폼이름", layout="wide")
st.title('플랫폼이름')
st.write('오디오딥')

VIDEO_DIR = Path("videos")
VIDEO_DIR.mkdir(exist_ok=True)

def list_uploaded_videos():
    video_files = [f for f in VIDEO_DIR.iterdir() if f.suffix in ['.mp4', '.mov', '.avi', '.mkv']]
    for i in range(0, len(video_files), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(video_files):
                with cols[j]:
                    video_file = video_files[i + j]
                    st.write(f"**{video_file.name}**")
                    st.video(str(video_file), format="video/mp4", start_time=0)
                    
                    # 오디오 추출 및 딥페이크 판별
                    audio_path = extract_audio(video_file)
                    if audio_path:
                        is_deepfake = analyze_audio(str(audio_path))
                        if is_deepfake:
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

def extract_audio(video_path):
    audio_path = video_path.with_suffix('.wav')
    try:
        subprocess.run([
            "ffmpeg", "-i", str(video_path), "-q:a", "0", "-map", "a", str(audio_path)
        ], check=True)
        return audio_path
    except Exception as e:
        st.error(f"오디오 추출 실패: {e}")
        return None

st.header("비디오 업로드")
uploaded_file = st.file_uploader("비디오 파일을 선택하세요", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    video_path = VIDEO_DIR / uploaded_file.name
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Video '{uploaded_file.name}' 업로드 성공!")

st.header("비디오 목록")
list_uploaded_videos()
