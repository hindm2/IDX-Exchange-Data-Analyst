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

## Week 2 — Dataset Understanding and Data Quality Review
Reviewed 321,181 residential single-family records across 84 columns.

Work Completed
Documented unique property types and filtering logic.
Reviewed column data types and separated market fields from metadata.
Calculated missing counts and percentages, flagging columns above 90% null.
Generated numerical summaries for ClosePrice, LivingArea, and DaysOnMarket.
Saved the filtered dataset as a CSV.
Findings and Limitations
Eight columns were completely empty.
Extreme prices, property sizes, and negative days on market require further review.
May, June, July, and September 2026 were excluded because their downloads appeared incomplete.
Script
dataset_understanding.py

Property-data CSVs are kept outside this repository.


