import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 불러오기 (빅맥 지수)
bigmac_df = pd.read_csv('csv/BigmacPriceCompare.csv')

# 빅맥 지수 데이터를 긴 형식으로 변환
bigmac_long_df = bigmac_df.melt(id_vars=['date'], 
                                value_vars=['Australia', 'China', 'India', 'Indonesia', 'Russia', 
                                            'South Africa', 'South Korea', 'Switzerland', 'United States'],
                                var_name='country', 
                                value_name='dollar_price')

# 날짜를 연도로 변환
bigmac_long_df['year'] = pd.to_datetime(bigmac_long_df['date'], format='%Y').dt.year

# 필요한 연도만 필터링 (2000년부터 2020년까지)
bigmac_long_df = bigmac_long_df[(bigmac_long_df['year'] >= 2000) & (bigmac_long_df['year'] <= 2020)]

# CSV 파일 불러오기 (물가 지수)
world_price_df = pd.read_csv('csv/WorldPriceCompareTo.csv')

# 국가 이름 통일 (Korea -> South Korea)
world_price_df = world_price_df.rename(columns={'Korea': 'South Korea'})

# 데이터 프레임을 긴 형식으로 변환
world_price_df_long = world_price_df.melt(id_vars=['date'], 
                                          value_vars=['South Korea', 'Australia', 'China', 'India', 'Indonesia', 
                                                      'Russia', 'South Africa', 'Switzerland', 'United States'],
                                          var_name='country', 
                                          value_name='price_index')

# 열 'date'를 연도로 변환
world_price_df_long['year'] = pd.to_datetime(world_price_df_long['date'], format='%Y').dt.year

# 필요한 연도만 필터링 (2000년부터 2020년까지)
world_price_df_long = world_price_df_long[(world_price_df_long['year'] >= 2000) & (world_price_df_long['year'] <= 2020)]

# 제목과 설명 추가
st.title('빅맥지수와 물가지수 시각화 (2000년부터 2020년까지)')
st.write('이 애플리케이션은 여러 국가의 빅맥 달러 가격과 물가 지수를 비교하여 시각화합니다.')

# 빅맥 지수와 물가지수 시각화할 국가 리스트 설정
selected_countries = ['Australia', 'South Korea', 'United States', 'Indonesia', 'Switzerland', 'China', 'Russia', 'South Africa', 'India']

# 국가별 그래프 생성
for country in selected_countries:
    # 빅맥 지수 데이터 필터링
    bigmac_data = bigmac_long_df[bigmac_long_df['country'] == country]
    
    # 물가지수 데이터 필터링
    world_price_data = world_price_df_long[world_price_df_long['country'] == country]
    
    # 데이터 병합 (연도를 기준으로 병합)
    combined_data = pd.merge(
        bigmac_data[['year', 'dollar_price']],
        world_price_data[['year', 'price_index']],
        on='year',
        suffixes=('_BigMac', '_PriceIndex')
    )
    
    # 병합된 데이터가 비어 있는지 확인
    if combined_data.empty:
        st.write(f"{country}의 데이터를 병합할 수 없습니다. 데이터가 없거나 연도가 일치하지 않습니다.")
        continue
    
    # 두 가지 값 비교를 위한 그래프 생성
    fig = go.Figure()

    # 빅맥 지수 라인 + 영역 채우기
    fig.add_trace(go.Scatter(
        x=combined_data['year'],
        y=combined_data['dollar_price'],
        mode='lines+markers',
        name='BigMac Index',
        line=dict(color='royalblue', width=4),
        marker=dict(size=8, color='royalblue', line=dict(width=2, color='darkblue')),
        fill='tozeroy',  # 영역을 x축(0)까지 채우기
        text='BigMac Index',
        hoverinfo='x+y+text'
    ))
    
    # 물가지수 라인 + 영역 채우기
    fig.add_trace(go.Scatter(
        x=combined_data['year'],
        y=combined_data['price_index'],
        mode='lines+markers',
        name='Price Index',
        line=dict(color='tomato', width=4),
        marker=dict(size=8, color='tomato', line=dict(width=2, color='darkred')),
        fill='tozeroy',  # 영역을 x축(0)까지 채우기
        text='Price Index',
        hoverinfo='x+y+text'
    ))

    # 레이아웃 설정
    fig.update_layout(
        title=f'{country}의 빅맥 지수와 물가 지수 비교',
        xaxis_title='연도',
        yaxis_title='값',
        template='plotly_dark',
        legend_title='지표',
        legend=dict(x=0.01, y=0.99, traceorder='normal'),
        xaxis=dict(range=[2000, 2020]),  # x축 범위를 2000년부터 2020년으로 고정
        yaxis=dict(title='값', showgrid=True),
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='rgba(0,0,0,0.1)'
    )
    
    # 그래프 표시
    st.plotly_chart(fig)
