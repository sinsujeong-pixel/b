import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    # Sales.xlsx 파일의 supermarket_sales_test 시트 로드
    df = pd.read_excel('Sales.xlsx', sheet_name='supermarket_sales_test')
    # 결측치 제거
    df = df.dropna()
    return df

try:
    df = load_data()

    st.title("📊 지점별 매출 및 평점 대시보드")

    # 사이드바에서 지점(Branch) 선택
    branches = sorted(df['Branch'].unique())
    selected_branch = st.sidebar.selectbox("지점(Branch) 선택", branches)

    # 선택된 지점 데이터 필터링
    filtered_df = df[df['Branch'] == selected_branch]

    # 메트릭 계산 (총매출, 평균매출, 평균 평점)
    total_sales = filtered_df['Total'].sum()
    avg_sales = filtered_df['Total'].mean()
    avg_rating = filtered_df['Rating'].mean()

    # Metric 영역 표시
    col1, col2, col3 = st.columns(3)
    col1.metric("총 매출 (Total Sales)", f"${total_sales:,.2f}")
    col2.metric("평균 매출 (Average Sales)", f"${avg_sales:,.2f}")
    col3.metric("평균 평점 (Average Rating)", f"{avg_rating:.2f} / 10")

    st.markdown("---")

    # 상품 카테고리(Product line)별 평균 매출 계산 및 막대그래프 시각화
    st.subheader(f"✨ {selected_branch} 지점의 상품 카테고리별 평균 매출")
    
    category_avg = filtered_df.groupby('Product line')['Total'].mean().reset_index()
    category_avg = category_avg.sort_values(by='Total', ascending=False)

    fig = px.bar(
        category_avg,
        x='Product line',
        y='Total',
        labels={'Total': '평균 매출 ($)', 'Product line': '상품 카테고리'},
        text_auto='.2s',
        color='Total',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(xaxis_title="상품 카테고리", yaxis_title="평균 매출 ($)", showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.info("Sales.xlsx 파일과 supermarket_sales_test 시트명이 정확하며 app.py와 같은 폴더에 있는지 확인해주세요.")
