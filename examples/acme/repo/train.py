"""Train the CreditScore model."""
import logging

import mlflow
import shap
import xgboost as xgb

logger = logging.getLogger("creditscore")


def train(X, y):
    with mlflow.start_run():
        model = xgb.XGBClassifier(n_estimators=400, max_depth=4)
        model.fit(X, y)
        mlflow.xgboost.log_model(model, "model")
        logger.info("model trained")
    return model


def explain(model, X):
    return shap.TreeExplainer(model).shap_values(X)
