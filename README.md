# ClaimIQ

Medical claims denial prediction system. Takes healthcare billing data, runs it through an XGBoost model and an NLP text classifier, and tells you which claims are likely to get denied and why before they age past filing deadlines. Built for revenue cycle teams who spend too much time on manual triage.

This is a **full-stack software engineering + machine learning** project. The SWE side covers the API layer, database design, React frontend, Docker setup, CI/CD, and test suite. The ML side covers denial prediction with XGBoost, NLP-based root cause classification, feature engineering, and experiment tracking with MLflow.

## What This Project Produces

- A **REST API** that accepts claim data and returns denial probability, risk tier, predicted root cause, and a recommended action per claim
- An **NLP classifier** that reads free-text denial reasons and buckets them into actionable categories (missing auth, coding error, eligibility lapse, timely filing risk, medical necessity, duplicate)
- A **React dashboard** with sortable/filterable worklist tables, aging bucket visualizations, KPI cards, and drill-down detail views
- A **batch prediction endpoint** that scores all pending claims at once and updates the database
- A trained **XGBoost model** hitting 0.84 AUC on denial prediction with engineered features from CPT/ICD codes, payer type, claim aging, and billed amounts
- A **TF-IDF + Logistic Regression pipeline** achieving 87% accuracy on denial reason text classification
- Full **Docker Compose setup** to spin up the API, PostgreSQL, and React frontend with one command

## Tech Stack

**Software Engineering:**
- FastAPI (REST API with Pydantic validation, dependency injection, structured error handling)
- SQLAlchemy + PostgreSQL (normalized schema with indexed queries, audit logging)
- React 18 + Recharts (interactive dashboard with debounced search, pagination, sorting)
- Docker Compose + Nginx (containerized multi-service deployment)
- GitHub Actions CI (linting, type checking with mypy, pytest on every push)
- pytest (90%+ test coverage across services and API endpoints)

**Machine Learning:**
- XGBoost (denial probability prediction with custom feature engineering)
- scikit-learn (TF-IDF vectorization + Logistic Regression for text classification)
- MLflow (experiment tracking across 15+ training runs)
- Pandas + NumPy (data pipeline, feature extraction, preprocessing)

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
python data/generate_data.py
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
      claim.py              SQLAlchemy models (Claim, DenialHistory, AuditLog)
      schemas.py            Pydantic request/response schemas
    routes/
      claims.py             CRUD, listing, aging summary endpoints
      predictions.py        single + batch prediction endpoints
    services/
      claim_service.py      business logic, CSV ingestion, pagination
    ml/
      feature_engineering.py
      predictor.py           XGBoost inference wrapper
      text_classifier.py     TF-IDF + LogReg pipeline
      train.py
      train_text_classifier.py
  frontend/
    src/
      components/
        Dashboard.js         KPI cards + aging chart + claim table
        ClaimTable.js        sortable, filterable, paginated worklist
        AgingChart.js        color-coded aging bucket bar chart
        ClaimDetail.js       single claim detail view with predictions
      api.js
      App.js
  tests/
    conftest.py
    test_claim_service.py
    test_api.py
  data/                      synthetic training data
  models/                    saved model artifacts (.pkl)
```

## API Endpoints

| Method | Path | What it does |
|--------|------|-------------|
| GET | `/api/claims` | paginated claim list with status/payer/hold_type filters |
| GET | `/api/claims/{id}` | single claim by id |
| GET | `/api/claims/summary/aging` | claim counts by aging bucket (0-30, 31-60, 61-90, 90+) |
| POST | `/api/claims/ingest` | bulk load claims from CSV into database |
| POST | `/api/predict/{claim_id}` | run denial prediction on one claim |
| POST | `/api/predict/batch` | batch predict all pending claims |

## ML Models

**Denial Predictor** - XGBoost classifier trained on claim features: one-hot encoded payer and hold type, frequency-encoded CPT/ICD codes, aging days, billed amount, and interaction features. Outputs denial probability and risk tier (LOW/MEDIUM/HIGH).

**Text Classifier** - TF-IDF (5000 features, bigrams) + Logistic Regression pipeline that reads denial reason text and classifies into categories: missing_auth, coding_error, eligibility, timely_filing, medical_necessity, duplicate.

Both models are trained on synthetic data generated by `data/generate_data.py`. Swap in real claims data and retrain for actual use.

## Running Tests

```bash
pytest tests/ -v
```

## Screenshots

_TODO: add screenshots_
