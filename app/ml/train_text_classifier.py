import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from app.ml.text_classifier import build_pipeline


TRAINING_DATA = [
    ("prior authorization not obtained before service", "authorization"),
    ("preauthorization was not obtained for this procedure", "authorization"),
    ("referral authorization expired before service date", "authorization"),
    ("service requires preauthorization which was not obtained", "authorization"),
    ("missing prior auth for inpatient admission", "authorization"),
    ("authorization number invalid or expired", "authorization"),
    ("no valid referral on file for date of service", "authorization"),
    ("auth required but not submitted with claim", "authorization"),

    ("diagnosis code does not support medical necessity", "medical_necessity"),
    ("insufficient documentation to support billed level of service", "medical_necessity"),
    ("procedure not covered under current benefit plan", "medical_necessity"),
    ("attach clinical notes supporting medical necessity", "medical_necessity"),
    ("medical records do not support the level of service billed", "medical_necessity"),
    ("service not medically necessary based on diagnosis", "medical_necessity"),
    ("clinical documentation does not justify procedure", "medical_necessity"),
    ("medical necessity not established for this service", "medical_necessity"),

    ("patient eligibility terminated on date of service", "eligibility"),
    ("patient not covered under plan on date of service", "eligibility"),
    ("coordination of benefits information missing", "eligibility"),
    ("subscriber id not found in system", "eligibility"),
    ("patient coverage lapsed before service date", "eligibility"),
    ("member not eligible on date of service", "eligibility"),
    ("insurance terminated prior to service", "eligibility"),
    ("coverage not active for date of service rendered", "eligibility"),

    ("claim submitted beyond timely filing deadline", "timely_filing"),
    ("claim received after filing limit expiration", "timely_filing"),
    ("late submission past 90 day filing window", "timely_filing"),
    ("timely filing limit exceeded for this claim", "timely_filing"),
    ("claim not filed within allowed time period", "timely_filing"),
    ("past deadline for claim submission", "timely_filing"),
    ("filing window closed for this date of service", "timely_filing"),
    ("exceeded timely filing limit of 120 days", "timely_filing"),

    ("invalid cpt code for reported place of service", "coding"),
    ("coding combination not allowed per payer guidelines", "coding"),
    ("missing modifier required for procedure code", "coding"),
    ("incorrect place of service code for procedure billed", "coding"),
    ("cpt code does not match diagnosis reported", "coding"),
    ("invalid modifier for this procedure code", "coding"),
    ("unbundling detected for procedure codes billed", "coding"),
    ("procedure code requires additional modifier", "coding"),
    ("diagnosis and procedure code mismatch", "coding"),
    ("invalid revenue code for outpatient service", "coding"),

    ("duplicate claim already processed for same date of service", "duplicate"),
    ("claim appears to be duplicate of previously paid claim", "duplicate"),
    ("service already adjudicated under different claim number", "duplicate"),
    ("duplicate submission detected for same provider and date", "duplicate"),
    ("this service was already paid on a prior claim", "duplicate"),
    ("possible duplicate claim for same patient same date", "duplicate"),

    ("billed amount exceeds allowed amount for this procedure", "billing"),
    ("provider not in network for this plan", "billing"),
    ("charges exceed fee schedule maximum", "billing"),
    ("balance billing not permitted for this service", "billing"),
    ("billed units exceed maximum allowed", "billing"),
    ("payment already made to another provider for this service", "billing"),
]


def main():
    texts = [t for t, _ in TRAINING_DATA]
    labels = [l for _, l in TRAINING_DATA]

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, stratify=labels, random_state=42
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))

    os.makedirs("models", exist_ok=True)
    joblib.dump(pipeline, "models/text_classifier.pkl")
    print("text classifier saved to models/text_classifier.pkl")


if __name__ == "__main__":
    main()
