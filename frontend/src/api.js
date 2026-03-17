import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
});

export function fetchClaims(page = 1, pageSize = 20, filters = {}) {
  const params = { page, page_size: pageSize, ...filters };
  return api.get('/api/claims', { params });
}

export function fetchClaimById(id) {
  return api.get(`/api/claims/${id}`);
}

export function fetchAgingSummary() {
  return api.get('/api/claims/summary/aging');
}

export function runPrediction(claimId) {
  return api.post(`/api/predict/${claimId}`);
}

export default api;
