# IDX-Exchange-Data-Analyst
Data Analyst Internship Project | IDX Exchange
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

### Data Access

This repository contains code only. Source data and generated CSV files are excluded.
