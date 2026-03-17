import joblib
import pandas as pd
from pathlib import Path

from app.ml.feature_engineering import extract_features


class DenialPredictor:
    def __init__(self, model_dir: str = "models"):
        model_path = Path(model_dir) / "denial_model.pkl"
        self.model = joblib.load(model_path)
        self.model_dir = model_dir

    def predict(self, claim_data: dict) -> dict:
        df = pd.DataFrame([claim_data])
        X, _ = extract_features(df, fit_mode=False, encoders_path=self.model_dir)

        proba = float(self.model.predict_proba(X)[:, 1][0])
        risk_tier = self._get_risk_tier(proba)
        root_cause = self._get_root_cause(claim_data)
        action = self._get_action(risk_tier, root_cause)

        return {
            "denial_probability": round(proba, 4),
            "risk_tier": risk_tier,
            "predicted_root_cause": root_cause,
            "recommended_action": action,
        }

    def predict_batch(self, claims: list[dict]) -> list[dict]:
        return [self.predict(c) for c in claims]

    def _get_risk_tier(self, proba: float) -> str:
        if proba >= 0.75:
            return "critical"
        if proba >= 0.5:
            return "high"
        if proba >= 0.25:
            return "medium"
        return "low"

    def _get_root_cause(self, claim: dict) -> str:
        hold = claim.get("hold_type", "")
        mapping = {
            "MISSING_AUTH": "authorization",
            "CODING_ERROR": "coding",
            "ELIGIBILITY": "eligibility",
            "TIMELY_FILING": "timely_filing",
            "MEDICAL_NECESSITY": "medical_necessity",
            "DUPLICATE_CLAIM": "duplicate",
            "INVALID_CPT": "coding",
            "MISSING_MODIFIER": "coding",
        }
        return mapping.get(hold, "other")

    def _get_action(self, risk_tier: str, root_cause: str) -> str:
        actions = {
            "authorization": "obtain prior auth or submit appeal with auth documentation",
            "coding": "review cpt/icd pairing and resubmit with correct codes",
            "eligibility": "verify patient eligibility and update coverage info",
            "timely_filing": "submit appeal with proof of timely submission",
            "medical_necessity": "attach clinical notes supporting medical necessity",
            "duplicate": "check for prior adjudication and void if duplicate",
        }
        base = actions.get(root_cause, "review claim details and resubmit")
        if risk_tier == "critical":
            return f"urgent: {base}"
        return base
