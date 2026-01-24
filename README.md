# Fraud Detection + Decisioning (IEEE-CIS)

End-to-end, industry-style fraud risk modeling pipeline: **train → evaluate → decision policy (decline/review/step-up/approve) → monitoring (drift + PSI)**.

## Problem
Fraud is rare (~3–4%). The goal is not only predicting fraud, but **ranking transactions by risk** and turning scores into **operational actions** under capacity constraints.

## Data
- Dataset: IEEE-CIS Fraud Detection (Kaggle)
- Merge: `train_transaction` + `train_identity` on `TransactionID` (left join)
- Split: **time-based 60/20/20** using `TransactionDT` to avoid leakage and reflect production drift

## Baseline model (numeric-only)
Why baseline first: ship a strong, simple model before adding complex encoding.

- Model: `HistGradientBoostingClassifier`
- Features: **400 numeric columns**
- Missing values: **median imputation** (fit on train, applied to valid/test)
- Primary metric: **PR-AUC (Average Precision)** (better for rare fraud than ROC-AUC)

### Performance (Validation → Test)
- Base fraud rate: **3.90% (valid)**, **3.44% (test)**
- PR-AUC: **0.572 (valid)** → **0.462 (test)** (expected drift on future slice)

## Decisioning (the real fraud system)
We convert risk scores into **actions** with a capacity-locked, rank-based policy:

- **Decline**: top **100**
- **Manual review**: ranks **101–1000**
- **Step-up verification** (OTP/3DS): ranks **1001–10000**
- **Approve**: remaining

### Policy quality (Valid → Test)
**Top-100 (Decline)**
- Precision@100: **1.00 (valid)**, **1.00 (test)**
- Recall@100: **0.0108 (valid)**, **0.0246 (test)**

**Top-1000 (Review queue)**
- Precision@1000: **0.915 (valid)**, **0.900 (test)**
- Recall@1000: **0.198 (valid)**, **0.221 (test)**

**Top-10000 (Step-up)**
- Precision@10000: **0.317 (valid)**, **0.243 (test)**
- Recall@10000: **0.688 (valid)**, **0.598 (test)**

> Note: A fixed-threshold policy can cause queue-volume drift under distribution shift. This project reports a **capacity-locked (rank-based)** policy to match operational constraints.

## Monitoring (temporal drift)
We emulate production monitoring using time bins (TransactionDT quantiles):

- **Score drift:** mean predicted risk varies across time
- **Fraud-rate drift:** fraud prevalence is non-stationary over time
- **PSI (score distribution):** max PSI = **0.067** (< 0.10) → **small distribution drift**

Artifacts:
- `reports/figures/score_drift_test.png`
- `reports/figures/fraud_rate_drift_test.png`
- `reports/figures/psi_score_drift_test.png`
- `reports/psi_by_timebin_test.csv`

## Repository structure
```text
fraud-detection-decisioning/
  notebooks/
  src/
  reports/
