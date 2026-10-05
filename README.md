# TwinPulse

## Dynamic Digital Twin for Cardiovascular Event Risk Prediction in Hypertensive Patients

TwinPulse is a research-oriented proof-of-concept developed for the **Digital Twin Challenge 2026 by Happiest Health**.

The project explores how a Digital Twin can combine historical clinical information with a replayed physiological data stream to represent a hypertensive patient's current health state and estimate the risk of a major cardiovascular or cerebrovascular event over a defined prediction horizon.

> **Note:** TwinPulse is an educational/research proof-of-concept and is not a clinically validated diagnostic or treatment system.

---

## Problem Statement

Hypertension is a major risk factor for cardiovascular and cerebrovascular disease. Traditional risk assessment often relies on static clinical measurements and historical patient information.

TwinPulse explores a more dynamic approach:

- Maintain a virtual representation of a patient.
- Combine historical clinical information with physiological time-series data.
- Extract meaningful physiological features from the data stream.
- Estimate future cardiovascular/cerebrovascular event risk using machine learning.
- Continuously update the Digital Twin state as new physiological observations are replayed.
- Present the patient's state and risk information through a doctor-facing dashboard.

---

## Proposed Solution

TwinPulse consists of five major layers:

```text
Historical Clinical Data
        +
Replayed Physiological Stream
        ↓
Data Processing & Feature Engineering
        ↓
Digital Twin Patient State
        ↓
Machine Learning Risk Prediction
        ↓
Doctor-Facing Dashboard
```

The physiological stream is based on recorded ambulatory ECG data from the SHAREE dataset and is replayed sequentially to simulate a continuously updating physiological input.

---

## Primary Dataset

### SHAREE — Smart Health for Assessing the Risk of Events via ECG

The project uses the **SHAREE dataset from PhysioNet** as its primary research dataset.

The dataset contains:

- Hypertensive patients
- Demographic and clinical information
- Ambulatory ECG recordings
- Blood pressure information
- Follow-up information
- Recorded cardiovascular/cerebrovascular outcomes

The dataset will be inspected before finalizing the exact prediction target and feature set.

Raw dataset files are **not committed to this repository**.

---

## Prediction Objective

The initial objective is to estimate the probability of a major cardiovascular/cerebrovascular event within a **12-month follow-up horizon**.

The exact target definition will be finalized after inspecting the original dataset metadata and outcome encoding.

The project will not claim to predict individual heart attacks or other medical events with clinical certainty.

---

## Digital Twin Concept

The Digital Twin represents a software-based virtual state of a patient.

It maintains information such as:

- Patient demographics
- Historical clinical information
- Physiological state
- Derived HRV features
- Current risk probability
- Risk category
- Recent state changes
- Prediction trajectory

The Digital Twin and machine learning model are treated as separate components.

```text
Digital Twin
    │
    ├── Historical State
    ├── Current Physiological State
    ├── Derived Features
    └── Risk State
             │
             ↓
       ML Prediction Model
             │
             ↓
       Updated Risk State
```

---

## Machine Learning

The ML pipeline will initially evaluate interpretable and tree-based models:

1. Logistic Regression
2. Random Forest
3. XGBoost, if justified by the experimental results

Deep learning will only be considered if it provides a meaningful technical benefit.

Potential feature categories include:

- Age
- Sex
- Systolic blood pressure
- Diastolic blood pressure
- Mean heart rate
- Mean RR interval
- SDNN
- RMSSD
- pNN50
- LF
- HF
- LF/HF
- Other HRV features where technically justified

The final feature set will be determined after dataset inspection and data-quality analysis.

---

## Explainability

TwinPulse will prioritize interpretable risk assessment.

The system will investigate feature-importance and explainability techniques such as:

- Logistic Regression coefficients
- Tree-based feature importance
- SHAP, if appropriate

The dashboard will present the major factors contributing to the model's current risk estimate.

---

## System Architecture

```text
                ┌─────────────────────────┐
                │ Historical Clinical Data│
                │ Demographics / BP / etc│
                └────────────┬────────────┘
                             │
                             │
                ┌────────────▼────────────┐
                │ Physiological Data      │
                │ Recorded ECG / HRV      │
                │ Replay Simulation       │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │ Data Processing         │
                │ Feature Engineering     │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │ Digital Twin Engine     │
                │ Patient State           │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │ ML Risk Prediction      │
                │ Probability + Category  │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │ Doctor Dashboard        │
                │ State + Risk + Factors  │
                └─────────────────────────┘
```

---

## Technology Stack

### Machine Learning

- Python
- Pandas
- NumPy
- SciPy
- Scikit-learn
- XGBoost, if required
- SHAP, if required

### Physiological Signal Processing

- ECG preprocessing
- QRS / R-peak detection
- RR interval extraction
- Heart Rate Variability analysis

### Backend

- To be finalized during implementation

### Frontend

- To be finalized during implementation

### Digital Twin

- Custom application-level Digital Twin state engine

### Development

- Git
- GitHub
- VS Code

---

## Repository Structure

```text
TwinPulse/
│
├── backend/
│
├── data/
│   └── README.md
│
├── digital-twin/
│
├── docs/
│   ├── architecture/
│   ├── presentation/
│   └── video/
│
├── frontend/
│
├── ml/
│   ├── experiments/
│   ├── models/
│   ├── notebooks/
│   ├── src/
│   └── README.md
│
├── tests/
│
├── .env.example
├── .gitignore
├── DECISIONS.md
├── LICENSE
├── README.md
└── ROADMAP.md
```

---

## Competition Requirements Mapping

TwinPulse is designed to address the major requirements of the Digital Twin Challenge:

| Requirement | TwinPulse Approach |
|---|---|
| Specific chronic/lifestyle condition | Hypertension |
| Static/historical data | SHAREE clinical and demographic information |
| Dynamic physiological data | Replayed ambulatory ECG/HRV stream |
| Algorithmic model | Machine learning risk prediction |
| Specific adverse outcome | 12-month cardiovascular/cerebrovascular event risk |
| Digital Twin | Software representation of patient state |
| Doctor interaction | Doctor-facing dashboard |
| Explainability | Feature importance / SHAP where appropriate |
| Public GitHub | This repository |
| Architecture documentation | `docs/architecture/` |
| Presentation | `docs/presentation/` |
| Video | `docs/video/` |

---

## Project Status

**Current phase:** Repository Foundation

The project is currently being initialized.

Next major milestone:

> Inspect the SHAREE dataset and finalize the target definition, available clinical variables, physiological data format, and feasible HRV feature pipeline.

---

## Important Limitations

TwinPulse is a research and educational proof-of-concept.

The project does **not** claim:

- Clinical validation
- Medical diagnosis
- Treatment recommendations
- Guaranteed event prediction
- Real-time clinical monitoring
- Generalization to the entire population
- Replacement of medical professionals

The model's performance will be reported honestly using appropriate evaluation metrics and patient-level validation.

---

## Team

**Team:** TwinPulse

**Institution:** SVCE, Bengaluru

Team member details and competition-specific information will be added to the project documentation as required.

---

## License

This project is released under the license included in the repository.

Dataset licensing and attribution will be respected separately according to the original dataset provider's terms.