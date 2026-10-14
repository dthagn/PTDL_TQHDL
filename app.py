"""
Unemployment Analysis Dashboard
Streamlit application for analyzing unemployment trends in Asian countries (2010-2024)
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_loader import (
    load_unemployment_data,
    load_statistics,
    load_analysis_results,
    load_correlation_results,
    load_findings,
    load_data_dictionary,
    load_source_metadata
)
from preprocessing import (
    add_period_column,
    filter_by_country,
    filter_by_year,
    filter_by_period,
    calculate_kpi_metrics,
    get_available_countries,
    get_available_years,
    get_available_periods
)
from visualization import (
    create_unemployment_trend,
    create_country_comparison,
    create_choropleth_map,
    create_gdp_unemployment_scatter,
    create_inflation_unemployment_scatter,
    create_youth_unemployment_comparison,
    create_period_comparison
)
from dashboard_utils import (
    display_kpi_card,
    display_correlation_table,
    display_findings_section,
    display_data_sources,
    display_limitations,
    display_methodology,
    display_error_message,
    display_warning_message,
    get_period_from_year
)


# Page configuration
st.set_page_config(
    page_title="Phân tích Thất nghiệp Châu Á 2010-2024",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-container {
        display: flex;
        justify-content: space-around;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


def load_data():
    """Load all required data files."""
    try:
        unemployment_df = load_unemployment_data()
        statistics_df = load_statistics()
        analysis_results_df = load_analysis_results()
        correlation_df = load_correlation_results()
        findings = load_findings()
        data_dict_df = load_data_dictionary()
        source_metadata_df = load_source_metadata()
        
        # Add period column
        unemployment_df = add_period_column(unemployment_df)
        
        return {
            'unemployment': unemployment_df,
            'statistics': statistics_df,
            'analysis_results': analysis_results_df,
            'correlation': correlation_df,
            'findings': findings,
            'data_dict': data_dict_df,
            'source_metadata': source_metadata_df
        }
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {str(e)}")
        return None


def main():
    """Main application function."""
    
    # Load data
    data = load_data()
    if data is None:
        st.stop()
    
    unemployment_df = data['unemployment']
    
    # Header
    st.markdown('<div class="main-title">Phân tích Xu hướng Thất nghiệp</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">5 quốc gia châu Á (2010-2024): Nhật Bản, Philippines, Hàn Quốc, Thái Lan, Việt Nam</div>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Điều hướng")
    
    pages = [
        "Tổng quan",
        "Xu hướng theo thời gian",
        "So sánh quốc gia",
        "GDP & Thất nghiệp",
        "Lạm phát",
        "Thanh niên",
        "Phân tích theo giai đoạn",
        "Dữ liệu",
        "Phương pháp",
        "Kết luận"
    ]
    
    selected_page = st.sidebar.radio("", pages)
    
    # Filters in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Bộ lọc")
    
    available_countries = get_available_countries(unemployment_df)
    available_years = get_available_years(unemployment_df)
    available_periods = get_available_periods(unemployment_df)
    
    selected_countries = st.sidebar.multiselect(
        "Quốc gia",
        available_countries,
        default=available_countries
    )
    
    selected_years = st.sidebar.multiselect(
        "Năm",
        available_years,
        default=available_years
    )
    
    selected_periods = st.sidebar.multiselect(
        "Giai đoạn",
        available_periods,
        default=available_periods
    )
    
    # Apply filters
    filtered_df = unemployment_df.copy()
    if selected_countries:
        filtered_df = filter_by_country(filtered_df, selected_countries)
    if selected_years:
        filtered_df = filter_by_year(filtered_df, selected_years)
    if selected_periods:
        filtered_df = filter_by_period(filtered_df, selected_periods)
    
    # Calculate KPI metrics based on filtered data
    kpi_metrics = calculate_kpi_metrics(filtered_df)
    
    # Display content based on selected page
    if selected_page == "Tổng quan":
        display_overview_page(filtered_df, kpi_metrics, selected_countries, selected_years)
    
    elif selected_page == "Xu hướng theo thời gian":
        display_trend_page(filtered_df, selected_countries)
    
    elif selected_page == "So sánh quốc gia":
        display_country_comparison_page(filtered_df, selected_countries)
    
    elif selected_page == "GDP & Thất nghiệp":
        display_gdp_unemployment_page(filtered_df, selected_countries, data['correlation'])
    
    elif selected_page == "Lạm phát":
        display_inflation_page(filtered_df, selected_countries, data['correlation'])
    
    elif selected_page == "Thanh niên":
        display_youth_page(filtered_df, selected_countries)
    
    elif selected_page == "Phân tích theo giai đoạn":
        display_period_page(filtered_df)
    
    elif selected_page == "Dữ liệu":
        display_data_page(data)
    
    elif selected_page == "Phương pháp":
        display_methodology_page()
    
    elif selected_page == "Kết luận":
        display_conclusion_page(data)


def display_overview_page(df, kpi_metrics, selected_countries, selected_years):
    """Display overview page with KPI cards and key charts."""
    st.markdown('<div class="section-header">Chỉ số chính (KPI)</div>', unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if selected_countries and len(selected_countries) == 1 and selected_years and len(selected_years) == 1:
            display_kpi_card(
                "Tỷ lệ thất nghiệp được chọn",
                kpi_metrics.get('selected_unemployment'),
                help_text=f"{selected_countries[0]} - {selected_years[0]}"
            )
        else:
            display_kpi_card(
                "Tỷ lệ thất nghiệp trung bình",
                kpi_metrics.get('avg_unemployment'),
                help_text="Trung bình theo bộ lọc hiện tại"
            )
    
    with col2:
        display_kpi_card(
            "Tỷ lệ thất nghiệp cao nhất",
            kpi_metrics.get('max_unemployment_rate'),
            help_text=f"Năm {int(kpi_metrics.get('max_unemployment_year', 0))}"
        )
    
    with col3:
        display_kpi_card(
            "Tăng trưởng GDP trung bình",
            kpi_metrics.get('avg_gdp_growth'),
            help_text="Trung bình theo bộ lọc hiện tại"
        )
    
    with col4:
        display_kpi_card(
            "Tỷ lệ thất nghiệp thanh niên trung bình",
            kpi_metrics.get('avg_youth_unemployment'),
            help_text="Trung bình theo bộ lọc hiện tại"
        )
    
    st.markdown("---")
    
    # Key charts
    st.markdown('<div class="section-header">Tổng quan trực quan</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_trend = create_unemployment_trend(df, selected_countries)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        fig_comparison = create_country_comparison(df, 'Unemployment_Rate')
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Map
    st.markdown('<div class="section-header">Bản đồ tỷ lệ thất nghiệp</div>', unsafe_allow_html=True)
    selected_map_year = st.selectbox("Chọn năm để hiển thị", options=sorted(df['Year'].unique()), index=len(sorted(df['Year'].unique()))-1)
    fig_map = create_choropleth_map(df, selected_map_year)
    st.plotly_chart(fig_map, use_container_width=True)


def display_trend_page(df, selected_countries):
    """Display unemployment trend over time."""
    st.markdown('<div class="section-header">Xu hướng tỷ lệ thất nghiệp theo thời gian</div>', unsafe_allow_html=True)
    
    fig = create_unemployment_trend(df, selected_countries)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics table
    st.markdown("---")
    st.subheader("Thống kê theo năm")
    yearly_stats = df.groupby('Year')['Unemployment_Rate'].agg(['mean', 'min', 'max', 'std']).reset_index()
    yearly_stats.columns = ['Năm', 'Trung bình', 'Tối thiểu', 'Tối đa', 'Độ lệch chuẩn']
    st.dataframe(yearly_stats, use_container_width=True, hide_index=True)


def display_country_comparison_page(df, selected_countries):
    """Display country comparison charts."""
    st.markdown('<div class="section-header">So sánh quốc gia</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_unemployment = create_country_comparison(df, 'Unemployment_Rate')
        st.plotly_chart(fig_unemployment, use_container_width=True)
    
    with col2:
        fig_gdp = create_country_comparison(df, 'GDP_Growth')
        st.plotly_chart(fig_gdp, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_youth = create_country_comparison(df, 'Youth_Unemployment_Rate')
        st.plotly_chart(fig_youth, use_container_width=True)
    
    with col2:
        fig_inflation = create_country_comparison(df, 'Inflation')
        st.plotly_chart(fig_inflation, use_container_width=True)
    
    # Detailed comparison table
    st.markdown("---")
    st.subheader("Bảng so sánh chi tiết")
    country_comparison = df.groupby('Country')[['Unemployment_Rate', 'Youth_Unemployment_Rate', 'GDP_Growth', 'Inflation']].mean().reset_index()
    country_comparison.columns = ['Quốc gia', 'Thất nghiệp TB', 'Thất nghiệp thanh niên TB', 'GDP TB', 'Lạm phát TB']
    st.dataframe(country_comparison, use_container_width=True, hide_index=True)


def display_gdp_unemployment_page(df, selected_countries, correlation_df):
    """Display GDP vs unemployment analysis."""
    st.markdown('<div class="section-header">Mối liên hệ giữa GDP và Thất nghiệp</div>', unsafe_allow_html=True)
    
    fig = create_gdp_unemployment_scatter(df, selected_countries)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Kết quả phân tích tương quan")
    
    # Filter correlation results
    gdp_correlation = correlation_df[correlation_df['Variable_X'] == 'GDP_Growth']
    
    if len(gdp_correlation) > 0:
        display_correlation_table(gdp_correlation)
    else:
        st.warning("Không có dữ liệu tương quan.")


def display_inflation_page(df, selected_countries, correlation_df):
    """Display inflation vs unemployment analysis."""
    st.markdown('<div class="section-header">Mối liên hệ giữa Lạm phát và Thất nghiệp</div>', unsafe_allow_html=True)
    
    fig = create_inflation_unemployment_scatter(df, selected_countries)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Kết quả phân tích tương quan")
    
    # Filter correlation results
    inflation_correlation = correlation_df[correlation_df['Variable_X'] == 'Inflation']
    
    if len(inflation_correlation) > 0:
        display_correlation_table(inflation_correlation)
    else:
        st.warning("Không có dữ liệu tương quan.")


def display_youth_page(df, selected_countries):
    """Display youth unemployment analysis."""
    st.markdown('<div class="section-header">Phân tích Thất nghiệp Thanh niên</div>', unsafe_allow_html=True)
    
    fig = create_youth_unemployment_comparison(df, selected_countries)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Youth Gap (Chênh lệch thanh niên)")
    
    # Calculate youth gap
    df_with_gap = df.copy()
    df_with_gap['Youth_Gap'] = df_with_gap['Youth_Unemployment_Rate'] - df_with_gap['Unemployment_Rate']
    
    youth_gap_stats = df_with_gap.groupby('Country')['Youth_Gap'].agg(['mean', 'min', 'max']).reset_index()
    youth_gap_stats.columns = ['Quốc gia', 'Youth Gap TB', 'Youth Gap Tối thiểu', 'Youth Gap Tối đa']
    st.dataframe(youth_gap_stats, use_container_width=True, hide_index=True)
    
    st.info("Youth Gap = Tỷ lệ thất nghiệp thanh niên - Tỷ lệ thất nghiệp tổng thể")


def display_period_page(df):
    """Display period-based analysis."""
    st.markdown('<div class="section-header">Phân tích theo Giai đoạn</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_unemployment = create_period_comparison(df, 'Unemployment_Rate')
        st.plotly_chart(fig_unemployment, use_container_width=True)
    
    with col2:
        fig_youth = create_period_comparison(df, 'Youth_Unemployment_Rate')
        st.plotly_chart(fig_youth, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_gdp = create_period_comparison(df, 'GDP_Growth')
        st.plotly_chart(fig_gdp, use_container_width=True)
    
    with col2:
        fig_inflation = create_period_comparison(df, 'Inflation')
        st.plotly_chart(fig_inflation, use_container_width=True)
    
    # Period statistics table
    st.markdown("---")
    st.subheader("Thống kê theo giai đoạn")
    period_stats = df.groupby('Period')[['Unemployment_Rate', 'Youth_Unemployment_Rate', 'GDP_Growth', 'Inflation']].mean().reset_index()
    period_stats.columns = ['Giai đoạn', 'Thất nghiệp TB', 'Thất nghiệp thanh niên TB', 'GDP TB', 'Lạm phát TB']
    st.dataframe(period_stats, use_container_width=True, hide_index=True)


def display_data_page(data):
    """Display data sources and raw data."""
    display_data_sources(data['source_metadata'], data['data_dict'])
    
    st.markdown("---")
    st.header("Dữ liệu thô")
    
    st.subheader("Bộ dữ liệu thất nghiệp")
    st.dataframe(data['unemployment'], use_container_width=True, height=400)
    
    st.markdown("---")
    st.subheader("Thống kê")
    st.dataframe(data['statistics'], use_container_width=True, height=300)
    
    st.markdown("---")
    st.subheader("Kết quả phân tích")
    st.dataframe(data['analysis_results'], use_container_width=True, height=300)


def display_methodology_page():
    """Display methodology section."""
    display_methodology()


def display_conclusion_page(data):
    """Display conclusion and findings."""
    display_findings_section(data['findings'])
    display_limitations()


if __name__ == "__main__":
    main()
