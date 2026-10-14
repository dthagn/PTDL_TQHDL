"""
Unemployment Map Chart
Choropleth map showing unemployment rate by country using ISO country codes.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ISO country codes mapping
ISO_COUNTRY_CODES = {
    'Japan': 'JPN',
    'Philippines': 'PHL',
    'South Korea': 'KOR',
    'Thailand': 'THA',
    'Vietnam': 'VNM'
}


def load_data():
    """Load the processed unemployment data."""
    df = pd.read_csv('../data/processed/unemployment_final.csv')
    return df


def create_unemployment_map(df, year=None):
    """
    Create choropleth map showing unemployment rate by country.
    
    Parameters:
        df: DataFrame with unemployment data
        year: Optional year filter (int). If None, uses most recent year.
    
    Returns:
        plotly.graph_objects.Figure: The unemployment choropleth map
    """
    df_filtered = df.copy()
    
    # Apply year filter
    if year is not None:
        df_filtered = df_filtered[df_filtered['Year'] == year]
        title_suffix = f'Year: {year}'
    else:
        # Use most recent year
        most_recent_year = df_filtered['Year'].max()
        df_filtered = df_filtered[df_filtered['Year'] == most_recent_year]
        title_suffix = f'Year: {most_recent_year}'
    
    # Ensure ISO country codes are used
    df_filtered['ISO_Code'] = df_filtered['Country'].map(ISO_COUNTRY_CODES)
    
    fig = px.choropleth(
        df_filtered,
        locations='ISO_Code',
        color='Unemployment_Rate',
        hover_name='Country',
        hover_data={
            'Year': True,
            'Unemployment_Rate': ':.2f'
        },
        color_continuous_scale='Viridis',
        title=f'Unemployment Rate by Country - {title_suffix}',
        labels={
            'Unemployment_Rate': 'Unemployment Rate (%)'
        },
        projection='natural earth'
    )
    
    fig.update_traces(
        hovertemplate='<b>%{hover_name}</b><br>' +
                      'Year: %{customdata[0]}<br>' +
                      'Unemployment Rate: %{z:.2f}%<br>' +
                      '<extra></extra>'
    )
    
    fig.update_layout(
        coloraxis_colorbar=dict(
            title='Unemployment Rate (%)',
            thickness=20,
            len=0.8
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor='gray',
            projection_type='natural earth'
        ),
        template='plotly_white',
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig


def get_chart(year=None):
    """
    Main function to create and return the map with optional year filter.
    
    Parameters:
        year: Optional year filter (int)
    
    Returns:
        plotly.graph_objects.Figure: The unemployment choropleth map
    """
    df = load_data()
    fig = create_unemployment_map(df, year=year)
    return fig


def get_available_years(df):
    """Get list of available years in the dataset."""
    return sorted(df['Year'].unique().tolist())


if __name__ == '__main__':
    df = load_data()
    print("Available years:", get_available_years(df))
    
    # Example: Show map for most recent year
    fig = get_chart()
    fig.show()
    
    # Example: Show map for 2020 (COVID year)
    fig = get_chart(year=2020)
    fig.show()
