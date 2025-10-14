// src/Login.jsx
import React, { useState } from 'react';
import './Login.css';

// Adicionamos onSwitchToRegister como uma "ponte"
function Login({ onLogin, onSwitchToRegister }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    // ... a lógica do handleSubmit continua EXATAMENTE a mesma ...
    event.preventDefault();
    setError('');
    try {
      const response = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ 'username': email, 'password': password })
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'E-mail ou senha incorretos');
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
        <h2>Meu Cofrinho de Bananas 🍌</h2>
        <form onSubmit={handleSubmit} className="login-form">
          <input
            type="email"
            placeholder="E-mail"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Senha"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
          <button type="submit">Entrar</button>
        </form>
        {error && <p className="login-error">{error}</p>}
        {/* ADICIONAMOS ESTE LINK ABAIXO */}
        <p className="register-link">
          Não tem uma conta? <a href="#" onClick={onSwitchToRegister}>Registre-se</a>
        </p>
      </div>
    </div>
  );
}

export default Login;