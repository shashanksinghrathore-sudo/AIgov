# Model Risk Management Procedure (Credit Models)

Owner: Head of Credit Risk. Effective 1 June 2025.

## Risk assessment
Each credit model has an entry in the model risk register with likelihood and severity ratings, mitigation actions and a control owner. Residual risk is accepted by the Chief Risk Officer before release.

## Validation
Independent validation is performed before release. The validation report records AUC, precision and recall against the acceptance criteria (AUC of at least 0.78 on the hold-out test set). Robustness is checked with a stress test on recession-period data.

## Change management
Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan. Models are tracked with version control.

## Monitoring
A model monitoring dashboard tracks population drift monthly. An alert is raised when the stability index crosses the threshold, and the model owner decides whether to retrain.
