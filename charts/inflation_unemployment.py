"""
Inflation vs Unemployment Chart
Scatter plot showing relationship between Inflation and Unemployment Rate.
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


def load_correlation_data():
    """Load correlation results from analysis."""
    try:
        corr_df = pd.read_csv('../analysis/correlation_results.csv')
        return corr_df
    except FileNotFoundError:
        return None


def create_inflation_unemployment_scatter(df, corr_df=None, show_trendline=False):
    """
    Create scatter plot showing Inflation vs Unemployment Rate.
    
    X-axis: Inflation (%)
    Y-axis: Unemployment Rate (%)
    Color: Country
    
    Parameters:
        df: DataFrame with unemployment data
        corr_df: DataFrame with correlation results (optional)
        show_trendline: Whether to show trendline (bool)
    
    Returns:
        plotly.graph_objects.Figure: The Inflation vs Unemployment scatter plot
    """
    fig = px.scatter(
        df,
        x='Inflation',
        y='Unemployment_Rate',
        color='Country',
        color_discrete_map=COUNTRY_COLORS,
        title='Inflation vs Unemployment Rate',
        labels={
            'Inflation': 'Inflation (%)',
            'Unemployment_Rate': 'Unemployment Rate (%)',
            'Country': 'Country'
        },
        hover_data={
            'Country': True,
            'Year': True,
            'Inflation': ':.2f',
            'Unemployment_Rate': ':.2f'
        },
        trendline='ols' if show_trendline else None
    )
    
    fig.update_traces(
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Year: %{customdata[0]}<br>' +
                      'Inflation: %{x:.2f}%<br>' +
                      'Unemployment Rate: %{y:.2f}%<br>' +
                      '<extra></extra>'
    )
    
    # Add correlation annotation if available
    if corr_df is not None:
        overall_corr = corr_df[
            (corr_df['Variable_X'] == 'Inflation') & 
            (corr_df['Variable_Y'] == 'Unemployment_Rate') &
            (corr_df['Scope'] == 'Overall (all countries)')
        ]
        
        if not overall_corr.empty:
            corr_value = overall_corr.iloc[0]['Correlation']
            n_value = overall_corr.iloc[0]['N']
            
            fig.add_annotation(
                text=f'Overall Correlation: {corr_value:.3f}<br>N={n_value}',
                xref='paper',
                yref='paper',
                x=0.02,
                y=0.98,
                showarrow=False,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='gray',
                borderwidth=1,
                font=dict(size=10)
            )
    
    fig.update_layout(
        xaxis=dict(
            title='Inflation (%)',
            zeroline=True
        ),
        yaxis=dict(
            title='Unemployment Rate (%)',
            range=[0, df['Unemployment_Rate'].max() * 1.1]
        ),
        hovermode='closest',
        legend=dict(
            title='Country',
            orientation='v',
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=0.01
        ),
        template='plotly_white'
    )
    
    return fig


def create_country_specific_scatter(df, country, corr_df=None):
    """
    Create scatter plot for a specific country with its correlation.
    
    Parameters:
        df: DataFrame with unemployment data
        country: Country name (str)
        corr_df: DataFrame with correlation results (optional)
    
    Returns:
        plotly.graph_objects.Figure: Country-specific scatter plot
    """
    df_country = df[df['Country'] == country].copy()
    
    fig = px.scatter(
        df_country,
        x='Inflation',
        y='Unemployment_Rate',
        title=f'Inflation vs Unemployment Rate - {country}',
        labels={
            'Inflation': 'Inflation (%)',
            'Unemployment_Rate': 'Unemployment Rate (%)'
        },
        hover_data={
            'Year': True,
            'Inflation': ':.2f',
            'Unemployment_Rate': ':.2f'
        },
        color_discrete_sequence=[COUNTRY_COLORS.get(country, '#1f77b4')],
        trendline='ols'
    )
    
    fig.update_traces(
        hovertemplate=f'<b>{country}</b><br>' +
                      'Year: %{{customdata[0]}}<br>' +
                      'Inflation: %{{x:.2f}}%<br>' +
                      'Unemployment Rate: %{{y:.2f}}%<br>' +
                      '<extra></extra>'
    )
    
    # Add country-specific correlation if available
    # Note: correlation_results.csv only has GDP correlations, not inflation by country
    # So we'll skip country-specific correlation annotation for inflation
    fig.update_layout(
        xaxis=dict(
            title='Inflation (%)',
            zeroline=True
        ),
        yaxis=dict(
            title='Unemployment Rate (%)',
            range=[0, df_country['Unemployment_Rate'].max() * 1.1]
        ),
        showlegend=False,
        template='plotly_white'
    )
    
    return fig


def get_chart(show_trendline=False, country=None):
    """
    Main function to create and return the chart.
    
    Parameters:
        show_trendline: Whether to show overall trendline (bool)
        country: Optional country name for country-specific view (str)
    
    Returns:
        plotly.graph_objects.Figure: The Inflation vs Unemployment scatter plot
    """
    df = load_data()
    corr_df = load_correlation_data()
    
    if country:
        fig = create_country_specific_scatter(df, country, corr_df)
    else:
        fig = create_inflation_unemployment_scatter(df, corr_df, show_trendline)
    
    return fig


def get_available_countries(df):
    """Get list of available countries in the dataset."""
    return sorted(df['Country'].unique().tolist())


if __name__ == '__main__':
    df = load_data()
    print("Available countries:", get_available_countries(df))
    
    # Example: Show overall scatter plot
    fig = get_chart(show_trendline=True)
    fig.show()
    
    # Example: Show country-specific plot
    fig = get_chart(country='Vietnam')
    fig.show()
