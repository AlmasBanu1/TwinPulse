# TwinPulse

## Dynamic Digital Twin for Cardiovascular Event Risk Prediction in Hypertensive Patients

**TwinPulse** is a research-oriented proof-of-concept developed for the **Digital Twin Challenge 2026 by Happiest Health**. It explores how historical clinical information and simulated physiological observations can be represented in a software-based Digital Twin, alongside an experimental machine-learning workflow for cardiovascular and cerebrovascular event classification.

> **Research disclaimer:** TwinPulse is an educational/research proof-of-concept. It is not clinically validated and must not be used for medical diagnosis, treatment decisions, or individual clinical risk assessment.

---

## 1. Team and Institution Details

**Team name:** TwinPulse

**Team members**

- **Almas Banu** — Sri Venkateshwara College of Engineering (SVCE), Bengaluru
- **Ansu Kumar** — GITAM Deemed to be University, Bengaluru

**Project repository:** [AlmasBanu1/TwinPulse](https://github.com/AlmasBanu1/TwinPulse)

**Challenge:** Digital Twin Challenge 2026 by Happiest Health

---

## 2. Project Title

**Dynamic Digital Twin for Cardiovascular Event Risk Prediction in Hypertensive Patients**

---

## 3. Problem Statement and Healthcare Use Case

Hypertension is an important risk factor for cardiovascular and cerebrovascular disease. Conventional risk assessment may rely on clinical measurements and historical patient information, while physiological measurements can change over time.

TwinPulse explores a software-based approach that combines a patient's clinical state with a changing stream of physiological observations. The intended research use case is a doctor-facing interface that presents a patient's recorded state and an exploratory machine-learning output in one place.

The project investigates whether clinical features, and potentially ECG-derived heart-rate-variability (HRV) features, can support classification experiments using the SHAREE dataset. The current results are preliminary and do not establish clinically useful prediction.

### Project objectives

- Represent selected patient information in a software-based Digital Twin.
- Accept clinical features for exploratory ML inference.
- Record simulated physiological observations, including heart-rate and HRV fields, in the Digital Twin state.
- Display the Digital Twin state and exploratory prediction through a dashboard.
- Evaluate a clinical-only baseline and a separate preliminary clinical-plus-HRV experiment.
- Document limitations and results transparently.

### Current implementation boundary

The application uses **simulated physiological observations** to update the Digital Twin state. These observations are **not** currently fed into the deployed prediction model. Real ECG replay and end-to-end HRV integration remain future work.

---

## 4. Proposed Solution and System Workflow

TwinPulse consists of a frontend dashboard, backend API, Digital Twin state engine, and machine-learning inference interface.

```text
Clinical Patient Features
          |
          v
   React + TypeScript Dashboard
          |
          | HTTP / REST
          v
      FastAPI Backend
          |
          +----------------------+
          |                      |
          v                      v
 Clinical ML Inference     Digital Twin Engine
          |                - Clinical state
          v                - Simulated physiological
 Exploratory Prediction      observations
                             - State version/history
          ^                      ^
          |                      |
          +----------------------+
```

### Workflow

1. The dashboard sends clinical features to the backend.
2. The inference interface produces an exploratory prediction using clinical features.
3. The Digital Twin records clinical state, simulated physiological observations, prediction state, and update history.
4. The dashboard displays the current state and prediction output.

**Important:** This workflow demonstrates software integration, not a clinically validated monitoring or risk-prediction system. Digital Twin state is currently stored in memory and may not persist after a backend restart.

---

## 5. Dataset

### SHAREE — Smart Health for Assessing the Risk of Events via ECG

TwinPulse uses the **SHAREE dataset from PhysioNet** for exploratory clinical and physiological data experiments.

Available dataset information includes:

- Demographic and clinical information for hypertensive patients
- Ambulatory ECG recordings
- QRS annotation files
- Blood-pressure and other clinical measurements
- Recorded vascular-event labels

### Data availability and quality

- The initial clinical cohort contains **139 patients**.
- There are **17 positive vascular-event labels** and **122 patients without a recorded event label** in the current cohort.
- ECG signal files are available for only a subset of the cohort in the current working dataset.
- The preliminary clinical-plus-HRV experiment uses **25 patients** with available ECG signals and extracted features.
- QRS annotations and derived RR intervals may contain errors, so HRV features require cautious interpretation.

The dataset's outcome encoding and prediction horizon must be interpreted according to the original dataset documentation. The current experiments do not establish a validated 12-month individual-risk prediction task.

Raw dataset files are not committed to this repository. Dataset licensing, attribution, and access conditions must be respected.

---

## 6. AI/ML Models and Frameworks

### Implemented model

The current baseline uses **Logistic Regression with class weighting** for an exploratory classification task based on clinical features.

The experiments compare:

1. **Clinical-only baseline:** demographic and clinical features.
2. **Clinical-plus-HRV baseline:** clinical features augmented with ECG-derived heart-rate-variability features.

The clinical-only experiment uses a larger cohort, while the combined-feature experiment is restricted to patients with available ECG signals and usable extracted features.

### Preliminary evaluation

- The clinical-only experiment on 139 patients produced a five-fold stratified out-of-fold **ROC-AUC of approximately 0.46**.
- In a separate 25-patient experiment, ROC-AUC was approximately **0.41** for clinical-only features and **0.42** for clinical-plus-HRV features.
- The HRV-augmented experiment did not improve the reported precision, recall, F1-score, or average precision.

These results are weak and preliminary. Small sample size, class imbalance, signal-quality concerns, and uncertain outcome semantics limit interpretation. They are **not evidence of clinically useful prediction**.

### Feature engineering explored

Depending on record availability and data quality, candidate features include:

- Age and sex
- Body mass index
- Systolic and diastolic blood pressure
- Other available clinical measurements
- ECG-derived mean heart rate and RR intervals
- HRV measures such as SDNN, RMSSD, and pNN50

The deployed inference interface currently uses clinical features only; HRV features are not integrated into deployed predictions.

### Explainability

Logistic Regression coefficients may help describe how input features influence the model's decision function. Coefficients alone do not establish causation or clinical importance. SHAP or other explanation methods may be investigated if appropriate for the final model and dataset. A validated, patient-specific explainability interface has not yet been established.

---

## 7. Technical Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite, Lucide icons |
| Backend API | FastAPI, Uvicorn, Pydantic |
| Machine learning | Python, scikit-learn, Logistic Regression, Joblib |
| Data processing | Pandas, NumPy |
| Physiological signal experiments | ECG/QRS annotation inspection, RR interval and HRV feature experiments |
| Digital Twin | Custom Python state engine with versioned state updates and update history |
| Testing | Python `unittest` for the API health check |
| Development tools | Git, GitHub, Visual Studio Code, Python virtual environment |

---

## 8. Architecture Diagram

The architecture documentation is included in the repository:

- **Architecture diagram (PDF):** [`docs/architecture/TwinPulse_Architecture_Diagram.pdf`](docs/architecture/TwinPulse_Architecture_Diagram.pdf)
- **Architecture notes:** [`docs/architecture/ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md)

The architecture describes the React dashboard, FastAPI backend, clinical-feature-based inference interface, and Digital Twin state engine. It also identifies the current boundary between simulated physiological observations and ML inference.

---

## 9. Presentation and Demonstration Video

- **Project presentation (PowerPoint):** [`docs/presentation/TwinPulse_Digital_Twin_Challenge_2026_By_Happiest_Health.pptx`](docs/presentation/TwinPulse_Digital_Twin_Challenge_2026_By_Happiest_Health.pptx)
- **Demonstration video (Google Drive):** [Watch the TwinPulse demonstration video](https://drive.google.com/file/d/19Lr3cA2bog7CS9aQbIdosBuhCoh-k9ho/view?usp=sharing)
- **Video file in repository, if preferred:** [`docs/video/TwinPulse.mp4`](docs/video/TwinPulse.mp4)

The demonstration video is intended to explain the problem, project architecture, implementation, and prototype workflow. The submission video should be at least **20 minutes** long, as required by the challenge guidelines.

---

## 10. Repository Structure

```text
TwinPulse/
├── backend/
├── data/
│   └── README.md
├── digital-twin/
├── docs/
│   ├── architecture/
│   ├── presentation/
│   └── video/
├── frontend/
├── ml/
│   ├── experiments/
│   ├── models/
│   ├── notebooks/
│   ├── src/
│   └── README.md
├── tests/
├── .env.example
├── .gitignore
├── DECISIONS.md
├── LICENSE
├── README.md
└── ROADMAP.md
```

Raw SHAREE dataset files are not committed to the repository.

---

## 11. Project Status and Limitations

### Implemented

- FastAPI backend with health and prediction endpoints
- React + TypeScript dashboard
- Digital Twin state management with versioned state history
- Clinical-feature-based ML inference interface
- Simulated physiological observations, including heart-rate and HRV fields
- Preliminary clinical-only and clinical-plus-HRV baseline experiments
- Architecture documentation and an automated API health test

### Current limitations

- The deployed prediction model uses clinical features only.
- Simulated physiological observations update the Digital Twin state but are not used by the deployed model to calculate predictions.
- Real ECG replay and end-to-end HRV integration remain incomplete.
- Preliminary evaluation is limited by class imbalance and the small number of patients with available ECG signal files.
- The model is not clinically validated, and its output must not be interpreted as an individual's clinical risk estimate.
- Persistent storage of Digital Twin state across backend restarts is not implemented.

TwinPulse does not claim clinical validation, medical diagnosis, treatment recommendations, guaranteed event prediction, real-time clinical monitoring, population-wide generalization, or replacement of medical professionals.

---

## 12. Open-Source License

TwinPulse is released under the **MIT License**. See the [`LICENSE`](LICENSE) file for the complete license text.

Dataset licensing, attribution, and access requirements are separate from the software license and must be respected according to the original dataset provider's terms.

---

## 13. Competition Submission Checklist

| Submission requirement | Included in repository |
|---|---|
| Team details and institution information | Listed in this README |
| Project title | Listed in this README |
| Problem statement and healthcare use case | Listed in this README |
| Technical stack and AI/ML model details | Listed in this README |
| Minimum 20-minute demonstration video | Linked above; confirm the final video duration meets the requirement |
| Open-source license | MIT License in `LICENSE` |
| Architecture diagram in PDF/PPT format | PDF linked above |
| Project presentation in PDF/PPT format | PowerPoint linked above |
| Public GitHub repository | [AlmasBanu1/TwinPulse](https://github.com/AlmasBanu1/TwinPulse) |

---

*TwinPulse is a research and educational proof-of-concept. All experimental results and implementation limitations are reported transparently; the system is not intended for clinical use.*
