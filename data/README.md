# Data Directory

This directory contains the project's data-related organization and documentation.

## Data Sources

TwinPulse primarily uses the **SHAREE — Smart Health for Assessing the Risk of Events via ECG** dataset from PhysioNet.

The dataset contains clinical/demographic information, ambulatory ECG recordings, and follow-up outcome information for hypertensive patients.

## Directory Organization

```text
data/
├── raw/
├── processed/
├── external/
└── README.md
```

### `raw/`

Original downloaded dataset files.

These files are intentionally excluded from GitHub.

### `processed/`

Generated datasets and feature tables created during preprocessing and feature engineering.

These files are excluded from GitHub because they are generated artifacts.

### `external/`

Optional supporting datasets used only when there is a justified project requirement.

Any external dataset must have appropriate attribution and licensing.

## Data Handling Rules

- Do not commit raw medical/physiological datasets.
- Do not commit unnecessary generated datasets.
- Do not commit personally identifiable information.
- Use only public, open, anonymized, or synthetic data permitted by the competition rules.
- Document important preprocessing decisions.
- Keep dataset versions and sources reproducible.
- Never fabricate observations or outcomes.

The exact SHAREE target definition and preprocessing pipeline will be finalized after dataset inspection.