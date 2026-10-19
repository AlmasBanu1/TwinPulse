from pathlib import Path
import json
import warnings

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "sharee_analysis_candidate.csv"
OUTPUT = ROOT / "experiments" / "sharee_diagnostics"
SEED = 42

CLINICAL_NUMERIC = ["age_years", "bmi", "sbp_mmHg"]
CLINICAL_CATEGORICAL = ["sex", "smoker"]

HRV_FEATURES = [
    "median_hr_bpm",
    "sdnn_ms",
    "rmssd_ms",
    "pnn50_percent",
    "nn_iqr_ms",
]

TARGET = "event_12mo_binary_candidate"


def make_pipeline(numeric_features, categorical_features):
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocess = ColumnTransformer([
        ("numeric", numeric_pipeline, numeric_features),
        ("categorical", categorical_pipeline, categorical_features),
    ])

    return Pipeline([
        ("preprocess", preprocess),
        ("model", LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=SEED,
        )),
    ])


def evaluate(df, name, numeric_features, categorical_features, cv):
    X = df[numeric_features + categorical_features].copy()
    y = df[TARGET].astype(int)

    model = make_pipeline(numeric_features, categorical_features)

    # Each patient's row is held out once; all preprocessing is fitted
    # within the corresponding training fold.
    probabilities = cross_val_predict(
        model, X, y, cv=cv, method="predict_proba"
    )[:, 1]

    predictions = (probabilities >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(
        y, predictions, labels=[0, 1]
    ).ravel()

    result = {
        "experiment": name,
        "n_patients": int(len(df)),
        "positive_cases": int(y.sum()),
        "negative_cases": int((y == 0).sum()),
        "folds": cv.n_splits,
        "threshold": 0.5,
        "precision": float(precision_score(
            y, predictions, zero_division=0
        )),
        "recall": float(recall_score(
            y, predictions, zero_division=0
        )),
        "f1": float(f1_score(
            y, predictions, zero_division=0
        )),
        "roc_auc_oof": float(roc_auc_score(y, probabilities)),
        "average_precision_oof": float(
            average_precision_score(y, probabilities)
        ),
        "confusion_matrix": {
            "tn": int(tn), "fp": int(fp),
            "fn": int(fn), "tp": int(tp),
        },
        "features": numeric_features + categorical_features,
        "random_seed": SEED,
    }

    print(f"\n===== {name} =====")
    print(json.dumps(result, indent=2))
    return result


def main():
    if not DATA.exists():
        raise FileNotFoundError(f"Missing input table: {DATA}")

    df = pd.read_csv(DATA)

    required = set(
        CLINICAL_NUMERIC + CLINICAL_CATEGORICAL
        + HRV_FEATURES + [TARGET, "record_id", "quality_flag"]
    )
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df["record_id"].duplicated().any():
        raise ValueError("Duplicate patient/record IDs detected.")

    if df[TARGET].isna().any() or set(df[TARGET].unique()) != {0, 1}:
        raise ValueError("Target must contain only non-missing 0 and 1.")

    if len(df) < 20 or df[TARGET].value_counts().min() < 4:
        raise ValueError(
            "Insufficient class counts for the configured four-fold CV."
        )

    # Deterministic folds; rows represent one record per patient.
    cv = StratifiedKFold(
        n_splits=4, shuffle=True, random_state=SEED
    )

    print("TwinPulse SHAREE exploratory baseline")
    print(f"Input: {DATA}")
    print(f"Patients: {len(df)}")
    print(f"Target counts: {df[TARGET].value_counts().to_dict()}")
    print(f"HRV quality flags: {df['quality_flag'].value_counts().to_dict()}")
    print("Important: QRS annotations are unaudited.")

    results = [
        evaluate(
            df,
            "clinical_only",
            CLINICAL_NUMERIC,
            CLINICAL_CATEGORICAL,
            cv,
        ),
        evaluate(
            df,
            "clinical_plus_hrv",
            CLINICAL_NUMERIC + HRV_FEATURES,
            CLINICAL_CATEGORICAL,
            cv,
        ),
    ]

    OUTPUT.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT / "baseline_results.json"
    output_file.write_text(
        json.dumps({
            "purpose": "Exploratory proof-of-concept only",
            "target": TARGET,
            "dataset": str(DATA),
            "limitations": [
                "Only 25 patients are available in this subset.",
                "The binary target is a candidate label.",
                "QRS annotations are unaudited.",
                "HRV features may be affected by annotation errors.",
                "Four-fold out-of-fold metrics are highly uncertain.",
                "These results do not establish clinical validity.",
                "Predictions at threshold 0.5 are exploratory only.",
            ],
            "results": results,
        }, indent=2),
        encoding="utf-8",
    )

    print(f"\nSaved results to: {output_file}")


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.filterwarnings("default")
        main()
