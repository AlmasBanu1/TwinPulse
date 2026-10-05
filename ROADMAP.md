# TwinPulse — Project Roadmap

> **Dynamic Digital Twin for Cardiovascular Event Risk Prediction in Hypertensive Patients**

---

## 1. Project Overview

TwinPulse is a research-oriented proof-of-concept Digital Twin platform designed to represent and update the modeled physiological risk state of a hypertensive patient by combining:

- Historical and clinical patient information
- Physiological time-series data
- Heart-rate variability (HRV) features derived from ECG
- Machine-learning-based cardiovascular risk prediction
- Explainable model outputs
- A doctor-facing Digital Twin dashboard

The project is being developed for the **Digital Twin Challenge 2026 by Happiest Health**.

### Primary Use Case

TwinPulse focuses on:

> **Cardiovascular/cerebrovascular event risk in hypertensive patients**

### Primary Prediction Horizon

> **12-month recorded cardiovascular/cerebrovascular event risk**

TwinPulse is a **research and educational proof-of-concept** and is not intended to diagnose disease, replace clinicians, or provide medical treatment recommendations.

---

# 2. Competition Requirements Mapping

TwinPulse must satisfy the core Digital Twin Challenge requirements.

| Competition Requirement | TwinPulse Approach |
|---|---|
| Specific chronic/lifestyle condition | Hypertension |
| Static/historical patient information | SHAREE clinical/demographic information |
| Dynamic/real-time physiological stream | Replayed physiological time-series derived from SHAREE ECG data |
| Algorithmic model | ML-based cardiovascular/cerebrovascular risk prediction |
| Specific adverse outcome | 12-month recorded cardiovascular/cerebrovascular event |
| Digital Twin | Continuously updated software representation of patient state |
| Doctor interaction | Doctor-facing dashboard |
| Open/synthetic/anonymized data | SHAREE open-access research dataset |
| Public GitHub repository | TwinPulse public repository |
| Architecture documentation | Architecture diagram + documentation |
| Presentation | Competition presentation |
| Video | Minimum 20-minute project video |

### Dynamic Stream Interpretation

SHAREE contains recorded ambulatory physiological data rather than a live consumer wearable feed.

Therefore, TwinPulse will use the recorded physiological time-series as a **replayed/simulated dynamic stream** during the prototype demonstration.

This means:

```text
Recorded physiological data
            ↓
      Stream replay
            ↓
   Sequential observations
            ↓
     Digital Twin updates
            ↓
      Risk state updates
```

The project must **not** claim that SHAREE provides live wearable or real-time clinical monitoring.

---

# 3. Primary Dataset

## SHAREE

**SHAREE — Smart Health for Assessing the Risk of Events via ECG**

Source:

- PhysioNet
- Open-access research dataset
- Hypertensive patients
- Long-term ambulatory ECG recordings
- Clinical/demographic information
- Recorded cardiovascular/cerebrovascular outcomes

The dataset will be inspected before finalizing:

- exact data schema
- preprocessing pipeline
- available clinical variables
- ECG/QRS processing method
- HRV feature set
- target-label construction
- final ML pipeline

### Important Dataset Rule

Raw SHAREE data must **not** be committed to the GitHub repository.

The repository may contain:

- preprocessing code
- feature-engineering code
- metadata/schema documentation
- experiment configurations
- reproducible instructions
- small non-sensitive test fixtures where appropriate

Local raw and generated datasets must remain excluded through `.gitignore`.

---

# 4. Prediction Target

The initial prediction objective is:

> **Predict whether a patient experienced a recorded major cardiovascular/cerebrovascular event during the 12-month follow-up period.**

Initial conceptual target:

```text
0 = No recorded major cardiovascular/cerebrovascular event
1 = Recorded major cardiovascular/cerebrovascular event
```

The exact target construction and event categories will be confirmed after inspecting the SHAREE metadata and outcome information.

### Important

The project will not claim to predict every possible cardiovascular event in the general population.

The model will be scoped to the population and outcome information supported by the selected dataset.

---

# 5. Digital Twin Concept

The Digital Twin is the **software representation of the modeled patient state**.

It combines historical information with dynamically updated physiological information.

Conceptually:

```text
Historical / Clinical Patient Data
                +
     Replayed Physiological Stream
                ↓
        Feature Extraction
                ↓
        Current Patient State
                ↓
          Digital Twin State
                ↓
        ML Risk Prediction
                ↓
      Updated Risk Probability
                ↓
       Doctor-Facing Dashboard
```

### Important Distinction

The Digital Twin and the ML model are separate concepts.

**Digital Twin:**
- Represents patient state
- Maintains historical and current information
- Updates as new physiological observations arrive
- Provides the state consumed by downstream prediction components

**ML Model:**
- Consumes engineered patient features/state
- Produces cardiovascular/cerebrovascular risk estimates
- Provides model-derived contributing factors

---

# 6. Development Phases

## Phase 0 — Repository & Project Foundation

### Status

- [x] Create GitHub repository
- [x] Create local project
- [x] Initialize Git
- [x] Connect local repository to GitHub
- [x] Create initial project structure
- [x] Create `.gitignore`
- [ ] Complete `README.md`
- [x] Complete `ROADMAP.md`
- [ ] Complete `DECISIONS.md`
- [ ] Add `LICENSE`
- [ ] Add dataset documentation
- [ ] Add `.gitkeep` files where required
- [ ] Make initial repository commit

### Milestone

A clean, public, version-controlled repository containing the agreed project foundation.

---

# Phase 1 — SHAREE Dataset Inspection

## Objective

Understand the real dataset before implementing the ML pipeline.

### Tasks

- [ ] Obtain SHAREE dataset
- [ ] Inspect directory structure
- [ ] Inspect `info.txt`
- [ ] Identify patient IDs
- [ ] Identify record IDs
- [ ] Inspect `.hea` files
- [ ] Inspect ECG recordings
- [ ] Inspect QRS annotation files
- [ ] Understand ECG-to-QRS mapping
- [ ] Understand event/outcome labels
- [ ] Map clinical information to patients
- [ ] Identify missing values
- [ ] Identify available demographic variables
- [ ] Identify available clinical variables
- [ ] Verify ECG sampling information
- [ ] Verify recording duration
- [ ] Understand annotation format
- [ ] Document the dataset schema
- [ ] Document preprocessing requirements
- [ ] Document any limitations discovered during inspection

### Milestone

Successfully trace at least one patient through:

```text
Clinical Metadata
      ↓
Patient / Record ID
      ↓
ECG / QRS Information
      ↓
Physiological Information
      ↓
Recorded Outcome
```

No ML training begins before this inspection is sufficiently complete.

---

# Phase 2 — Data Preprocessing

## Objective

Create a reproducible and patient-aware preprocessing pipeline.

### Tasks

- [ ] Implement dataset loading
- [ ] Validate ECG records
- [ ] Process QRS/R-peak information
- [ ] Generate RR intervals where appropriate
- [ ] Handle invalid RR intervals
- [ ] Handle missing or unusable recordings
- [ ] Validate physiological ranges
- [ ] Preserve patient identifiers
- [ ] Create patient-level processing pipeline
- [ ] Generate processed intermediate data locally
- [ ] Document preprocessing decisions
- [ ] Verify preprocessing reproducibility

### Data Leakage Rule

All preprocessing, splitting, feature engineering, and validation decisions must preserve patient-level separation.

No patient may appear in both training and evaluation sets through different recordings, windows, or derived observations.

---

# Phase 3 — Physiological & HRV Feature Engineering

## Objective

Convert ECG/QRS-derived physiological information into meaningful features suitable for patient-level modeling.

The following are **candidate features**, not guaranteed final features.

## Time-Domain HRV

Potential features:

- [ ] Mean heart rate
- [ ] Mean RR interval
- [ ] SDNN
- [ ] RMSSD
- [ ] pNN50

## Frequency-Domain HRV

Potential features:

- [ ] LF
- [ ] HF
- [ ] LF/HF

## Nonlinear HRV

Potential features:

- [ ] Sample entropy
- [ ] Other nonlinear features only if technically justified and feasible

## Clinical / Historical Features

Potential features:

- [ ] Age
- [ ] Sex
- [ ] Systolic blood pressure
- [ ] Diastolic blood pressure
- [ ] Other relevant clinical variables available in SHAREE

### Feature Selection Rule

The final feature set will be determined only after:

1. Dataset inspection
2. Data-quality analysis
3. Physiological validity checks
4. Computational feasibility
5. Model performance evaluation
6. Leakage assessment

### Milestone

Create a clean, reproducible **patient-level feature table**.

Example conceptual schema:

```text
patient_id
age
sex
systolic_bp
diastolic_bp
mean_hr
mean_rr
sdnn
rmssd
pnn50
lf
hf
lf_hf
sample_entropy
event_12m
```

The actual schema will be finalized after dataset inspection.

---

# Phase 4 — Exploratory Data Analysis

## Objective

Understand the dataset before model selection and training.

### Tasks

- [ ] Analyze class distribution
- [ ] Inspect feature distributions
- [ ] Identify missing values
- [ ] Identify outliers
- [ ] Analyze event vs non-event groups
- [ ] Analyze feature correlations
- [ ] Examine physiological patterns
- [ ] Identify potential data-quality issues
- [ ] Document important observations

### Dataset Limitation

The selected dataset is relatively small and contains a limited number of recorded events.

Therefore:

- Accuracy alone must not be used as the primary evaluation measure.
- Complex models must be justified.
- Patient-level validation is mandatory.
- Model results must be presented as proof-of-concept findings.
- Performance uncertainty and limitations must be documented.

---

# Phase 5 — ML Baseline & Model Development

## Objective

Build a reliable baseline before considering more complex models.

### Model 1 — Logistic Regression

- [ ] Prepare training data
- [ ] Apply required preprocessing/scaling
- [ ] Train baseline model
- [ ] Evaluate model
- [ ] Record experiment
- [ ] Document configuration

### Model 2 — Random Forest

- [ ] Train model
- [ ] Evaluate model
- [ ] Compare with Logistic Regression
- [ ] Tune only where justified
- [ ] Record experiment

### Model 3 — XGBoost

XGBoost will be considered only if justified by:

- Dataset characteristics
- Baseline results
- Computational feasibility
- Expected benefit
- Interpretability requirements

Tasks if selected:

- [ ] Train model
- [ ] Evaluate model
- [ ] Compare against previous models
- [ ] Record experiment

### Deep Learning

LSTM, GRU, or other deep-learning models are **not mandatory**.

They will only be considered if there is a strong technical justification and sufficient data support.

The project prioritizes:

> **Reliable, explainable, reproducible results over unnecessary model complexity.**

---

# Phase 6 — Model Evaluation

## Required Metrics

- [ ] Recall
- [ ] Precision
- [ ] F1-score
- [ ] ROC-AUC
- [ ] PR-AUC
- [ ] Confusion matrix

## Validation

- [ ] Use patient-level train/test separation
- [ ] Use appropriate cross-validation where feasible
- [ ] Prevent leakage from multiple observations of the same patient
- [ ] Document random seeds
- [ ] Document preprocessing configuration
- [ ] Record model configurations
- [ ] Record final experiment results
- [ ] Compare candidate models fairly

### Important Rule

No performance number may be:

- fabricated
- estimated without experimentation
- copied without attribution
- selectively reported to exaggerate performance

All final performance claims must come from actual experiments performed for TwinPulse.

---

# Phase 7 — Model Explainability

## Objective

Provide understandable model-derived factors contributing to the risk prediction.

### Tasks

- [ ] Identify important features
- [ ] Implement feature importance
- [ ] Consider SHAP if appropriate
- [ ] Generate patient-level explanations where feasible
- [ ] Convert model outputs into understandable risk factors
- [ ] Validate explanation pipeline

### Example

```text
Risk Level: HIGH

Model-derived contributing factors:
- Reduced HRV
- Elevated systolic blood pressure
- Altered LF/HF ratio
```

These are **model-derived associations/features**, not medical diagnoses or treatment recommendations.

The final explanations must be based on actual model results.

---

# Phase 8 — ML Inference Pipeline

## Objective

Convert the research ML workflow into a reusable inference component.

### Conceptual Pipeline

```text
Patient Data
     ↓
Input Validation
     ↓
Feature Processing
     ↓
HRV / Physiological Features
     ↓
Trained ML Model
     ↓
Risk Probability
     ↓
Risk Category
     ↓
Model Explanation
```

### Tasks

- [ ] Create inference module
- [ ] Load trained model
- [ ] Load preprocessing components
- [ ] Validate input features
- [ ] Generate risk probability
- [ ] Generate risk category
- [ ] Generate model-derived contributing factors
- [ ] Define stable ML output schema
- [ ] Test inference pipeline

### Example Output Contract

The final schema will be confirmed during integration.

Conceptually:

```json
{
  "patient_id": "TP-1042",
  "risk_probability": 0.78,
  "risk_level": "HIGH",
  "prediction_horizon_months": 12,
  "top_factors": [
    "Reduced HRV",
    "Elevated systolic blood pressure"
  ]
}
```

The values above are illustrative only and must **not** be presented as actual model results.

---

# Phase 9 — Dynamic Stream Replay

## Objective

Demonstrate how physiological observations can update the Digital Twin over time.

### Concept

```text
Recorded SHAREE Physiological Data
              ↓
        Stream Replay
              ↓
     Sequential Observations
              ↓
      Feature / State Update
              ↓
       Digital Twin Update
              ↓
       ML Risk Inference
              ↓
        Updated Risk State
```

### Tasks

- [ ] Define replay format
- [ ] Define replay timing
- [ ] Define observation/state schema
- [ ] Process sequential physiological observations
- [ ] Update Digital Twin state
- [ ] Trigger inference at appropriate intervals
- [ ] Record risk trajectory
- [ ] Test replay with representative data

### Important

This is a **prototype simulation/replay of recorded physiological data**.

It must not be described as live clinical monitoring.

---

# Phase 10 — Digital Twin Integration

## Objective

Connect the ML inference component with the Digital Twin engine developed by the software workstream.

### Digital Twin Responsibilities

The Digital Twin engine should maintain relevant patient state such as:

- Patient identity
- Historical clinical information
- Current physiological state
- Derived HRV state
- Latest model risk state
- Risk trajectory
- Timestamped updates

### Tasks

- [ ] Define ML → Digital Twin interface
- [ ] Define patient state schema
- [ ] Define state update mechanism
- [ ] Connect replayed physiological stream
- [ ] Update patient state
- [ ] Trigger ML inference
- [ ] Store/update risk state
- [ ] Return updated state to backend
- [ ] Test integration

---

# Phase 11 — Doctor Dashboard Integration

## Objective

Provide a conceptual doctor-facing interface for interacting with the virtual patient.

### Potential Dashboard Information

- [ ] Patient profile
- [ ] Digital Twin current state
- [ ] Risk probability
- [ ] Risk level
- [ ] Risk trajectory
- [ ] Physiological trends
- [ ] Important model-derived factors
- [ ] Historical timeline
- [ ] Prediction horizon
- [ ] Model explanation
- [ ] Stream replay controls where useful

The final dashboard will be implemented primarily by the software workstream.

---

# Phase 12 — Testing & Validation

## ML Testing

- [ ] Unit-test feature calculations
- [ ] Validate preprocessing
- [ ] Validate inference
- [ ] Test missing inputs
- [ ] Test invalid inputs
- [ ] Test edge cases
- [ ] Confirm reproducibility

## Integration Testing

- [ ] Test ML/backend communication
- [ ] Test Digital Twin state updates
- [ ] Test physiological stream replay
- [ ] Test dashboard data
- [ ] Test end-to-end patient workflow

## Security & Data Handling

- [ ] Verify no raw medical data is committed
- [ ] Verify no secrets are committed
- [ ] Verify `.env` handling
- [ ] Verify API input validation
- [ ] Verify appropriate anonymization/data handling

---

# Phase 13 — Documentation

## Required Documentation

- [ ] README
- [ ] Problem statement
- [ ] Dataset documentation
- [ ] Data-processing methodology
- [ ] HRV feature methodology
- [ ] ML methodology
- [ ] Model evaluation
- [ ] Explainability methodology
- [ ] Digital Twin architecture
- [ ] Dynamic stream replay methodology
- [ ] API documentation
- [ ] Setup instructions
- [ ] Architecture diagram
- [ ] Limitations
- [ ] Ethical considerations
- [ ] License information

---

# Phase 14 — Competition Submission

## Required Deliverables

- [ ] Public GitHub repository
- [ ] Team details
- [ ] College information
- [ ] Project title
- [ ] Problem statement/use case
- [ ] Technical stack
- [ ] AI/ML model and framework details
- [ ] Working prototype
- [ ] Architecture diagram PDF/PPT
- [ ] Presentation PDF/PPT
- [ ] Minimum 20-minute video
- [ ] Open-source license
- [ ] Final testing
- [ ] GitHub audit
- [ ] Submission form

### Competition Deadline

> **20 October 2026 — 7:00 PM IST**

---

# 15. Internal Target Schedule

These are **internal target dates**, not hard technical deadlines.

| Date | Target |
|---|---|
| Oct 5 | Repository foundation |
| Oct 6–7 | SHAREE dataset inspection |
| Oct 7–9 | Preprocessing + ECG/QRS + HRV pipeline |
| Oct 9–11 | Feature engineering + EDA |
| Oct 11–13 | ML experiments |
| Oct 13–14 | Evaluation + explainability |
| Oct 14–15 | ML integration |
| Oct 15 | Feature-complete target |
| Oct 16–17 | Integration + testing |
| Oct 18 | Documentation + presentation |
| Oct 19 | Video + GitHub audit + submission preparation |
| Oct 20 | Final buffer + submission |

If a technical blocker changes the schedule, the team may adjust these dates without changing project scope unless the roadmap is explicitly updated.

---

# 16. Workstream Ownership

## ML / Data Workstream — User

Primary responsibility:

- [ ] Dataset inspection
- [ ] Dataset preprocessing
- [ ] ECG/QRS processing
- [ ] RR interval generation
- [ ] HRV feature engineering
- [ ] Exploratory data analysis
- [ ] ML experiments
- [ ] Model evaluation
- [ ] Explainability
- [ ] ML inference pipeline
- [ ] ML documentation

## Software / Product Workstream — Teammate

Primary responsibility:

- [ ] Backend/API
- [ ] Database
- [ ] Digital Twin state engine
- [ ] Dynamic stream replay infrastructure
- [ ] Frontend/dashboard
- [ ] ML integration
- [ ] End-to-end application flow
- [ ] Deployment
- [ ] Software testing
- [ ] Product documentation

## Shared Responsibilities

- [ ] System architecture
- [ ] API/interface decisions
- [ ] Integration
- [ ] End-to-end testing
- [ ] GitHub management
- [ ] Presentation
- [ ] Competition video
- [ ] Final submission
- [ ] Technical defense/interview preparation

---

# 17. Git & Collaboration Rules

## Main Branch

`main` must remain stable.

No unfinished development should be pushed directly to `main`.

## Feature Branches

Examples:

```text
feature/ml-pipeline
feature/hrv-features
feature/model-evaluation
feature/ml-integration

feature/backend
feature/frontend
feature/digital-twin
```

## Development Workflow

```text
Create / switch to feature branch
            ↓
Implement one logical task
            ↓
Test
            ↓
Commit
            ↓
Push
            ↓
Pull Request
            ↓
Review
            ↓
Merge into main
```

### Commit Rules

Use meaningful commit messages.

Examples:

```text
chore: initialize TwinPulse repository
docs: add SHAREE dataset documentation
feat: implement RR interval extraction
feat: add HRV feature pipeline
feat: add baseline logistic regression
feat: integrate ML inference API
fix: handle invalid RR intervals
```

---

# 18. Non-Negotiable Project Rules

1. **No fabricated data or ML results.**
2. **No raw SHAREE data in GitHub.**
3. **No patient-level data leakage.**
4. **Train/test separation must happen at the patient level.**
5. **Accuracy alone is not sufficient.**
6. **No exaggerated clinical claims.**
7. **TwinPulse is a research/educational proof-of-concept.**
8. **TwinPulse is not a clinical diagnostic tool.**
9. **The system must not provide treatment recommendations.**
10. **Synthetic data may be used for software testing or demonstration only when clearly labeled.**
11. **Real dataset results and synthetic demonstration data must not be mixed without explicit labeling.**
12. **No unnecessary deep-learning complexity.**
13. **Every major architectural decision must be documented in `DECISIONS.md`.**
14. **`ROADMAP.md` is the single source of truth for project scope and progress.**
15. **No major feature is added or removed without explicitly updating the roadmap.**
16. **`main` must remain stable.**
17. **Feature branches should be used for development.**
18. **Every meaningful change must have a meaningful commit message.**
19. **Working functionality takes priority over unnecessary features.**
20. **Competition requirements take priority over optional enhancements.**
21. **Medical interpretation must remain appropriately cautious.**
22. **All reported results must be reproducible from the project code and documented configuration where feasible.**

---

# 19. Project Limitations to Acknowledge

The final project documentation must explicitly acknowledge relevant limitations, including where applicable:

- Small dataset size
- Limited number of recorded events
- Dataset population characteristics
- Potential class imbalance
- Retrospective research data
- Recorded physiological data rather than live wearable data
- Limited generalizability
- Proof-of-concept rather than clinical validation
- Potential uncertainty in model estimates

These limitations must not be hidden in the final presentation.

---

# 20. Definition of Done

TwinPulse will be considered competition-ready when:

- [ ] SHAREE data pipeline works
- [ ] Patient-level feature generation is reproducible
- [ ] ML model produces real predictions
- [ ] Evaluation is documented honestly
- [ ] Explainability works
- [ ] ML inference pipeline works
- [ ] Physiological stream replay works
- [ ] Digital Twin state can be updated
- [ ] ML and Digital Twin communicate correctly
- [ ] Backend and ML communicate correctly
- [ ] Doctor-facing dashboard displays the Digital Twin
- [ ] End-to-end patient workflow works
- [ ] Documentation is complete
- [ ] Architecture diagram is complete
- [ ] Presentation is complete
- [ ] 20+ minute video is complete
- [ ] Public GitHub repository is clean
- [ ] No secrets are committed
- [ ] No raw medical data is committed
- [ ] Competition submission requirements are satisfied

---

# 21. Current Immediate Next Step

The next development task is:

> **Inspect the actual SHAREE dataset before implementing the ML pipeline.**

The immediate goal is to understand:

```text
SHAREE
  ↓
Directory Structure
  ↓
info.txt
  ↓
Patient IDs
  ↓
Record IDs
  ↓
ECG / QRS Data
  ↓
Clinical Information
  ↓
Recorded Outcomes
```

No model training will begin until the dataset structure and outcome mapping are sufficiently understood.

---

## Roadmap Status

**Current Phase:** Phase 0 — Repository & Project Foundation

**Next Phase:** Phase 1 — SHAREE Dataset Inspection

**Project:** TwinPulse

**Competition:** Digital Twin Challenge 2026 — Happiest Health

**Competition Deadline:** 20 October 2026, 7:00 PM IST