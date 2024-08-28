import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

# 제목과 설명 추가
st.markdown("<h1 style='font-size: 32px;'>선별 국가</h1>", unsafe_allow_html=True)
st.write('')
#st.write('아래 이미지는 한국을 기준으로 상대적인 빅맥가격을 시각화한 자료입니다')

# 이미지 파일 경로 설정
image_path = "png/BigmacMap.png"

# 이미지 파일 열기
image = Image.open(image_path)

# 이미지 표시
st.image(image, caption="", use_column_width=True)