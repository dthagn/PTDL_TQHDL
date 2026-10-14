# QA REPORT - Unemployment Analysis Project

**QA Reviewer:** Agent 5 (Data Quality Reviewer + QA Engineer + Academic Reviewer)  
**Review Date:** 2026-09-21  
**Project:** Phân tích xu hướng thất nghiệp và mối liên hệ với các yếu tố kinh tế – xã hội tại một số quốc gia châu Á giai đoạn 2010–2024  
**Scope:** 5 Asian countries (Japan, Philippines, South Korea, Thailand, Vietnam), 2010-2024

---

## EXECUTIVE SUMMARY

**Overall Status:** NEED REVISION

The project demonstrates strong data quality practices with real data from World Bank, proper documentation, and correct statistical methods. However, there are **2 CRITICAL issues** and **1 HIGH issue** that must be addressed before the project can be considered complete.

---

## CRITICAL ISSUES

### Issue 1: Missing Gender-Specific Unemployment Data

**Agent responsible:** Agent 1 (Data Engineer)

**File:** `data/processed/unemployment_final.csv`, `data/processed/source_metadata.csv`

**Problem:** 
- Male_Unemployment_Rate and Female_Unemployment_Rate are completely missing from the final dataset
- Gender gap analysis cannot be performed (Research Question 6 cannot be answered)
- PROJECT_SPEC requires gender gap analysis as a core research question

**Evidence:**
- `data/processed/unemployment_final.csv` contains only: Country, Country_Code, Year, GDP_Growth, GDP_per_Capita, Inflation, Labor_Force_Participation, Population, Unemployment_Rate, Youth_Unemployment_Rate
- `source_metadata.csv` states: "NOT AVAILABLE - ILOSTAT API requires authentication. World Bank API did not provide gender-specific data for these countries. Variable excluded from final dataset."
- `findings.md` Section 5 states: "Gender gap analysis cannot be performed with the available data"

**Required action:**
Agent 1 must attempt alternative data sources for gender-segmented unemployment data:
1. Try World Bank API with different indicator codes (SL.UEM.MA.ZS, SL.UEM.FE.ZS) - verify if data is actually available
2. Try alternative sources: OECD, national statistical offices of the 5 countries
3. If truly unavailable, document this as a major limitation and consider adjusting the research scope

**Priority:** CRITICAL

---

### Issue 2: Incomplete Correlation Analysis

**Agent responsible:** Agent 2 (Data Analyst)

**File:** `analysis/correlation_results.csv`

**Problem:**
- Correlation analysis includes GDP vs Unemployment by country (5 country-specific correlations)
- Correlation analysis is MISSING Inflation vs Unemployment by country (only overall correlation provided)
- This limits the ability to answer Research Question 5 at the country level

**Evidence:**
- `correlation_results.csv` contains 8 rows:
  - 2 overall correlations (GDP vs Unemployment, Inflation vs Unemployment)
  - 5 country-specific GDP vs Unemployment correlations
  - 0 country-specific Inflation vs Unemployment correlations
- `findings.md` Section 8 provides overall Inflation correlation but does not provide country-level breakdown

**Required action:**
Agent 2 must add country-specific Inflation vs Unemployment correlations to `correlation_results.csv` and update `findings.md` with country-level analysis.

**Priority:** CRITICAL

---

## HIGH ISSUES

### Issue 3: Incomplete Country-Level Statistics in findings.md

**Agent responsible:** Agent 2 (Data Analyst)

**File:** `analysis/findings.md`

**Problem:**
- Section 3 "Country Comparison" provides average unemployment rates by country
- However, the period-specific changes (Pre-COVID, COVID, Recovery) shown in findings.md do not match the calculated values in `analysis_results.csv`
- The values appear to be manually calculated and may have errors

**Evidence:**
- `findings.md` lines 67-89 show country-specific period changes
- Example: Japan Pre-COVID (2010-2019): 3.579% (but `statistics.csv` shows Japan overall mean is 3.275%)
- The period calculations in `findings.md` should be derived from `analysis_results.csv` which has the correct aggregated data

**Required action:**
Agent 2 should:
1. Verify all period-specific calculations in `findings.md` against `analysis_results.csv`
2. Ensure all statistics are programmatically derived, not manually calculated
3. Add a verification step to the analysis pipeline

**Priority:** HIGH

---

## MEDIUM ISSUES

### Issue 4: Missing Error Handling in Streamlit App

**Agent responsible:** Agent 4 (Streamlit Developer)

**File:** `app.py`

**Problem:**
- The app has basic error handling in `load_data()` function
- However, individual page functions do not have try-catch blocks
- If a visualization fails, the entire app may crash

**Evidence:**
- `app.py` lines 99-124 have error handling for data loading
- Page display functions (lines 229-462) do not have individual error handling
- If `create_unemployment_trend()` or other visualization functions fail, no graceful degradation

**Required action:**
Agent 4 should add try-catch blocks to each page display function with user-friendly error messages.

**Priority:** MEDIUM

---

### Issue 5: Inflation Data Outlier Not Investigated

**Agent responsible:** Agent 2 (Data Analyst)

**File:** `analysis/statistics.csv`, `findings.md`

**Problem:**
- Vietnam Inflation shows a maximum of 18.678% (in 2011)
- This is a significant outlier compared to other countries and years
- No investigation or explanation provided in findings.md

**Evidence:**
- `statistics.csv` line 25: Vietnam Inflation Max = 18.6777322770706
- This is significantly higher than other countries (Philippines max 5.978%, South Korea max 5.089%)
- `findings.md` does not mention this outlier or provide context

**Required action:**
Agent 2 should investigate this outlier (likely due to Vietnam's high inflation in 2011) and add a brief explanation in the findings or limitations section.

**Priority:** MEDIUM

---

## LOW ISSUES

### Issue 6: Inconsistent Date Format in Metadata

**Agent responsible:** Agent 1 (Data Engineer)

**File:** `data/processed/source_metadata.csv`

**Problem:**
- retrieval_date shows "2026-09-21" which is in the future relative to the project timeline
- This appears to be a system date issue

**Evidence:**
- `source_metadata.csv` lines 2-10 all show retrieval_date as "2026-09-21"

**Required action:**
Agent 1 should verify the actual data retrieval dates and update the metadata accordingly.

**Priority:** LOW

---

### Issue 7: Minor Typo in Dashboard Title

**Agent responsible:** Agent 4 (Streamlit Developer)

**File:** `app.py`

**Problem:**
- Line 57: page_title="Phân tích Thất nghiệp Châu Á 2010-2024"
- The title is correct but could be more descriptive

**Required action:**
Optional: Consider updating to "Phân tích Xu hướng Thất nghiệp Châu Á 2010-2024" for clarity.

**Priority:** LOW

---

## DATA QA RESULTS

### ✅ PASSED CHECKS

1. **Data Sources:** All data sourced from World Bank API (real data, no fake data)
2. **Indicators:** Correct World Bank indicator codes used
3. **Definitions:** Data dictionary provides clear definitions for all variables
4. **Units:** All units correctly specified (Percent, US Dollars, People)
5. **Countries:** Correct 5 countries (Japan, Philippines, South Korea, Thailand, Vietnam) with proper ISO codes
6. **Years:** Correct year range (2010-2024) with complete coverage
7. **Missing Values:** No missing values in the final dataset (100% completeness)
8. **Duplicates:** No duplicate Country-Year pairs detected
9. **Datatypes:** All numeric columns have correct datatypes
10. **Outliers:** Values are within reasonable ranges (except Vietnam 2011 inflation noted above)
11. **Merge Logic:** Data merged correctly using outer join on Country, Country_Code, Year
12. **No Hard-coded Data:** All data loaded from CSV files, no hard-coded values in analysis
13. **No Mock Data:** No synthetic or generated data used

### ❌ FAILED CHECKS

1. **Gender Data:** Male_Unemployment_Rate and Female_Unemployment_Rate missing (CRITICAL)
2. **Correlation Completeness:** Missing country-level Inflation correlations (CRITICAL)

---

## ANALYSIS QA RESULTS

### ✅ PASSED CHECKS

1. **Mean Calculations:** Correct mean values calculated and documented
2. **Min/Max:** Correct minimum and maximum values identified
3. **Change Calculations:** Period changes correctly calculated as percentage points
4. **Youth Gap:** Correctly calculated as Youth_Unemployment_Rate - Unemployment_Rate
5. **COVID Comparison:** Correct period classification (Pre-COVID: 2010-2019, COVID: 2020-2021, Recovery: 2022-2024)
6. **Percentage vs Percentage Point:** Correctly uses "percentage point" for differences between percentages
7. **Formulas:** All formulas match PROJECT_SPEC requirements

### ❌ FAILED CHECKS

1. **Gender Gap:** Cannot be calculated due to missing data (CRITICAL)
2. **Country-Level Period Statistics:** Manual calculations may have errors (HIGH)

---

## CORRELATION QA RESULTS

### ✅ PASSED CHECKS

1. **Pearson Method:** Correctly uses Pearson correlation coefficient
2. **Sample Size:** Overall N=75 is adequate; country-level N=15 is acceptable for exploratory analysis
3. **Missing Handling:** No missing values in correlation variables
4. **Causation Language:** Correctly states "correlation does not imply causation" and avoids causal language

### ❌ FAILED CHECKS

1. **Completeness:** Missing country-level Inflation vs Unemployment correlations (CRITICAL)

---

## VISUALIZATION QA RESULTS

### ✅ PASSED CHECKS

1. **Chart Types:** Correct chart types used (Line for trends, Bar for comparisons, Scatter for correlations, Choropleth for maps)
2. **Variables:** Correct variables used in all charts
3. **Units:** All axes correctly labeled with units (%)
4. **Countries:** Correct 5 countries displayed
5. **Years:** Correct year range (2010-2024)
6. **Titles:** All charts have descriptive titles
7. **Axes:** All axes properly labeled
8. **Legends:** Legends present where needed
9. **Tooltips:** Interactive tooltips with correct formatting
10. **Colors:** Consistent color mapping across all charts
11. **Map Codes:** Correct ISO 3166-1 alpha-3 codes used (JPN, PHL, KOR, THA, VNM)

### ❌ FAILED CHECKS

None

---

## STREAMLIT QA RESULTS

### ✅ PASSED CHECKS

1. **App Structure:** Well-organized with modular imports
2. **Filters:** Country, Year, and Period filters implemented correctly
3. **KPIs:** KPI cards display correct metrics
4. **Charts:** All charts render correctly
5. **Navigation:** Sidebar navigation with 10 pages
6. **Layout:** Wide layout with proper column arrangements
7. **No Hard-coded Data:** All data loaded from files
8. **No Mock Data:** No synthetic data in dashboard
9. **Responsive:** Uses Streamlit's responsive layout

### ❌ FAILED CHECKS

1. **Error Handling:** Insufficient error handling in page functions (MEDIUM)

---

## ACADEMIC DEFENSE QUESTIONS

### 1. Why was this topic chosen?
**Answer:** Unemployment is a critical economic indicator that affects social stability and individual well-being. Understanding unemployment trends in rapidly developing Asian economies provides insights into the relationship between economic growth and labor market dynamics.

### 2. Why were these 5 countries chosen?
**Answer:** These 5 countries represent a diverse range of Asian economies: Japan (developed), South Korea (newly industrialized), Thailand (upper-middle income), Philippines (emerging economy), and Vietnam (fast-growing emerging economy). This diversity allows for meaningful comparative analysis.

### 3. Why was the period 2010-2024 chosen?
**Answer:** This period captures pre-COVID trends (2010-2019), the COVID-19 shock (2020-2021), and the recovery phase (2022-2024). It provides a complete business cycle including an unprecedented global crisis.

### 4. Why was Unemployment Rate used?
**Answer:** Unemployment rate is the most widely recognized indicator of labor market health. It allows for direct comparison across countries and time periods, and is consistently available from international sources like World Bank.

### 5. Where does World Bank get its data from?
**Answer:** World Bank compiles data from national statistical offices, international organizations (like ILO for unemployment data), and its own research. For unemployment indicators, World Bank uses "Modeled ILO estimates" which are harmonized across countries.

### 6. How does ILOSTAT differ from World Bank?
**Answer:** ILOSTAT is the International Labour Organization's database, which provides more detailed labor market statistics including gender-segmented and age-segmented data. World Bank often sources its labor data from ILO but may have different coverage or indicator availability.

### 7. Why was a Line chart chosen?
**Answer:** Line charts are the standard for displaying time series data as they show trends and changes over time clearly. They allow viewers to see the trajectory of unemployment rates across the 15-year period.

### 8. Why was a Bar chart chosen?
**Answer:** Bar charts are ideal for comparing categorical data (countries) and showing differences in average values. They provide clear visual comparison of unemployment rates across the 5 countries.

### 9. Why was a Scatter plot used?
**Answer:** Scatter plots are the appropriate visualization for examining the relationship between two continuous variables (GDP Growth vs Unemployment, Inflation vs Unemployment). They show the correlation pattern and individual data points.

### 10. What is Pearson correlation?
**Answer:** Pearson correlation coefficient measures the linear relationship between two continuous variables. It ranges from -1 (perfect negative correlation) to +1 (perfect positive correlation), with 0 indicating no linear correlation.

### 11. Does correlation prove causation?
**Answer:** No. Correlation only indicates a statistical association between variables. Causation requires additional evidence from controlled experiments or rigorous causal inference methods. This analysis only reports correlations, not causal relationships.

### 12. How is missing data handled?
**Answer:** In this dataset, there are no missing values in the final merged dataset (100% completeness). If missing data were present, the approach would be to keep it as missing rather than impute values, to avoid introducing bias.

### 13. Why not impute missing data?
**Answer:** Imputation can introduce bias and uncertainty, especially in economic time series data. Keeping missing values as missing is more transparent and allows users to understand data limitations.

### 14. How is the gender gap calculated?
**Answer:** Gender Gap = Female_Unemployment_Rate - Male_Unemployment_Rate (in percentage points). However, this calculation could not be performed because gender-segmented unemployment data was not available for these countries from the World Bank API.

### 15. How does youth unemployment differ from overall unemployment?
**Answer:** Youth unemployment (ages 15-24) is typically higher than overall unemployment because young people are entering the labor market for the first time and may lack experience or face skills mismatches. The "Youth Gap" in this analysis averages 3.9 percentage points across the 5 countries.

### 16. How is the COVID period defined?
**Answer:** COVID period is defined as 2020-2021, representing the peak pandemic years. Pre-COVID is 2010-2019 and Recovery is 2022-2024. This classification allows for comparing labor market performance across these distinct phases.

### 17. Why was GDP Growth used?
**Answer:** GDP growth is a key macroeconomic indicator that reflects overall economic health. According to Okun's Law, there is typically an inverse relationship between GDP growth and unemployment, making it an important variable to examine.

### 18. Why was Inflation used?
**Answer:** Inflation affects purchasing power and can influence labor market dynamics. The Phillips curve suggests an inverse relationship between inflation and unemployment, though this relationship has weakened in recent decades.

### 19. What are the limitations of the dataset?
**Answer:** Key limitations include: (1) Missing gender-segmented data, (2) Missing education-level unemployment data, (3) Limited to 5 countries, (4) Country-level correlations based on only 15 data points, (5) All data from World Bank estimates which may have inherent modeling assumptions.

### 20. Would results change if different countries were selected?
**Answer:** Yes, results would likely differ because each country has unique economic structures, labor market policies, and cultural factors. The findings from these 5 Asian countries may not generalize to other regions or country groups.

---

## FINAL REVIEW

### STATUS: NEED REVISION

The project cannot be marked as PASS due to:

1. **CRITICAL Issue #1:** Missing gender-specific unemployment data prevents answering Research Question 6 (Gender gap analysis)
2. **CRITICAL Issue #2:** Incomplete correlation analysis (missing country-level Inflation correlations)

### Required Actions Before PASS:

1. **Agent 1** must attempt to obtain gender-segmented unemployment data from alternative sources, or if truly unavailable, this must be documented as a fundamental limitation that may require adjusting the research scope
2. **Agent 2** must complete the correlation analysis by adding country-level Inflation vs Unemployment correlations
3. **Agent 2** must verify all period-specific statistics in findings.md against analysis_results.csv
4. **Agent 4** should add error handling to page display functions (recommended but not blocking)

### Re-QA Required:

After the above fixes are implemented, Agent 5 must re-run the QA review to verify:
- Gender data availability or proper documentation of limitation
- Complete correlation analysis
- Accurate statistics in findings.md

---

## POSITIVE OBSERVATIONS

The project demonstrates several strengths:

1. **Data Integrity:** All data is real from World Bank API, no fake or synthetic data
2. **Documentation:** Comprehensive data dictionary, source metadata, and validation report
3. **Methodology:** Correct statistical methods (Pearson correlation, proper percentage point calculations)
4. **Transparency:** Clear documentation of limitations (missing gender data, correlation vs causation)
5. **Code Quality:** Well-structured, modular code with proper separation of concerns
6. **Visualization:** Appropriate chart types with consistent styling and proper labeling
7. **Academic Rigor:** Proper avoidance of causal language, acknowledgment of limitations

---

**QA Review Completed**
**Next Steps:** Address CRITICAL and HIGH issues, then request re-QA
