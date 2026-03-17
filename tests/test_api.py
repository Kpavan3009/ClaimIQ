from app.models.claim import Claim


def _seed_claim(db, **overrides):
    defaults = {
        "claim_number": "CLM-API001",
        "patient_id": "PAT-20001",
        "cpt_code": "99214",
        "icd_code": "J06.9",
        "payer_id": "PYR-002",
        "payer_name": "Aetna",
        "billed_amount": 1800.00,
        "aging_days": 30,
        "hold_type": "MISSING_AUTH",
        "status": "pending",
    }
    defaults.update(overrides)
    claim = Claim(**defaults)
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim


def test_list_claims_200(client, db_session):
    _seed_claim(db_session)
    resp = client.get("/api/claims")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    assert len(data["claims"]) >= 1


def test_get_claim_by_id_200(client, db_session):
    claim = _seed_claim(db_session)
    resp = client.get(f"/api/claims/{claim.id}")
    assert resp.status_code == 200
    assert resp.json()["claim_number"] == "CLM-API001"


def test_get_claim_404(client):
    resp = client.get("/api/claims/99999")
    assert resp.status_code == 404


def test_list_claims_pagination(client, db_session):
    for i in range(5):
        _seed_claim(db_session, claim_number=f"CLM-APIP{i:03d}")
    resp = client.get("/api/claims?page=1&page_size=2")
    data = resp.json()
    assert len(data["claims"]) == 2
    assert data["page_size"] == 2


def test_aging_summary_endpoint(client, db_session):
    _seed_claim(db_session, claim_number="CLM-AG1", aging_days=15)
    _seed_claim(db_session, claim_number="CLM-AG2", aging_days=100)
    resp = client.get("/api/claims/summary/aging")
    assert resp.status_code == 200
    data = resp.json()
    assert "0-30" in data
    assert "90+" in data
