"""
Country Comparison Chart
Bar chart comparing unemployment rates between 5 countries with year and period filters.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Consistent color scheme for countries across all charts
COUNTRY_COLORS = {
    'Japan': '#1f77b4',
    'Philippines': '#ff7f0e',
    'South Korea': '#2ca02c',
    'Thailand': '#d62728',
    'Vietnam': '#9467bd'
}


def load_data():
    """Load the processed unemployment data."""
    df = pd.read_csv('../data/processed/unemployment_final.csv')
    return df


def add_period_filter(df):
    """
    Add period column for filtering: Pre-COVID, COVID, Recovery.
    """
    def get_period(year):
        if year <= 2019:
            return 'Pre-COVID (2010-2019)'
        elif year <= 2021:
            return 'COVID (2020-2021)'
        else:
            return 'Recovery (2022-2024)'
    
    df = df.copy()
    df['Period'] = df['Year'].apply(get_period)
    return df


def create_country_comparison(df, year=None, period=None):
    """
    Create bar chart comparing unemployment rates between countries.
    
    Parameters:
        df: DataFrame with unemployment data
        year: Optional year filter (int)
        period: Optional period filter (str: 'Pre-COVID (2010-2019)', 'COVID (2020-2021)', 'Recovery (2022-2024)')
    
    Returns:
        plotly.graph_objects.Figure: The country comparison chart
    """
    df_filtered = df.copy()
    
    # Apply filters
    if year is not None:
        df_filtered = df_filtered[df_filtered['Year'] == year]
        title_suffix = f'Year: {year}'
    elif period is not None:
        df_filtered = df_filtered[df_filtered['Period'] == period]
        title_suffix = f'Period: {period}'
    else:
        # If no filter, use most recent year
        most_recent_year = df_filtered['Year'].max()
        df_filtered = df_filtered[df_filtered['Year'] == most_recent_year]
        title_suffix = f'Year: {most_recent_year}'
    
    # Calculate average by country if multiple rows per country
    df_agg = df_filtered.groupby('Country')['Unemployment_Rate'].mean().reset_index()
    
    fig = px.bar(
        df_agg,
        x='Country',
        y='Unemployment_Rate',
        color='Country',
        color_discrete_map=COUNTRY_COLORS,
        title=f'Unemployment Rate by Country - {title_suffix}',
        labels={
            'Country': 'Country',
            'Unemployment_Rate': 'Unemployment Rate (%)'
        },
        text='Unemployment_Rate'
    )
    
    fig.update_traces(
        texttemplate='%{y:.2f}%',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' +
                      'Unemployment Rate: %{y:.2f}%<br>' +
                      '<extra></extra>'
    )
    
    fig.update_layout(
        xaxis=dict(title='Country'),
        yaxis=dict(
            title='Unemployment Rate (%)',
            range=[0, df_agg['Unemployment_Rate'].max() * 1.2]
        ),
        showlegend=False,
        template='plotly_white'
    )
    
    return fig


def get_chart(year=None, period=None):
    """
    Main function to create and return the chart with optional filters.
    
    Parameters:
        year: Optional year filter (int)
        period: Optional period filter (str)
    
    Returns:
        plotly.graph_objects.Figure: The country comparison chart
    """
    df = load_data()
    df = add_period_filter(df)
    fig = create_country_comparison(df, year=year, period=period)
    return fig


def get_available_years(df):
    """Get list of available years in the dataset."""
    return sorted(df['Year'].unique().tolist())


def get_available_periods(df):
    """Get list of available periods in the dataset."""
    df = add_period_filter(df)
    return sorted(df['Period'].unique().tolist())


if __name__ == '__main__':
    df = load_data()
    print("Available years:", get_available_years(df))
    print("Available periods:", get_available_periods(df))
    
    # Example: Show chart for most recent year
    fig = get_chart()
    fig.show()
    
    # Example: Show chart for COVID period
    fig = get_chart(period='COVID (2020-2021)')
    fig.show()
