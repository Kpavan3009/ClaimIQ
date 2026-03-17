import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <nav className="sidebar">
          <div className="logo">ClaimIQ</div>
          <Link to="/" className="nav-link">Dashboard</Link>
          <Link to="/claims" className="nav-link">Claims</Link>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<div>Dashboard</div>} />
            <Route path="/claims" element={<div>Claims</div>} />
            <Route path="/claims/:id" element={<div>Claim Detail</div>} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
