// src/Register.jsx
import React, { useState } from 'react';
import './Register.css';

function Register({ onSwitchToLogin }) { // Recebe a função para voltar ao login
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage('');
    setIsError(false);

    try {
      const response = await fetch('http://127.0.0.1:8000/registrar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Falha ao registrar.');
      }
      
      setMessage('Usuário registrado com sucesso! Você já pode fazer o login.');

    } catch (err) {
      setMessage(err.message);
      setIsError(true);
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h2>Criar Nova Conta</h2>
        <form onSubmit={handleSubmit} className="register-form">
          <input
            type="email"
            placeholder="E-mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Registrar</button>
        </form>
        {message && (
          <p className={`form-message ${isError ? 'error' : 'success'}`}>
            {message}
          </p>
        )}
        <p className="login-link">
          Já tem uma conta? <a href="#" onClick={onSwitchToLogin}>Faça o login</a>
        </p>
      </div>
    </div>
  );
}

export default Register;