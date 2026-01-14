
# 1) clone the repo (copy the URL from GitHub)
git clone https://github.com/<your-username>/fraud-detection-decisioning.git
cd fraud-detection-decisioning

# 2) create folders
mkdir -p data notebooks src/fraud reports/figures tests .github/workflows

# 3) create empty files
touch README.md requirements.txt .gitignore
touch notebooks/01_eda.ipynb
touch src/fraud/__init__.py src/fraud/data.py src/fraud/features.py src/fraud/train.py \
      src/fraud/evaluate.py src/fraud/calibrate.py src/fraud/policy.py src/fraud/explain.py \
      src/fraud/monitoring.py
touch reports/model_card.md reports/thresholds.json reports/sample_decisions.csv
touch tests/test_split_no_leakage.py tests/test_metrics.py

# 4) commit + push
git add .
git commit -m "chore: scaffold project structure"
git push
