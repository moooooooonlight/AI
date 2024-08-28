import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

# 제목과 설명 추가
st.markdown("<h1 style='font-size: 32px;'>빅데이터를 활용한 빅맥가격의 물가 대체성 분석</h1>", unsafe_allow_html=True)
st.write('')
st.write('')

# 이미지 파일 경로 설정
image_path = "png/CompareMac.png"

# 이미지 파일 열기
image = Image.open(image_path)

# 이미지 표시
st.image(image, caption="위 이미지는 한국을 기준으로 상대적인 빅맥가격을 시각화한 자료", use_column_width=True)