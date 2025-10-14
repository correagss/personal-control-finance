// src/App.jsx
import React, { useState } from 'react';
import Login from './Login.jsx';
import Register from './Register.jsx'; // Importa o componente de Registro
import Dashboard from './Dashboard.jsx';

function App() {
  const [token, setToken] = useState(localStorage.getItem('authToken'));
  // Nova memória para saber qual tela mostrar: 'login' ou 'register'
  const [currentView, setCurrentView] = useState('login'); 

  const handleLogin = (newToken) => {
    localStorage.setItem('authToken', newToken);
    setToken(newToken);
  };
  
  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
    setCurrentView('login'); // Ao deslogar, volta para a tela de login
  };

  // Se o usuário NÃO está logado...
  if (!token) {
    if (currentView === 'login') {
      // ...e a visão atual é 'login', mostra o componente de Login
      return <Login onLogin={handleLogin} onSwitchToRegister={() => setCurrentView('register')} />;
    } else {
      // ...e a visão atual é 'register', mostra o componente de Registro
      return <Register onSwitchToLogin={() => setCurrentView('login')} />;
    }
  }

  // Se o usuário ESTÁ logado, mostra o Dashboard
  return <Dashboard token={token} onLogout={handleLogout} />;
}

export default App;