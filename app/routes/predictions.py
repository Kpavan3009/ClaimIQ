from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas import PredictionResponse
from app.services.claim_service import ClaimService
from app.ml.predictor import DenialPredictor

router = APIRouter(prefix="/api/predict", tags=["predictions"])

predictor = None


def get_predictor():
    global predictor
    if predictor is None:
        predictor = DenialPredictor()
    return predictor


@router.post("/{claim_id}", response_model=PredictionResponse)
def predict_claim(claim_id: int, db: Session = Depends(get_db)):
    service = ClaimService(db)
    claim = service.get_claim_by_id(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="claim not found")

    claim_data = {
        "payer_name": claim.payer_name,
        "hold_type": claim.hold_type,
        "cpt_code": claim.cpt_code,
        "icd_code": claim.icd_code,
        "aging_days": claim.aging_days,
        "billed_amount": claim.billed_amount,
    }

    pred = get_predictor()
    result = pred.predict(claim_data)

    service.update_claim_prediction(
        claim_id, result["denial_probability"], result["predicted_root_cause"]
    )

    return result


@router.post("/batch", response_model=list[PredictionResponse])
def predict_batch(claim_ids: list[int], db: Session = Depends(get_db)):
    service = ClaimService(db)
    pred = get_predictor()
    results = []

    for cid in claim_ids:
        claim = service.get_claim_by_id(cid)
        if not claim:
            raise HTTPException(status_code=404, detail=f"claim {cid} not found")

        claim_data = {
            "payer_name": claim.payer_name,
            "hold_type": claim.hold_type,
            "cpt_code": claim.cpt_code,
            "icd_code": claim.icd_code,
            "aging_days": claim.aging_days,
            "billed_amount": claim.billed_amount,
        }

        result = pred.predict(claim_data)
        service.update_claim_prediction(
            cid, result["denial_probability"], result["predicted_root_cause"]
        )
        results.append(result)

    return results
