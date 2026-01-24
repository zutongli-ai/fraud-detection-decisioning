# Fraud Detection + Decisioning (IEEE-CIS)

End-to-end, industry-style fraud risk pipeline: **train → evaluate → decision policy (decline / review / step-up / approve) → monitoring (drift + PSI)**.

This project focuses on what real fraud systems do: **rank transactions by risk** and convert scores into **operational actions under capacity constraints**.

---

## Problem

Fraud is rare (~3–4%). Accuracy is misleading.

We care about:
- **PR-AUC (Average Precision):** quality under class imbalance
- **Precision@K / Recall@K:** quality of the *top alerts* given limited review capacity
- **Operational decisions:** how many we block/review/step-up, and what fraud we catch

---

## Data

- Dataset: **IEEE-CIS Fraud Detection** (Kaggle)
- Join: `train_transaction` + `train_identity` on `TransactionID` (left join)
- Split: **time-based 60/20/20** using `TransactionDT` (prevents leakage + reflects production drift)

> ⚠️ Raw Kaggle files are NOT committed to GitHub. Put them under `data/raw/ieee/` locally.

---

## Baseline model (numeric-only)

Why baseline first: ship a strong simple model before complex encoding.

- Model: `HistGradientBoostingClassifier`
- Features: **400 numeric columns**
- Missing values: **median imputation** (fit on train, applied to valid/test)
- Primary metric: **PR-AUC (Average Precision)**

---

## Results (Validation → Test)

**Base rate**
- Validation: **3.90%**
- Test: **3.44%**

**PR-AUC**
- Validation PR-AUC: **0.572**
- Test PR-AUC: **0.462**

**Precision@K / Recall@K** (ranking performance)
- **K=1000** (review-like capacity):
  - Valid: precision **0.915**, recall **0.198**
  - Test:  precision **0.900**, recall **0.221**
- **K=10000** (review + step-up total capacity):
  - Valid: precision **0.317**, recall **0.688**
  - Test:  precision **0.243**, recall **0.598**

Interpretation:
- Precision@K measures: “If we only look at the top K risky transactions, what fraction are fraud?”
- Even at K=10,000, precision is ~**8× lift** vs base rate (0.317 / 0.039 ≈ 8.1) on validation.

---

## Decisioning policy (capacity-locked)

Instead of using a fixed probability threshold (which causes alert volume to drift),
we use **rank-based thresholds** so the queue size stays stable.

Example policy:
- Top **K_decline** → **decline**
- Next **K_review** → **review**
- Next **K_step_up** → **step-up**
- Rest → **approve**

Artifacts:
- `reports/sample_decisions_test.csv`
- `reports/sample_decisions_test_rank_policy.csv`
- `reports/metrics_summary.json`

---

## Monitoring (drift + PSI)

We generate simple monitoring artifacts you’d expect in production:

1) **Score drift over time bins** (mean score per time slice)
2) **Fraud rate drift over time bins** (label drift)
3) **PSI over time bins** (distribution shift vs first bin)

Figures (in repo):
- `reports/figures/score_drift_test.png`
- `reports/figures/fraud_rate_over_time_test.png`
- `reports/figures/psi_score_drift_test.png`
- `reports/figures/pr_curve_valid.png`

---

## Key plots

### PR Curve (Validation)
![PR Curve](reports/figures/pr_curve_valid.png)

### Score drift over time (Test)
![Score Drift](reports/figures/score_drift_test.png)

### Fraud rate over time (Test)
![Fraud Rate Drift](reports/figures/fraud_rate_over_time_test.png)

### PSI over time (Test)
![PSI Drift](reports/figures/psi_score_drift_test.png)

---

## Repo structure

```text
fraud-detection-decisioning/
  README.md
  .gitignore
  data/                 # NOT tracked (put Kaggle files locally)
  notebooks/
    01_eda.ipynb
  src/
    fraud/
      prepare_ieee.py    # merge + parquet export
  reports/
    figures/
    metrics_summary.json
    psi_by_timebin_test.csv
    sample_decisions_test.csv
    sample_decisions_test_rank_policy.csv
    model_card.md
