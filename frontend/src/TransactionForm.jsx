import React, { useState, useEffect } from 'react';
import './TransactionForm.css';

function TransactionForm({ token, onTransactionAdded, transacaoParaEditar, onUpdateDone }) {
  const [descricao, setDescricao] = useState('');
  const [valor, setValor] = useState('');
  const [tipo, setTipo] = useState('saida');
  const [error, setError] = useState('');
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (transacaoParaEditar) {
      setDescricao(transacaoParaEditar.descricao);
      setValor(transacaoParaEditar.valor);
      setTipo(transacaoParaEditar.tipo);
      setIsEditing(true);
    } else {
      setIsEditing(false);
    }
  }, [transacaoParaEditar]); 

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    
    
    const url = isEditing
      ? `${import.meta.env.VITE_API_URL}/transacoes/${transacaoParaEditar.id}` 
      : `${import.meta.env.VITE_API_URL}/transacoes/`;

    const method = isEditing ? 'PUT' : 'POST';

    try {
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ descricao, valor: parseFloat(valor), tipo })
      });
      if (!response.ok) {
        throw new Error(`Falha ao ${isEditing ? 'atualizar' : 'adicionar'} transação.`);
      }
      
      setDescricao('');
      setValor('');
      setTipo('saida');
      setIsEditing(false);
      
      if (isEditing) {
        onUpdateDone(); 
      } else {
        onTransactionAdded(); 
      }
    } catch (err) {
      
      setError(err.message);
    }
  };

  return (
    <div className="form-container">
      <h2>{isEditing ? 'Edit Transaction' : 'Add New Transaction'}</h2>
      <form onSubmit={handleSubmit} className="transaction-form">
        <input
          type="text"
          placeholder="Description"
          value={descricao}
          onChange={(e) => setDescricao(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Value"
          value={valor}
          onChange={(e) => setValor(e.target.value)}
          step="0.01"
          required
        />
        <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
          <option value="saida">Exit</option>
          <option value="entrada">Enter</option>
        </select>
        <button type="submit">{isEditing ? 'Save' : 'To add'}</button>
      </form>
      {error && <p style={{color: 'red'}}>{error}</p>}
    </div>
  );
}

export default TransactionForm;