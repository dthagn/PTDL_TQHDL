"""
Youth vs Overall Unemployment Chart
Line chart comparing youth unemployment rate with overall unemployment rate.
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


def create_youth_unemployment_comparison(df, country=None):
    """
    Create line chart comparing youth unemployment with overall unemployment.
    
    X-axis: Year
    Y-axis: Unemployment Rate (%)
    Lines: Youth Unemployment Rate vs Overall Unemployment Rate
    
    Parameters:
        df: DataFrame with unemployment data
        country: Optional country filter (str). If None, shows overall average.
    
    Returns:
        plotly.graph_objects.Figure: The youth vs overall unemployment comparison chart
    """
    df_filtered = df.copy()
    
    if country:
        df_filtered = df_filtered[df_filtered['Country'] == country]
        title_suffix = f'- {country}'
    else:
        # Calculate yearly averages across all countries
        df_filtered = df_filtered.groupby('Year').agg({
            'Unemployment_Rate': 'mean',
            'Youth_Unemployment_Rate': 'mean'
        }).reset_index()
        df_filtered['Country'] = 'Overall Average'
        title_suffix = '- All Countries (Average)'
    
    # Melt data for line chart
    df_melted = df_filtered.melt(
        id_vars=['Year', 'Country'],
        value_vars=['Unemployment_Rate', 'Youth_Unemployment_Rate'],
        var_name='Unemployment_Type',
        value_name='Rate'
    )
    
    # Rename for display
    df_melted['Unemployment_Type'] = df_melted['Unemployment_Type'].replace({
        'Unemployment_Rate': 'Overall Unemployment',
        'Youth_Unemployment_Rate': 'Youth Unemployment'
    })
    
    fig = px.line(
        df_melted,
        x='Year',
        y='Rate',
        color='Unemployment_Type',
        title=f'Youth vs Overall Unemployment Rate {title_suffix}',
        labels={
            'Year': 'Year',
            'Rate': 'Unemployment Rate (%)',
            'Unemployment_Type': 'Unemployment Type'
        },
        markers=True,
        line_dash='Unemployment_Type',
        color_discrete_map={
            'Overall Unemployment': '#1f77b4',
            'Youth Unemployment': '#ff7f0e'
        },
        hover_data={
            'Country': True,
            'Year': True,
            'Rate': ':.2f'
        }
    )
    
    fig.update_traces(
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Country: %{customdata[0]}<br>' +
                      'Year: %{x}<br>' +
                      'Rate: %{y:.2f}%<br>' +
                      '<extra></extra>'
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
            range=[0, df_melted['Rate'].max() * 1.1]
        ),
        hovermode='x unified',
        legend=dict(
            title='Unemployment Type',
            orientation='v',
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=0.01
        ),
        template='plotly_white'
    )
    
    return fig


def create_youth_gap_chart(df, country=None):
    """
    Create line chart showing youth gap over time.
    
    Youth Gap = Youth_Unemployment_Rate - Unemployment_Rate
    
    Parameters:
        df: DataFrame with unemployment data
        country: Optional country filter (str). If None, shows overall average.
    
    Returns:
        plotly.graph_objects.Figure: The youth gap chart
    """
    df_filtered = df.copy()
    
    # Calculate youth gap
    df_filtered['Youth_Gap'] = df_filtered['Youth_Unemployment_Rate'] - df_filtered['Unemployment_Rate']
    
    if country:
        df_filtered = df_filtered[df_filtered['Country'] == country]
        title_suffix = f'- {country}'
        color = COUNTRY_COLORS.get(country, '#1f77b4')
    else:
        # Calculate yearly averages across all countries
        df_filtered = df_filtered.groupby('Year').agg({
            'Youth_Gap': 'mean'
        }).reset_index()
        df_filtered['Country'] = 'Overall Average'
        title_suffix = '- All Countries (Average)'
        color = '#1f77b4'
    
    fig = px.line(
        df_filtered,
        x='Year',
        y='Youth_Gap',
        title=f'Youth Gap (Youth - Overall) {title_suffix}',
        labels={
            'Year': 'Year',
            'Youth_Gap': 'Youth Gap (percentage points)'
        },
        markers=True,
        color_discrete_sequence=[color],
        hover_data={
            'Country': True,
            'Year': True,
            'Youth_Gap': ':.2f'
        }
    )
    
    fig.update_traces(
        hovertemplate='<b>Youth Gap</b><br>' +
                      'Country: %{customdata[0]}<br>' +
                      'Year: %{x}<br>' +
                      'Gap: %{y:.2f} pp<br>' +
                      '<extra></extra>'
    )
    
    fig.update_layout(
        xaxis=dict(
            title='Year',
            tickmode='linear',
            dtick=1,
            range=[2009.5, 2024.5]
        ),
        yaxis=dict(
            title='Youth Gap (percentage points)',
            zeroline=True
        ),
        hovermode='x unified',
        showlegend=False,
        template='plotly_white'
    )
    
    return fig


def get_chart(chart_type='comparison', country=None):
    """
    Main function to create and return the chart.
    
    Parameters:
        chart_type: Type of chart ('comparison' or 'gap')
        country: Optional country filter (str)
    
    Returns:
        plotly.graph_objects.Figure: The youth unemployment chart
    """
    df = load_data()
    
    if chart_type == 'comparison':
        fig = create_youth_unemployment_comparison(df, country)
    elif chart_type == 'gap':
        fig = create_youth_gap_chart(df, country)
    else:
        raise ValueError("chart_type must be 'comparison' or 'gap'")
    
    return fig


def get_available_countries(df):
    """Get list of available countries in the dataset."""
    return sorted(df['Country'].unique().tolist())


if __name__ == '__main__':
    df = load_data()
    print("Available countries:", get_available_countries(df))
    
    # Example: Show comparison chart for all countries
    fig = get_chart(chart_type='comparison')
    fig.show()
    
    # Example: Show comparison chart for specific country
    fig = get_chart(chart_type='comparison', country='Vietnam')
    fig.show()
    
    # Example: Show youth gap chart for all countries
    fig = get_chart(chart_type='gap')
    fig.show()
