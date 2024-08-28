import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv('csv/WorldPrice.csv')

# 데이터 프레임을 긴 형식으로 변환
df_long = df.melt(id_vars=['date'], 
                  value_vars=['South Korea', 'Australia', 'China', 'India', 'Indonesia', 'Russia', 'South Africa', 'Switzerland', 'United States'],
                  var_name='country', 
                  value_name='price_index')

# 열 'date'를 연도로 변환
df_long.rename(columns={'date': 'year'}, inplace=True)

# 연도별, 국가별 물가 지수 평균 계산 (이미 데이터가 연도별이므로 평균 계산은 필요 없음)
yearly_avg_df = df_long.groupby(['country', 'year'])['price_index'].mean().reset_index()

# 제목과 설명 추가
st.title('세계의 각 물가 지수 추이')
st.write('2000년 ~ 2020년까지의 물가지수의 연평균을 점의 움직임으로 시각화')

# 국가 리스트 (기본적으로 모든 국가 선택)
country_list = ['Australia', 'South Korea', 'United States', 'Indonesia', 'Switzerland', 'China', 'Russia', 'South Africa', 'India']

# 선택된 국가에 따른 데이터 필터링 (모든 국가가 기본적으로 선택됨)
filtered_df = yearly_avg_df[yearly_avg_df['country'].isin(country_list)]

# 색상 팔레트 설정 (plotly.express의 색상 팔레트를 사용)
colors = px.colors.qualitative.Plotly
country_color_map = {country: colors[i % len(colors)] for i, country in enumerate(country_list)}

# 빈 그래프 객체 생성
fig = go.Figure()

# 선택된 국가별로 데이터를 추가하여 흔적이 남도록 함
for country in country_list:
    country_data = filtered_df[filtered_df['country'] == country]
    fig.add_trace(go.Scatter(
        x=country_data['year'],
        y=country_data['price_index'],
        mode='lines+markers',
        name=country,
        line=dict(color=country_color_map[country]),  # 색상 설정
        marker=dict(size=8, color=country_color_map[country], line=dict(width=2, color='black'))
    ))

# 레이아웃 설정
fig.update_layout(
    title='연도별 국가별 물가 지수 평균',
    xaxis_title='연도',
    yaxis_title='물가 지수 평균',
    xaxis=dict(range=[filtered_df['year'].min(), filtered_df['year'].max()]),
    yaxis=dict(range=[filtered_df['price_index'].min(), filtered_df['price_index'].max()]),
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
    for country in country_list:
        country_data = filtered_df[(filtered_df['country'] == country) & (filtered_df['year'] <= year)]
        frame_data.append(go.Scatter(
            x=country_data['year'],
            y=country_data['price_index'],
            mode='lines+markers',
            name=country,
            line=dict(color=country_color_map[country]),  # 색상 설정
            marker=dict(size=8, color=country_color_map[country], line=dict(width=2, color='black'))
        ))
    frames.append(go.Frame(data=frame_data, name=str(year)))

fig.frames = frames

st.plotly_chart(fig)

# 피벗 테이블 생성 (연도별 평균 반영)
pivot_table = filtered_df.pivot_table(values='price_index', index='country', columns='year')

# 테이블 표시
st.subheader('연도별 국가들의 물가 지수 평균 테이블')
st.write(pivot_table)
