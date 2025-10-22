import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Login.css';
import PasswordInput from './PasswordInput'; 

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      
      const response = await fetch(`${import.meta.env.VITE_API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ 'username': email, 'password': password })
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Incorrect email or password.');
      }
      const data = await response.json();
      onLogin(data.access_token);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    
    <div className="login-container">
      <div className="login-card">
        <h2>PERSONAL FINANCE CONTROL 📊</h2>
        <form onSubmit={handleSubmit} className="login-form">
          <input
            type="email"
            placeholder="E-mail"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
          <PasswordInput
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required={true}
          />
          <button type="submit">Enter</button>
        </form>
        {error && <p className="login-error">{error}</p>}
        <p className="register-link">
          Don't have an account? <Link to="/register">Register</Link>
        </p>
        <p className="privacy-link" style={{ marginTop: '12px', fontSize: '14px' }}>
          <Link to="/politica-de-privacidade">Privacy Politicy</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;