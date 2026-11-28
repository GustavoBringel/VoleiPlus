import { Link } from 'react-router-dom';
import './Dashboard.css';

export default function Dashboard() {
  // Dados mockados para demonstração
  const teams = [
    {
      id: 1,
      name: 'Falcões',
      category: 'Sub-17',
      athletesCount: 12,
      nextTraining: '2026-03-15T19:00:00',
    },
    {
      id: 2,
      name: 'Águias',
      category: 'Adulto',
      athletesCount: 8,
      nextTraining: '2026-03-18T19:00:00',
    },
  ];

  const formatDate = dateString => {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
  };

  if (teams.length === 0) {
    return (
      <div className="dashboard">
        <div className="dashboard-header">
          <h1>Minhas Equipes</h1>
          <Link to="/teams/new" className="btn btn-primary">
            + Nova Equipe
          </Link>
        </div>

        <div className="empty-state">
          <div className="empty-icon">🏐</div>
          <h2>Nenhuma equipe ainda</h2>
          <p>Crie sua primeira equipe para começar a gerenciar treinos, atletas e avaliações.</p>
          <Link to="/teams/new" className="btn btn-primary">
            Criar primeira equipe
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Minhas Equipes</h1>
        <Link to="/teams/new" className="btn btn-primary">
          + Nova Equipe
        </Link>
      </div>

      <div className="teams-grid">
        {teams.map(team => (
          <article key={team.id} className="team-card">
            <div className="team-card-header">
              <span className="team-icon">🏐</span>
              <div className="team-info">
                <h2>{team.name}</h2>
                <span className="team-category">{team.category}</span>
              </div>
            </div>
            <div className="team-stats">
              <div className="stat">
                <span className="stat-value">{team.athletesCount}</span>
                <span className="stat-label">Atletas</span>
              </div>
              <div className="stat">
                <span className="stat-value">{formatDate(team.nextTraining)}</span>
                <span className="stat-label">Próximo treino</span>
              </div>
            </div>
            <div className="team-actions">
              <Link to={`/teams/${team.id}/trainings`} className="btn btn-secondary btn-small">
                Ver treinos
              </Link>
              <Link to={`/teams/${team.id}/athletes`} className="btn btn-secondary btn-small">
                Ver atletas
              </Link>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
