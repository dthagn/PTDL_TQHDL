"""
Unemployment Trend Chart (2010-2024)
Line chart showing unemployment rate trends for 5 Asian countries.
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


def create_unemployment_trend(df):
    """
    Create line chart showing unemployment rate trends from 2010-2024.
    
    X-axis: Year
    Y-axis: Unemployment Rate (%)
    Color: Country
    
    Returns:
        plotly.graph_objects.Figure: The unemployment trend chart
    """
    fig = px.line(
        df,
        x='Year',
        y='Unemployment_Rate',
        color='Country',
        color_discrete_map=COUNTRY_COLORS,
        title='Unemployment Rate Trends (2010-2024)',
        labels={
            'Year': 'Year',
            'Unemployment_Rate': 'Unemployment Rate (%)',
            'Country': 'Country'
        },
        markers=True,
        hover_data={
            'Country': True,
            'Year': True,
            'Unemployment_Rate': ':.2f'
        }
    )
    
    fig.update_layout(
        xaxis=dict(
            title='Year',
            tickmode='linear',
            dtick=1,
            range=[2009.5, 2024.5]
        ),
        yaxis=dict(
            title='Unemployment Rate (%)',
            range=[0, df['Unemployment_Rate'].max() * 1.2]
        ),
        hovermode='x unified',
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
    
    fig.update_traces(
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Year: %{x}<br>' +
                      'Unemployment Rate: %{y:.2f}%<br>' +
                      '<extra></extra>'
    )
    
    return fig


def get_chart():
    """Main function to create and return the chart."""
    df = load_data()
    fig = create_unemployment_trend(df)
    return fig


if __name__ == '__main__':
    fig = get_chart()
    fig.show()
