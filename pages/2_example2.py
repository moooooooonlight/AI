import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv('BigmacPrice.csv')

# 날짜를 연도로 변환
df['year'] = pd.to_datetime(df['date']).dt.year

# 연도별, 국가별 dollar_price 평균 계산
yearly_avg_df = df.groupby(['name', 'year'])['dollar_price'].mean().reset_index()

# 제목과 설명 추가
st.title('빅맥지수 시각화')
st.write('여러 국가의 연도별 빅맥 달러 가격 평균을 점의 움직임으로 시각화')

# 선택된 국가 리스트
selected_countries = ['Australia', 'South Korea', 'United States', 'Indonesia', 'Switzerland', 'China', 'Russia', 'South Africa', 'India']

# 선택된 국가에 따른 데이터 필터링
filtered_df = yearly_avg_df[yearly_avg_df['name'].isin(selected_countries)]

# 색상 팔레트 설정 (plotly.express의 색상 팔레트를 사용)
colors = px.colors.qualitative.Plotly

# 빈 그래프 객체 생성
fig = go.Figure()

# 선택된 국가별로 데이터를 추가하여 흔적이 남도록 함
for i, country in enumerate(selected_countries):
    country_data = filtered_df[filtered_df['name'] == country]
    fig.add_trace(go.Scatter(
        x=country_data['year'],
        y=country_data['dollar_price'],
        mode='lines+markers',
        name=country,
        line=dict(color=colors[i % len(colors)]),  # 색상 설정
        marker=dict(size=8, color=colors[i % len(colors)], line=dict(width=2, color='black'))
    ))

# 레이아웃 설정
fig.update_layout(
    title='연도별 국가별 빅맥 달러 가격 평균',
    xaxis_title='연도',
    yaxis_title='빅맥 달러 가격 평균',
    xaxis=dict(range=[filtered_df['year'].min(), filtered_df['year'].max()]),
    yaxis=dict(range=[filtered_df['dollar_price'].min(), filtered_df['dollar_price'].max()]),
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        buttons=[dict(label="Play",
                      method="animate",
                      args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)])]
    )],
    template='plotly_white'  # 흰색 배경 템플릿 적용
)

# 애니메이션 프레임 생성
frames = []
years = sorted(filtered_df['year'].unique())
for year in years:
    frame_data = []
    for country in selected_countries:
        country_data = filtered_df[(filtered_df['name'] == country) & (filtered_df['year'] <= year)]
        frame_data.append(go.Scatter(
            x=country_data['year'],
            y=country_data['dollar_price'],
            mode='lines+markers',
            name=country,
            line=dict(color=colors[selected_countries.index(country) % len(colors)]),  # 색상 설정
            marker=dict(size=8, color=colors[selected_countries.index(country) % len(colors)], line=dict(width=2, color='black'))
        ))
    frames.append(go.Frame(data=frame_data, name=str(year)))

fig.frames = frames

st.plotly_chart(fig)

# 피벗 테이블 생성 (연도별 평균 반영)
pivot_table = filtered_df.pivot_table(values='dollar_price', index='name', columns='year')

# 테이블 표시
st.subheader('연도별 국가들의 빅맥 달러 가격 평균 테이블')
st.write(pivot_table)
