import React, { useState, useEffect, useCallback } from 'react';
import './Dashboard.css';
import TransactionForm from './TransactionForm';

function Dashboard({ token, onLogout }) {
  const [saldo, setSaldo] = useState(null);
  const [transacoes, setTransacoes] = useState([]);
  const [error, setError] = useState('');
  const [transacaoEmEdicao, setTransacaoEmEdicao] = useState(null);

  const buscarDados = useCallback(async () => {
    try {
      const [resSaldo, resTransacoes] = await Promise.all([
        
        fetch(`${import.meta.env.VITE_API_URL}/saldo`, { headers: { 'Authorization': `Bearer ${token}` } }),
        fetch(`${import.meta.env.VITE_API_URL}/transacoes/`, { headers: { 'Authorization': `Bearer ${token}` } })
      ]);
      if (!resSaldo.ok || !resTransacoes.ok) { throw new Error('Failed to fetch data.'); }
      const dataSaldo = await resSaldo.json();
      const dataTransacoes = await resTransacoes.json();
      setSaldo(dataSaldo);
      setTransacoes(dataTransacoes);
    } catch (err) {
      setError(err.message);
      if (err.response?.status === 401) onLogout();
    }
  }, [token, onLogout]);

  useEffect(() => {
    if (token) buscarDados();
  }, [token, buscarDados]);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this transaction?')) return;
    try {
      
      await fetch(`${import.meta.env.VITE_API_URL}/transacoes/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      buscarDados();
    } catch (err) {
      setError('Failed to delete transaction.');
    }
  };

  const handleEdit = (transacao) => {
    setTransacaoEmEdicao(transacao); 
    window.scrollTo(0, 0); 
  };
  
  const handleUpdateDone = () => {
    setTransacaoEmEdicao(null); 
    buscarDados(); 
  };

  return (
    
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>PERSONAL FINANCE CONTROL📊</h1>
        <button onClick={onLogout} className="logout-button">Exit</button>
      </header>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {saldo && (
        <div className="saldo-container">
          <h2>Current Balance</h2>
          <p className="saldo-valor">R$ {saldo.saldo.toFixed(2)}</p>
        </div>
      )}
      <TransactionForm
        token={token}
        onTransactionAdded={buscarDados}
        transacaoParaEditar={transacaoEmEdicao}
        onUpdateDone={handleUpdateDone}
      />
      <div className="transacoes-container">
        <h2>My Transactions</h2>
        <ul className="transacoes-lista">
          {transacoes.length > 0 ? (
            transacoes.map(transacao => (
              <li key={transacao.id} className={`transacao-item ${transacao.tipo}`}>
                <div className="transacao-info">
                  <span>{transacao.descricao}</span>
                  <small>{new Date(transacao.data).toLocaleDateString('pt-BR')}</small>
                </div>
                <div className="transacao-acoes">
                  <span className="valor">R$ {transacao.valor.toFixed(2)}</span>
                  <button className="edit-btn" onClick={() => handleEdit(transacao)}>Edit</button>
                  <button className="delete-btn" onClick={() => handleDelete(transacao.id)}>X</button>
                </div>
              </li>
            ))
          ) : (
            <p>No transactions found.</p>
          )}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;