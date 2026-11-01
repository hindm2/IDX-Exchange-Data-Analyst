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

### Objective

Inspect dataset structure, review missing values, examine numeric
distributions, and flag potential data-quality issues before cleaning.

### Dataset Scope and Validation

Week 1 combined the monthly files and filtered them to
`PropertyType == "Residential"`.

Weeks 2–3 used those Residential-only outputs. The property-type
check confirmed that every record was Residential, so no additional
rows were removed.

| Measure | Sold | Listings |
|---------|-----:|---------:|
| Raw records combined in Week 1 | 736,473 | 1,034,830 |
| Residential records retained in Week 1 | 495,291 | 658,117 |
| Records inspected in Weeks 2–3 | 495,291 | 658,117 |
| Columns inspected | 84 | 84 |
| Columns flagged as above 90% missing | 15 | 13 |

During Weeks 2–3, no records or columns were removed.
Missing values and potential outliers were documented for later cleaning.

### Missing-Value Review

Missing counts and percentages were calculated for every column.
Columns with more than 90% missing values were flagged for review.

Core analysis fields are retained even when partially missing.
Non-core fields with very low coverage are candidates for removal
during cleaning; no columns have been removed at this stage.

Confirmed completely empty fields in the sold dataset include:

- TaxYear
- FireplacesTotal
- TaxAnnualAmount
- AboveGradeFinishedArea
- ElementarySchoolDistrict

The full column-level recommendations are saved in each dataset's
`missing_value_report.csv`.

### Numeric Distribution Review — Sold

These statistics describe the data before outlier handling.
LivingArea values are shown in their recorded units.

| Field | Minimum | Median | Mean | 95th percentile | 99th percentile | Maximum |
|-------|--------:|-------:|-----:|----------------:|----------------:|--------:|
| ClosePrice | $0 | $825,000 | ~$1,189,311 | $2,859,933.60 | $5,600,000 | $989,500,000 |
| LivingArea | 0 | 1,648 | ~1,902.61 | 3,568.20 | 5,300 | 17,021,320 |
| DaysOnMarket | -288 | 19 | ~37.64 | 132 | 235 | 12,430 |

Histograms, boxplots, and percentile summaries were generated for
ClosePrice, ListPrice, OriginalListPrice, LivingArea, LotSizeAcres,
BedroomsTotal, BathroomsTotalInteger, DaysOnMarket, and YearBuilt.

### Initial Findings

- Mean close price exceeds the median, indicating a right-skewed
  distribution that warrants reviewing high-value records.
- Median DaysOnMarket is 19 days, compared with a mean of approximately
  37.64 days.
- Zero prices, negative DaysOnMarket, and exceptionally large property
  measurements require investigation.
- Extreme examples include 175 bathrooms, 45 bedrooms, and approximately
  7.8 million acres.
- IQR outlier flags are screening tools, not proof of incorrect data.
  No outliers were removed during validation.

### Sold Price Compared with List Price

The comparison uses 495,288 records with finite, positive ClosePrice
and ListPrice values. Three records were excluded from this calculation
only; they remain in the saved dataset.

| Sale outcome | Records | Percentage |
|--------------|--------:|-----------:|
| Above list price | 196,241 | 39.62% |
| At list price | 86,393 | 17.44% |
| Below list price | 212,654 | 42.94% |

### Additional Checks

Date-consistency summaries and county-level close-price summaries
were generated. These outputs require interpretation before drawing
conclusions. County summaries include sample counts to help identify
small groups.

### Deliverables

Script: `weeks2_3_dataset_validation.py`

Separate `listings` and `sold` output folders contain:

| Output | Purpose |
|--------|---------|
| property_types_in_input.csv | Property categories found in each input |
| column_types.csv | Column names and data types |
| field_classification.csv | Market fields, metadata, and fields needing review |
| missing_value_report.csv | Missing counts, percentages, and recommendations |
| numeric_distribution_summary.csv | Numeric statistics and outlier-screening counts |
| date_consistency_summary.csv | Date-order checks |
| validation_report.txt | Processing summary |
| Distribution PNGs | Histograms and boxplots |
| Validated Residential CSV | Residential records retained for later cleaning |

The sold folder also contains `county_close_prices.csv`.

### Status

Validation and report generation are complete. Review of missing-value
decisions, charts, date issues, and county results is ongoing.
The datasets have not yet undergone duplicate removal, imputation,
or outlier cleaning.

Mortgage-rate enrichment was not performed in this validation run.


