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
## Week 1 — Monthly Dataset Aggregation

**Script:** `week1_monthly_aggregation_with_counts.py`

Combines available monthly MLS Listing and Sold files into two separate datasets, filters both to `PropertyType == "Residential"`, and saves the results as CSV files.

### Data Coverage

- Requested period: January 2024–September 2026.
- Available files: 29 monthly files per dataset.
- Months not provided: May, June, July, and September 2026.
- Missing months are documented and excluded from the combined datasets.

### Row Counts

| Dataset | Before Concatenation | After Concatenation | Before Residential Filter | After Residential Filter |
|---|---:|---:|---:|---:|
| Listings | 894,360 | 894,360 | 894,360 | 568,163 |
| Sold | 638,834 | 638,834 | 638,834 | 429,193 |

### Tools

Python, pandas, and Google Colab.


