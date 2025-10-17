// src/Register.jsx
// src/Register.jsx
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Register.css';
import PasswordInput from './PasswordInput'; 

function Register() { 
  const navigate = useNavigate(); 
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage('');
    setIsError(false);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/registrar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to register.');
      }
      setMessage('User registered successfully! Redirecting to login...');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      setMessage(err.message);
      setIsError(true);
    }
  };

  return (
    // ... JSX continua igual
    <div className="register-container">
      <div className="register-card">
        <h2>Create New Account</h2>
        <form onSubmit={handleSubmit} className="register-form">
          <input
            type="email"
            placeholder="E-mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <PasswordInput
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required={true}
          />
          <button type="submit">Register</button>
        </form>
        {message && (
          <p className={`form-message ${isError ? 'error' : 'success'}`}>
            {message}
          </p>
        )}
        <p className="login-link">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </div>
    </div>
  );
}

export default Register;