import { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import './TrainingsList.css';

export default function TrainingsList() {
  const { teamId } = useParams();
  const [trainings, setTrainings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadTrainings = async () => {
      try {
        setIsLoading(true);
        await new Promise(resolve => setTimeout(resolve, 500));
        const mockTrainings = [
          {
            id: 1,
            date: '2026-03-15T19:00:00',
            endTime: '2026-03-15T21:00:00',
            location: 'Quadra 2',
            notes: 'Foco em passe e saque',
          },
          {
            id: 2,
            date: '2026-03-12T19:00:00',
            endTime: '2026-03-12T20:30:00',
            location: 'Quadra 1',
            notes: 'Treino tático',
          },
          {
            id: 3,
            date: '2026-03-08T19:00:00',
            endTime: '2026-03-08T21:00:00',
            location: 'Quadra 2',
            notes: null,
          },
        ];
        setTrainings(mockTrainings);
      } catch {
        setError('Erro ao carregar treinos');
      } finally {
        setIsLoading(false);
      }
    };
    loadTrainings();
  }, [teamId]);

  const formatDate = dateString => {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', { weekday: 'long', day: '2-digit', month: '2-digit' });
  };

  if (isLoading) {
    return (
      <div className="trainings-list">
        <div className="page-header">
          <Link to="/teams" className="back-link" aria-label="Voltar">
            ← Voltar
          </Link>
          <h1>Treinos</h1>
        </div>
        <div className="trainings-list-skeleton">
          {[1, 2, 3].map(i => (
            <article key={i} className="training-card skeleton">
              <div className="skeleton" style={{ height: '1.5rem', width: '40%' }}></div>
              <div
                className="skeleton"
                style={{ height: '1rem', width: '60%', marginTop: '0.5rem' }}
              ></div>
              <div
                className="skeleton"
                style={{ height: '1rem', width: '50%', marginTop: '0.5rem' }}
              ></div>
              <div
                className="skeleton"
                style={{ height: '2.5rem', width: '100%', marginTop: '1rem' }}
              ></div>
            </article>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="trainings-list">
        <div className="page-header">
          <Link to="/teams" className="back-link">
            ← Voltar
          </Link>
          <h1>Treinos</h1>
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
    <div className="trainings-list">
      <div className="page-header">
        <Link to="/teams" className="back-link" aria-label="Voltar para equipes">
          ← Voltar
        </Link>
        <h1>Treinos</h1>
        <Link to={`/teams/${teamId}/trainings/new`} className="btn btn-primary">
          + Novo Treino
        </Link>
      </div>

      {trainings.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📅</div>
          <h2>Nenhum treino agendado</h2>
          <p>Crie o primeiro treino para começar a registrar presenças.</p>
          <Link to={`/teams/${teamId}/trainings/new`} className="btn btn-primary">
            Agendar primeiro treino
          </Link>
        </div>
      ) : (
        <div className="trainings-list-container">
          {trainings.map(training => (
            <article key={training.id} className="training-card">
              <div className="training-header">
                <div className="training-date">
                  <span className="date-day">{new Date(training.date).getDate()}</span>
                  <span className="date-month">
                    {new Date(training.date).toLocaleDateString('pt-BR', { month: 'short' })}
                  </span>
                </div>
                <div className="training-info">
                  <h2>{formatDate(training.date)}</h2>
                  <p className="training-time">
                    {new Date(training.date).toLocaleTimeString('pt-BR', {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}{' '}
                    -
                    {new Date(training.endTime).toLocaleTimeString('pt-BR', {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </p>
                  <p className="training-location">📍 {training.location}</p>
                </div>
              </div>
              {training.notes && <p className="training-notes">{training.notes}</p>}
              <div className="training-actions">
                <Link to={`/trainings/${training.id}/attendance`} className="btn btn-primary">
                  📋 Chamada
                </Link>
                <Link
                  to={`/teams/${teamId}/trainings/${training.id}/edit`}
                  className="btn btn-secondary"
                >
                  ✏️ Editar
                </Link>
                <button className="btn btn-danger" onClick={() => handleDelete(training.id)}>
                  🗑️ Excluir
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

function handleDelete(id) {
  if (window.confirm('Tem certeza que deseja excluir este treino?')) {
    // Simula exclusão
    console.log('Excluir treino:', id);
  }
}
