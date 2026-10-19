# TwinPulse — SHAREE Exploratory Baseline Report

## Purpose

Compare a clinical-only logistic regression baseline with a clinical-plus-HRV
variant for the TwinPulse research proof-of-concept.

This is an exploratory experiment, not a clinically validated prediction system.

## Dataset and target

- Available records: 25 unique patients
- Candidate positive outcomes: 17
- Candidate negative outcomes: 8
- Target column: `event_12mo_binary_candidate`
- Validation: stratified four-fold cross-validation
- Model: logistic regression with class weighting
- Classification threshold: 0.5
- Random seed: 42

The binary target remains a candidate label pending confirmation of the
dataset's exact outcome definition and timing.

## Results

| Metric | Clinical-only | Clinical + HRV |
|---|---:|---:|
| Precision | 0.688 | 0.667 |
| Recall | 0.647 | 0.588 |
| F1-score | 0.667 | 0.625 |
| Out-of-fold ROC-AUC | 0.412 | 0.419 |
| Out-of-fold average precision | 0.627 | 0.621 |
| True negatives | 3 | 3 |
| False positives | 5 | 5 |
| False negatives | 6 | 7 |
| True positives | 11 | 10 |

## Features

### Clinical-only

- Age
- BMI
- Systolic blood pressure
- Sex
- Smoking status

### Clinical + HRV

The clinical features above, plus:

- Median heart rate
- SDNN
- RMSSD
- pNN50
- NN interval interquartile range

Patient identifiers, outcome text, target-derived information, source text,
quality flags, annotation counts, and annotation caveats were not used as
predictor features.

## Interpretation

The clinical-plus-HRV model did not improve precision, recall, F1-score, or
average precision compared with the clinical-only baseline. Its ROC-AUC was
slightly higher, but both ROC-AUC values were below 0.5.

These results do not demonstrate useful event discrimination. The apparent
precision and F1-scores should not be interpreted independently of the small
sample, high event prevalence, and poor ROC-AUC.

## Limitations

1. Only 25 of the 139 dataset records currently have ECG signal files available.
2. There are only eight candidate negative cases.
3. The target definition and timing remain subject to confirmation.
4. The dataset documents QRS annotations as unaudited.
5. HRV features may be affected by annotation errors and signal artifacts.
6. Four-fold cross-validation estimates are highly uncertain with this sample.
7. No independent external validation has been performed.
8. These experiments do not establish clinical validity or patient-level
   medical decision-making utility.

## Conclusion

This baseline establishes an initial reproducible comparison, but neither model
should be presented as clinically reliable. Additional data verification and
independent evaluation would be needed before making performance claims.

## Reproducibility

- Script: `ml/experiments/run_sharee_baseline.py`
- Machine-readable results: `ml/experiments/sharee_diagnostics/baseline_results.json`
- Data-quality report: `ml/experiments/sharee_diagnostics/data_quality_report.txt`

Raw SHAREE recordings and patient-level processed data must not be committed
to the public repository.
