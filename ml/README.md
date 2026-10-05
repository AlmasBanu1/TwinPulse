# Machine Learning Pipeline

This directory contains the machine learning pipeline for TwinPulse.

## Responsibilities

The ML workstream covers:

1. Dataset inspection
2. Data preprocessing
3. Feature engineering
4. HRV feature extraction
5. Exploratory data analysis
6. Model training
7. Model comparison
8. Evaluation
9. Explainability
10. Inference pipeline
11. Integration with the Digital Twin

## Planned Structure

```text
ml/
├── experiments/
├── models/
├── notebooks/
├── src/
└── README.md
```

### `experiments/`

Experiment configurations, comparison records, and reproducibility notes.

### `models/`

Locally generated trained model artifacts.

Model binaries are excluded from GitHub unless a future decision explicitly determines that a specific small artifact should be versioned.

### `notebooks/`

Exploratory and analytical notebooks.

### `src/`

Reusable production-oriented ML code.

Potential modules include:

```text
src/
├── data/
├── features/
├── preprocessing/
├── training/
├── evaluation/
├── explainability/
└── inference/
```

The exact module structure will be created as implementation begins.

## Initial Model Strategy

The baseline progression is:

```text
Logistic Regression
        ↓
Random Forest
        ↓
XGBoost (if justified)
```

Deep learning is optional and will not be introduced merely for complexity.

## Evaluation

Model evaluation will prioritize:

- Recall
- Precision
- F1-score
- ROC-AUC
- PR-AUC
- Confusion matrix
- Cross-validation results

Accuracy alone will not be used as the primary measure because the dataset is expected to contain relatively few positive outcomes.

## Validation Rule

Patient-level separation between training and evaluation data is mandatory.

The same patient's physiological observations must never appear across training and test splits in a way that causes data leakage.

## Reproducibility

All experiments should record:

- Dataset version/source
- Feature set
- Preprocessing steps
- Model configuration
- Random seed where applicable
- Evaluation metrics
- Important observations

No ML result should be fabricated or manually altered.