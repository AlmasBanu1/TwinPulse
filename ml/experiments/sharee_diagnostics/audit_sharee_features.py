
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "processed" / "sharee_model_table.csv"


def main():
    df = pd.read_csv(INPUT)

    print("=" * 55)
    print("1. AGE AUDIT")
    print("=" * 55)
    print("Minimum age:", df["age"].min())
    print("Patients younger than 55:", int((df["age"] < 55).sum()))
    print(
        df.loc[df["age"] < 55,
               ["record_id", "age", "vascular_event", "target_event"]]
        .sort_values("age")
        .to_string(index=False)
    )

    print("\n" + "=" * 55)
    print("2. CLINICAL FEATURE CORRELATIONS")
    print("=" * 55)

    features = [
        "age", "weight_kg", "height_cm", "bsa", "bmi",
        "sbp", "dbp", "imt_max", "lvmi", "ef",
    ]
    corr = df[features].corr(numeric_only=True)
    print(corr.round(2).to_string())

    print("\n" + "=" * 55)
    print("3. TARGET COUNTS BY RECORDED EVENT")
    print("=" * 55)
    print(
        df.groupby("vascular_event", dropna=False)
        .agg(
            patients=("record_id", "size"),
            events=("target_event", "sum"),
            mean_age=("age", "mean"),
        )
        .round(2)
        .to_string()
    )

    print("\n" + "=" * 55)
    print("4. DUPLICATE / IDENTIFIER CHECK")
    print("=" * 55)
    print("Duplicate record IDs:", df["record_id"].duplicated().sum())
    print("Unique target values:", sorted(df["target_event"].unique()))


if __name__ == "__main__":
    main()
