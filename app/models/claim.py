from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
    func,
)

from app.database import Base


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    claim_number = Column(String(50), unique=True, nullable=False)
    patient_id = Column(String(50), nullable=False)
    cpt_code = Column(String(10))
    icd_code = Column(String(10))
    payer_id = Column(String(50))
    payer_name = Column(String(100))
    billed_amount = Column(Float)
    claim_date = Column(DateTime)
    aging_days = Column(Integer, default=0)
    hold_type = Column(String(50))
    denial_reason_text = Column(Text, nullable=True)
    status = Column(String(20), default="pending")
    denial_probability = Column(Float, nullable=True)
    predicted_root_cause = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class DenialHistory(Base):
    __tablename__ = "denial_history"

    id = Column(Integer, primary_key=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    denial_date = Column(DateTime)
    denial_code = Column(String(20))
    denial_category = Column(String(50))
    resolution_date = Column(DateTime, nullable=True)
    resolved = Column(Boolean, default=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    action = Column(String(50))
    details = Column(Text)
    user_id = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=func.now())
