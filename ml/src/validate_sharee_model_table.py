
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "processed" / "sharee_model_table.csv"


def main():
    if not INPUT.exists():
        raise FileNotFoundError(f"Modeling table not found: {INPUT}")

    df = pd.read_csv(INPUT)

    print("=" * 60)
    print("1. DATASET SHAPE")
    print("=" * 60)
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\n" + "=" * 60)
    print("2. COLUMN NAMES AND DATA TYPES")
    print("=" * 60)
    print(df.dtypes.to_string())

    print("\n" + "=" * 60)
    print("3. MISSING VALUES")
    print("=" * 60)
    missing = df.isna().sum()
    missing_report = pd.DataFrame({
        "missing_count": missing,
        "missing_percent": (missing / len(df) * 100).round(2),
    })
    print(missing_report.to_string())

    print("\n" + "=" * 60)
    print("4. CLINICAL FEATURE SUMMARY")
    print("=" * 60)

    feature_columns = [
        "age",
        "weight_kg",
        "height_cm",
        "bsa",
        "bmi",
        "sbp",
        "dbp",
        "imt_max",
        "lvmi",
        "ef",
    ]

    available = [c for c in feature_columns if c in df.columns]
    print(df[available].describe().round(2).to_string())

    print("\n" + "=" * 60)
    print("5. CATEGORICAL VALUE COUNTS")
    print("=" * 60)

    for column in ["gender", "smoker", "vascular_event"]:
        if column in df.columns:
            print(f"\n{column}:")
            print(df[column].value_counts(dropna=False).to_string())

    print("\n" + "=" * 60)
    print("6. TARGET CONSISTENCY")
    print("=" * 60)

    expected_target = (df["vascular_event"] != "none").astype("int8")

    print("Target mismatches:", int(
        (df["target_event"] != expected_target).sum()
    ))
    print("Duplicate patient IDs:", int(df["record_id"].duplicated().sum()))
    print("Positive events:", int(df["target_event"].sum()))
    print("Negative outcomes:", int((df["target_event"] == 0).sum()))

    if len(df) != 139:
        raise ValueError(f"Expected 139 patients, found {len(df)}")

    if df["record_id"].duplicated().any():
        raise ValueError("Duplicate patient IDs detected.")

    if (df["target_event"] != expected_target).any():
        raise ValueError("Target labels do not match the source outcomes.")

    print("\nValidation checks passed.")


if __name__ == "__main__":
    main()
