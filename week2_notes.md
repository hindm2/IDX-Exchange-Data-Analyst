# Week 2 — Dataset Understanding and Data Quality Review

Reviewed 321,181 residential single-family records across 84 columns.

## Work Completed
- Documented unique property types and filtering logic.
- Reviewed column data types and separated market fields from metadata.
- Calculated missing counts and percentages, flagging columns above 90% null.
- Generated numerical summaries for ClosePrice, LivingArea, and DaysOnMarket.
- Saved the filtered dataset as a CSV.

## Findings and Limitations
- Eight columns were completely empty.
- Extreme prices, property sizes, and negative days on market require further review.
- May, June, July, and September 2026 were excluded because their downloads appeared incomplete.

## Script
`dataset_understanding.py`

Property-data CSVs are kept outside this repository.
