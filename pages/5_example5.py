import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv('csv/confint.csv')

# 중앙값 계산
df['mean'] = (df['lwr'] + df['upper']) / 2

# 신뢰 구간 길이 계산
df['range'] = df['upper'] - df['lwr']

# 제목과 설명 추가
st.title('나라별 신뢰 구간 시각화 (Bubble + Bar Chart)')
st.write('이 애플리케이션은 각 나라의 신뢰 구간을 버블과 세로 막대 차트로 시각화합니다.')

# 색상 팔레트 설정 (Plotly Express의 기본 색상 팔레트 사용)
colors = px.colors.qualitative.Plotly

# 그래프 생성
fig = go.Figure()

# 세로 막대 (신뢰 구간 표시)
for i, country in enumerate(df['Country']):
    fig.add_trace(go.Bar(
        x=[country],
        y=[df.loc[df['Country'] == country, 'lwr'].values[0]],  # 막대의 시작값을 lwr로 설정
        name=f'{country} 신뢰 구간',
        marker=dict(color=colors[i % len(colors)], opacity=0.5),
        width=0.4,
        base=df.loc[df['Country'] == country, 'lwr'].values[0],  # 막대의 시작값 설정
        customdata=[df.loc[df['Country'] == country, 'upper'].values[0] - df.loc[df['Country'] == country, 'lwr'].values[0]],  # 막대 길이
        hovertemplate='%{y}에서 %{customdata}까지'
    ))

# 버블 차트 (중앙값 표시)
for i, country in enumerate(df['Country']):
    fig.add_trace(go.Scatter(
        x=[country],
        y=[df.loc[df['Country'] == country, 'mean'].values[0]],
        mode='markers',
        marker=dict(size=[df.loc[df['Country'] == country, 'range'].values[0] * 10], color=colors[i % len(colors)], opacity=0.6),
        name=f'{country} 중앙값'
    ))

# 레이아웃 설정
fig.update_layout(
    title='나라별 신뢰 구간 (버블 + 막대 차트)',
    xaxis_title='국가',
    yaxis_title='값',
    template='plotly_white',
    showlegend=True,
    barmode='overlay'  # 막대가 겹치지 않도록 설정
)

# 그래프 표시
st.plotly_chart(fig)
