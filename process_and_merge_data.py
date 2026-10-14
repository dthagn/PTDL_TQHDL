"""
Validate, clean, and merge World Bank data into final dataset.
"""

import pandas as pd
import os
from datetime import datetime
import json

# Country code mapping (World Bank to standard ISO 3166-1 alpha-3)
COUNTRY_CODE_MAP = {
    'JP': 'JPN',
    'KR': 'KOR',
    'PH': 'PHL',
    'TH': 'THA',
    'VN': 'VNM'
}

# Country name mapping
COUNTRY_NAME_MAP = {
    'Japan': 'Japan',
    'Korea, Rep.': 'South Korea',
    'Philippines': 'Philippines',
    'Thailand': 'Thailand',
    'Viet Nam': 'Vietnam'
}

# Expected year range
START_YEAR = 2010
END_YEAR = 2024
EXPECTED_YEARS = list(range(START_YEAR, END_YEAR + 1))
EXPECTED_COUNTRIES = ['Japan', 'South Korea', 'Philippines', 'Thailand', 'Vietnam']

def load_raw_data():
    """Load all raw World Bank CSV files."""
    data_dir = 'data/raw/worldbank'
    files = os.listdir(data_dir)
    
    datasets = {}
    for file in files:
        if file.endswith('_wb.csv'):
            indicator_name = file.replace('_wb.csv', '').replace('_', ' ').title()
            df = pd.read_csv(os.path.join(data_dir, file))
            datasets[indicator_name] = df
            print(f"Loaded {indicator_name}: {len(df)} records")
    
    return datasets

def validate_dataset(df, indicator_name):
    """Validate a single dataset."""
    issues = []
    
    # Get the actual value column (first column that's not Country, Country_Code, Year, Indicator_Code)
    value_cols = [col for col in df.columns if col not in ['Country', 'Country_Code', 'Year', 'Indicator_Code']]
    if not value_cols:
        issues.append(f"No value column found for {indicator_name}")
        return issues
    
    value_col = value_cols[0]
    
    # Check country
    unique_countries = df['Country'].unique()
    for country in unique_countries:
        if country not in COUNTRY_NAME_MAP:
            issues.append(f"Unexpected country: {country}")
    
    # Check year range
    years = df['Year'].unique()
    for year in years:
        if year < START_YEAR or year > END_YEAR:
            issues.append(f"Year out of range: {year}")
    
    # Check for duplicates
    duplicates = df.duplicated(subset=['Country', 'Year']).sum()
    if duplicates > 0:
        issues.append(f"Found {duplicates} duplicate records")
    
    # Check missing values
    missing = df[value_col].isna().sum()
    if missing > 0:
        issues.append(f"Found {missing} missing values")
    
    # Check datatype
    if not pd.api.types.is_numeric_dtype(df[value_col]):
        issues.append(f"Non-numeric values in {value_col}")
    
    # Check value ranges (basic sanity checks)
    if value_col in df.columns:
        values = df[value_col].dropna()
        if len(values) > 0:
            min_val = values.min()
            max_val = values.max()
            
            # Indicator-specific range checks
            if 'Unemployment_Rate' in value_col or 'Labor_Force_Participation' in value_col:
                if min_val < 0 or max_val > 100:
                    issues.append(f"Value range issue for {value_col}: min={min_val}, max={max_val}")
            elif 'GDP_Growth' in value_col:
                if min_val < -50 or max_val > 50:
                    issues.append(f"Unusual GDP growth values: min={min_val}, max={max_val}")
            elif 'Population' in value_col:
                if min_val < 0:
                    issues.append(f"Negative population value: {min_val}")
    
    return issues

def standardize_data(df, indicator_name):
    """Standardize column names and country codes."""
    df = df.copy()
    
    # Standardize country names
    df['Country'] = df['Country'].map(COUNTRY_NAME_MAP).fillna(df['Country'])
    
    # Standardize country codes
    df['Country_Code'] = df['Country_Code'].map(COUNTRY_CODE_MAP).fillna(df['Country_Code'])
    
    # Get the actual value column
    value_cols = [col for col in df.columns if col not in ['Country', 'Country_Code', 'Year', 'Indicator_Code']]
    if value_cols:
        value_col = value_cols[0]
        # Keep only necessary columns
        cols_to_keep = ['Country', 'Country_Code', 'Year', value_col]
        df = df[cols_to_keep]
    
    return df

def merge_datasets(datasets):
    """Merge all datasets into one final dataframe."""
    # Start with the first dataset
    indicator_names = list(datasets.keys())
    merged = datasets[indicator_names[0]].copy()
    
    # Merge with remaining datasets
    for indicator_name in indicator_names[1:]:
        df = datasets[indicator_name]
        merged = pd.merge(merged, df, on=['Country', 'Country_Code', 'Year'], how='outer')
    
    # Sort by Country and Year
    merged = merged.sort_values(['Country', 'Year']).reset_index(drop=True)
    
    return merged

def create_data_dictionary():
    """Create data dictionary with indicator definitions."""
    definitions = {
        'Country': {
            'description': 'Country name',
            'unit': 'N/A',
            'source': 'World Bank',
            'indicator_code': 'N/A',
            'definition': 'Full name of the country'
        },
        'Country_Code': {
            'description': 'ISO 3166-1 alpha-3 country code',
            'unit': 'N/A',
            'source': 'World Bank',
            'indicator_code': 'N/A',
            'definition': 'Three-letter country code according to ISO 3166-1 standard'
        },
        'Year': {
            'description': 'Calendar year',
            'unit': 'Year',
            'source': 'World Bank',
            'indicator_code': 'N/A',
            'definition': 'Calendar year for which the data is reported'
        },
        'Unemployment_Rate': {
            'description': 'Unemployment rate, total (% of total labor force)',
            'unit': 'Percent',
            'source': 'World Bank',
            'indicator_code': 'SL.UEM.TOTL.ZS',
            'definition': 'Unemployment refers to the share of the labor force that is without work but available for and seeking employment.'
        },
        'Youth_Unemployment_Rate': {
            'description': 'Unemployment rate, youth total (% of total labor force ages 15-24)',
            'unit': 'Percent',
            'source': 'World Bank',
            'indicator_code': 'SL.UEM.1524.ZS',
            'definition': 'Unemployment youth refers to the share of the labor force ages 15-24 without work but available for and seeking employment.'
        },
        'GDP_Growth': {
            'description': 'GDP growth (annual %)',
            'unit': 'Percent',
            'source': 'World Bank',
            'indicator_code': 'NY.GDP.MKTP.KD.ZG',
            'definition': 'Annual percentage growth rate of GDP at market prices based on constant local currency.'
        },
        'GDP_per_Capita': {
            'description': 'GDP per capita (current US$)',
            'unit': 'US Dollars',
            'source': 'World Bank',
            'indicator_code': 'NY.GDP.PCAP.CD',
            'definition': 'GDP per capita is gross domestic product divided by midyear population.'
        },
        'Inflation': {
            'description': 'Inflation, consumer prices (annual %)',
            'unit': 'Percent',
            'source': 'World Bank',
            'indicator_code': 'FP.CPI.TOTL.ZG',
            'definition': 'Annual percentage change in consumer price indices as measured by the consumer price index.'
        },
        'Labor_Force_Participation': {
            'description': 'Labor force participation rate, total (% of total population ages 15+)',
            'unit': 'Percent',
            'source': 'World Bank',
            'indicator_code': 'SL.TLF.CACT.ZS',
            'definition': 'Labor force participation rate is the proportion of the population ages 15 and older that is economically active.'
        },
        'Population': {
            'description': 'Population, total',
            'unit': 'People',
            'source': 'World Bank',
            'indicator_code': 'SP.POP.TOTL',
            'definition': 'Total population is based on the de facto definition of population, which counts all residents regardless of legal status.'
        }
    }
    
    df_dict = pd.DataFrame.from_dict(definitions, orient='index')
    df_dict.index.name = 'column'
    df_dict = df_dict.reset_index()
    
    return df_dict

def create_source_metadata():
    """Create source metadata file."""
    metadata = [
        {
            'variable': 'Unemployment_Rate',
            'source': 'World Bank',
            'URL': 'https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS',
            'indicator_code': 'SL.UEM.TOTL.ZS',
            'retrieval_date': datetime.now().strftime('%Y-%m-%d'),
            'definition': 'Unemployment refers to the share of the labor force that is without work but available for and seeking employment.',
            'notes': 'Modeled ILO estimate'
        },
        {
            'variable': 'Youth_Unemployment_Rate',
            'source': 'World Bank',
            'URL': 'https://data.worldbank.org/indicator/SL.UEM.1524.ZS',
            'indicator_code': 'SL.UEM.1524.ZS',
            'retrieval_date': datetime.now().strftime('%Y-%m-%d'),
            'definition': 'Unemployment youth refers to the share of the labor force ages 15-24 without work but available for and seeking employment.',
            'notes': 'Modeled ILO estimate'
        },
        {
            'variable': 'GDP_Growth',
            'source': 'World Bank',
            'URL': 'https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG',
            'indicator_code': 'NY.GDP.MKTP.KD.ZG',
            'retrieval_date': datetime.now().strftime('%Y-%m-%d'),
            'definition': 'Annual percentage growth rate of GDP at market prices based on constant local currency.',
            'notes': 'World Bank national accounts data'
        },
        {
            'variable': 'GDP_per_Capita',
            'source': 'World Bank',
            'URL': 'https://data.worldbank.org/indicator/NY.GDP.PCAP.CD',
            'indicator_code': 'NY.GDP.PCAP.CD',
            'retrieval_date': datetime.now().strftime('%Y-%m-%d'),
            'definition': 'GDP per capita is gross domestic product divided by midyear population.',
            'notes': 'Current US$'
        },
        {
            'variable': 'Inflation',
            'source': 'World Bank',
            'URL': 'https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG',
            'indicator_code': 'FP.CPI.TOTL.ZG',
            'retrieval_date': datetime.now().strftime('%Y-%m-%d'),
            'definition': 'Annual percentage change in consumer price indices as measured by the consumer price index.',
            'notes': 'World Bank national accounts data'
        },
        {
            'variable': 'Labor_Force_Participation',
            'source': 'World Bank',
            'URL': 'https://data.worldbank.org/indicator/SL.TLF.CACT.ZS',
            'indicator_code': 'SL.TLF.CACT.ZS',
            'retrieval_date': datetime.now().strftime('%Y-%m-%d'),
            'definition': 'Labor force participation rate is the proportion of the population ages 15 and older that is economically active.',
            'notes': 'Modeled ILO estimate'
        },
        {
            'variable': 'Population',
            'source': 'World Bank',
            'URL': 'https://data.worldbank.org/indicator/SP.POP.TOTL',
            'indicator_code': 'SP.POP.TOTL',
            'retrieval_date': datetime.now().strftime('%Y-%m-%d'),
            'definition': 'Total population is based on the de facto definition of population, which counts all residents regardless of legal status.',
            'notes': 'World Bank staff estimates'
        },
        {
            'variable': 'Male_Unemployment_Rate',
            'source': 'ILOSTAT',
            'URL': 'https://ilostat.ilo.org/',
            'indicator_code': 'UNE_RT_M',
            'retrieval_date': datetime.now().strftime('%Y-%m-%d'),
            'definition': 'Unemployment rate, male (% of male labor force)',
            'notes': 'NOT AVAILABLE - ILOSTAT API requires authentication. World Bank API did not provide gender-specific data for these countries. Variable excluded from final dataset.'
        },
        {
            'variable': 'Female_Unemployment_Rate',
            'source': 'ILOSTAT',
            'URL': 'https://ilostat.ilo.org/',
            'indicator_code': 'UNE_RT_F',
            'retrieval_date': datetime.now().strftime('%Y-%m-%d'),
            'definition': 'Unemployment rate, female (% of female labor force)',
            'notes': 'NOT AVAILABLE - ILOSTAT API requires authentication. World Bank API did not provide gender-specific data for these countries. Variable excluded from final dataset.'
        }
    ]
    
    return pd.DataFrame(metadata)

def create_validation_report(merged_df, datasets, validation_issues):
    """Create validation report in markdown format."""
    report = []
    
    report.append("# Data Validation Report")
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("\n## Dataset Overview")
    report.append(f"\n- **Total rows:** {len(merged_df)}")
    report.append(f"- **Total countries:** {merged_df['Country'].nunique()}")
    report.append(f"- **Countries:** {', '.join(sorted(merged_df['Country'].unique()))}")
    report.append(f"- **Year range:** {merged_df['Year'].min()} - {merged_df['Year'].max()}")
    report.append(f"- **Expected years:** {START_YEAR} - {END_YEAR}")
    report.append(f"- **Expected countries:** {', '.join(EXPECTED_COUNTRIES)}")
    
    report.append("\n## Data Coverage")
    report.append("\n### Records per Country")
    for country in sorted(merged_df['Country'].unique()):
        country_df = merged_df[merged_df['Country'] == country]
        years = country_df['Year'].sort_values().unique()
        report.append(f"\n**{country}:**")
        report.append(f"- Records: {len(country_df)}")
        report.append(f"- Years: {years.min()} - {years.max()}")
        report.append(f"- Missing years: {set(EXPECTED_YEARS) - set(years)}")
    
    report.append("\n### Missing Values by Variable")
    for col in merged_df.columns:
        if col not in ['Country', 'Country_Code', 'Year']:
            missing = merged_df[col].isna().sum()
            missing_pct = (missing / len(merged_df)) * 100
            report.append(f"\n**{col}:**")
            report.append(f"- Missing: {missing} ({missing_pct:.2f}%)")
            report.append(f"- Available: {len(merged_df) - missing} ({100 - missing_pct:.2f}%)")
    
    report.append("\n## Data Quality Checks")
    
    # Check for duplicates
    duplicates = merged_df.duplicated(subset=['Country', 'Year']).sum()
    report.append(f"\n### Duplicates")
    report.append(f"- Duplicate Country-Year pairs: {duplicates}")
    
    # Check data types
    report.append(f"\n### Data Types")
    for col in merged_df.columns:
        dtype = merged_df[col].dtype
        report.append(f"- {col}: {dtype}")
    
    # Check value ranges
    report.append(f"\n### Value Range Summary")
    for col in merged_df.columns:
        if col not in ['Country', 'Country_Code', 'Year']:
            if pd.api.types.is_numeric_dtype(merged_df[col]):
                report.append(f"\n**{col}:**")
                report.append(f"- Min: {merged_df[col].min():.2f}")
                report.append(f"- Max: {merged_df[col].max():.2f}")
                report.append(f"- Mean: {merged_df[col].mean():.2f}")
    
    report.append("\n## Validation Issues")
    if validation_issues:
        for indicator, issues in validation_issues.items():
            if issues:
                report.append(f"\n### {indicator}")
                for issue in issues:
                    report.append(f"- {issue}")
    else:
        report.append("\nNo validation issues detected.")
    
    report.append("\n## Excluded Variables")
    report.append("\nThe following variables were excluded from the final dataset:")
    report.append("\n- **Male_Unemployment_Rate:** Not available from World Bank API for these countries. ILOSTAT API requires authentication.")
    report.append("- **Female_Unemployment_Rate:** Not available from World Bank API for these countries. ILOSTAT API requires authentication.")
    
    report.append("\n## Data Sources")
    report.append("\nAll data sourced from World Bank API (api.worldbank.org)")
    report.append("\n- Unemployment indicators: Modeled ILO estimates")
    report.append("- Economic indicators: World Bank national accounts data")
    report.append("- Population: World Bank staff estimates")
    
    report.append("\n## Notes")
    report.append("\n- Data represents official estimates from World Bank")
    report.append("- Missing values indicate data not available from source")
    report.append("- No imputation or synthetic data generation performed")
    report.append("- Country codes standardized to ISO 3166-1 alpha-3 format")
    
    return '\n'.join(report)

def main():
    """Main processing function."""
    print("=" * 60)
    print("DATA PROCESSING AND MERGE")
    print("=" * 60)
    
    # Load raw data
    print("\n1. Loading raw data...")
    datasets = load_raw_data()
    
    # Validate each dataset
    print("\n2. Validating datasets...")
    validation_issues = {}
    for indicator_name, df in datasets.items():
        print(f"   Validating {indicator_name}...")
        issues = validate_dataset(df, indicator_name)
        validation_issues[indicator_name] = issues
        if issues:
            print(f"   Issues found: {len(issues)}")
            for issue in issues:
                print(f"     - {issue}")
        else:
            print(f"   No issues found")
    
    # Standardize data
    print("\n3. Standardizing data...")
    standardized_datasets = {}
    for indicator_name, df in datasets.items():
        standardized_datasets[indicator_name] = standardize_data(df, indicator_name)
        print(f"   Standardized {indicator_name}")
    
    # Merge datasets
    print("\n4. Merging datasets...")
    merged = merge_datasets(standardized_datasets)
    print(f"   Merged dataset: {len(merged)} rows, {len(merged.columns)} columns")
    
    # Save merged dataset
    output_file = 'data/processed/unemployment_final.csv'
    merged.to_csv(output_file, index=False)
    print(f"   Saved to {output_file}")
    
    # Create data dictionary
    print("\n5. Creating data dictionary...")
    data_dict = create_data_dictionary()
    data_dict.to_csv('data/processed/data_dictionary.csv', index=False)
    print("   Saved to data/processed/data_dictionary.csv")
    
    # Create source metadata
    print("\n6. Creating source metadata...")
    source_metadata = create_source_metadata()
    source_metadata.to_csv('data/processed/source_metadata.csv', index=False)
    print("   Saved to data/processed/source_metadata.csv")
    
    # Create validation report
    print("\n7. Creating validation report...")
    report = create_validation_report(merged, datasets, validation_issues)
    with open('data_validation_report.md', 'w') as f:
        f.write(report)
    print("   Saved to data_validation_report.md")
    
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    print(f"\nFinal dataset: {len(merged)} rows")
    print(f"Variables: {list(merged.columns)}")
    print(f"Countries: {', '.join(sorted(merged['Country'].unique()))}")
    print(f"Years: {merged['Year'].min()} - {merged['Year'].max()}")

if __name__ == "__main__":
    main()
