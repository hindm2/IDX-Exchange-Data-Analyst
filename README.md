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

### What it does

- Checks that every required month has exactly one input file.
- Combines 30 months of Listings and 33 months of Sold data.
- Keeps records where `PropertyType = Residential`.
- Verifies that the combined Residential row count equals the sum of the monthly Residential counts.
- Saves two combined CSVs and a detailed text report.
- Preserves duplicates and all property subtypes within Residential.

### Row counts

| Dataset | Monthly files | Period covered | Raw rows across files | Residential rows after combining |
|---------|--------------:|----------------|----------------------:|---------------------------------:|
| Listings | 30 | Jan 2024–Jun 2026 | 915,823 | 583,065 |
| Sold | 33 | Jan 2024–Sep 2026 | 736,473 | 495,291 |

Both combined datasets contain 84 columns.

### Findings and limitations

- The Residential filter excluded 332,758 Listing records and 241,182 Sold records.
- July, August, and September 2026 Listing files each contain only 1,000 raw rows. These months were excluded because the downloads appear incomplete.
- January 2026 Listings contains only 2,606 raw rows, including 1,721 Residential records. This month remains included but is flagged for completeness review.
- File availability and row counts alone do not confirm that downloads are complete.
- Listings and Sold have different end dates. Direct monthly comparisons should use their shared period, January 2024–June 2026.
- Period coverage is based on filenames; record-level date ranges still require validation.

### Output files

- `CRMLS_listings_Residential_202401_202606.csv`
- `CRMLS_sold_Residential_202401_202609.csv`
- `outputs/week1_output.txt`

Property-level CSV files are kept outside this repository.

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


