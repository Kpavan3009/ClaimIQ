from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas import ClaimResponse, ClaimListResponse
from app.services.claim_service import ClaimService

router = APIRouter(prefix="/api/claims", tags=["claims"])


@router.get("", response_model=ClaimListResponse)
def list_claims(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    payer: str = Query(None),
    hold_type: str = Query(None),
    db: Session = Depends(get_db),
):
    service = ClaimService(db)
    result = service.get_claims(page, page_size, status, payer, hold_type)
    return result


@router.get("/summary/aging")
def aging_summary(db: Session = Depends(get_db)):
    service = ClaimService(db)
    return service.get_aging_summary()


@router.get("/{claim_id}", response_model=ClaimResponse)
def get_claim(claim_id: int, db: Session = Depends(get_db)):
    service = ClaimService(db)
    claim = service.get_claim_by_id(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="claim not found")
    return claim


@router.post("/ingest")
def ingest_claims(filepath: str, db: Session = Depends(get_db)):
    service = ClaimService(db)
    count = service.load_claims_from_csv(filepath)
    return {"ingested": count}
