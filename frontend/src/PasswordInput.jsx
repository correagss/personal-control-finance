// src/PasswordInput.jsx
import React, { useState } from 'react';
import { AiOutlineEye, AiOutlineEyeInvisible } from 'react-icons/ai'; // 1. Importa os ícones
import './PasswordInput.css';

// A estrutura do componente (props) continua a mesma
function PasswordInput({ value, onChange, placeholder, required = false }) {
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);

  const togglePasswordVisibility = () => {
    setIsPasswordVisible(!isPasswordVisible);
  };

  return (
    <div className="password-input-wrapper">
      <input
        // O input continua exatamente o mesmo
        type={isPasswordVisible ? 'text' : 'password'}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
      />
      <button
        type="button"
        className="password-toggle-btn"
        onClick={togglePasswordVisibility}
        title={isPasswordVisible ? 'Hide password' : 'Show password'}
      >
        {/* 2. A ÚNICA MUDANÇA É AQUI! */}
        {/* Em vez do emoji, agora usamos os componentes de ícone */}
        {isPasswordVisible ? <AiOutlineEyeInvisible /> : <AiOutlineEye />}
      </button>
    </div>
  );
}

export default PasswordInput;