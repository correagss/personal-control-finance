// src/PrivacyPolicy.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './PrivacyPolicy.css';

function PrivacyPolicy() {
  return (
    <div className="privacy-container">
      <h1>Privacy Policy</h1>
      <p><strong>Last updated:</strong> [10/15/2025]</p>

      <h2>1. Information Collection</h2>
      <p>
        We collect the following information when you register for our service:
        <ul>
          <li><strong>Email address:</strong> Used solely to identify your account and allow the login process.</li>
          <li><strong>Password:</strong> Your password is processed through a hashing algorithm (Argon2) before being stored. We never store your password in plain text. Only the hash — an irreversible cryptographic representation of your password — is kept in our database.</li>
        </ul>
      </p>

      <h2>2. Use of Information</h2>
      <p>
        Your information is used exclusively to:
        <ul>
          <li>Authenticate your access to the platform.</li>
          <li>Associate the financial transactions you create with your account.</li>
        </ul>
      </p>

      <h2>3. Data Sharing</h2>
      <p>
        <strong>We do not share your email, password, or financial data with anyone.</strong> All information is securely stored and treated as confidential. This is a portfolio project and has no commercial purposes.
      </p>

      <Link to="/" className="back-link">Back to Login</Link>
    </div>
  );
}

export default PrivacyPolicy;
