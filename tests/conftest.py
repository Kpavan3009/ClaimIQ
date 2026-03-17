import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app

engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_claim_data():
    return {
        "claim_number": "CLM-TEST001",
        "patient_id": "PAT-10001",
        "cpt_code": "99213",
        "icd_code": "E11.9",
        "payer_id": "PYR-001",
        "payer_name": "Blue Cross",
        "billed_amount": 2500.00,
        "claim_date": datetime(2024, 6, 1),
        "aging_days": 45,
        "hold_type": "CODING_ERROR",
        "status": "pending",
    }
