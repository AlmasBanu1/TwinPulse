
from pathlib import Path
import csv
import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "raw" / "SHAREE" / "info.txt"
OUTPUT_DIR = ROOT / "data" / "processed"

COLUMNS = [
    "record_id",
    "gender",
    "age",
    "weight_kg",
    "height_cm",
    "bsa",
    "bmi",
    "smoker",
    "sbp",
    "dbp",
    "imt_max",
    "lvmi",
    "ef",
    "vascular_event",
]

NUMERIC_COLUMNS = [
    "age", "weight_kg", "height_cm", "bsa", "bmi",
    "sbp", "dbp", "imt_max", "lvmi", "ef",
]

MISSING_VALUES = {"", "n/a", "na", "nan", "null"}


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Source file not found: {SOURCE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    records = []
    rejected_lines = []
    metadata_lines = []

    with SOURCE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file, delimiter="\t")

        header = next(reader, None)
        if header is None:
            raise ValueError("The source file is empty.")

        print("Original header:")
        print(header)

        for line_number, row in enumerate(reader, start=2):
            if not row or not any(value.strip() for value in row):
                continue

            # Patient rows should begin with a numeric record ID.
            if not row[0].strip().isdigit():
                metadata_lines.append({
                    "line_number": line_number,
                    "content": "\t".join(row),
                })
                continue

            if len(row) != len(COLUMNS):
                rejected_lines.append({
                    "line_number": line_number,
                    "field_count": len(row),
                    "content": "\t".join(row),
                })
                continue

            record = {
                column: value.strip()
                for column, value in zip(COLUMNS, row)
            }

            records.append(record)

    if not records:
        raise ValueError("No valid patient rows were found.")

    df = pd.DataFrame(records, columns=COLUMNS)

    # Normalize missing-value tokens and categorical fields.
    for column in COLUMNS:
        df[column] = df[column].map(
            lambda value: (
                pd.NA
                if str(value).strip().lower() in MISSING_VALUES
                else str(value).strip()
            )
        )

    df["record_id"] = df["record_id"].astype("string")
    df["gender"] = df["gender"].str.upper()
    df["smoker"] = df["smoker"].str.lower()
    df["vascular_event"] = df["vascular_event"].str.lower()

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Audit parsing failures and duplicate patient IDs.
    duplicate_ids = df.loc[
        df["record_id"].duplicated(keep=False), "record_id"
    ].tolist()

    allowed_events = {
        "none",
        "myocardial infarction",
        "stroke",
        "syncope",
    }

    observed_events = set(df["vascular_event"].dropna().unique())
    unexpected_events = sorted(observed_events - allowed_events)

    # Do not silently discard records or unexpected labels.
    cleaned_path = OUTPUT_DIR / "sharee_clinical_cleaned.csv"
    df.to_csv(cleaned_path, index=False, na_rep="")

    missingness = (
        df.isna().sum()
        .rename("missing_count")
        .to_frame()
    )
    missingness["missing_percent"] = (
        missingness["missing_count"] / len(df) * 100
    ).round(2)
    missingness.to_csv(
        OUTPUT_DIR / "sharee_clinical_missingness.csv"
    )

    outcome_counts = (
        df["vascular_event"]
        .value_counts(dropna=False)
        .rename_axis("vascular_event")
        .reset_index(name="count")
    )
    outcome_counts.to_csv(
        OUTPUT_DIR / "sharee_clinical_outcome_counts.csv",
        index=False,
    )

    audit = {
        "source_file": str(SOURCE),
        "patient_rows_parsed": int(len(df)),
        "unique_patient_ids": int(df["record_id"].nunique()),
        "duplicate_patient_ids": duplicate_ids,
        "rejected_numeric_id_rows": rejected_lines,
        "non_patient_metadata_lines": metadata_lines,
        "observed_outcomes": {
            str(key): int(value)
            for key, value in df["vascular_event"]
            .value_counts(dropna=False)
            .items()
        },
        "unexpected_outcomes": unexpected_events,
        "numeric_columns": NUMERIC_COLUMNS,
        "clinical_features_with_missing_values": {
            column: int(df[column].isna().sum())
            for column in NUMERIC_COLUMNS
        },
        "note": (
            "Parsing audit only. Outcome semantics and feature validity "
            "must be confirmed before model training."
        ),
    }

    audit_path = OUTPUT_DIR / "sharee_clinical_audit.json"
    audit_path.write_text(
        json.dumps(audit, indent=2),
        encoding="utf-8",
    )

    print("\n--- CLINICAL DATA AUDIT ---")
    print(f"Patient rows parsed: {len(df)}")
    print(f"Unique patient IDs: {df['record_id'].nunique()}")
    print(f"Duplicate IDs: {duplicate_ids}")
    print(f"Rejected numeric-ID rows: {len(rejected_lines)}")
    print(f"Non-patient metadata lines: {len(metadata_lines)}")

    print("\nOutcome counts:")
    print(outcome_counts.to_string(index=False))

    print("\nMissing numeric values:")
    print(missingness.loc[NUMERIC_COLUMNS].to_string())

    print("\nUnexpected outcome labels:", unexpected_events)
    print("\nSaved files:")
    print(cleaned_path)
    print(OUTPUT_DIR / "sharee_clinical_missingness.csv")
    print(OUTPUT_DIR / "sharee_clinical_outcome_counts.csv")
    print(audit_path)


if __name__ == "__main__":
    main()
