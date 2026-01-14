## Repository structure
```text
fraud-detection-decisioning/
  README.md
  requirements.txt
  .gitignore
  data/                # not tracked (instructions in README)
  notebooks/
    01_eda.ipynb
  src/
    fraud/
      data.py          # load + split + validation
      features.py      # feature pipeline
      train.py         # training entrypoint
      evaluate.py      # metrics + plots
      calibrate.py     # probability calibration
      policy.py        # approve/review/decline thresholds + cost
      explain.py       # SHAP + error analysis
      monitoring.py    # drift checks (PSI, score shifts)
  reports/
    figures/
    model_card.md
    thresholds.json
    sample_decisions.csv
  tests/
    test_split_no_leakage.py
    test_metrics.py
