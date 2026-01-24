# Model Card — IEEE-CIS Fraud Detection (Baseline + Decisioning)

## Intended use
Rank transactions by fraud risk to support operational actions under capacity constraints:
**decline / review / step-up / approve**.

## Data
- Source: IEEE-CIS Fraud Detection (Kaggle)
- Join: transaction + identity on `TransactionID`
- Split: chronological **60/20/20** using `TransactionDT` (prevents leakage, matches production)

## Model (baseline)
- Algorithm: `HistGradientBoostingClassifier`
- Features: numeric-only baseline (**400 numeric columns**)
- Missing values: median imputation (fit on train only)
- Output: risk score used for ranking and decisioning

## Metrics
Base rates:
- Valid: 0.0390
- Test: 0.0344

PR-AUC (Average Precision):
- Valid: 0.572
- Test: 0.462

## Decision policy (capacity-locked, rank-based)
Actions:
- Decline: top 100
- Review: ranks 101–1000
- Step-up: ranks 1001–10000
- Approve: remaining

Policy performance:
- Valid: Precision@100=1.00, Precision@1000=0.915, Precision@10000=0.317
- Test:  Precision@100=1.00, Precision@1000=0.900, Precision@10000=0.243

## Monitoring
Temporal bins (TransactionDT quantiles) on test slice:
- Score drift + fraud-rate drift plots
- PSI drift of score distribution vs earliest bin
- Max PSI: 0.067 (small distribution drift)

## Limitations
- Numeric-only baseline: categoricals not yet encoded
- Scores are ranking-first; calibration not yet applied
- Offline evaluation; production needs delayed-label monitoring and feedback loop

## Next improvements
- Categorical encoding (one-hot / frequency; leakage-safe)
- Calibration + cost-based threshold optimization (expected profit / cost curve)
- Feature drift PSI + retrain triggers
