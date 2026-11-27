import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './Settings.css';

export default function Settings() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      await logout();
      navigate('/login', { replace: true });
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setIsLoggingOut(false);
    }
  };

  return (
    <div className="settings-container">
      <header className="settings-header">
        <h1>Configurações</h1>
      </header>

      <div className="settings-content">
        <section className="settings-section">
          <h2>Conta</h2>
          <div className="account-info">
            <div className="account-avatar">{user?.name?.charAt(0).toUpperCase() || 'U'}</div>
            <div className="account-details">
              <h3>{user?.name || 'Usuário'}</h3>
              <p>{user?.email || 'email@exemplo.com'}</p>
            </div>
          </div>
        </section>

        <section className="settings-section">
          <h2>Preferências</h2>
          <div className="preferences-list">
            <label className="preference-item">
              <span>
                <strong>Tema escuro</strong>
                <p>Usar cores escuras na interface</p>
              </span>
              <input type="checkbox" defaultChecked={false} disabled />
            </label>
            <label className="preference-item">
              <span>
                <strong>Notificações</strong>
                <p>Receber alertas de treinos e avaliações</p>
              </span>
              <input type="checkbox" defaultChecked={true} disabled />
            </label>
            <label className="preference-item">
              <span>
                <strong>Sincronização automática</strong>
                <p>Sincronizar dados quando online</p>
              </span>
              <input type="checkbox" defaultChecked={true} disabled />
            </label>
          </div>
        </section>

        <section className="settings-section">
          <h2>Sobre</h2>
          <div className="about-info">
            <p>
              <strong>Vôlei+</strong> - Gestão e Desenvolvimento Esportivo
            </p>
            <p>Versão 1.0.0 (MVP)</p>
            <p>Projeto de extensão - UFT 2026/2</p>
            <p>Desenvolvido por Flavio Henrique e Gustavo Bringel</p>
          </div>
        </section>

        <section className="settings-section danger-zone">
          <h2>Zona de perigo</h2>
          <button className="btn btn-danger" onClick={handleLogout} disabled={isLoggingOut}>
            {isLoggingOut ? 'Saindo...' : 'Sair da conta'}
          </button>
        </section>
      </div>
    </div>
  );
}
