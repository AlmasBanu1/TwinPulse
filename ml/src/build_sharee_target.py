
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

INPUT = ROOT / "data" / "processed" / "sharee_clinical_cleaned.csv"
OUTPUT = ROOT / "data" / "processed" / "sharee_model_table.csv"

EXPECTED_PATIENTS = 139
EXPECTED_POSITIVE_EVENTS = 17
EXPECTED_NEGATIVE_OUTCOMES = 122

VALID_OUTCOMES = {
    "none",
    "myocardial infarction",
    "stroke",
    "syncope",
}


def main():
    # 1. Check that the input file exists.
    if not INPUT.exists():
        raise FileNotFoundError(
            f"Cleaned clinical data not found: {INPUT}"
        )

    # 2. Read patient IDs as strings to preserve leading zeros.
    df = pd.read_csv(
        INPUT,
        dtype={"record_id": "string"},
    )

    # 3. Check required columns.
    required = {"record_id", "vascular_event"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    # 4. Normalize patient IDs.
    df["record_id"] = (
        df["record_id"]
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .str.zfill(5)
    )

    # Reject empty, malformed, or unexpected-length identifiers.
    if df["record_id"].isna().any() or (
        df["record_id"].str.fullmatch(r"\d{5}").fillna(False).eq(False).any()
    ):
        raise ValueError(
            "Invalid patient IDs found. Expected five-digit numeric IDs."
        )

    # 5. Normalize outcome labels.
    df["vascular_event"] = (
        df["vascular_event"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    if df["vascular_event"].isna().any():
        raise ValueError("Missing outcome labels found.")

    # Do not silently convert unexpected labels into positive outcomes.
    unexpected = set(df["vascular_event"].unique()) - VALID_OUTCOMES

    if unexpected:
        raise ValueError(
            f"Unexpected outcome labels found: {sorted(unexpected)}"
        )

    # 6. Check patient ID uniqueness.
    if df["record_id"].duplicated().any():
        duplicates = df.loc[
            df["record_id"].duplicated(keep=False), "record_id"
        ].tolist()

        raise ValueError(
            f"Duplicate patient IDs found: {duplicates}"
        )

    # 7. Create the binary exploratory outcome.
    # 0 = no event recorded in the source outcome field
    # 1 = myocardial infarction, stroke, or syncope recorded
    df["target_event"] = (
        df["vascular_event"] != "none"
    ).astype("int8")

    # 8. Report outcome mapping and cohort counts.
    print("Outcome mapping:")
    print(
        df.groupby(["vascular_event", "target_event"])
        .size()
        .rename("patients")
        .reset_index()
        .to_string(index=False)
    )

    print("\nBinary target counts:")
    print(
        df["target_event"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    positive_events = int(df["target_event"].sum())
    negative_outcomes = int((df["target_event"] == 0).sum())

    print("\nTotal patients:", len(df))
    print("Unique patients:", df["record_id"].nunique())
    print("Positive events:", positive_events)
    print("Negative outcomes:", negative_outcomes)

    # 9. Check expected cohort counts.
    if len(df) != EXPECTED_PATIENTS:
        raise ValueError(
            f"Expected {EXPECTED_PATIENTS} patients, found {len(df)}."
        )

    if positive_events != EXPECTED_POSITIVE_EVENTS:
        raise ValueError(
            f"Expected {EXPECTED_POSITIVE_EVENTS} positive events, "
            f"found {positive_events}."
        )

    if negative_outcomes != EXPECTED_NEGATIVE_OUTCOMES:
        raise ValueError(
            f"Expected {EXPECTED_NEGATIVE_OUTCOMES} negative outcomes, "
            f"found {negative_outcomes}."
        )

    # 10. Save the modeling table.
    # Keep the original event label for auditing, but exclude it
    # from model inputs when training to prevent target leakage.
    df.to_csv(OUTPUT, index=False)

    print(f"\nSaved modeling table to:\n{OUTPUT}")
    print("\nAll target-building checks passed.")


if __name__ == "__main__":
    main()
