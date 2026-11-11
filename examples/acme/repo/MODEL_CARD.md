# Model card: CreditScore v4

**Intended use:** decision support for consumer loan applications in the EU and US. Not intended for business lending.

**Model:** gradient-boosted trees (XGBoost), 62 features.

**Performance:** AUC 0.81 on the 2025 hold-out test set. Evaluation results are logged in MLflow.

**Limitations:** performance degrades for applicants with fewer than six months of credit history. Fairness across protected groups has not been measured.

**Explanations:** SHAP values provide the main factors behind each score for the applicant-facing reason codes.
