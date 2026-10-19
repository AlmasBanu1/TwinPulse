# TwinPulse — System Architecture

## 1. Purpose

TwinPulse is a research-oriented Digital Twin proof-of-concept for exploring cardiovascular and cerebrovascular event prediction in hypertensive patients.

The prototype combines a clinical patient profile, a versioned software representation of patient state, simulated physiological observations, and an experimental machine-learning inference pipeline.

**Clinical safety:** TwinPulse is not clinically validated. Its model output must not be used for diagnosis, treatment, or medical decisions.

## 2. Architecture Overview

```text
                  SHAREE Research Dataset
                            |
                            v
                 Clinical Data Preparation
                            |
                            v
                  Binary Target Construction
                            |
                            v
                  Logistic Regression Model
                            |
                            v
                    Fitted Model Pipeline
                            |
                            v
+---------------------------------------------------+
|                  TwinPulse Backend                |
|                                                   |
|  Patient Profile / Digital Twin State             |
|              |                                    |
|              v                                    |
|  Versioned State Updates and Activity History     |
|              |                                    |
|              v                                    |
|  Clinical-Feature Model Inference                 |
+--------------------------+------------------------+
                           |
                       FastAPI
                           |
                           v
+---------------------------------------------------+
|                React + TypeScript                 |
|                                                   |
|  Patient Overview                                 |
|  Clinical Profile                                 |
|  Exploratory Model Output                         |
|  Simulated Physiological Observations             |
|  Digital Twin State and Activity History          |
+---------------------------------------------------+
```

The fitted model is trained separately from the running dashboard. The backend loads the saved pipeline for inference.

## 3. Main Components

### 3.1 Research Data and Preparation

The SHAREE dataset is the primary research dataset.

The current clinical preparation and target-building pipeline produces a modeling table from the cleaned clinical data.

Relevant implementation files:

- `ml/src/prepare_sharee_clinical.py`
- `ml/src/build_sharee_target.py`
- `ml/src/validate_sharee_model_table.py`

Raw dataset files must not be committed to the public repository.

### 3.2 Prediction Target

The current binary target is defined as:

- `0`: No vascular event recorded in the source outcome field.
- `1`: Myocardial infarction, stroke, or syncope recorded.

The modeling cohort contains 139 patients: 17 positive outcomes and 122 negative outcomes.

The interpretation is limited to the recorded outcome labels and available cohort. It does not represent every possible cardiovascular event.

### 3.3 Machine-Learning Pipeline

The baseline model is Logistic Regression.

Numeric inputs:

- Age
- BMI
- Systolic blood pressure
- Diastolic blood pressure
- Maximum intima-media thickness (IMT)
- Left ventricular mass index (LVMI)
- Ejection fraction (EF)

Categorical inputs:

- Gender
- Smoking status

The training pipeline applies median imputation and standardization to numeric variables, and most-frequent imputation and one-hot encoding to categorical variables.

The fitted pipeline is saved at:

`data/processed/baseline/sharee_logistic_pipeline.joblib`

Inference is implemented in `ml/src/predictor_interface.py`.

The returned score is an experimental model output. It is not a calibrated clinical risk estimate.

### 3.4 Backend and Digital Twin Engine

The backend uses FastAPI.

The Digital Twin maintains a software representation of the selected patient's clinical profile and current application state.

The demonstrated workflow supports:

1. Creating a virtual patient.
2. Recording clinical information.
3. Adding a simulated physiological observation.
4. Updating the twin's state version.
5. Recording state activity.
6. Running exploratory model inference and recording the prediction update.

The dashboard smoke test demonstrated state versions 1, 2, and 3 for clinical creation, physiological update, and prediction update, respectively.

### 3.5 Frontend Dashboard

The frontend uses React and TypeScript with Vite.

The dashboard provides:

- Patient overview
- Clinical profile entry
- Digital Twin state display
- Exploratory model output
- Simulated physiological input
- State version and activity history

The interface labels simulated observations as demo data and identifies the application as a research prototype.

## 4. Current Data Flow

### Clinical Profile and Prediction

```text
Clinical Profile
       |
       v
Backend Patient State
       |
       v
Clinical Features
       |
       v
Fitted Logistic Regression Pipeline
       |
       v
Exploratory Score and Binary Class
       |
       v
Updated Digital Twin State
       |
       v
Dashboard and Activity History
```

### Simulated Physiological Update

```text
Demo Heart Rate / SDNN / RMSSD
                 |
                 v
          Backend Update
                 |
                 v
       Digital Twin State Version
                 |
                 v
          Activity History
                 |
                 v
             Dashboard
```

**Important:** The current baseline model does not consume the simulated heart rate, SDNN, or RMSSD values. These observations update the Digital Twin state but are not currently integrated into model inference.

## 5. Preliminary Model Evaluation

The baseline was evaluated using five-fold stratified out-of-fold predictions.

| Metric | Result |
|---|---:|
| Patients | 139 |
| Positive outcomes | 17 |
| Negative outcomes | 122 |
| ROC-AUC | 0.4634 |
| Average precision | 0.1252 |
| Precision | 0.1321 |
| Recall / sensitivity | 0.4118 |
| F1 score | 0.2000 |

At the default 0.5 threshold:

| Outcome | Count |
|---|---:|
| True negatives | 76 |
| False positives | 46 |
| False negatives | 10 |
| True positives | 7 |

These preliminary results indicate weak discrimination. The small number of positive outcomes, lack of external validation, and absence of probability calibration limit interpretation.

## 6. Current Implementation vs. Planned Work

### Demonstrated in the prototype

- React/TypeScript dashboard
- FastAPI connectivity
- Clinical profile creation
- Versioned Digital Twin state
- Simulated physiological updates
- Activity history
- Logistic Regression inference using clinical and demographic inputs

### Not yet demonstrated as integrated functionality

- Sequential replay of the SHAREE ECG recordings through the dashboard
- ECG signal preprocessing and R-peak detection as part of the running application
- HRV feature extraction from replayed ECG
- Feeding updated ECG-derived features into the risk model
- Clinically validated or calibrated event-risk predictions
- External validation on an independent cohort

These items must remain described as planned work until implemented and tested.

## 7. Technology Stack

- Python
- Pandas and NumPy
- Scikit-learn
- Joblib
- FastAPI
- React
- TypeScript
- Vite
- Git and GitHub

## 8. Limitations and Safety

TwinPulse is an educational and research proof-of-concept.

It does not provide a medical diagnosis, treatment recommendations, or a clinically validated prediction of an individual's future event risk.

The current dashboard's simulated physiological observations are not real wearable measurements or a live ECG stream.

The model's performance must be reported transparently. No claim of clinical usefulness should be made without appropriate additional validation.

## 9. Next Architecture Milestones

1. Verify API contracts and automated integration tests.
2. Document the SHAREE schema and preprocessing assumptions.
3. Implement and test ECG replay and signal-quality handling.
4. Develop and validate ECG-derived HRV features.
5. Evaluate whether physiological features improve prediction using patient-level validation.
6. Integrate only verified features into the inference pipeline.
7. Complete the competition presentation, demo video, and reproducibility instructions.
