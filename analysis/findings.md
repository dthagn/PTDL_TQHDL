# Data Analysis Findings

## 1. Data Overview

**Scope:** 5 Asian countries (Japan, Philippines, South Korea, Thailand, Vietnam) from 2010-2024

**Data Coverage:**
- Number of countries: 5
- Number of years: 15 (2010-2024)
- Total rows: 75
- Country coverage: 100% (all 5 countries have complete data for all 15 years)

**Missing Data:**
- No missing values in key variables (Unemployment_Rate, Youth_Unemployment_Rate, GDP_Growth, Inflation, GDP_per_Capita, Labor_Force_Participation, Population)
- Data completeness: 100%

**Data Distribution (Overall):**
- Unemployment_Rate: Mean 2.357%, Median 2.522%, Std 1.164%, Range 0.249% - 5.102%
- Youth_Unemployment_Rate: Mean 6.296%, Median 6.434%, Std 2.250%, Range 1.231% - 10.145%
- GDP_Growth: Mean 3.596%, Median 3.433%, Std 3.222%, Range -9.518% - 8.538%
- Inflation: Mean 2.607%, Median 2.393%, Std 2.793%, Range -0.898% - 18.678%

**Data Sources:**
- All variables sourced from World Bank
- Gender-specific unemployment data (Male_Unemployment_Rate, Female_Unemployment_Rate) were not available due to ILOSTAT API authentication requirements and World Bank API limitations for these countries. These variables were excluded from the final dataset.

---

## 2. Main Trends

### Overall Unemployment Trend (2010-2024)
- 2010: 2.753%
- 2011: 2.559%
- 2012: 2.456%
- 2013: 2.433%
- 2014: 2.421%
- 2015: 2.489%
- 2016: 2.403%
- 2017: 2.346%
- 2018: 2.111%
- 2019: 2.146%
- 2020: 2.493%
- 2021: 2.689%
- 2022: 2.116%
- 2023: 1.971%
- 2024: 1.974%

**Key Observations:**
- Unemployment rate showed a general declining trend from 2010 to 2019 (2.753% to 2.146%)
- A slight increase occurred during 2020-2021 (COVID period), peaking at 2.689% in 2021
- Post-2021, unemployment declined to its lowest levels in 2023-2024 (around 1.97%)

---

## 3. Country Comparison

### Average Unemployment Rate by Country (2010-2024)
1. South Korea: 3.305%
2. Japan: 3.275%
3. Philippines: 2.907%
4. Vietnam: 1.562%
5. Thailand: 0.737%

**Country-Specific Changes by Period:**

**Japan:**
- Pre-COVID (2010-2019): 3.579%
- COVID (2020-2021): 2.808% (change: -0.771 pp)
- Recovery (2022-2024): 2.571% (change: -0.237 pp)

**Philippines:**
- Pre-COVID (2010-2019): 3.069%
- COVID (2020-2021): 2.960% (change: -0.109 pp)
- Recovery (2022-2024): 2.333% (change: -0.627 pp)

**South Korea:**
- Pre-COVID (2010-2019): 3.370%
- COVID (2020-2021): 3.785% (change: +0.415 pp)
- Recovery (2022-2024): 2.772% (change: -1.013 pp)

**Thailand:**
- Pre-COVID (2010-2019): 0.628%
- COVID (2020-2021): 1.157% (change: +0.529 pp)
- Recovery (2022-2024): 0.818% (change: -0.339 pp)

**Vietnam:**
- Pre-COVID (2010-2019): 1.412%
- COVID (2020-2021): 2.243% (change: +0.831 pp)
- Recovery (2022-2024): 1.606% (change: -0.637 pp)

**Key Findings:**
- Thailand consistently had the lowest unemployment rate across all periods
- South Korea had the highest unemployment rate during the COVID period
- Japan showed a unique pattern with declining unemployment during COVID
- Vietnam experienced the largest increase during COVID (+0.831 pp)
- South Korea showed the largest decline during recovery (-1.013 pp)

---

## 4. COVID Period Analysis

### Period Comparison

| Period | Avg Unemployment | Avg Youth Unemployment | Avg GDP Growth | Avg Inflation | N |
|--------|------------------|------------------------|----------------|---------------|---|
| Pre-COVID (2010-2019) | 2.412% | 6.396% | 4.281% | 2.575% | 50 |
| COVID (2020-2021) | 2.591% | 6.751% | 0.027% | 1.454% | 10 |
| Recovery (2022-2024) | 2.020% | 5.659% | 3.689% | 3.484% | 15 |

**Changes:**
- Pre-COVID to COVID: +0.179 percentage points in unemployment
- COVID to Recovery: -0.571 percentage points in unemployment
- Pre-COVID to Recovery: -0.392 percentage points in unemployment

**Key Observations:**
- Unemployment increased slightly during the COVID period (+0.179 pp)
- GDP growth dropped dramatically during COVID (from 4.281% to 0.027%)
- Unemployment declined significantly during the recovery period (-0.571 pp)
- Recovery period shows the lowest unemployment rate (2.020%) despite moderate GDP growth (3.689%)

---

## 5. Gender Analysis

**Data Limitation:**
- Male_Unemployment_Rate and Female_Unemployment_Rate are NOT available in the dataset
- According to source_metadata.csv, ILOSTAT API requires authentication and World Bank API did not provide gender-specific data for these countries
- These variables were excluded from the final dataset
- Gender gap analysis cannot be performed with the available data

---

## 6. Youth Unemployment Analysis

### Youth Gap Definition
Youth Gap = Youth_Unemployment_Rate - Unemployment_Rate (in percentage points)

### Overall Youth Gap
- Mean: 3.939 percentage points
- Median: 4.215 percentage points
- Std: 1.482 percentage points

### Youth Gap by Country
1. South Korea: 5.265 pp (std: 1.152)
2. Philippines: 5.102 pp (std: 0.651)
3. Vietnam: 3.922 pp (std: 0.983)
4. Thailand: 3.093 pp (std: 1.003)
5. Japan: 2.312 pp (std: 0.977)

### Youth Gap by Period
- Pre-COVID (2010-2019): 3.985 pp
- COVID (2020-2021): 4.160 pp
- Recovery (2022-2024): 3.639 pp

**Key Findings:**
- Youth unemployment is consistently higher than overall unemployment across all countries
- South Korea and Philippines show the largest youth gaps (over 5 pp)
- Japan shows the smallest youth gap (2.312 pp)
- Youth gap slightly increased during COVID period (+0.175 pp)
- Youth gap decreased during recovery period (-0.521 pp)

---

## 7. GDP Growth vs Unemployment Rate Relationship

### Overall Correlation
- Pearson correlation coefficient: -0.1166
- Sample size (N): 75
- Interpretation: The data shows a weak negative correlation between GDP Growth and Unemployment Rate

**Note:** Correlation does not imply causation. This only shows a statistical relationship.

### Correlation by Country
- Japan: 0.3872 (N=15) - positive correlation
- Philippines: 0.1720 (N=15) - weak positive correlation
- South Korea: -0.0306 (N=15) - very weak negative correlation
- Thailand: -0.4476 (N=15) - moderate negative correlation
- Vietnam: -0.4652 (N=15) - moderate negative correlation

**Key Observations:**
- Overall correlation is weak (-0.1166), suggesting limited linear relationship
- Country-level correlations vary significantly
- Japan and Philippines show positive correlations (higher GDP associated with higher unemployment)
- Thailand and Vietnam show moderate negative correlations (higher GDP associated with lower unemployment)
- South Korea shows almost no correlation

---

## 8. Inflation vs Unemployment Rate Relationship

### Overall Correlation
- Pearson correlation coefficient: -0.2595
- Sample size (N): 75
- Interpretation: The data shows a weak to moderate negative correlation between Inflation and Unemployment Rate

**Note:** Correlation does not imply causation. This only shows a statistical relationship.

### Correlation by Country
- Japan: -0.4943 (N=15) - moderate negative correlation
- Philippines: -0.1116 (N=15) - weak negative correlation
- South Korea: -0.6523 (N=15) - moderate to strong negative correlation
- Thailand: -0.1313 (N=15) - weak negative correlation
- Vietnam: -0.6878 (N=15) - moderate to strong negative correlation

**Key Observations:**
- Overall correlation is weak to moderate (-0.2595)
- South Korea and Vietnam show stronger negative correlations
- Japan shows a moderate negative correlation
- Philippines and Thailand show weak negative correlations
- All countries show negative correlations, suggesting higher inflation tends to be associated with lower unemployment in this dataset

---

## 9. Limitations

### Data Availability
1. **Gender-specific data:** Male and Female unemployment rates are not available due to ILOSTAT API authentication requirements and World Bank API limitations. This prevents gender gap analysis.

2. **Education-level data:** Education-related unemployment variables were not included in the final dataset as they were not reliably available for all countries.

3. **Time period:** Analysis is limited to 2010-2024. Longer-term trends cannot be assessed.

### Methodological Limitations
1. **Correlation vs Causation:** All correlation analyses show statistical relationships only. No causal claims can be made based on this data.

2. **Sample size:** Country-level correlations are based on only 15 data points per country, which limits statistical power.

3. **External factors:** The analysis does not account for other economic, social, or policy factors that may influence unemployment.

4. **Data sources:** All data comes from World Bank estimates. Modeled ILO estimates are used for unemployment and labor force participation, which may have inherent limitations.

### Scope Limitations
1. **Geographic scope:** Only 5 Asian countries are included. Findings may not generalize to other regions.
2. **Variable definitions:** All variables use World Bank definitions. Different definitions might yield different results.

---

## 10. Answers to Research Questions

### Q1: Tỷ lệ thất nghiệp thay đổi như thế nào trong giai đoạn 2010–2024?
**Answer:** Based on the data from 5 Asian countries (2010-2024):
- Overall unemployment rate declined from 2.753% in 2010 to 1.974% in 2024
- The trend showed a general decline from 2010-2019 (2.753% to 2.146%)
- A slight increase occurred during the COVID period (2020-2021), peaking at 2.689% in 2021
- Post-2021, unemployment declined to its lowest levels in 2023-2024 (around 1.97%)
- Net change from 2010 to 2024: -0.779 percentage points

### Q2: Tỷ lệ thất nghiệp khác nhau như thế nào giữa 5 quốc gia?
**Answer:** Average unemployment rates by country (2010-2024):
- South Korea: 3.305% (highest)
- Japan: 3.275%
- Philippines: 2.907%
- Vietnam: 1.562%
- Thailand: 0.737% (lowest)

The range between highest (South Korea) and lowest (Thailand) is 2.568 percentage points. Thailand consistently maintained the lowest unemployment rate throughout the period.

### Q3: COVID-19 có liên quan như thế nào đến biến động thất nghiệp?
**Answer:** Based on the period analysis:
- Pre-COVID (2010-2019): Average unemployment 2.412%
- COVID (2020-2021): Average unemployment 2.591% (+0.179 pp)
- Recovery (2022-2024): Average unemployment 2.020% (-0.571 pp from COVID)

Country-specific responses varied:
- Japan: Unemployment decreased during COVID (-0.771 pp)
- Philippines: Slight increase during COVID (+0.109 pp)
- South Korea: Increase during COVID (+0.415 pp)
- Thailand: Increase during COVID (+0.529 pp)
- Vietnam: Largest increase during COVID (+0.831 pp)

All countries showed declining unemployment during the recovery period. The data shows a slight increase in unemployment during the COVID period, followed by a significant decline during recovery.

### Q4: GDP Growth có mối liên hệ như thế nào với thất nghiệp?
**Answer:** Correlation analysis shows:
- Overall Pearson correlation: -0.1166 (weak negative correlation, N=75)
- Country-level correlations vary significantly:
  - Japan: 0.3872 (positive)
  - Philippines: 0.1720 (weak positive)
  - South Korea: -0.0306 (very weak negative)
  - Thailand: -0.4476 (moderate negative)
  - Vietnam: -0.4652 (moderate negative)

The data shows a weak overall negative correlation between GDP Growth and Unemployment Rate. However, the relationship varies by country, with some showing positive correlations. This suggests the relationship is not consistent across countries and may depend on other factors.

**Important:** This correlation does not prove causation. The data only shows a statistical association.

### Q5: Inflation có mối liên hệ như thế nào với thất nghiệp?
**Answer:** Correlation analysis shows:
- Overall Pearson correlation: -0.2595 (weak to moderate negative correlation, N=75)
- Country-level correlations:
  - Japan: -0.4943 (moderate negative)
  - Philippines: -0.1116 (weak negative)
  - South Korea: -0.6523 (moderate to strong negative)
  - Thailand: -0.1313 (weak negative)
  - Vietnam: -0.6878 (moderate to strong negative)

The data shows a weak to moderate negative correlation between Inflation and Unemployment Rate across all countries. This suggests that higher inflation tends to be associated with lower unemployment in this dataset.

**Important:** This correlation does not prove causation. The data only shows a statistical association.

### Q6: Tỷ lệ thất nghiệp giữa nam và nữ có khác nhau không?
**Answer:** This question cannot be answered with the available data.

**Reason:** Male_Unemployment_Rate and Female_Unemployment_Rate are not available in the dataset. According to source_metadata.csv, ILOSTAT API requires authentication and World Bank API did not provide gender-specific data for these countries. These variables were excluded from the final dataset. Gender gap analysis cannot be performed.

### Q7: Thất nghiệp thanh niên khác thất nghiệp tổng thể như thế nào?
**Answer:** Youth Gap (Youth_Unemployment_Rate - Unemployment_Rate) analysis:
- Overall mean: 3.939 percentage points
- Youth unemployment is consistently higher than overall unemployment across all countries

By country:
- South Korea: 5.265 pp (largest gap)
- Philippines: 5.102 pp
- Vietnam: 3.922 pp
- Thailand: 3.093 pp
- Japan: 2.312 pp (smallest gap)

By period:
- Pre-COVID (2010-2019): 3.985 pp
- COVID (2020-2021): 4.160 pp (slight increase)
- Recovery (2022-2024): 3.639 pp (decrease)

Youth unemployment is consistently higher than overall unemployment by approximately 4 percentage points on average across the 5 countries.

### Q8: Nếu dữ liệu phù hợp, trình độ học vấn có mối liên hệ như thế nào với thất nghiệp?
**Answer:** This question cannot be answered with the available data.

**Reason:** Education-related variables (Education_Level, Education_Unemployment_Rate) were not included in the final dataset as they were not reliably available for all 5 countries through the World Bank API. The PROJECT_SPEC indicates these variables could be supplemented "when there is actual data that is sufficiently reliable and has compatible definitions," but such data was not available for this analysis.

---

## Data Files Generated

1. **analysis/statistics.csv** - Contains basic statistics (mean, median, min, max, std) for all variables by overall, country, and period
2. **analysis/analysis_results.csv** - Contains aggregated results for visualization (yearly, country, and period averages)
3. **analysis/correlation_results.csv** - Contains correlation coefficients for GDP vs Unemployment and Inflation vs Unemployment relationships
4. **analysis/findings.md** - This document with comprehensive analysis findings

---

**Analysis completed by Agent 2 (Data Analyst)**
**Date:** 2026-09-21
**Data scope:** 5 Asian countries (Japan, Philippines, South Korea, Thailand, Vietnam), 2010-2024
**Data source:** World Bank
