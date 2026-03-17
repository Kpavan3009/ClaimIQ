import pandas as pd
import numpy as np


def extract_features(df):
    features = pd.DataFrame()

    features["aging_days"] = df["aging_days"].astype(float)
    features["billed_amount"] = df["billed_amount"].astype(float)

    features["aging_x_amount"] = features["aging_days"] * features["billed_amount"]
    features["is_high_value"] = (features["billed_amount"] > 5000).astype(int)

    payer_dummies = pd.get_dummies(df["payer_name"], prefix="payer")
    features = pd.concat([features, payer_dummies], axis=1)

    hold_dummies = pd.get_dummies(df["hold_type"], prefix="hold")
    features = pd.concat([features, hold_dummies], axis=1)

    cpt_freq = df["cpt_code"].value_counts(normalize=True).to_dict()
    features["cpt_freq"] = df["cpt_code"].map(cpt_freq).astype(float)

    icd_freq = df["icd_code"].value_counts(normalize=True).to_dict()
    features["icd_freq"] = df["icd_code"].map(icd_freq).astype(float)

    feature_names = list(features.columns)

    return features.values.astype(np.float32), feature_names
