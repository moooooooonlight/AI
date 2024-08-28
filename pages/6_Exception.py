import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# CSV 파일 불러오기
df = pd.read_csv('csv/conf.csv')

# 중앙값 계산
df['mean'] = (df['lwr'] + df['upper']) / 2

# 신뢰 구간 길이 계산
df['range'] = df['upper'] - df['lwr']

# 페이지 제목
st.title('예외에 대한 검증')

# 데이터 분석 및 인도 강조
st.write("""
    Switzerland ‑ India 는 왜 물가의 빅맥가격이 연동되지 않는지에 대한 추가적인 가설 제시    
""")

india_exception1_path = 'png/indiaException1.png'
india_exception2_path = 'png/indiaException2.png'

st.write('')
st.write('')

image1 = Image.open(india_exception1_path)
image2 = Image.open(india_exception2_path)

st.image(image1, caption="Switzerland 물가와 빅맥가격의 산점도", use_column_width=True)

st.write('')
st.write('')
st.write('')

st.image(image2, caption="India 물가와 빅맥가격의 산점도", use_column_width=True)

