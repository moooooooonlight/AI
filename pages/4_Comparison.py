import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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

# 국가별 위도, 경도 정보 설정
country_coords = {
    'South Korea': (35.9078, 127.7669),
    'Australia': (-25.2744, 133.7751),
    'China': (35.8617, 104.1954),
    'India': (20.5937, 78.9629),
    'Indonesia': (-0.7893, 113.9213),
    'Russia': (61.5240, 105.3188),
    'South Africa': (-30.5595, 22.9375),
    'Switzerland': (46.8182, 8.2275),
    'United States': (37.0902, -95.7129)
}

# 지구본 생성 함수
def create_globe():
    fig = go.Figure()

    # 각 나라에 빨간색 마커 및 빅맥 이모티콘 추가
    for country, (lat, lon) in country_coords.items():
        # 빅맥 이모티콘 추가
        fig.add_trace(go.Scattergeo(
            lon=[lon],
            lat=[lat],
            text='🍔',  # 빅맥 이모티콘 추가
            mode='text',
            textfont=dict(size=20, family='Arial', weight='bold'),  # 두껍게
            showlegend=False
        ))
        
        # 국가 이름 추가 (빅맥 이모티콘 아래)
        fig.add_trace(go.Scattergeo(
            lon=[lon],
            lat=[lat - 2],  # 이모티콘 밑에 위치시키기 위해 약간의 조정
            text=f"{country}",
            mode='text',
            textfont=dict(size=14, color='black', family='Arial', weight='bold'),  # 두껍게
            showlegend=False
        ))

    # 지구본 레이아웃 설정
    fig.update_geos(
        showcountries=True, countrycolor="LightGray",
        showcoastlines=True, coastlinecolor="Gray",
        projection_type="orthographic",  # 지구본 형태
        lataxis_showgrid=True, lonaxis_showgrid=True,
        landcolor='lightgreen',  # 육지 색상
        oceancolor='lightblue',  # 바다 색상
        showocean=True,          # 바다 표시
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        height=600,
        clickmode='event+select',  # 클릭 모드 활성화
    )
    
    return fig

# Streamlit session state 사용
if 'selected_country' not in st.session_state:
    st.session_state['selected_country'] = None

# 지구본 표시
st.plotly_chart(create_globe(), use_container_width=True)

# 드롭다운 메뉴로 국가 선택
selected_country = st.selectbox('국가 선택', options=list(country_coords.keys()))

# 국가 선택 시 해당 데이터 시각화
if selected_country:
    st.subheader(f'{selected_country}의 빅맥 가격과 물가 지수 비교')

    # 빅맥 지수 데이터 필터링
    bigmac_data = bigmac_long_df[bigmac_long_df['country'] == selected_country]

    # 물가지수 데이터 필터링
    world_price_data = world_price_df_long[world_price_df_long['country'] == selected_country]

    # 데이터 병합 (연도를 기준으로 병합)
    combined_data = pd.merge(
        bigmac_data[['year', 'dollar_price']],
        world_price_data[['year', 'price_index']],
        on='year',
        suffixes=('_BigMac', '_PriceIndex')
    )

    # 병합된 데이터가 비어 있는지 확인
    if combined_data.empty:
        st.write(f"{selected_country}의 데이터를 병합할 수 없습니다. 데이터가 없거나 연도가 일치하지 않습니다.")
    else:
        # 두 가지 값 비교를 위한 그래프 생성
        fig = go.Figure()

        # 빅맥 지수 라인 + 영역 채우기
        fig.add_trace(go.Scatter(
            x=combined_data['year'],
            y=combined_data['dollar_price'],
            mode='lines+markers',
            name='BigMac Price',
            line=dict(color='royalblue', width=4),
            marker=dict(size=8, color='royalblue', line=dict(width=2, color='darkblue')),
            fill='tozeroy',  # 영역을 x축(0)까지 채우기
            text='BigMac Price',
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
            title=f'{selected_country}의 빅맥 가격과 물가 지수 비교',
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

else:
    st.write("아직 국가를 선택하지 않았습니다.")
