import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchClaimById, runPrediction } from '../api';

function ClaimDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [claim, setClaim] = useState(null);
  const [predicting, setPredicting] = useState(false);

  useEffect(() => {
    fetchClaimById(id)
      .then((resp) => setClaim(resp.data))
      .catch(() => setClaim(null));
  }, [id]);

  const handlePredict = async () => {
    setPredicting(true);
    try {
      await runPrediction(id);
      const resp = await fetchClaimById(id);
      setClaim(resp.data);
    } catch (e) {}
    setPredicting(false);
  };

  if (!claim) return <div className="loading-cell">Loading...</div>;

  const fields = [
    ['Claim Number', claim.claim_number],
    ['Patient ID', claim.patient_id],
    ['CPT Code', claim.cpt_code],
    ['ICD Code', claim.icd_code],
    ['Payer', claim.payer_name],
    ['Billed Amount', `$${claim.billed_amount?.toLocaleString()}`],
    ['Claim Date', new Date(claim.claim_date).toLocaleDateString()],
    ['Aging Days', `${claim.aging_days}d`],
    ['Hold Type', claim.hold_type],
    ['Status', claim.status],
    ['Denial Probability', claim.denial_probability !== null ? `${(claim.denial_probability * 100).toFixed(1)}%` : 'Not predicted'],
    ['Predicted Root Cause', claim.predicted_root_cause || 'N/A'],
  ];

  return (
    <div className="claim-detail">
      <button className="back-btn" onClick={() => navigate(-1)}>&larr; Back</button>
      <h2 className="page-title">{claim.claim_number}</h2>

      <div className="detail-grid">
        {fields.map(([label, value]) => (
          <div key={label} className="detail-field">
            <span className="detail-label">{label}</span>
            <span className="detail-value">{value}</span>
          </div>
        ))}
      </div>

      {claim.denial_reason_text && (
        <div className="denial-text-box">
          <h3>Denial Reason</h3>
          <p>{claim.denial_reason_text}</p>
        </div>
      )}

      <button className="predict-btn" onClick={handlePredict} disabled={predicting}>
        {predicting ? 'Running...' : 'Run Prediction'}
      </button>
    </div>
  );
}

export default ClaimDetail;
