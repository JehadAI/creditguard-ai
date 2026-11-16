# 🛡️ CreditGuard AI — Credit Card Fraud Detection

A Streamlit app that scores credit card transactions with a machine-learning model trained in Google Colab.

**Pages:** Dashboard · Single Transaction · Batch Prediction · Model Information

## Project structure
```
creditguard-ai/
├── app.py                 # entry point + navigation
├── detector.py            # inference: same preprocessing as training (no Streamlit code)
├── core.py, ui.py         # cached loaders, session state, FinTech styling
├── views/                 # the four pages
├── artifacts/             # saved from Colab
│   ├── fraud_model.joblib, scaler.joblib, threshold.joblib
│   ├── preprocessing_config.joblib / .json
│   ├── model_report.json  # metrics, confusion matrix, features, dataset info, library versions
│   └── sample_data/       # sample_normal.csv, sample_fraud.csv, sample_batch.csv
├── tests/                 # pytest (pipeline + UI smoke tests)
├── .streamlit/config.toml # dark FinTech theme
└── requirements.txt
```

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Use your own Colab output
Run the notebook, download `fraud_artifacts.zip`, and replace the contents of `artifacts/` with it.
**Then update `requirements.txt` with the library versions printed by the last cells of the notebook**
(also stored in `artifacts/model_report.json → versions`). A pickled scikit-learn / XGBoost model is only
guaranteed to load with the versions it was trained with; the app shows a sidebar warning if they differ.

## Test
```bash
pytest -q
```
Covers: a normal transaction, a fraudulent transaction, a batch CSV (results must equal the saved confusion matrix),
feature order / scaler consistency, and that every page renders.

## Deploy on Streamlit Community Cloud
1. Push this folder to a GitHub repository (include `artifacts/`; the model is < 1 MB).
2. Go to share.streamlit.io → **Create app** → pick the repo, branch and `app.py`.
3. Deploy — you get a public URL.

## Batch CSV format
Columns `Time, V1 … V28, Amount` (any order; extra columns such as an ID are kept). An optional `Class` column (0/1)
enables a comparison of predictions against the truth.

> Demo project: the model expects the dataset's anonymised PCA features and was trained on 2013 European data.
> It must not be the only basis for real blocking decisions.
