import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './TeamsList.css';

export default function TeamsList() {
  const [teams, setTeams] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  // Simula carregamento de dados
  useEffect(() => {
    const loadTeams = async () => {
      try {
        setIsLoading(true);
        // Simula API call
        await new Promise(resolve => setTimeout(resolve, 500));
        const mockTeams = [
          {
            id: 1,
            name: 'Falcões',
            category: 'Sub-17',
            coach: 'João Silva',
            athletesCount: 12,
            active: true,
            nextTraining: '2026-03-15T19:00:00',
          },
          {
            id: 2,
            name: 'Águias',
            category: 'Adulto',
            coach: 'Maria Santos',
            athletesCount: 8,
            active: true,
            nextTraining: '2026-03-18T19:00:00',
          },
          {
            id: 3,
            name: 'Tubarões',
            category: 'Sub-15',
            coach: 'Pedro Costa',
            athletesCount: 10,
            active: false,
            nextTraining: null,
          },
        ];
        setTeams(mockTeams);
      } catch {
        setError('Erro ao carregar equipes');
      } finally {
        setIsLoading(false);
      }
    };
    loadTeams();
  }, []);

  const filteredTeams = teams.filter(team =>
    team.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDeactivate = async teamId => {
    if (
      !window.confirm(
        'Tem certeza que deseja inativar esta equipe? Os treinos e atletas serão preservados.'
      )
    ) {
      return;
    }
    try {
      // Simula API call
      await new Promise(resolve => setTimeout(resolve, 300));
      setTeams(prev => prev.map(t => (t.id === teamId ? { ...t, active: false } : t)));
    } catch {
      alert('Erro ao inativar equipe');
    }
  };

  const formatDate = dateString => {
    if (!dateString) return '—';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
  };

  if (isLoading) {
    return (
      <div className="teams-list">
        <div className="page-header">
          <h1>Equipes</h1>
        </div>
        <div className="teams-grid">
          {[1, 2, 3].map(i => (
            <article key={i} className="team-card skeleton">
              <div className="team-card-header">
                <div
                  className="team-icon skeleton"
                  style={{ height: '40px', width: '40px', borderRadius: '50%' }}
                ></div>
                <div className="team-info">
                  <div className="skeleton" style={{ height: '1.25rem', width: '60%' }}></div>
                  <div
                    className="skeleton"
                    style={{
                      height: '0.8rem',
                      width: '40%',
                      marginTop: '0.25rem',
                      borderRadius: '999px',
                    }}
                  ></div>
                </div>
              </div>
              <div className="team-stats">
                <div className="stat">
                  <div className="skeleton" style={{ height: '1.5rem', width: '2rem' }}></div>
                  <div
                    className="skeleton"
                    style={{ height: '0.75rem', width: '4rem', marginTop: '0.125rem' }}
                  ></div>
                </div>
                <div className="stat">
                  <div className="skeleton" style={{ height: '1.5rem', width: '2rem' }}></div>
                  <div
                    className="skeleton"
                    style={{ height: '0.75rem', width: '4rem', marginTop: '0.125rem' }}
                  ></div>
                </div>
              </div>
              <div className="team-actions">
                <div className="skeleton btn-small" style={{ height: '40px' }}></div>
                <div className="skeleton btn-small" style={{ height: '40px' }}></div>
              </div>
            </article>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="teams-list">
        <div className="page-header">
          <h1>Equipes</h1>
        </div>
        <div className="error-state">
          <p>{error}</p>
          <button className="btn btn-primary" onClick={() => window.location.reload()}>
            Tentar novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="teams-list">
      <div className="page-header">
        <h1>Equipes</h1>
        <Link to="/teams/new" className="btn btn-primary">
          + Nova Equipe
        </Link>
      </div>

      <div className="search-bar">
        <input
          type="search"
          placeholder="Buscar equipe..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          className="search-input"
          aria-label="Buscar equipe"
        />
      </div>

      {filteredTeams.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🏐</div>
          <h2>{searchTerm ? 'Nenhuma equipe encontrada' : 'Nenhuma equipe cadastrada'}</h2>
          <p>
            {searchTerm ? 'Tente outro termo de busca.' : 'Crie sua primeira equipe para começar.'}
          </p>
          {!searchTerm && (
            <Link to="/teams/new" className="btn btn-primary">
              Criar primeira equipe
            </Link>
          )}
        </div>
      ) : (
        <div className="teams-grid">
          {filteredTeams.map(team => (
            <article key={team.id} className={`team-card ${!team.active ? 'inactive' : ''}`}>
              <div className="team-card-header">
                <span className="team-icon">🏐</span>
                <div className="team-info">
                  <h2>{team.name}</h2>
                  <span className="team-category">{team.category}</span>
                </div>
              </div>
              <div className="team-meta">
                <span className="meta-item">
                  <strong>Treinador:</strong> {team.coach}
                </span>
                <span className="meta-item">
                  <strong>Atletas:</strong> {team.athletesCount}
                </span>
                <span className="meta-item">
                  <strong>Próximo:</strong> {formatDate(team.nextTraining)}
                </span>
                <span className={`status-badge ${team.active ? 'active' : 'inactive'}`}>
                  {team.active ? 'Ativa' : 'Inativa'}
                </span>
              </div>
              <div className="team-actions">
                <Link to={`/teams/${team.id}/trainings`} className="btn btn-secondary btn-small">
                  Treinos
                </Link>
                <Link to={`/teams/${team.id}/athletes`} className="btn btn-secondary btn-small">
                  Atletas
                </Link>
                {team.active && (
                  <button
                    className="btn btn-danger btn-small"
                    onClick={() => handleDeactivate(team.id)}
                  >
                    Inativar
                  </button>
                )}
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
