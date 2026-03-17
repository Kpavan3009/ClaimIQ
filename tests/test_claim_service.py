from app.models.claim import Claim
from app.services.claim_service import ClaimService


def _insert_claim(db, **overrides):
    defaults = {
        "claim_number": "CLM-SVC001",
        "patient_id": "PAT-10001",
        "cpt_code": "99213",
        "icd_code": "E11.9",
        "payer_id": "PYR-001",
        "payer_name": "Blue Cross",
        "billed_amount": 2500.00,
        "aging_days": 45,
        "hold_type": "CODING_ERROR",
        "status": "pending",
    }
    defaults.update(overrides)
    claim = Claim(**defaults)
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim


def test_get_claims_pagination(db_session):
    for i in range(5):
        _insert_claim(db_session, claim_number=f"CLM-PAGE{i:03d}")
    service = ClaimService(db_session)
    result = service.get_claims(page=1, page_size=2)
    assert len(result["claims"]) == 2
    assert result["total"] == 5
    assert result["page"] == 1


def test_get_claims_second_page(db_session):
    for i in range(5):
        _insert_claim(db_session, claim_number=f"CLM-P2-{i:03d}")
    service = ClaimService(db_session)
    result = service.get_claims(page=3, page_size=2)
    assert len(result["claims"]) == 1


def test_get_claim_by_id(db_session):
    claim = _insert_claim(db_session)
    service = ClaimService(db_session)
    found = service.get_claim_by_id(claim.id)
    assert found is not None
    assert found.claim_number == "CLM-SVC001"


def test_get_claim_by_id_not_found(db_session):
    service = ClaimService(db_session)
    assert service.get_claim_by_id(99999) is None


def test_update_claim_prediction(db_session):
    claim = _insert_claim(db_session, claim_number="CLM-PRED1")
    service = ClaimService(db_session)
    updated = service.update_claim_prediction(claim.id, 0.85, "coding")
    assert updated.denial_probability == 0.85
    assert updated.predicted_root_cause == "coding"


def test_update_prediction_missing_claim(db_session):
    service = ClaimService(db_session)
    result = service.update_claim_prediction(99999, 0.5, "other")
    assert result is None


def test_aging_summary(db_session):
    _insert_claim(db_session, claim_number="CLM-A1", aging_days=10)
    _insert_claim(db_session, claim_number="CLM-A2", aging_days=50)
    _insert_claim(db_session, claim_number="CLM-A3", aging_days=75)
    _insert_claim(db_session, claim_number="CLM-A4", aging_days=120)
    service = ClaimService(db_session)
    summary = service.get_aging_summary()
    assert summary["0-30"] == 1
    assert summary["31-60"] == 1
    assert summary["61-90"] == 1
    assert summary["90+"] == 1


def test_get_claims_status_filter(db_session):
    _insert_claim(db_session, claim_number="CLM-D1", status="denied")
    _insert_claim(db_session, claim_number="CLM-P1", status="pending")
    service = ClaimService(db_session)
    result = service.get_claims(status_filter="denied")
    assert result["total"] == 1
    assert result["claims"][0].status == "denied"
