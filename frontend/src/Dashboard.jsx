// src/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import './Dashboard.css';

function Dashboard({ token, onLogout }) {
  // Memória para guardar o saldo
  const [saldo, setSaldo] = useState(null);
  const [error, setError] = useState('');

  // useEffect: O "Macaco Trabalhador" do React.
  // Ele roda o código aqui dentro AUTOMATICAMENTE quando o componente aparece na tela.
  useEffect(() => {
    const buscarDados = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/saldo/', {
          method: 'GET',
          headers: {
            // A parte mais importante: enviando nosso "passe secreto"!
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Falha ao buscar dados. Faça login novamente.');
        }

        const data = await response.json();
        setSaldo(data); // Guarda os dados do saldo na memória

      } catch (err) {
        setError(err.message);
        if (err.response && err.response.status === 401) {
          onLogout(); // Se o token for inválido, desloga o usuário
        }
      }
    };

    buscarDados();
  }, [token, onLogout]); // A lista de dependências. Roda de novo se o token mudar.

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Meu Cofrinho de Bananas 🍌</h1>
        <button onClick={onLogout} className="logout-button">
          Sair
        </button>
      </header>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {saldo ? ( // Se 'saldo' NÃO for nulo, mostra o card
        <div className="saldo-container">
          <h2>Saldo Atual</h2>
          <p className="saldo-valor">R$ {saldo.saldo.toFixed(2)}</p>
        </div>
      ) : ( // Se 'saldo' for nulo (carregando), mostra uma mensagem
        <p>Carregando saldo...</p>
      )}

      {/* Aqui virá a lista de transações e o formulário */}
    </div>
  );
}

export default Dashboard;