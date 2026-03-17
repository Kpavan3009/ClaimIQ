import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchClaims } from '../api';

const COLUMNS = [
  { key: 'claim_number', label: 'Claim #' },
  { key: 'patient_id', label: 'Patient' },
  { key: 'cpt_code', label: 'CPT' },
  { key: 'payer_name', label: 'Payer' },
  { key: 'billed_amount', label: 'Amount' },
  { key: 'aging_days', label: 'Aging' },
  { key: 'status', label: 'Status' },
  { key: 'denial_probability', label: 'Risk' },
];

function ClaimTable() {
  const navigate = useNavigate();
  const [claims, setClaims] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(15);
  const [search, setSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [sortKey, setSortKey] = useState('aging_days');
  const [sortDir, setSortDir] = useState('desc');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
      setPage(1);
    }, 300);
    return () => clearTimeout(timer);
  }, [search]);

  const loadClaims = useCallback(async () => {
    setLoading(true);
    try {
      const filters = {};
      if (debouncedSearch) {
        filters.payer = debouncedSearch;
      }
      const resp = await fetchClaims(page, pageSize, filters);
      setClaims(resp.data.claims);
      setTotal(resp.data.total);
    } catch (e) {
      setClaims([]);
    }
    setLoading(false);
  }, [page, pageSize, debouncedSearch]);

  useEffect(() => {
    loadClaims();
  }, [loadClaims]);

  const sorted = [...claims].sort((a, b) => {
    const aVal = a[sortKey] ?? 0;
    const bVal = b[sortKey] ?? 0;
    if (aVal < bVal) return sortDir === 'asc' ? -1 : 1;
    if (aVal > bVal) return sortDir === 'asc' ? 1 : -1;
    return 0;
  });

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir('desc');
    }
  };

  const totalPages = Math.ceil(total / pageSize);

  const riskBadge = (prob) => {
    if (prob === null || prob === undefined) return <span className="badge badge-none">--</span>;
    if (prob >= 0.75) return <span className="badge badge-critical">{(prob * 100).toFixed(0)}%</span>;
    if (prob >= 0.5) return <span className="badge badge-high">{(prob * 100).toFixed(0)}%</span>;
    if (prob >= 0.25) return <span className="badge badge-med">{(prob * 100).toFixed(0)}%</span>;
    return <span className="badge badge-low">{(prob * 100).toFixed(0)}%</span>;
  };

  const statusBadge = (s) => {
    const cls = s === 'denied' ? 'badge-critical' : s === 'paid' ? 'badge-low' : 'badge-pending';
    return <span className={`badge ${cls}`}>{s}</span>;
  };

  return (
    <div className="claim-table-wrap">
      <div className="table-toolbar">
        <input
          className="search-input"
          type="text"
          placeholder="Filter by payer..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <span className="record-count">{total} claims</span>
      </div>

      <div className="table-scroll">
        <table className="claim-table">
          <thead>
            <tr>
              {COLUMNS.map((col) => (
                <th key={col.key} onClick={() => handleSort(col.key)} className="sortable">
                  {col.label}
                  {sortKey === col.key && (
                    <span className="sort-arrow">{sortDir === 'asc' ? ' \u2191' : ' \u2193'}</span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={COLUMNS.length} className="loading-cell">Loading...</td></tr>
            ) : sorted.map((c) => (
              <tr key={c.id} onClick={() => navigate(`/claims/${c.id}`)} className="clickable-row">
                <td>{c.claim_number}</td>
                <td>{c.patient_id}</td>
                <td>{c.cpt_code}</td>
                <td>{c.payer_name}</td>
                <td>${c.billed_amount?.toLocaleString()}</td>
                <td>{c.aging_days}d</td>
                <td>{statusBadge(c.status)}</td>
                <td>{riskBadge(c.denial_probability)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="pagination">
        <button disabled={page <= 1} onClick={() => setPage(page - 1)}>Prev</button>
        <span>{page} / {totalPages || 1}</span>
        <button disabled={page >= totalPages} onClick={() => setPage(page + 1)}>Next</button>
      </div>
    </div>
  );
}

export default ClaimTable;
