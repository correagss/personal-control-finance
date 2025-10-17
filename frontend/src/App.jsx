// src/App.jsx (CORRIGIDO)
import React, { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login.jsx';
import Register from './Register.jsx';
import Dashboard from './Dashboard.jsx';
import PrivacyPolicy from './PrivacyPolicy.jsx';

function App() {
  const [token, setToken] = useState(localStorage.getItem('authToken'));

  const handleLogin = (newToken) => {
    localStorage.setItem('authToken', newToken);
    setToken(newToken);
  };
  
  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
  };

  return (
    <Routes>
      {!token ? (
        
        <>
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/politica-de-privacidade" element={<PrivacyPolicy />} />
          <Route path="/" element={<Navigate to="/login" />} /> {}
          <Route path="*" element={<Navigate to="/login" />} /> {}
        </>
      ) : (
        
        <>
          <Route path="/dashboard" element={<Dashboard token={token} onLogout={handleLogout} />} />
          <Route path="/" element={<Navigate to="/dashboard" />} /> {}
          <Route path="*" element={<Navigate to="/dashboard" />} /> {}
        </>
      )}
    </Routes>
  );
}

export default App;