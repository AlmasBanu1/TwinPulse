# TwinPulse — Project Decisions

This document records major technical, architectural, dataset, and scope decisions made during the development of TwinPulse.

The purpose is to preserve the reasoning behind important decisions and prevent accidental architectural drift.

---

## Decision 001 — Project Name

**Date:** 5 October 2026  
**Decision:** Use `TwinPulse` as the project name.

### Reason

The name communicates the project's Digital Twin focus and its emphasis on physiological/cardiovascular state monitoring.

---

## Decision 002 — Project Focus

**Date:** 5 October 2026  
**Decision:** Focus TwinPulse on cardiovascular/cerebrovascular event risk in hypertensive patients.

### Reason

The competition requires a Digital Twin proof-of-concept for a specific chronic or lifestyle condition.

Hypertension provides a clear chronic-condition context, while cardiovascular/cerebrovascular events provide a concrete adverse outcome for prediction.

---

## Decision 003 — Primary Dataset

**Date:** 5 October 2026  
**Decision:** Use SHAREE (Smart Health for Assessing the Risk of Events via ECG) from PhysioNet as the primary dataset.

### Reason

SHAREE provides:

- Hypertensive patient data
- Clinical/demographic information
- Ambulatory ECG recordings
- Physiological time-series information
- Recorded cardiovascular/cerebrovascular outcomes

This provides a defensible connection between patient characteristics, physiological signals, and the selected prediction target.

The dataset will be inspected before the exact preprocessing and feature-engineering pipeline is finalized.

---

## Decision 004 — Use of Recorded Physiological Data as Dynamic Stream

**Date:** 5 October 2026  
**Decision:** Use recorded SHAREE physiological time-series data as a replayed/simulated dynamic stream for the Digital Twin prototype.

### Reason

The competition requires dynamic/real-time data.

SHAREE provides recorded physiological time-series data rather than a live wearable device feed.

Therefore, the prototype will replay recorded physiological observations sequentially to demonstrate how the Digital Twin can update over time.

### Important Constraint

TwinPulse must not claim that SHAREE provides live wearable monitoring or real-time clinical monitoring.

The implementation will clearly describe this as:

> **Replayed/simulated physiological streaming using recorded open-access data.**

---

## Decision 005 — Digital Twin vs ML Model

**Date:** 5 October 2026  
**Decision:** Treat the Digital Twin and ML model as separate system components.

### Digital Twin

The Digital Twin represents the modeled state of the patient and maintains:

- Historical information
- Current physiological state
- Derived features/state
- Latest risk state
- Risk trajectory

### ML Model

The ML model consumes engineered patient/state features and produces:

- Risk probability
- Risk category
- Model-derived contributing factors

### Reason

This separation makes the architecture clearer and avoids incorrectly treating the prediction model itself as the Digital Twin.

---

## Decision 006 — Primary Prediction Horizon

**Date:** 5 October 2026  
**Decision:** Target recorded cardiovascular/cerebrovascular events during a 12-month follow-up period.

### Reason

The selected dataset contains follow-up outcome information that supports a future-event prediction problem.

### Constraint

The exact binary target construction must be confirmed after inspecting the SHAREE metadata.

---

## Decision 007 — Patient-Level Data Splitting

**Date:** 5 October 2026  
**Decision:** All train/test and validation separation must occur at the patient level.

### Reason

Physiological recordings may produce multiple observations, windows, or derived features for the same patient.

Randomly splitting such observations could place data from the same patient in both training and evaluation sets, resulting in data leakage and overly optimistic performance.

Therefore:

> A patient must belong entirely to one evaluation partition.

---

## Decision 008 — ML Model Progression

**Date:** 5 October 2026  
**Decision:** Begin with simple interpretable models and increase complexity only when justified.

### Planned Progression

```text
Logistic Regression
        ↓
Random Forest
        ↓
XGBoost if justified
```

### Reason

The dataset is relatively small and contains a limited number of recorded events.

A simpler model may be more appropriate, interpretable, and defensible than an unnecessarily complex model.

---

## Decision 009 — Deep Learning

**Date:** 5 October 2026  
**Decision:** Deep learning is optional, not mandatory.

### Reason

LSTM/GRU or other deep-learning approaches may introduce unnecessary complexity and overfitting risk for a relatively small patient-level dataset.

Deep learning will only be considered if:

- The available data supports it
- There is a clear technical reason
- It provides meaningful improvement
- It can be evaluated fairly
- It does not weaken project reliability

---

## Decision 010 — Evaluation Metrics

**Date:** 5 October 2026  
**Decision:** Do not rely on accuracy alone.

### Primary Metrics

- Recall
- Precision
- F1-score
- ROC-AUC
- PR-AUC
- Confusion matrix

### Reason

The dataset contains a limited number of positive events, making class imbalance and false-negative behavior particularly important.

---

## Decision 011 — Explainability

**Date:** 5 October 2026  
**Decision:** Include model explainability in the final system.

### Planned Approach

Depending on the final model:

- Feature importance
- Model-specific explanations
- SHAP where appropriate

### Reason

The competition requires a doctor-facing Digital Twin concept, and model-derived contributing factors make the prediction more understandable.

The explanations will be presented as model-derived factors and not as medical diagnoses.

---

## Decision 012 — Raw Dataset Handling

**Date:** 5 October 2026  
**Decision:** Do not commit raw SHAREE data to GitHub.

### Reason

The competition permits anonymized/open-source/synthetic data, but storing large research datasets directly in the repository is unnecessary and makes the repository difficult to manage.

The repository will instead contain:

- Dataset source information
- Acquisition instructions
- Expected directory structure
- Preprocessing instructions
- Code required to reproduce the pipeline

---

## Decision 013 — Synthetic Data Usage

**Date:** 5 October 2026  
**Decision:** Synthetic data may be used for software development, testing, and demonstration where necessary, but it must remain clearly separated from real SHAREE training/evaluation data.

### Reason

The software team may need data before the ML pipeline is complete.

Synthetic/mock data can allow backend, frontend, and Digital Twin components to be developed in parallel.

### Constraint

Synthetic data must never be presented as real patient data or as evidence of model performance.

---

## Decision 014 — No Fabricated Results

**Date:** 5 October 2026  
**Decision:** All ML performance metrics and experimental results must come from actual experiments.

### Reason

The project must remain technically and academically defensible.

No accuracy, precision, recall, F1, ROC-AUC, PR-AUC, or other metric may be invented or estimated for presentation purposes.

---

## Decision 015 — Medical Claims

**Date:** 5 October 2026  
**Decision:** TwinPulse will be presented as a research/educational proof-of-concept.

### The project will NOT claim:

- Clinical diagnosis
- Clinically validated risk prediction
- Real-time clinical monitoring
- Guaranteed cardiovascular event prediction
- Treatment recommendations
- Generalization to the entire population

### The project MAY claim:

- Research-oriented risk stratification
- Digital Twin state representation
- HRV-based physiological modeling
- Machine-learning-based risk estimation
- Explainable model outputs
- Prototype doctor-facing decision-support visualization

---

## Decision 016 — GitHub Repository Strategy

**Date:** 5 October 2026  
**Decision:** Use one public GitHub repository for the complete TwinPulse project.

### Reason

The competition requires a public GitHub submission, and a single repository makes the complete system easier to evaluate.

The repository will contain:

- ML pipeline
- Backend
- Frontend
- Digital Twin engine
- Documentation
- Architecture
- Tests
- Setup instructions

Raw datasets and secrets will remain excluded.

---

## Decision 017 — Branching Strategy

**Date:** 5 October 2026  
**Decision:** Use `main` as the stable branch and feature branches for development.

### Example Branches

```text
feature/ml-pipeline
feature/hrv-features
feature/model-evaluation
feature/ml-integration

feature/backend
feature/frontend
feature/digital-twin
```

### Reason

The project has two major workstreams being developed in parallel.

Feature branches reduce the risk of unfinished work breaking `main`.

---

## Decision 018 — ROADMAP as Source of Truth

**Date:** 5 October 2026  
**Decision:** `ROADMAP.md` is the single source of truth for project scope and progress.

### Rule

Major changes to:

- project scope
- prediction target
- architecture
- dataset
- major features
- development phases

must be reflected in `ROADMAP.md`.

---

## Decision 019 — Architecture Changes

**Date:** 5 October 2026  
**Decision:** Major architectural changes require explicit team agreement.

### Rule

Neither workstream should silently change the agreed architecture.

If a better approach is discovered:

1. Identify the problem.
2. Explain the proposed change.
3. Evaluate the impact.
4. Agree on the change.
5. Update `ROADMAP.md`.
6. Record the decision here.
7. Implement it.

---

## Decision 020 — Current Project State

**Date:** 5 October 2026  
**Decision:** The current agreed project direction is:

```text
Project:
TwinPulse

Condition:
Hypertension

Primary Risk Domain:
Cardiovascular / Cerebrovascular

Primary Dataset:
SHAREE

Physiological Source:
Ambulatory ECG → QRS/RR → HRV

Dynamic Stream:
Recorded physiological data replay

Prediction Horizon:
12-month recorded event outcome

Digital Twin:
Patient state representation

ML:
Risk prediction + explainability

Dashboard:
Doctor-facing Digital Twin interface
```

This decision supersedes earlier alternative project directions discussed during planning.

---

# Decision Change Log

| Decision | Status |
|---|---|
| Project name: TwinPulse | Active |
| Hypertension focus | Active |
| Cardiovascular/cerebrovascular risk | Active |
| SHAREE primary dataset | Active |
| Replayed physiological stream | Active |
| Digital Twin + ML separation | Active |
| Patient-level splitting | Mandatory |
| Logistic Regression baseline | Active |
| Random Forest | Active |
| XGBoost | Conditional |
| Deep Learning | Optional |
| Explainability | Active |
| Raw dataset excluded from GitHub | Mandatory |
| Synthetic data separation | Mandatory |
| No fabricated results | Mandatory |
| `main` as stable branch | Active |
| `ROADMAP.md` as source of truth | Mandatory |

---

## How to Add Future Decisions

When a major technical decision is made, add a new entry using:

```text
## Decision XXX — <Decision Title>

Date: <Date>
Decision: <What was decided>

Reason:
<Why it was decided>

Constraints / Consequences:
<Important implications>
```

Do not rewrite historical decisions simply because the implementation later changes.

If a decision is intentionally reversed, document the new decision and explain why the previous decision was changed.