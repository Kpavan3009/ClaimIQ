import React from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ClaimTable from './components/ClaimTable';
import ClaimDetail from './components/ClaimDetail';

function NavLink({ to, children }) {
  const location = useLocation();
  const active = location.pathname === to;
  return (
    <Link to={to} className={`nav-link ${active ? 'nav-active' : ''}`}>
      {children}
    </Link>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <nav className="sidebar">
          <div className="logo">ClaimIQ</div>
          <NavLink to="/">Dashboard</NavLink>
          <NavLink to="/claims">Claims</NavLink>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/claims" element={<ClaimTable />} />
            <Route path="/claims/:id" element={<ClaimDetail />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
