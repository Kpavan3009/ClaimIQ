# ClaimIQ

Medical claims denial prediction system. Takes claim data, runs it through an XGBoost model and an NLP text classifier, and tells you which claims are likely to get denied and why. Built for revenue cycle teams who are tired of guessing.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **ML:** XGBoost (denial probability), scikit-learn (denial reason classification via TF-IDF + LogisticRegression)
- **Frontend:** React 18, Recharts, React Router
- **Infra:** Docker Compose, Nginx, GitHub Actions CI
- **Tracking:** MLflow for experiment logging

## Quick Start

```bash
git clone https://github.com/Kpavan3009/ClaimIQ.git
cd ClaimIQ
docker compose up --build
```

API runs on `http://localhost:8000`, frontend on `http://localhost:3000`.

To run locally without Docker:

```bash
pip install -r requirements.txt
python -m app.ml.train
python -m app.ml.train_text_classifier
uvicorn app.main:app --reload
```

## Project Structure

```
ClaimIQ/
  app/
    config.py
    database.py
    main.py
    models/
      claim.py          # SQLAlchemy models (Claim, DenialHistory, AuditLog)
      schemas.py        # Pydantic request/response schemas
    routes/
      claims.py         # CRUD + listing + aging summary
      predictions.py    # single + batch prediction endpoints
    services/
      claim_service.py  # business logic, CSV ingestion
    ml/
      feature_engineering.py
      predictor.py      # XGBoost inference wrapper
      text_classifier.py
      train.py
      train_text_classifier.py
  frontend/
    src/
      components/
        Dashboard.js
        ClaimTable.js
        AgingChart.js
        ClaimDetail.js
      api.js
      App.js
  tests/
    conftest.py
    test_claim_service.py
    test_api.py
  data/                 # synthetic training data
  models/               # saved model artifacts
  migrations/           # alembic migrations
```

## API Endpoints

| Method | Path | What it does |
|--------|------|-------------|
| GET | `/api/claims` | paginated claim list, supports status/payer/hold_type filters |
| GET | `/api/claims/{id}` | single claim by id |
| GET | `/api/claims/summary/aging` | aging bucket counts (0-30, 31-60, 61-90, 90+) |
| POST | `/api/claims/ingest` | load claims from CSV |
| POST | `/api/predict/{claim_id}` | run denial prediction on one claim |
| POST | `/api/predict/batch` | batch predict multiple claims |

## ML Models

**Denial Predictor** - XGBoost classifier trained on claim features (payer, hold type, CPT/ICD frequency encoding, aging days, billed amount). Outputs denial probability and risk tier (low/medium/high/critical).

**Text Classifier** - TF-IDF + Logistic Regression pipeline that reads denial reason text and classifies into categories: authorization, medical_necessity, eligibility, timely_filing, coding, duplicate, billing.

Both models are trained on synthetic data. Swap in real claims data and retrain for production use.

## Running Tests

```bash
pytest tests/ -v
```

## Screenshots

_TODO: add screenshots_
