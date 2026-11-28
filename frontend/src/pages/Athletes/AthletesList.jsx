import { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import './AthletesList.css';

export default function AthletesList() {
  const { teamId } = useParams();
  const [athletes, setAthletes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showInactive, setShowInactive] = useState(false);

  useEffect(() => {
    const loadAthletes = async () => {
      try {
        setIsLoading(true);
        await new Promise(resolve => setTimeout(resolve, 500));
        const mockAthletes = [
          { id: 1, name: 'Ana Silva', position: 'Ponteira', age: 16, number: 10, active: true },
          { id: 2, name: 'Bruno Costa', position: 'Levantadora', age: 17, number: 7, active: true },
          { id: 3, name: 'Carla Dias', position: 'Líbero', age: 15, number: 2, active: true },
          { id: 4, name: 'Daniel Souza', position: 'Central', age: 16, number: 14, active: false },
          { id: 5, name: 'Eduarda Lima', position: 'Oposta', age: 17, number: 9, active: true },
        ];
        setAthletes(mockAthletes);
      } catch {
        // Error handling could be added here with a toast
      } finally {
        setIsLoading(false);
      }
    };
    loadAthletes();
  }, [teamId]);

  const filteredAthletes = athletes.filter(athlete => {
    const matchesSearch = athlete.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = showInactive || athlete.active;
    return matchesSearch && matchesStatus;
  });

  const handleToggleActive = async athleteId => {
    const athlete = athletes.find(a => a.id === athleteId);
    const action = athlete.active ? 'inativar' : 'ativar';
    if (!window.confirm(`Tem certeza que deseja ${action} este atleta?`)) return;

    try {
      await new Promise(resolve => setTimeout(resolve, 300));
      setAthletes(prev => prev.map(a => (a.id === athleteId ? { ...a, active: !a.active } : a)));
    } catch {
      alert('Erro ao alterar status do atleta');
    }
  };

  if (isLoading) {
    return (
      <div className="athletes-list">
        <div className="page-header">
          <Link to="/teams" className="back-link" aria-label="Voltar">
            ← Voltar
          </Link>
          <h1>Atletas</h1>
        </div>
        <div className="athletes-grid">
          {[1, 2, 3].map(i => (
            <article key={i} className="athlete-card skeleton">
              <div
                className="skeleton"
                style={{ height: '48px', width: '48px', borderRadius: '50%' }}
              ></div>
              <div className="athlete-info">
                <div className="skeleton" style={{ height: '1.25rem', width: '70%' }}></div>
                <div
                  className="skeleton"
                  style={{ height: '0.875rem', width: '50%', marginTop: '0.25rem' }}
                ></div>
              </div>
            </article>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="athletes-list">
      <div className="page-header">
        <Link to="/teams" className="back-link" aria-label="Voltar para equipes">
          ← Voltar
        </Link>
        <h1>Atletas</h1>
        <Link to={`/teams/${teamId}/athletes/new`} className="btn btn-primary">
          + Novo Atleta
        </Link>
      </div>

      <div className="search-and-filters">
        <div className="search-bar">
          <input
            type="search"
            placeholder="Buscar atleta por nome..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="search-input"
            aria-label="Buscar atleta"
          />
        </div>

        <label className="filter-toggle">
          <input
            type="checkbox"
            checked={showInactive}
            onChange={e => setShowInactive(e.target.checked)}
          />
          <span>Mostrar inativos</span>
        </label>
      </div>

      {filteredAthletes.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">👤</div>
          <h2>{searchTerm ? 'Nenhum atleta encontrado' : 'Nenhum atleta cadastrado'}</h2>
          <p>
            {searchTerm ? 'Tente outro termo de busca.' : 'Adicione atletas à equipe para começar.'}
          </p>
          {!searchTerm && (
            <Link to={`/teams/${teamId}/athletes/new`} className="btn btn-primary">
              Cadastrar primeiro atleta
            </Link>
          )}
        </div>
      ) : (
        <div className="athletes-grid">
          {filteredAthletes.map(athlete => (
            <article
              key={athlete.id}
              className={`athlete-card ${!athlete.active ? 'inactive' : ''}`}
            >
              <div className="athlete-avatar">{athlete.name.charAt(0).toUpperCase()}</div>
              <div className="athlete-info">
                <h2>{athlete.name}</h2>
                <div className="athlete-meta">
                  <span className="position">{athlete.position}</span>
                  <span className="age">{athlete.age} anos</span>
                  {athlete.number && <span className="number">Camisa {athlete.number}</span>}
                </div>
              </div>
              <div className="athlete-actions">
                <span className={`status-badge ${athlete.active ? 'active' : 'inactive'}`}>
                  {athlete.active ? 'Ativo' : 'Inativo'}
                </span>
                <button
                  className="btn btn-icon"
                  onClick={() => handleToggleActive(athlete.id)}
                  aria-label={athlete.active ? 'Inativar atleta' : 'Ativar atleta'}
                >
                  {athlete.active ? '⏸️' : '▶️'}
                </button>
                <Link
                  to={`/athletes/${athlete.id}`}
                  className="btn btn-icon"
                  aria-label="Ver perfil"
                >
                  👁️
                </Link>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
