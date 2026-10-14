# Data Validation Report

**Generated:** 2026-09-21 22:21:40

## Dataset Overview

- **Total rows:** 75
- **Total countries:** 5
- **Countries:** Japan, Philippines, South Korea, Thailand, Vietnam
- **Year range:** 2010 - 2024
- **Expected years:** 2010 - 2024
- **Expected countries:** Japan, South Korea, Philippines, Thailand, Vietnam

## Data Coverage

### Records per Country

**Japan:**
- Records: 15
- Years: 2010 - 2024
- Missing years: set()

**Philippines:**
- Records: 15
- Years: 2010 - 2024
- Missing years: set()

**South Korea:**
- Records: 15
- Years: 2010 - 2024
- Missing years: set()

**Thailand:**
- Records: 15
- Years: 2010 - 2024
- Missing years: set()

**Vietnam:**
- Records: 15
- Years: 2010 - 2024
- Missing years: set()

### Missing Values by Variable

**GDP_Growth:**
- Missing: 0 (0.00%)
- Available: 75 (100.00%)

**GDP_per_Capita:**
- Missing: 0 (0.00%)
- Available: 75 (100.00%)

**Inflation:**
- Missing: 0 (0.00%)
- Available: 75 (100.00%)

**Labor_Force_Participation:**
- Missing: 0 (0.00%)
- Available: 75 (100.00%)

**Population:**
- Missing: 0 (0.00%)
- Available: 75 (100.00%)

**Unemployment_Rate:**
- Missing: 0 (0.00%)
- Available: 75 (100.00%)

**Youth_Unemployment_Rate:**
- Missing: 0 (0.00%)
- Available: 75 (100.00%)

## Data Quality Checks

### Duplicates
- Duplicate Country-Year pairs: 0

### Data Types
- Country: str
- Country_Code: str
- Year: int64
- GDP_Growth: float64
- GDP_per_Capita: float64
- Inflation: float64
- Labor_Force_Participation: float64
- Population: int64
- Unemployment_Rate: float64
- Youth_Unemployment_Rate: float64

### Value Range Summary

**GDP_Growth:**
- Min: -9.52
- Max: 8.54
- Mean: 3.60

**GDP_per_Capita:**
- Min: 1683.16
- Max: 49626.68
- Mean: 17005.55

**Inflation:**
- Min: -0.90
- Max: 18.68
- Mean: 2.61

**Labor_Force_Participation:**
- Min: 54.75
- Max: 77.48
- Mean: 65.68

**Population:**
- Min: 49554112.00
- Max: 128070000.00
- Mean: 90107648.12

**Unemployment_Rate:**
- Min: 0.25
- Max: 5.10
- Mean: 2.36

**Youth_Unemployment_Rate:**
- Min: 1.23
- Max: 10.14
- Mean: 6.30

## Validation Issues

## Excluded Variables

The following variables were excluded from the final dataset:

- **Male_Unemployment_Rate:** Not available from World Bank API for these countries. ILOSTAT API requires authentication.
- **Female_Unemployment_Rate:** Not available from World Bank API for these countries. ILOSTAT API requires authentication.

## Data Sources

All data sourced from World Bank API (api.worldbank.org)

- Unemployment indicators: Modeled ILO estimates
- Economic indicators: World Bank national accounts data
- Population: World Bank staff estimates

## Notes

- Data represents official estimates from World Bank
- Missing values indicate data not available from source
- No imputation or synthetic data generation performed
- Country codes standardized to ISO 3166-1 alpha-3 format