import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

# 제목과 설명 추가
st.markdown("<h1>결론</h1>", unsafe_allow_html=True)
st.write('')
st.write('')

# 이미지 파일 경로 설정
image_path = "png/ConclusionImage.png"

# 이미지 파일 열기
image = Image.open(image_path)


# 이미지 표시
st.image(image, caption="빅맥가격의 물가 대체성", use_column_width=True)