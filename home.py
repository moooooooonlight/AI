import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

# 제목과 설명 추가
st.markdown("<h1 style='font-size: 32px;'>각 나라의 빅맥 가격과 물가의 상관관계 심층 분석</h1>", unsafe_allow_html=True)
st.write('이 애플리케이션은 여러 국가의 연도별 빅맥 달러 가격 평균을 점의 움직임으로 시각화합니다. 이동한 자리에 그래프의 흔적이 남습니다.')

st.write('')
st.write('')
st.write('')

# 이미지 파일 경로 설정
image_path = "png/CompareMac.png"

# 이미지 파일 열기
image = Image.open(image_path)

# 이미지 표시
st.image(image, caption="대한민국 기준", use_column_width=True)