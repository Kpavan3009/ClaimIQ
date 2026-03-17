from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ClaimBase(BaseModel):
    claim_number: str
    patient_id: str
    cpt_code: str
    icd_code: str
    payer_id: str
    payer_name: str
    billed_amount: float
    claim_date: datetime
    hold_type: str
    denial_reason_text: Optional[str] = None


class ClaimCreate(ClaimBase):
    pass


class ClaimResponse(ClaimBase):
    id: int
    aging_days: int
    status: str
    denial_probability: Optional[float] = None
    predicted_root_cause: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PredictionResponse(BaseModel):
    denial_probability: float
    risk_tier: str
    predicted_root_cause: str
    recommended_action: str


class ClaimListResponse(BaseModel):
    claims: list[ClaimResponse]
    total: int
    page: int
    page_size: int


class DenialHistoryResponse(BaseModel):
    id: int
    claim_id: int
    denial_date: datetime
    denial_code: str
    denial_category: str
    resolution_date: Optional[datetime] = None
    resolved: bool

    model_config = ConfigDict(from_attributes=True)
