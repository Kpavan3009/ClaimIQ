import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
import xgboost as xgb
import mlflow
import mlflow.xgboost

from app.ml.feature_engineering import extract_features


def main():
    df = pd.read_csv("data/claims.csv")

    X, feature_names = extract_features(df)
    y = (df["status"] == "denied").astype(int).values

    pos_count = y.sum()
    neg_count = len(y) - pos_count
    scale_pos_weight = neg_count / pos_count if pos_count > 0 else 1.0

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    params = {
        "max_depth": 6,
        "n_estimators": 200,
        "learning_rate": 0.1,
        "scale_pos_weight": scale_pos_weight,
        "eval_metric": "logloss",
        "random_state": 42,
        "use_label_encoder": False,
    }

    mlflow.set_experiment("denial_prediction")

    with mlflow.start_run():
        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)

        y_pred_proba = model.predict_proba(X_test)[:, 1]
        y_pred = model.predict(X_test)

        auc = roc_auc_score(y_test, y_pred_proba)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        print(f"AUC: {auc:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1: {f1:.4f}")

        mlflow.log_params(params)
        mlflow.log_metric("auc", auc)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1", f1)
        mlflow.xgboost.log_model(model, "model")

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/denial_model.pkl")
    joblib.dump(feature_names, "models/feature_names.pkl")
    print("model saved to models/denial_model.pkl")


if __name__ == "__main__":
    main()
