# Visualization Specification

This document describes all charts created for the unemployment analysis dashboard.

---

## Chart 1: Unemployment Trend

**File:** `unemployment_trend.py`

**Objective:** Show the trend of unemployment rates from 2010-2024 across 5 Asian countries.

**Chart Type:** Line chart

**Variables:**
- X-axis: Year (2010-2024)
- Y-axis: Unemployment Rate (%)
- Color: Country

**Filters:** None (shows all years and all countries)

**Tooltip:**
- Country
- Year
- Unemployment Rate (%)

**Reason for Chart Choice:** Line chart is ideal for time series data to show trends and changes over time. It allows easy comparison of unemployment trajectories across countries.

**Data Source:** `data/processed/unemployment_final.csv`

**Key Features:**
- Consistent color scheme across all countries
- Markers on each data point for clarity
- Y-axis range adjusted to data values
- Hover mode unified for easy comparison

---

## Chart 2: Country Comparison

**File:** `country_comparison.py`

**Objective:** Compare unemployment rates between 5 countries with optional year and period filters.

**Chart Type:** Bar chart

**Variables:**
- X-axis: Country
- Y-axis: Unemployment Rate (%)
- Color: Country

**Filters:**
- Year: Optional (single year selection)
- Period: Optional (Pre-COVID 2010-2019, COVID 2020-2021, Recovery 2022-2024)
- Default: Shows most recent year if no filter selected

**Tooltip:**
- Country
- Unemployment Rate (%)

**Reason for Chart Choice:** Bar chart is best for comparing categorical data (countries) and allows easy ranking of unemployment rates.

**Data Source:** `data/processed/unemployment_final.csv`

**Key Features:**
- Text labels showing exact values on bars
- Period column added for filtering (Pre-COVID, COVID, Recovery)
- Aggregates multiple rows per country when needed
- No legend needed (color is redundant with x-axis)

---

## Chart 3: Unemployment Map

**File:** `unemployment_map.py`

**Objective:** Display unemployment rates geographically using a choropleth map.

**Chart Type:** Choropleth map

**Variables:**
- Location: Country (using ISO country codes)
- Color: Unemployment Rate (%)

**Filters:**
- Year: Optional (single year selection)
- Default: Shows most recent year if no filter selected

**Tooltip:**
- Country
- Year
- Unemployment Rate (%)

**Reason for Chart Choice:** Choropleth map provides geographic context and allows visual assessment of regional patterns in unemployment.

**Data Source:** `data/processed/unemployment_final.csv`

**Key Features:**
- Uses standard ISO country codes (JPN, PHL, KOR, THA, VNM)
- Natural earth projection for accurate geography
- Continuous color scale (Viridis) for unemployment rates
- Colorbar with unit (%)

**ISO Country Codes:**
- Japan: JPN
- Philippines: PHL
- South Korea: KOR
- Thailand: THA
- Vietnam: VNM

---

## Chart 4: GDP vs Unemployment

**File:** `gdp_unemployment.py`

**Objective:** Explore the relationship between GDP Growth and Unemployment Rate with correlation information.

**Chart Type:** Scatter plot

**Variables:**
- X-axis: GDP Growth (%)
- Y-axis: Unemployment Rate (%)
- Color: Country

**Filters:**
- Country: Optional (for country-specific view)
- Trendline: Optional (OLS trendline for overall view)

**Tooltip:**
- Country
- Year
- GDP Growth (%)
- Unemployment Rate (%)

**Reason for Chart Choice:** Scatter plot is ideal for examining relationships between two continuous variables. It allows visualization of correlation patterns.

**Data Source:** 
- `data/processed/unemployment_final.csv`
- `analysis/correlation_results.csv` (for correlation values)

**Key Features:**
- Displays overall correlation coefficient from analysis
- Country-specific view available with individual correlation
- Optional OLS trendline
- Zero lines on both axes for reference

**Correlation Information:**
- Overall correlation: -0.117 (weak negative)
- Country-specific correlations vary significantly
- Correlation values sourced from Agent 2 analysis

**Important Note:** Correlation does not imply causation. This chart shows statistical relationships only.

---

## Chart 5: Youth vs Overall Unemployment

**File:** `youth_unemployment.py`

**Objective:** Compare youth unemployment rates with overall unemployment rates over time.

**Chart Type:** Line chart (two views available)

**View 1: Comparison Chart**
- Variables:
  - X-axis: Year (2010-2024)
  - Y-axis: Unemployment Rate (%)
  - Lines: Youth Unemployment Rate vs Overall Unemployment Rate

**View 2: Youth Gap Chart**
- Variables:
  - X-axis: Year (2010-2024)
  - Y-axis: Youth Gap (percentage points)
  - Youth Gap = Youth_Unemployment_Rate - Unemployment_Rate

**Filters:**
- Country: Optional (for country-specific view)
- Default: Shows average across all countries

**Tooltip:**
- Country
- Year
- Rate (%) or Gap (pp)

**Reason for Chart Choice:** Line chart allows comparison of two time series. Youth gap chart highlights the difference between youth and overall unemployment.

**Data Source:** `data/processed/unemployment_final.csv`

**Key Features:**
- Two chart types: comparison and gap
- Country-specific or overall average view
- Consistent colors: blue for overall, orange for youth
- Gap chart shows zero line for reference

**Youth Gap Definition:** Youth Gap = Youth_Unemployment_Rate - Unemployment_Rate (in percentage points)

---

## Chart 6: Inflation vs Unemployment

**File:** `inflation_unemployment.py`

**Objective:** Explore the relationship between Inflation and Unemployment Rate.

**Chart Type:** Scatter plot

**Variables:**
- X-axis: Inflation (%)
- Y-axis: Unemployment Rate (%)
- Color: Country

**Filters:**
- Country: Optional (for country-specific view)
- Trendline: Optional (OLS trendline for overall view)

**Tooltip:**
- Country
- Year
- Inflation (%)
- Unemployment Rate (%)

**Reason for Chart Choice:** Scatter plot is ideal for examining relationships between two continuous variables.

**Data Source:** 
- `data/processed/unemployment_final.csv`
- `analysis/correlation_results.csv` (for overall correlation)

**Key Features:**
- Displays overall correlation coefficient from analysis
- Country-specific view available
- Optional OLS trendline
- Zero lines on both axes for reference

**Correlation Information:**
- Overall correlation: -0.259 (weak to moderate negative)
- Country-specific correlations not available in correlation_results.csv

**Important Note:** Correlation does not imply causation. This chart shows statistical relationships only.

---

## Charts Not Created

### Gender Unemployment Chart

**Status:** NOT CREATED

**Reason:** Gender-specific unemployment data (Male_Unemployment_Rate, Female_Unemployment_Rate) is not available in the dataset. According to `analysis/findings.md`, ILOSTAT API requires authentication and World Bank API did not provide gender-specific data for these countries. These variables were excluded from the final dataset.

**Alternative:** Gender gap analysis cannot be performed with available data.

---

### Education Unemployment Chart

**Status:** NOT CREATED

**Reason:** Education-related variables (Education_Level, Education_Unemployment_Rate) were not included in the final dataset as they were not reliably available for all 5 countries through the World Bank API. The PROJECT_SPEC indicates these variables could be supplemented "when there is actual data that is sufficiently reliable and has compatible definitions," but such data was not available for this analysis.

**Alternative:** Education analysis unavailable due to insufficient compatible data.

---

## Design Principles Applied

### Consistent Color Scheme
All charts use the same color mapping for countries:
- Japan: #1f77b4 (blue)
- Philippines: #ff7f0e (orange)
- South Korea: #2ca02c (green)
- Thailand: #d62728 (red)
- Vietnam: #9467bd (purple)

### Chart Elements
Each chart includes:
- Title
- Axis labels with units
- Legend where appropriate
- Tooltips with relevant information
- Readable scale and range
- Template: plotly_white for clean appearance

### Data Integrity
- All charts use real data from `data/processed/unemployment_final.csv`
- No hard-coded values
- No mock data
- Charts dynamically load from CSV files
- Correlation values sourced from Agent 2 analysis

### Reusable Functions
Each chart file includes:
- `load_data()` function to load data
- `get_chart()` function as main entry point
- Helper functions for specific chart types
- Optional filter parameters
- Example usage in `__main__` block

---

## Dependencies

All charts require:
- Python 3.x
- pandas
- plotly
- plotly.graph_objects

Data files required:
- `data/processed/unemployment_final.csv`
- `analysis/correlation_results.csv` (for correlation charts)

---

## Handoff to Agent 4

All visualization files have been created in the `charts/` directory:
- `unemployment_trend.py`
- `country_comparison.py`
- `unemployment_map.py`
- `gdp_unemployment.py`
- `youth_unemployment.py`
- `inflation_unemployment.py`
- `visualization_spec.md` (this file)

Charts are ready for integration into Streamlit dashboard by Agent 4.

**Visualization completed by Agent 3 (Visualization Specialist)**
**Date:** 2026-09-21
**Data scope:** 5 Asian countries (Japan, Philippines, South Korea, Thailand, Vietnam), 2010-2024
