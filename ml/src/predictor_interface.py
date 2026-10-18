
"""Inference interface for the TwinPulse SHAREE baseline model.

The returned probability is an exploratory model score, not a
clinically validated estimate of an individual's future event risk.
"""

from pathlib import Path

import joblib
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
MODEL_FILE = (
    ROOT
    / "data"
    / "processed"
    / "baseline"
    / "sharee_logistic_pipeline.joblib"
)

NUMERIC_FEATURES = [
    "age",
    "bmi",
    "sbp",
    "dbp",
    "imt_max",
    "lvmi",
    "ef",
]

CATEGORICAL_FEATURES = [
    "gender",
    "smoker",
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


class TwinPulsePredictor:
    """Load the fitted pipeline and predict for supplied patient features."""

    def __init__(self, model_path: Path = MODEL_FILE):
        self.model_path = Path(model_path)

        if not self.model_path.is_file():
            raise FileNotFoundError(
                f"Fitted model not found: {self.model_path}. "
                "Run ml/src/train_baseline.py first."
            )

        self.model = joblib.load(self.model_path)

    def predict(self, patient_features: dict) -> dict:
        """Return an exploratory score and predicted class.

        Required keys:
        age, bmi, sbp, dbp, imt_max, lvmi, ef, gender, smoker
        """
        if not isinstance(patient_features, dict):
            raise TypeError("patient_features must be a dictionary.")

        missing = [
            feature
            for feature in FEATURES
            if feature not in patient_features
        ]

        if missing:
            raise ValueError(
                f"Missing required features: {missing}"
            )

        # Ignore extra keys; only the trained features are passed on.
        row = {
            feature: patient_features[feature]
            for feature in FEATURES
        }
        input_df = pd.DataFrame([row], columns=FEATURES)

        # Numeric fields must be numeric or missing.
        for feature in NUMERIC_FEATURES:
            try:
                input_df[feature] = pd.to_numeric(
                    input_df[feature],
                    errors="raise",
                )
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Feature '{feature}' must be numeric or missing."
                ) from exc

        # Require a real value for each categorical field.
        for feature in CATEGORICAL_FEATURES:
            value = input_df.at[0, feature]

            if pd.isna(value):
                raise ValueError(
                    f"Feature '{feature}' cannot be missing."
                )

            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"Feature '{feature}' must be a non-empty string."
                )

            input_df.at[0, feature] = value.strip()

        # The pipeline handles numeric missing values through imputation.
        # The score is not calibrated or clinically validated.
        probability = float(
            self.model.predict_proba(input_df)[0, 1]
        )

        predicted_class = int(probability >= 0.5)

        return {
            "model": "LogisticRegression",
            "prediction": predicted_class,
            "exploratory_score": probability,
            "threshold": 0.5,
            "interpretation": (
                "Exploratory model output only; not a clinically "
                "validated cardiovascular event risk estimate."
            ),
        }


def main():
    predictor = TwinPulsePredictor()

    # Synthetic example values for a software smoke test.
    # These are not a real patient's measurements.
    example_patient = {
        "age": 60,
        "bmi": 27.0,
        "sbp": 145,
        "dbp": 90,
        "imt_max": 0.9,
        "lvmi": 110,
        "ef": 60,
        "gender": "M",
        "smoker": "No",
    }

    result = predictor.predict(example_patient)

    print("TwinPulse inference smoke test")
    print("Synthetic example only; not a real patient.")
    print(f"Predicted class: {result['prediction']}")
    print(
        "Exploratory model score: "
        f"{result['exploratory_score']:.4f}"
    )
    print(result["interpretation"])


if __name__ == "__main__":
    main()
