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

TwinPulse combines historical clinical information, a Digital Twin state engine, and exploratory machine-learning inference in a doctor-facing dashboard.

The current proof-of-concept has five main components:

1. **Clinical data:** Patient demographic and clinical features supplied to the inference interface.
2. **Physiological observations:** Simulated heart-rate and HRV observations used to update the Digital Twin state.
3. **Digital Twin engine:** Maintains versioned clinical state, physiological state, prediction state, and update history in memory.
4. **ML inference:** Produces an exploratory classification output using clinical features.
5. **Dashboard and API:** A React dashboard communicates with a FastAPI backend to display state and invoke updates and predictions.

### Current Data Flow

```text
Clinical Patient Features
          |
          v
   FastAPI Backend
          |
          v
 Clinical ML Inference ------> Exploratory Prediction
          |                            |
          +-------------+--------------+
                        v
                Digital Twin State
                        ^
                        |
             Simulated Physiological
                   Observations
                        |
                        v
                React Dashboard
```

**Implementation boundary:** The current dashboard does not replay real ECG recordings. Simulated physiological observations update the Digital Twin but are not fed into the deployed prediction model. Real ECG replay and end-to-end HRV integration remain future work.

---

## Primary Dataset

### SHAREE — Smart Health for Assessing the Risk of Events via ECG

TwinPulse uses the SHAREE dataset from PhysioNet for its exploratory clinical and physiological data experiments.

The available dataset information includes:

- Demographic and clinical information for hypertensive patients
- Ambulatory ECG recordings
- QRS annotation files
- Blood-pressure and other clinical measurements
- Recorded vascular-event labels

### Data Availability and Quality

The initial clinical cohort contains 139 patients, including 17 positive vascular-event labels and 122 patients without a recorded event label. ECG signal files have been available for only a subset of the cohort in the current working dataset.

The preliminary clinical-plus-HRV experiment uses 25 patients with available ECG signals and extracted features. QRS annotations and derived RR intervals may contain errors, so the resulting HRV features require cautious interpretation.

The dataset's outcome encoding and prediction horizon must be interpreted according to the original dataset documentation. The project does not assume that the current experiments establish a validated 12-month individual-risk prediction task.

Raw dataset files are not committed to this repository. Dataset licensing, attribution, and access conditions must be respected.

---

## Prediction Objective

TwinPulse explores machine-learning approaches for identifying cardiovascular and cerebrovascular event labels in the SHAREE dataset.

The initial clinical baseline uses demographic and clinical features. A separate preliminary experiment compares clinical-only features with clinical features augmented by ECG-derived heart rate variability (HRV) features.

The deployed inference interface currently uses clinical features only. The HRV experiment is exploratory and does not establish that physiological features improve prediction.

The exact prediction horizon and target definition must follow the original dataset's outcome documentation. The current experiments should not be interpreted as validated predictions of an individual patient's 12-month cardiovascular risk.

**Important:** TwinPulse is a research and educational proof-of-concept, not a clinically validated diagnostic or risk-assessment system.

---

## Digital Twin Concept

TwinPulse implements a software-based representation of a patient's state. The current Digital Twin engine maintains versioned state updates in memory.

### State Maintained

- Patient identifier
- Clinical state
- Physiological observations
- Latest prediction output
- State version and update timestamp
- History of state updates

### Current State Flow

```text
Clinical Features
       |
       v
Digital Twin State <--- Simulated Physiological Observations
       |
       v
Clinical-Only ML Inference
       |
       v
Exploratory Prediction
       |
       v
Updated Digital Twin State
```

The Digital Twin engine and ML inference interface are separate components. The current application records simulated physiological observations, but those observations are not used by the deployed model to calculate predictions.

**Implementation limitation:** State is stored in memory and is not guaranteed to persist after a backend restart. A validated physiological risk trajectory and real-time ECG-driven updates are not yet implemented.

---

## Machine Learning

TwinPulse uses a research-oriented machine-learning pipeline to investigate cardiovascular and cerebrovascular event classification using the SHAREE dataset.

### Models and Experiments

The implemented baseline uses **Logistic Regression with class weighting**. Preliminary experiments compare:

1. **Clinical-only baseline:** demographic and clinical features.
2. **Clinical + HRV baseline:** clinical features augmented with ECG-derived heart rate variability features.

The clinical-only model uses a larger clinical cohort, while the combined-feature experiment is restricted to patients with available ECG signal files and usable extracted features.

### Preliminary Evaluation

The initial clinical-only experiment on 139 patients showed weak discrimination, with a five-fold stratified out-of-fold ROC-AUC of approximately 0.46.

The separate 25-patient experiment produced ROC-AUC values of approximately 0.41 for clinical-only features and 0.42 for clinical-plus-HRV features. The HRV-augmented experiment did not improve the reported precision, recall, F1-score, or average precision.

These results are preliminary and are not evidence of clinically useful prediction. The small sample, class imbalance, signal-quality concerns, and uncertain outcome semantics limit interpretation.

### Feature Engineering

Potential features include:

- Age and sex
- Body mass index
- Systolic and diastolic blood pressure
- Available clinical measurements
- ECG-derived mean heart rate and RR intervals
- HRV measures such as SDNN, RMSSD, and pNN50

Feature availability and quality depend on the dataset records. The deployed inference interface currently accepts clinical features only; HRV features are not yet integrated into deployed predictions.

### Evaluation Principles

- Report class imbalance and sample size alongside metrics.
- Fit preprocessing within each training fold.
- Avoid claims of clinical validity or generalization from preliminary experiments.
- Treat signal-derived features cautiously because the available QRS annotations have not been fully validated.

---

## Explainability

TwinPulse prioritizes transparent reporting of its machine-learning experiments.

### Current Status

The current baseline uses Logistic Regression, whose fitted coefficients can help describe how input features influence the model's decision function. However, coefficients alone do not establish causation or clinical importance.

### Planned Improvements

- Report model coefficients with feature names and preprocessing details.
- Investigate SHAP or other suitable explainability techniques if justified by the final model and dataset.
- Present feature contributions only after verifying that the explanation method is appropriate.
- Clearly distinguish model explanations from medical conclusions.

**Current limitation:** A validated, patient-specific explainability interface has not yet been established. TwinPulse does not claim that its current dashboard provides clinically validated explanations for cardiovascular events.

---

## System Architecture

TwinPulse consists of a React frontend, FastAPI backend, Digital Twin state engine, and a clinical-feature-based ML inference interface.

### Implemented Architecture

```text
+-----------------------------+
| React + TypeScript Dashboard|
+--------------+--------------+
               |
               | HTTP / REST
               v
+-----------------------------+
| FastAPI Backend             |
| Health / Prediction / Twin  |
| State Update Endpoints      |
+---------+-------------+-----+
          |             |
          v             v
+----------------+  +----------------------+
| Clinical ML    |  | Digital Twin Engine  |
| Inference      |  | Versioned State      |
|                |  | Update History       |
+-------+--------+  +----------+-----------+
        |                      ^
        | Prediction           |
        +----------------------+
                               |
                  Simulated Physiological
                        Observations
```

### Current Data Flow

1. The dashboard sends clinical features to the backend.
2. The inference interface produces an exploratory prediction from clinical features.
3. The Digital Twin records clinical state, simulated physiological observations, prediction state, and update history.
4. The dashboard displays the current state and prediction output.

### Not Yet Integrated

- Sequential replay of real ECG recordings through the application.
- Feeding verified ECG-derived HRV features into deployed predictions.
- Clinically validated risk calibration or patient-specific explanations.
- Persistent storage of Digital Twin state across backend restarts.

The architecture describes a working research proof-of-concept. It does not represent a clinically validated monitoring or prediction system.

---

## Technology Stack

### Machine Learning and Data Processing

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- ECG/HRV feature extraction experiments

### Backend

- FastAPI
- Uvicorn
- Pydantic
- Python-based ML inference interface
- REST API endpoints for health checks, predictions, and Digital Twin state updates

### Frontend

- React
- TypeScript
- Vite
- Lucide icons

### Digital Twin

- Custom Python Digital Twin state engine
- Versioned patient-state updates
- Clinical state, physiological observations, prediction state, and event history
- In-memory state storage for the current proof-of-concept

### Development and Testing

- Git and GitHub
- Visual Studio Code
- Python virtual environment
- Python `unittest` for the API health check

---

## Repository Structure

```text
TwinPulse/
|
|-- backend/
|
|-- data/
|   `-- README.md
|
|-- digital-twin/
|
|-- docs/
|   |-- architecture/
|   |-- presentation/
|   `-- video/
|
|-- frontend/
|
|-- ml/
|   |-- experiments/
|   |-- models/
|   |-- notebooks/
|   |-- src/
|   `-- README.md
|
|-- tests/
|
|-- .env.example
|-- .gitignore
|-- DECISIONS.md
|-- LICENSE
|-- README.md
`-- ROADMAP.md
```

Raw SHAREE dataset files are not committed to the repository. The `docs/presentation/` and `docs/video/` directories are reserved for competition deliverables.

---

## Competition Requirements Mapping

| Competition Requirement | TwinPulse Implementation | Status |
|---|---|---|
| Specific chronic condition | Hypertension | Defined |
| Historical clinical data | SHAREE clinical cohort and clinical-feature experiments | Evaluated experimentally |
| Dynamic physiological data | Simulated physiological observations update the Digital Twin | Implemented as simulation |
| Algorithmic model | Logistic Regression baseline and inference interface | Implemented; preliminary performance is weak |
| Adverse health outcome | SHAREE vascular-event labels | Target semantics require careful interpretation |
| Digital Twin | Versioned patient state and update history | Implemented in memory |
| Doctor-facing interaction | React dashboard connected to FastAPI | Implemented as proof-of-concept |
| Explainability | Logistic Regression coefficients can be investigated | Further work required |
| Public GitHub repository | TwinPulse repository | Available |
| Architecture documentation | `docs/architecture/ARCHITECTURE.md` | Available |
| Competition presentation | `docs/presentation/TwinPulse_Digital_Twin_Challenge_2026_By_Happiest_Health.pptx` | Available |
| Demonstration video | `docs/video/TwinPulse.mp4` | Available |
| Architecture pdf | `docs/architecture/TwinPulse_Architecture_Diagram.pdf` | Available |

The current implementation demonstrates the software workflow, not a clinically validated cardiovascular risk prediction system. Real ECG replay, deployed HRV fusion, external validation, and clinical validation remain incomplete.

---

## Project Status

**Current phase:** Working research proof-of-concept

### Implemented

- FastAPI backend with health and prediction endpoints.
- React + TypeScript dashboard.
- Digital Twin state management with versioned state history.
- Clinical-feature-based ML inference interface.
- Simulated physiological observations, including heart rate and HRV fields.
- Preliminary clinical-only and clinical-plus-HRV baseline experiments.
- Architecture documentation and an automated API health test.

### Current Limitations

- The deployed prediction model uses clinical features only.
- Simulated physiological observations update the Digital Twin state but are not used by the deployed model to calculate predictions.
- Real ECG replay and end-to-end HRV integration remain incomplete.
- Preliminary evaluation results are limited by the small number of patients with available ECG signal files and the dataset's class imbalance.
- The model is not clinically validated, and its output must not be interpreted as an individual's clinical risk estimate.

### Next Priorities

1. Finalize dataset and evaluation documentation.
2. Verify the reproducibility of the ML experiments and API.
3. Complete the competition presentation and demonstration video.
4. Document the implemented functionality and remaining limitations accurately.


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

**Team Name:** TwinPulse

TwinPulse was developed for the **Digital Twin Challenge 2026 by Happiest Health**.

### Team Members and Institutions

1. Almas Banu - Sri Venkateshwara College of Engineering (SVCE), Bengaluru

2. Ansu Kumar - GITAM Deemed to be University, Bengaluru

** Repository:** [AlmasBanu1/TwinPulse](https://github.com/AlmasBanu1/TwinPulse)


---

## Competition Deliverables

- Architecture Diagram: [TwinPulse Architecture PDF](docs/architecture/TwinPulse_Architecture_Diagram.pdf)

- Project Presentation: [TwinPulse Presentation](docs/presentation/TwinPulse_Digital_Twin_Challenge_2026_By_Happiest_Health.pptx)

- Demonstration Video: https://drive.google.com/file/d/19Lr3cA2bog7CS9aQbIdosBuhCoh-k9ho/view?usp=sharing

---

## License

This project is released under the license included in the repository.

Dataset licensing and attribution will be respected separately according to the original dataset provider's terms.