"""IDX Exchange Week 1: combine monthly listings and sold CSV files.

Put monthly CSVs in a folder named data or IDX_Analysis beside this script, then run:
    python week1_monthly_aggregation.py

Requires pandas. Reads local files; it does not download data from an API.
The output folder contains two Residential-only CSVs and a copy of this
script with actual row counts and missing months appended as comments.
Missing months are skipped and documented, not treated as zero sales.
This produces a partial dataset until all required months are supplied.
"""
from datetime import date, timedelta
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
if not DATA_DIR.is_dir():
    DATA_DIR = BASE_DIR / "IDX_Analysis"
# Change DATA_DIR if your CSV folder has a different name.
OUTPUT_DIR = BASE_DIR / "combined_output"
START_MONTH = "2024-01"
# Automatically use the last completed month (September 2026 in October 2026).
END_MONTH = (date.today().replace(day=1) - timedelta(days=1)).strftime("%Y-%m")


def find_monthly_files(data_dir, prefix, months):
    """Use available months and document gaps; use _filled if both versions exist."""
    if not data_dir.is_dir():
        raise FileNotFoundError(f"CSV folder not found: {data_dir}")
    selected = []
    notes = []
    missing = []
    for month in months:
        stem = f"{prefix}{month.strftime('%Y%m')}"
        original = data_dir / f"{stem}.csv"
        filled = data_dir / f"{stem}_filled.csv"
        if filled.is_file():
            selected.append(filled)
            if original.is_file():
                notes.append(f"Used {filled.name}; skipped {original.name} to avoid double counting.")
        elif original.is_file():
            selected.append(original)
        else:
            missing.append(month.strftime("%Y-%m"))
            notes.append(f"Missing month: {stem}.csv (or {stem}_filled.csv); skipped.")
    if not selected:
        raise FileNotFoundError(f"No {prefix} monthly files found in the required date range.")
    notes.insert(0, f"{prefix}: {len(selected)} of {len(months)} monthly files available")
    notes.insert(1, "Missing months: " + (", ".join(missing) if missing else "none"))
    return selected, notes, bool(missing)


def combine_and_filter(paths, label):
    frames = []
    counts = [f"{label} row counts"]
    for path in paths:
        frame = pd.read_csv(path, low_memory=False)
        if "PropertyType" not in frame.columns:
            raise ValueError(f"PropertyType column is missing in {path.name}")
        frames.append(frame)
        counts.append(f"Before concatenation: {path.name} = {len(frame):,} rows")

    # Before concatenation: total rows across the individual monthly datasets.
    before_concat = sum(len(frame) for frame in frames)
    counts.append(f"Total before concatenation = {before_concat:,} rows")

    # Stack rows and reset the index; preserve all input rows, including duplicates.
    combined = pd.concat(frames, ignore_index=True)
    del frames
    counts.append(f"After concatenation = {len(combined):,} rows")
    assert len(combined) == before_concat, "Unexpected row-count change during concatenation"

    # Before Residential filter: all rows in the combined dataset.
    before_filter = len(combined)
    counts.append(f"Before Residential filter = {before_filter:,} rows")

    # Exact match required by the handbook. Do not filter PropertySubType.
    residential = combined.loc[combined["PropertyType"] == "Residential"].copy()
    counts.append(f"After Residential filter = {len(residential):,} rows")
    counts.append(f"Rows removed by filter = {before_filter - len(residential):,}")
    return residential, counts


def main():
    months = pd.period_range(START_MONTH, END_MONTH, freq="M")
    if len(months) == 0:
        raise ValueError("The end month must not be earlier than the start month.")

    # Check availability, but continue with existing files when months are missing.
    listings_files, listings_notes, listings_partial = find_monthly_files(DATA_DIR, "CRMLSListing", months)
    sold_files, sold_notes, sold_partial = find_monthly_files(DATA_DIR, "CRMLSSold", months)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report = [f"Requested date range: {START_MONTH} through {END_MONTH}"]
    if listings_partial or sold_partial:
        report.append("PARTIAL COVERAGE: missing months were skipped; confirm scope with supervisor.")
    report.extend(listings_notes + sold_notes)
    print("\n".join(report))
    date_suffix = f"{START_MONTH.replace('-', '')}_{END_MONTH.replace('-', '')}"

    # Process the datasets separately to reduce peak memory use.
    for label, paths, partial in [("listings", listings_files, listings_partial), ("sold", sold_files, sold_partial)]:
        residential, counts = combine_and_filter(paths, label)
        coverage = "_partial" if partial else ""
        output_file = OUTPUT_DIR / f"CRMLS_{label}_Residential_{date_suffix}{coverage}.csv"
        residential.to_csv(output_file, index=False)
        del residential
        report.extend(counts)
        print("\n".join(counts))
        print(f"Saved: {output_file}\n")

    # Produce a submission copy with verified counts as Python comments.
    # Actual counts are recorded only after successful processing of both datasets.
    source = Path(__file__).read_text(encoding="utf-8")
    source = source.split("\n# VERIFIED ROW COUNTS FROM RUN", 1)[0]
    comments = "\n# VERIFIED ROW COUNTS FROM RUN\n"
    comments += "\n".join(f"# {line}" for line in report) + "\n"
    submission = OUTPUT_DIR / "week1_monthly_aggregation_with_counts.py"
    submission.write_text(source + comments, encoding="utf-8")
    print(f"Submit this script with the actual row-count comments: {submission}")


if __name__ == "__main__":
    main()

# VERIFIED ROW COUNTS FROM RUN
# Requested date range: 2024-01 through 2026-09
# PARTIAL COVERAGE: missing months were skipped; confirm scope with supervisor.
# CRMLSListing: 29 of 33 monthly files available
# Missing months: 2026-05, 2026-06, 2026-07, 2026-09
# Missing month: CRMLSListing202605.csv (or CRMLSListing202605_filled.csv); skipped.
# Missing month: CRMLSListing202606.csv (or CRMLSListing202606_filled.csv); skipped.
# Missing month: CRMLSListing202607.csv (or CRMLSListing202607_filled.csv); skipped.
# Missing month: CRMLSListing202609.csv (or CRMLSListing202609_filled.csv); skipped.
# CRMLSSold: 29 of 33 monthly files available
# Missing months: 2026-05, 2026-06, 2026-07, 2026-09
# Missing month: CRMLSSold202605.csv (or CRMLSSold202605_filled.csv); skipped.
# Missing month: CRMLSSold202606.csv (or CRMLSSold202606_filled.csv); skipped.
# Missing month: CRMLSSold202607.csv (or CRMLSSold202607_filled.csv); skipped.
# Missing month: CRMLSSold202609.csv (or CRMLSSold202609_filled.csv); skipped.
# listings row counts
# Before concatenation: CRMLSListing202401.csv = 27,454 rows
# Before concatenation: CRMLSListing202402.csv = 27,447 rows
# Before concatenation: CRMLSListing202403.csv = 32,282 rows
# Before concatenation: CRMLSListing202404.csv = 36,503 rows
# Before concatenation: CRMLSListing202405.csv = 38,796 rows
# Before concatenation: CRMLSListing202406.csv = 35,893 rows
# Before concatenation: CRMLSListing202407.csv = 36,340 rows
# Before concatenation: CRMLSListing202408.csv = 35,305 rows
# Before concatenation: CRMLSListing202409.csv = 34,625 rows
# Before concatenation: CRMLSListing202410.csv = 34,730 rows
# Before concatenation: CRMLSListing202411.csv = 25,128 rows
# Before concatenation: CRMLSListing202412.csv = 19,417 rows
# Before concatenation: CRMLSListing202501.csv = 37,469 rows
# Before concatenation: CRMLSListing202502.csv = 33,983 rows
# Before concatenation: CRMLSListing202503.csv = 38,492 rows
# Before concatenation: CRMLSListing202504.csv = 40,187 rows
# Before concatenation: CRMLSListing202505.csv = 40,271 rows
# Before concatenation: CRMLSListing202506.csv = 26,399 rows
# Before concatenation: CRMLSListing202507.csv = 27,345 rows
# Before concatenation: CRMLSListing202508.csv = 25,210 rows
# Before concatenation: CRMLSListing202509.csv = 26,923 rows
# Before concatenation: CRMLSListing202510.csv = 27,586 rows
# Before concatenation: CRMLSListing202511.csv = 20,677 rows
# Before concatenation: CRMLSListing202512.csv = 18,773 rows
# Before concatenation: CRMLSListing202601.csv = 2,606 rows
# Before concatenation: CRMLSListing202602.csv = 32,884 rows
# Before concatenation: CRMLSListing202603.csv = 39,153 rows
# Before concatenation: CRMLSListing202604.csv = 39,020 rows
# Before concatenation: CRMLSListing202608.csv = 33,462 rows
# Total before concatenation = 894,360 rows
# After concatenation = 894,360 rows
# Before Residential filter = 894,360 rows
# After Residential filter = 568,163 rows
# Rows removed by filter = 326,197
# sold row counts
# Before concatenation: CRMLSSold202401_filled.csv = 17,958 rows
# Before concatenation: CRMLSSold202402.csv = 19,925 rows
# Before concatenation: CRMLSSold202403_filled.csv = 23,276 rows
# Before concatenation: CRMLSSold202404_filled.csv = 24,640 rows
# Before concatenation: CRMLSSold202405_filled.csv = 26,487 rows
# Before concatenation: CRMLSSold202406_filled.csv = 24,328 rows
# Before concatenation: CRMLSSold202407_filled.csv = 26,240 rows
# Before concatenation: CRMLSSold202408.csv = 24,558 rows
# Before concatenation: CRMLSSold202409.csv = 21,267 rows
# Before concatenation: CRMLSSold202410.csv = 23,274 rows
# Before concatenation: CRMLSSold202411.csv = 20,279 rows
# Before concatenation: CRMLSSold202412.csv = 20,241 rows
# Before concatenation: CRMLSSold202501_filled.csv = 18,738 rows
# Before concatenation: CRMLSSold202502.csv = 18,702 rows
# Before concatenation: CRMLSSold202503.csv = 21,445 rows
# Before concatenation: CRMLSSold202504.csv = 23,262 rows
# Before concatenation: CRMLSSold202505.csv = 23,154 rows
# Before concatenation: CRMLSSold202506.csv = 22,883 rows
# Before concatenation: CRMLSSold202507.csv = 23,646 rows
# Before concatenation: CRMLSSold202508.csv = 22,972 rows
# Before concatenation: CRMLSSold202509.csv = 22,443 rows
# Before concatenation: CRMLSSold202510.csv = 23,233 rows
# Before concatenation: CRMLSSold202511.csv = 19,088 rows
# Before concatenation: CRMLSSold202512.csv = 20,538 rows
# Before concatenation: CRMLSSold202601.csv = 16,487 rows
# Before concatenation: CRMLSSold202602.csv = 19,010 rows
# Before concatenation: CRMLSSold202603.csv = 23,372 rows
# Before concatenation: CRMLSSold202604.csv = 24,261 rows
# Before concatenation: CRMLSSold202608.csv = 23,127 rows
# Total before concatenation = 638,834 rows
# After concatenation = 638,834 rows
# Before Residential filter = 638,834 rows
# After Residential filter = 429,193 rows
# Rows removed by filter = 209,641
