"""
Download World Bank data for unemployment and economic indicators.
Countries: Vietnam (VNM), Thailand (THA), Japan (JPN), South Korea (KOR), Philippines (PHL)
Time period: 2010-2024
"""

import requests
import pandas as pd
from datetime import datetime
import json

# World Bank indicator codes
INDICATORS = {
    'Unemployment_Rate': 'SL.UEM.TOTL.ZS',
    'Youth_Unemployment_Rate': 'SL.UEM.1524.ZS',
    'Male_Unemployment_Rate': 'SL.UEM.MA.ZS',
    'Female_Unemployment_Rate': 'SL.UEM.FE.ZS',
    'GDP_Growth': 'NY.GDP.MKTP.KD.ZG',
    'GDP_per_Capita': 'NY.GDP.PCAP.CD',
    'Inflation': 'FP.CPI.TOTL.ZG',
    'Labor_Force_Participation': 'SL.TLF.CACT.ZS',
    'Population': 'SP.POP.TOTL'
}

# Country codes
COUNTRIES = ['VNM', 'THA', 'JPN', 'KOR', 'PHL']

# Year range
START_YEAR = 2010
END_YEAR = 2024

def download_indicator(indicator_name, indicator_code):
    """Download data for a single indicator from World Bank API."""
    url = f"http://api.worldbank.org/v2/country/{';'.join(COUNTRIES)}/indicator/{indicator_code}"
    params = {
        'format': 'json',
        'per_page': 1000,
        'date': f'{START_YEAR}:{END_YEAR}'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if len(data) < 2 or not data[1]:
            print(f"Warning: No data for {indicator_name} ({indicator_code})")
            return None
        
        # Parse data
        records = []
        for item in data[1]:
            if item['value'] is not None:
                year = int(item['date'])
                if START_YEAR <= year <= END_YEAR:
                    records.append({
                        'Country': item['country']['value'],
                        'Country_Code': item['country']['id'],
                        'Year': year,
                        indicator_name: item['value'],
                        'Indicator_Code': indicator_code
                    })
        
        if not records:
            print(f"Warning: No valid records for {indicator_name} in year range")
            return None
        
        df = pd.DataFrame(records)
        print(f"Downloaded {len(df)} records for {indicator_name}")
        return df
        
    except Exception as e:
        print(f"Error downloading {indicator_name}: {e}")
        return None

def main():
    """Download all indicators and save to CSV files."""
    retrieval_date = datetime.now().strftime('%Y-%m-%d')
    
    # Download each indicator
    for indicator_name, indicator_code in INDICATORS.items():
        print(f"\nDownloading {indicator_name} ({indicator_code})...")
        df = download_indicator(indicator_name, indicator_code)
        
        if df is not None:
            # Save to CSV
            filename = f"data/raw/worldbank/{indicator_name.lower()}_wb.csv"
            df.to_csv(filename, index=False)
            print(f"Saved to {filename}")
            
            # Save metadata
            metadata = {
                'variable': indicator_name,
                'source': 'World Bank',
                'indicator_code': indicator_code,
                'retrieval_date': retrieval_date,
                'countries': COUNTRIES,
                'year_range': f"{START_YEAR}-{END_YEAR}",
                'records': len(df)
            }
            
            metadata_filename = f"data/raw/worldbank/{indicator_name.lower()}_metadata.json"
            with open(metadata_filename, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"Saved metadata to {metadata_filename}")
    
    print("\nDownload complete!")

if __name__ == "__main__":
    main()
