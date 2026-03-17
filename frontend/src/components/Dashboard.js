import React, { useState, useEffect } from 'react';
import { fetchClaims } from '../api';
import AgingChart from './AgingChart';
import ClaimTable from './ClaimTable';

function Dashboard() {
  const [kpis, setKpis] = useState({ total: 0, highRisk: 0, avgAging: 0, atRiskAmount: 0 });

  useEffect(() => {
    fetchClaims(1, 1000)
      .then((resp) => {
        const claims = resp.data.claims;
        const total = resp.data.total;
        const highRisk = claims.filter((c) => c.denial_probability >= 0.5).length;
        const avgAging = claims.length > 0
          ? Math.round(claims.reduce((s, c) => s + c.aging_days, 0) / claims.length)
          : 0;
        const atRiskAmount = claims
          .filter((c) => c.denial_probability >= 0.5)
          .reduce((s, c) => s + (c.billed_amount || 0), 0);

        setKpis({ total, highRisk, avgAging, atRiskAmount });
      })
      .catch(() => {});
  }, []);

  const cards = [
    { label: 'Total Claims', value: kpis.total.toLocaleString(), accent: '#58a6ff' },
    { label: 'High Risk', value: kpis.highRisk.toLocaleString(), accent: '#ef4444' },
    { label: 'Avg Aging', value: `${kpis.avgAging}d`, accent: '#f97316' },
    { label: 'At-Risk Amount', value: `$${kpis.atRiskAmount.toLocaleString()}`, accent: '#eab308' },
  ];

  return (
    <div className="dashboard">
      <h2 className="page-title">Dashboard</h2>

      <div className="kpi-grid">
        {cards.map((c) => (
          <div key={c.label} className="kpi-card" style={{ borderTop: `3px solid ${c.accent}` }}>
            <div className="kpi-value">{c.value}</div>
            <div className="kpi-label">{c.label}</div>
          </div>
        ))}
      </div>

      <AgingChart />
      <ClaimTable />
    </div>
  );
}

export default Dashboard;
