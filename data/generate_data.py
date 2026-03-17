import csv
import random
import uuid
from datetime import datetime, timedelta

random.seed(42)

CPT_CODES = ["99213", "99214", "99215", "99223", "99232", "99233",
             "99281", "99282", "99283", "99284", "99285"]

ICD_CODES = ["E11.9", "I10", "J18.9", "M54.5", "K21.0",
             "N39.0", "J44.1", "I25.10", "E78.5", "Z87.891"]

PAYERS = ["Blue Cross", "Aetna", "UnitedHealth", "Cigna",
          "Humana", "Medicare", "Medicaid"]

HOLD_TYPES = ["MISSING_AUTH", "CODING_ERROR", "ELIGIBILITY",
              "TIMELY_FILING", "MEDICAL_NECESSITY", "DUPLICATE_CLAIM",
              "INVALID_CPT", "MISSING_MODIFIER"]

DENIAL_TEMPLATES = [
    "prior authorization not obtained before service",
    "diagnosis code does not support medical necessity",
    "patient eligibility terminated on date of service",
    "claim submitted beyond timely filing deadline",
    "duplicate claim already processed for same date of service",
    "invalid cpt code for reported place of service",
    "missing modifier required for procedure code",
    "coding combination not allowed per payer guidelines",
    "referral authorization expired before service date",
    "patient not covered under plan on date of service",
    "procedure not covered under current benefit plan",
    "insufficient documentation to support billed level of service",
    "coordination of benefits information missing",
    "service requires preauthorization which was not obtained",
    "billed amount exceeds allowed amount for this procedure",
    "provider not in network for this plan",
    "incorrect place of service code for procedure billed",
]

STATUS_CHOICES = ["pending"] * 60 + ["denied"] * 25 + ["resolved"] * 15

NUM_RECORDS = 50000

rows = []
base_date = datetime(2024, 1, 1)

for i in range(NUM_RECORDS):
    claim_number = f"CLM-{uuid.uuid4().hex[:8].upper()}"
    patient_id = f"PAT-{random.randint(10000, 99999)}"
    cpt_code = random.choice(CPT_CODES)
    icd_code = random.choice(ICD_CODES)
    payer_name = random.choice(PAYERS)
    payer_id = f"PYR-{PAYERS.index(payer_name) + 1:03d}"
    billed_amount = round(random.uniform(150, 15000), 2)
    aging_days = random.randint(1, 120)
    hold_type = random.choice(HOLD_TYPES)
    status = random.choice(STATUS_CHOICES)
    claim_date = base_date + timedelta(days=random.randint(0, 365))

    if status == "denied" or random.random() < 0.3:
        denial_reason_text = random.choice(DENIAL_TEMPLATES)
    else:
        denial_reason_text = ""

    rows.append({
        "claim_number": claim_number,
        "patient_id": patient_id,
        "cpt_code": cpt_code,
        "icd_code": icd_code,
        "payer_id": payer_id,
        "payer_name": payer_name,
        "billed_amount": billed_amount,
        "claim_date": claim_date.strftime("%Y-%m-%d"),
        "aging_days": aging_days,
        "hold_type": hold_type,
        "denial_reason_text": denial_reason_text,
        "status": status,
        "denial_probability": "",
        "predicted_root_cause": "",
    })

output_path = "data/claims.csv"
fieldnames = list(rows[0].keys())

with open(output_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"generated {len(rows)} claims to {output_path}")
