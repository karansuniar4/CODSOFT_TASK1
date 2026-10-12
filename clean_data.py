"""
AI-Assisted Data Cleaning & Preprocessing
CodSoft Data Analytics Internship — Task 1

This starter project uses transparent, reviewable rules (not an external AI API)
to flag and clean common data-quality problems.
Run from this project folder: python clean_data.py
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent
INPUT_FILE = ROOT / "data" / "messy_customers.csv"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    df = pd.read_csv(INPUT_FILE)
    original_rows = len(df)

    # 1. Inspect the source before changing anything.
    missing_before = df.isna().sum()
    blank_strings = df.astype("string").apply(
        lambda col: col.str.strip().eq("").sum()
    )
    duplicates_before = int(df.duplicated().sum())

    print("\n=== ORIGINAL DATA PREVIEW ===")
    print(df.head())
    print("\n=== ORIGINAL STRUCTURE ===")
    df.info()
    print("\n=== MISSING VALUES (pandas nulls) ===")
    print(missing_before)
    print("\n=== BLANK STRINGS ===")
    print(blank_strings)
    print(f"\nExact duplicate rows: {duplicates_before}")

    # 2. Normalize blank cells and trim text.
    cleaned = df.copy()
    cleaned = cleaned.replace(r"^\s*$", pd.NA, regex=True)
    for col in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[col] = cleaned[col].astype("string").str.strip()

    # 3. Normalize city capitalization and convert numeric columns safely.
    if "City" in cleaned.columns:
        cleaned["City"] = cleaned["City"].str.title()

    for col in ["Age", "PurchaseAmount", "CustomerID"]:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    # 4. Flag potentially invalid values; do not silently invent replacements.
    if "Age" in cleaned.columns:
        cleaned.loc[~cleaned["Age"].between(0, 120), "Age"] = pd.NA
    if "PurchaseAmount" in cleaned.columns:
        cleaned.loc[cleaned["PurchaseAmount"] < 0, "PurchaseAmount"] = pd.NA

    # 5. Remove exact duplicate records.
    cleaned = cleaned.drop_duplicates().copy()

    # 6. Fill numeric missing values with the median; text with a clear label.
    # For real business data, confirm these choices with a domain expert first.
    for col in cleaned.select_dtypes(include=["number"]).columns:
        if cleaned[col].isna().any():
            median_value = cleaned[col].median()
            if pd.notna(median_value):
                cleaned[col] = cleaned[col].fillna(median_value)

    for col in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[col] = cleaned[col].fillna("Unknown")

    # 7. Export cleaned data and a simple quality report.
    output_csv = OUTPUT_DIR / "cleaned_customers.csv"
    cleaned.to_csv(output_csv, index=False)

    report = {
        "input_file": str(INPUT_FILE.relative_to(ROOT)),
        "rows_before": original_rows,
        "rows_after": len(cleaned),
        "exact_duplicates_removed": duplicates_before,
        "missing_values_before_by_column": {
            str(k): int(v) for k, v in missing_before.items()
        },
        "blank_strings_before_by_column": {
            str(k): int(v) for k, v in blank_strings.items()
        },
        "missing_values_after_by_column": {
            str(k): int(v) for k, v in cleaned.isna().sum().items()
        },
        "output_file": str(output_csv.relative_to(ROOT)),
        "notes": [
            "Invalid numeric strings were converted to missing values.",
            "Numeric missing values were filled with column medians where available.",
            "Text missing values were labeled Unknown.",
            "Review these policies before applying them to real business data."
        ]
    }
    report_path = OUTPUT_DIR / "quality_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\n=== CLEANED DATA PREVIEW ===")
    print(cleaned.head())
    print(f"\nSaved cleaned data: {output_csv}")
    print(f"Saved quality report: {report_path}")

if __name__ == "__main__":
    main()
