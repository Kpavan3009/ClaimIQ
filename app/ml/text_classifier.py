import joblib
from pathlib import Path


class DenialReasonClassifier:
    def __init__(self, model_dir: str = "models"):
        model_path = Path(model_dir) / "text_classifier.pkl"
        self.pipeline = joblib.load(model_path)
        self.categories = self.pipeline.classes_

    def classify(self, text: str) -> dict:
        if not text or not text.strip():
            return {"category": "unknown", "confidence": 0.0}

        category = self.pipeline.predict([text])[0]
        probas = self.pipeline.predict_proba([text])[0]
        confidence = float(max(probas))

        return {"category": category, "confidence": round(confidence, 4)}

    def classify_batch(self, texts: list[str]) -> list[dict]:
        return [self.classify(t) for t in texts]


def build_pipeline():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline

    return Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words="english",
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            random_state=42,
        )),
    ])
