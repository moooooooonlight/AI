import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv('csv/conf.csv')

# 중앙값 계산
df['mean'] = (df['lwr'] + df['upper']) / 2

# 신뢰 구간 길이 계산
df['range'] = df['upper'] - df['lwr']

# 제목과 설명 추가
st.title('나라별 회귀계수의 신뢰구간 (95%)')
st.write('각 나라의 추세비교회귀분석의 회귀계수의 신뢰구간 시각화')

# 색상 팔레트 설정 (Plotly Express의 기본 색상 팔레트 사용)
colors = px.colors.qualitative.Plotly
color_0_included = 'blue'  # 0을 포함하는 신뢰 구간 색상
color_0_excluded = 'red'   # 0을 포함하지 않는 신뢰 구간 색상

# 그래프 생성
fig = go.Figure()

# 세로 막대 (신뢰 구간 표시)
for i, country in enumerate(df['Country']):
    color = color_0_included if df.loc[df['Country'] == country, 'lwr'].values[0] <= 0 <= df.loc[df['Country'] == country, 'upper'].values[0] else color_0_excluded
    fig.add_trace(go.Bar(
        x=[country],
        y=[df.loc[df['Country'] == country, 'upper'].values[0] - df.loc[df['Country'] == country, 'lwr'].values[0]],  # 막대의 높이를 신뢰 구간으로 설정
        name=f'{country} 신뢰 구간',
        marker=dict(color=color, opacity=0.5),
        width=0.4,
        base=df.loc[df['Country'] == country, 'lwr'].values[0],  # 막대의 시작값 설정
        customdata=[df.loc[df['Country'] == country, 'upper'].values[0]],  # 신뢰 구간의 상한 값
        hovertemplate='%{base}에서 %{customdata}까지'
    ))

# 버블 차트 (중앙값 표시)
for i, country in enumerate(df['Country']):
    color = color_0_included if df.loc[df['Country'] == country, 'lwr'].values[0] <= 0 <= df.loc[df['Country'] == country, 'upper'].values[0] else color_0_excluded
    fig.add_trace(go.Scatter(
        x=[country],
        y=[df.loc[df['Country'] == country, 'mean'].values[0]],
        mode='markers',
        marker=dict(size=[max(10, df.loc[df['Country'] == country, 'range'].values[0] * 100)],  # 최소 크기 10을 설정하여 0이 아닌 크기로 표시
                     color=color,
                     opacity=0.6),
        name=f'{country} 중앙값'
    ))

# 기준선 0 추가
fig.add_trace(go.Scatter(
    x=df['Country'],
    y=[0] * len(df['Country']),
    mode='lines',
    line=dict(color='red', width=2, dash='dash'),  # 기준선 색상 및 스타일
    name='기준선 0'
))

# 레이아웃 설정
fig.update_layout(
    title='나라별 신뢰 구간 (버블 + 막대 차트)',
    xaxis_title='국가',
    yaxis_title='값',
    template='plotly_white',
    showlegend=False,  # 범례 제거
    barmode='overlay'  # 막대가 겹치지 않도록 설정
)

# 그래프 표시
st.plotly_chart(fig)
