import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.models.claim import Claim, AuditLog


class ClaimService:
    def __init__(self, db: Session):
        self.db = db

    def load_claims_from_csv(self, filepath: str) -> int:
        df = pd.read_csv(filepath)
        df = df.where(pd.notnull(df), None)
        df["denial_probability"] = None
        df["predicted_root_cause"] = None

        records = df.to_dict(orient="records")
        for rec in records:
            if rec.get("denial_reason_text") == "":
                rec["denial_reason_text"] = None

        self.db.bulk_insert_mappings(Claim, records)
        self.db.commit()
        return len(records)

    def get_claims(
        self,
        page: int = 1,
        page_size: int = 20,
        status_filter: str = None,
        payer_filter: str = None,
        hold_type_filter: str = None,
    ):
        query = self.db.query(Claim)

        if status_filter:
            query = query.filter(Claim.status == status_filter)
        if payer_filter:
            query = query.filter(Claim.payer_name == payer_filter)
        if hold_type_filter:
            query = query.filter(Claim.hold_type == hold_type_filter)

        total = query.count()
        claims = query.offset((page - 1) * page_size).limit(page_size).all()

        return {"claims": claims, "total": total, "page": page, "page_size": page_size}

    def get_claim_by_id(self, claim_id: int):
        return self.db.query(Claim).filter(Claim.id == claim_id).first()

    def update_claim_prediction(
        self, claim_id: int, denial_prob: float, root_cause: str
    ):
        claim = self.get_claim_by_id(claim_id)
        if not claim:
            return None

        claim.denial_probability = denial_prob
        claim.predicted_root_cause = root_cause

        audit = AuditLog(
            claim_id=claim_id,
            action="prediction_update",
            details=f"denial_prob={denial_prob:.4f}, root_cause={root_cause}",
        )
        self.db.add(audit)
        self.db.commit()
        self.db.refresh(claim)
        return claim

    def get_aging_summary(self):
        buckets = self.db.query(
            func.sum(case((Claim.aging_days <= 30, 1), else_=0)).label("days_0_30"),
            func.sum(
                case(
                    (Claim.aging_days.between(31, 60), 1),
                    else_=0,
                )
            ).label("days_31_60"),
            func.sum(
                case(
                    (Claim.aging_days.between(61, 90), 1),
                    else_=0,
                )
            ).label("days_61_90"),
            func.sum(case((Claim.aging_days > 90, 1), else_=0)).label("days_90_plus"),
        ).first()

        return {
            "0-30": buckets.days_0_30 or 0,
            "31-60": buckets.days_31_60 or 0,
            "61-90": buckets.days_61_90 or 0,
            "90+": buckets.days_90_plus or 0,
        }
