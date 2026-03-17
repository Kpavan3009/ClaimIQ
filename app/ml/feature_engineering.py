import pandas as pd
import numpy as np
import joblib
from pathlib import Path


PAYER_CATEGORIES = [
    "Blue Cross", "Aetna", "UnitedHealth", "Cigna",
    "Humana", "Medicare", "Medicaid",
]

HOLD_CATEGORIES = [
    "MISSING_AUTH", "CODING_ERROR", "ELIGIBILITY",
    "TIMELY_FILING", "MEDICAL_NECESSITY", "DUPLICATE_CLAIM",
    "INVALID_CPT", "MISSING_MODIFIER",
]


def extract_features(df, fit_mode=False, encoders_path=None):
    features = pd.DataFrame()

    features["aging_days"] = df["aging_days"].astype(float)
    features["billed_amount"] = df["billed_amount"].astype(float)

    features["aging_x_amount"] = features["aging_days"] * features["billed_amount"]
    features["is_high_value"] = (features["billed_amount"] > 5000).astype(int)

    for payer in PAYER_CATEGORIES:
        col = f"payer_{payer}"
        features[col] = (df["payer_name"] == payer).astype(int)

    for hold in HOLD_CATEGORIES:
        col = f"hold_{hold}"
        features[col] = (df["hold_type"] == hold).astype(int)

    if fit_mode:
        cpt_freq = df["cpt_code"].value_counts(normalize=True).to_dict()
        icd_freq = df["icd_code"].value_counts(normalize=True).to_dict()

        if encoders_path:
            enc_dir = Path(encoders_path)
            enc_dir.mkdir(parents=True, exist_ok=True)
            joblib.dump(cpt_freq, enc_dir / "cpt_freq.pkl")
            joblib.dump(icd_freq, enc_dir / "icd_freq.pkl")
    else:
        enc_dir = Path(encoders_path or "models")
        cpt_path = enc_dir / "cpt_freq.pkl"
        icd_path = enc_dir / "icd_freq.pkl"

        if cpt_path.exists() and icd_path.exists():
            cpt_freq = joblib.load(cpt_path)
            icd_freq = joblib.load(icd_path)
        else:
            cpt_freq = df["cpt_code"].value_counts(normalize=True).to_dict()
            icd_freq = df["icd_code"].value_counts(normalize=True).to_dict()

    default_cpt = np.mean(list(cpt_freq.values())) if cpt_freq else 0.0
    default_icd = np.mean(list(icd_freq.values())) if icd_freq else 0.0

    features["cpt_freq"] = df["cpt_code"].map(cpt_freq).fillna(default_cpt).astype(float)
    features["icd_freq"] = df["icd_code"].map(icd_freq).fillna(default_icd).astype(float)

    feature_names = list(features.columns)

    return features.values.astype(np.float32), feature_names
