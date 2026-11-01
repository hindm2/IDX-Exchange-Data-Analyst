# IDX Exchange - MLS Analytics Internship 
Data Analyst Internship Project | IDX Exchange

Code, progress, and findings for my **IDX Exchange 12-Week Data Analyst Internship** (MLS Analytics & Tableau Dashboard Program).

## Data

Monthly CRMLS (California Regional MLS) Listing and Sold files, with a requested analysis period of **January 2024–September 2026**.

MLS property data is confidential. **Source data and generated property-level CSV files are excluded from this repository.** Only code, documentation, and aggregate findings are shared.

## Workflow

Monthly aggregation → Dataset exploration and validation → Mortgage rate enrichment → Data cleaning → Feature engineering and outlier review → Tableau dashboards → Final report

## Roadmap

- [x] **Week 1:** Monthly dataset aggregation and Residential filtering
- [x] **Weeks 2–3:** Dataset understanding, validation, exploratory analysis, and mortgage rate enrichment
- [ ] **Weeks 4–5:** Data cleaning, transformation, and quality flags
- [ ] **Week 6:** Feature engineering and housing market metrics
- [ ] **Week 7:** Outlier detection and quality review
- [ ] **Weeks 8–10:** Tableau dashboards for market and competitive analysis
- [ ] **Weeks 11–12:** Market intelligence report and final presentation

---
## Week 1 — Monthly Aggregation

Combined 66 monthly CSV files covering January 2024 through September 2026.
Listings and sold records were processed separately and filtered to
`PropertyType = Residential`. No PropertySubType filter was applied.

| Dataset | Monthly Files | Raw Rows | Residential Rows | Rows Excluded |
|---------|--------------:|---------:|-----------------:|--------------:|
| Listings | 33 | 1,034,830 | 658,117 | 376,713 |
| Sold | 33 | 736,473 | 495,291 | 241,182 |

### Validation

- All 33 expected months are present for each dataset.
- No missing months or duplicate monthly files were found.
- Every monthly CSV contains more than 1,000 data rows.
- Duplicate records and other data-quality issues have not yet been cleaned.

### Generated Outputs

| File | Description |
|------|-------------|
| `CRMLS_listings_Residential_202401_202609.csv` | Combined Residential listings |
| `CRMLS_sold_Residential_202401_202609.csv` | Combined Residential sold records |
| `week1_aggregation_report.txt` | Monthly row counts and aggregation summary |

The combined CSVs are stored separately from the 66 raw monthly files.

## Weeks 2-3— Dataset Understanding and Data Quality Review
### Week 2 — Dataset Structuring, Validation and EDA


**Objective:** Inspect dataset structure, assess missing values, review numeric distributions, and identify data-quality issues for later cleaning.

**Script:** [week2_dataset_understanding.py](week2_dataset_understanding.py)

**Period:** January 2024–September 2026.

### Dataset Structure and Missing Values

Both inputs were already filtered to `PropertyType == "Residential"` during Week 1. Validation confirmed that all input records were Residential. No additional property-type filtering was needed, and no SingleFamilyResidence restriction was applied.

| Measure | Sold | Listings |
|---------|-----:|---------:|
| Residential records inspected | 495,291 | 658,117 |
| Original columns | 84 | 84 |
| Columns above 90% missing | 15 | 13 |
| High-missing non-core columns dropped | 15 | 13 |
| Columns retained in analysis dataset | 69 | 71|

**Sold dataset:** all 495,291 records were retained. Column removal changed the dataset from 84 to 69 columns; it did not remove property records.

The following 15 sold columns were dropped from the separate analysis copy because they exceeded 90% missing values and were not designated core fields:

`WaterfrontYN`, `BasementYN`, `FireplacesTotal`,
`AboveGradeFinishedArea`, `TaxAnnualAmount`, `BuilderName`,
`TaxYear`, `BuildingAreaTotal`, `ElementarySchoolDistrict`,
`CoBuyerAgentFirstName`, `BelowGradeFinishedArea`, `BusinessType`,
`CoveredSpaces`, `LotSizeDimensions`, and
`MiddleOrJuniorSchoolDistrict`.

- Core fields were retained even when partially missing.
- Fields were classified as market-analysis fields, metadata, or other fields requiring review.
- The original input datasets were preserved.

### Numeric Distributions — Sold

Numeric summaries include minimum, maximum, mean, median, and the 1st, 5th, 25th, 50th, 75th, 95th, and 99th percentiles.

| Field | Minimum | Median | Mean | 95th Percentile | 99th Percentile | Maximum |
|-------|--------:|-------:|-----:|----------------:|----------------:|--------:|
| ClosePrice | $0 | $825,000 | ~$1,189,311 | $2,859,933.60 | $5,600,000 | $989,500,000 |
| LivingArea* | 0 | 1,648 | ~1,902.61 | 3,568.20 | 5,300 | 17,021,320 |
| DaysOnMarket | -288 | 19 | ~37.64 | 132 | 235 | 12,430 |

*LivingArea is shown in the recorded units; units require verification.*
### EDA Answers — Sold

Results describe the Residential sold dataset before duplicate removal
and outlier cleaning.

| Question | Answer |
|----------|--------|
| Median / mean close price | $825,000 / approximately $1,189,311 |
| Median / mean DaysOnMarket | 19 days / approximately 37.64 days |
| Sold above / below / at list price | 39.62% / 42.94% / 17.44% |
| Listing date after close date | 75 of 495,290 comparable records |
| Purchase-contract date after close date | 242 of 495,094 comparable records |
| Listing date after purchase-contract date | 315 of 495,093 comparable records |

The list-price comparison uses 495,288 records with finite, positive
ClosePrice and ListPrice values. Date comparisons include only records
where both dates could be parsed. Date-issue counts may overlap and
should not be added together as a count of unique affected records.

### Days on Market Distribution

| DaysOnMarket | Records | Percentage |
|--------------|--------:|-----------:|
| Negative — flagged for review | 56 | 0.01% |
| 0 | 20,006 | 4.04% |
| 1–7 | 99,894 | 20.17% |
| 8–30 | 190,174 | 38.40% |
| 31–60 | 88,524 | 17.87% |
| 61–90 | 43,472 | 8.78% |
| 91–180 | 42,319 | 8.54% |
| Over 180 | 10,846 | 2.19% |

No missing or nonnumeric DaysOnMarket values were found.
Negative values were flagged separately rather than treated as quick sales.
Percentages may not total exactly 100% because of rounding.

### Counties with the Highest Median Close Prices

Rankings include counties with at least 200 records having finite,
positive ClosePrice values. Counts represent records, not necessarily
unique properties; duplicates and high outliers have not yet been removed.

| County | Median Close Price | Records |
|--------|-------------------:|--------:|
| San Mateo | $1,700,000 | 8,452 |
| Santa Clara | $1,590,000 | 21,067 |
| San Francisco | $1,200,000 | 1,128 |
| Santa Cruz | $1,188,000 | 3,556 |
| Orange | $1,185,000 | 55,786 |
| Alameda | $1,130,000 | 23,432 |
| Monterey | $910,000 | 4,726 |
| Los Angeles | $905,000 | 123,098 |
| San Diego | $900,000 | 61,652 |
| San Luis Obispo | $875,000 | 7,270 |

San Mateo has the highest median close price among counties meeting
the minimum record-count requirement. Date inconsistencies and negative
DaysOnMarket values will be investigated during cleaning.

Histograms and boxplots were reviewed for:

- ClosePrice, ListPrice, and OriginalListPrice
- LivingArea and LotSizeAcres
- BedroomsTotal and BathroomsTotalInteger
- DaysOnMarket and YearBuilt

Histograms display values between the 1st and 99th percentiles for readability. Boxplots use all finite numeric values, with the ClosePrice axis zoomed to $0–$4 million. These display choices do not remove records from the dataset.

### Initial Findings

- Mean close price exceeds the median, consistent with a right-skewed price distribution.
- Median DaysOnMarket is 19 days, while the mean is approximately 37.64 days.
- Zero prices, negative DaysOnMarket, and exceptionally large property measurements require investigation.
- Extreme examples include a $989.5 million close price, 45 bedrooms, 175 bathrooms, and approximately 7.8 million acres.
- Extreme values were flagged for review, not automatically removed.
- Spearman correlations were calculated to explore relationships among numeric fields.

### Sale Price Compared with List Price

The earlier validation run compared 495,288 sold records with finite, positive ClosePrice and ListPrice values.

| Outcome | Records | Percentage |
|---------|--------:|-----------:|
| Above list price | 196,241 | 39.62% |
| At list price | 86,393 | 17.44% |
| Below list price | 212,654 | 42.94% |

Three records were excluded from this calculation only.

### Validation Status

The sold analysis dataset contains **495,291 rows and 69 columns** after removing high-missing non-core columns.

No duplicate records or numeric outlier rows were removed, and no missing values were imputed. Further cleaning will address the issues identified during validation.

Mortgage-rate enrichment is documented separately.
