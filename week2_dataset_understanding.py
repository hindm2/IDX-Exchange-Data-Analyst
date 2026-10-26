"""MLS dataset understanding deliverable.

Colab: %run /content/dataset_understanding.py
Inputs: extracted monthly sold CSVs under /content/IDX_data.
Outputs: filtered CSV and reports under /content/dataset_reports.
No imputation, outlier removal, or duplicate removal is performed.
May, June, July, September 2026 are excluded because their 1,000-row
downloads are potentially incomplete. Coverage is preliminary.
"""
from pathlib import Path
import argparse
import re
import pandas as pd

EXCLUDED = {"202605", "202606", "202607", "202609"}
NUMERIC = ["ClosePrice", "LivingArea", "DaysOnMarket"]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="/content/IDX_data")
    parser.add_argument("--output", default="/content/dataset_reports")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    paths = {}
    for path in sorted(Path(args.input).rglob("*.csv")):
        if "__MACOSX" in path.parts or path.name.startswith("._"):
            continue
        match = re.fullmatch(r"CRMLSSold(\d{6})(?:_filled)?\.csv", path.name)
        if not match:
            continue
        month = match.group(1)
        if not "202401" <= month <= "202609" or month in EXCLUDED:
            continue
        if month in paths:
            raise ValueError(f"Multiple files for {month}; choose one before running.")
        paths[month] = path
    if not paths:
        raise FileNotFoundError("No eligible monthly sold CSVs found in input folder.")
    frames, inventory = [], []
    for month, path in sorted(paths.items()):
        frame = pd.read_csv(path, low_memory=False)
        required = {"PropertyType", "PropertySubType", *NUMERIC}
        if not required.issubset(frame.columns):
            raise ValueError(f"{path.name}: missing columns {required - set(frame.columns)}")
        frames.append(frame)
        inventory.append({"Month": month, "File": path.name, "Rows": len(frame)})
    raw = pd.concat(frames, ignore_index=True)
    unique_types = sorted(raw["PropertyType"].dropna().astype(str).unique())
    type_counts = raw["PropertyType"].value_counts(dropna=False)
    type_counts.rename_axis("PropertyType").reset_index(name="Rows").to_csv(
        output / "property_type_counts.csv", index=False)
    # Keep only records meeting BOTH exact-match conditions.
    filtered = raw.loc[
        raw["PropertyType"].eq("Residential") &
        raw["PropertySubType"].eq("SingleFamilyResidence")
    ].copy()
    # Report pandas nulls; zero values are not counted as nulls.
    missing = pd.DataFrame({
        "Data_type": filtered.dtypes.astype(str),
        "Missing_count": filtered.isna().sum(),
        "Missing_percent": filtered.isna().mean() * 100,
    })
    missing["Above_90_percent"] = missing["Missing_percent"] > 90
    missing = missing.sort_values("Missing_percent", ascending=False)
    missing.to_csv(output / "missing_value_report.csv", index_label="Column")
    missing.loc[missing["Above_90_percent"]].to_csv(
        output / "above_90_percent_null.csv", index_label="Column")
    numbers = filtered[NUMERIC].apply(pd.to_numeric, errors="coerce")
    summary = numbers.describe(percentiles=[.01, .05, .25, .5, .75, .95, .99]).T
    summary = summary.rename(columns={"50%": "median"})
    summary.to_csv(output / "numeric_distribution_summary.csv", index_label="Field")
    # Preserve all filtered columns and original values in the saved dataset.
    filtered.to_csv(output / "sold_residential_single_family_filtered.csv", index=False)
    pd.DataFrame(inventory).to_csv(output / "monthly_file_inventory.csv", index=False)
    notes = (
        f"Unique property types before filtering: {unique_types}\n"
        "Filter: PropertyType == 'Residential' AND "
        "PropertySubType == 'SingleFamilyResidence'.\n"
        f"Monthly files used: {len(paths)}\n"
        f"Before concatenation (sum): {sum(item['Rows'] for item in inventory):,}\n"
        f"After concatenation / before filtering: {len(raw):,}\n"
        f"After filtering: {len(filtered):,} rows, {filtered.shape[1]} columns\n"
        "Excluded potentially incomplete months: May, June, July, September 2026.\n"
        "Other downloads have not been independently verified as complete.\n"
        "Null counts are based on pandas isna(); zeros are retained.\n"
        "Numeric summaries use non-null values; non-numeric strings are coerced\n"
        "to null only in the summary copy. Median is the 50th percentile.\n"
        "No rows removed for duplicates, invalid prices, or outliers.\n"
    )
    (output / "dataset_understanding_report.txt").write_text(notes, encoding="utf-8")
    print(notes)
    print(missing.round(2).to_string())
    print(summary.round(2).to_string())
    print(f"Saved dataset and reports to {output}")

if __name__ == "__main__":
    main()
