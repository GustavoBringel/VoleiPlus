import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './Attendance.css';

export default function Attendance() {
  const { trainingId } = useParams();
  const navigate = useNavigate();
  const [training, setTraining] = useState(null);
  const [athletes, setAthletes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);
  const [saved, setSaved] = useState(false);
  const [saveResult, setSaveResult] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        await new Promise(resolve => setTimeout(resolve, 500));
        // Mock data
        setTraining({
          id: 1,
          date: '2026-03-15T19:00:00',
          endTime: '2026-03-15T21:00:00',
          location: 'Quadra 2',
        });
        setAthletes([
          { id: 1, name: 'Ana Silva', position: 'Ponteira', present: true },
          { id: 2, name: 'Bruno Costa', position: 'Levantadora', present: false },
          { id: 3, name: 'Carla Dias', position: 'Líbero', present: false },
          { id: 4, name: 'Daniel Souza', position: 'Central', present: true },
          { id: 5, name: 'Eduarda Lima', position: 'Oposta', present: true },
          { id: 6, name: 'Felipe Santos', position: 'Ponteira', present: false },
        ]);
      } catch {
        setError('Erro ao carregar dados da chamada');
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, [trainingId]);

  const handleToggle = athleteId => {
    setAthletes(prev => prev.map(a => (a.id === athleteId ? { ...a, present: !a.present } : a)));
  };

  const handleMarkAll = () => {
    const allPresent = athletes.every(a => a.present);
    setAthletes(prev => prev.map(a => ({ ...a, present: !allPresent })));
  };

  const handleSave = async () => {
    setIsSaving(true);
    setError(null);
    try {
      await new Promise(resolve => setTimeout(resolve, 800));
      const presentCount = athletes.filter(a => a.present).length;
      const absentCount = athletes.length - presentCount;
      setSaveResult({ present: presentCount, absent: absentCount });
      setSaved(true);
    } catch {
      setError('Erro ao salvar chamada');
    } finally {
      setIsSaving(false);
    }
  };

  const formatDateTime = dateString => {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
      weekday: 'long',
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (isLoading) {
    return (
      <div className="attendance-container">
        <div className="attendance-header">
          <h1>Chamada</h1>
        </div>
        <div className="attendance-skeleton">
          <div
            className="skeleton"
            style={{ height: '1.5rem', width: '60%', marginBottom: '1rem' }}
          ></div>
          <div
            className="skeleton"
            style={{ height: '1rem', width: '80%', marginBottom: '1.5rem' }}
          ></div>
          {[1, 2, 3, 4, 5].map(i => (
            <div key={i} className="athlete-row skeleton">
              <div
                className="skeleton"
                style={{ height: '48px', width: '48px', borderRadius: '50%' }}
              ></div>
              <div className="skeleton" style={{ height: '1.25rem', width: '70%' }}></div>
              <div
                className="skeleton"
                style={{ height: '2.5rem', width: '2.5rem', borderRadius: '8px' }}
              ></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error && !saved) {
    return (
      <div className="attendance-container">
        <div className="attendance-header">
          <h1>Chamada</h1>
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

  const presentCount = athletes.filter(a => a.present).length;

  return (
    <div className="attendance-container">
      <header className="attendance-header">
        <h1>Chamada</h1>
        <button className="btn btn-icon" onClick={() => navigate(-1)} aria-label="Voltar">
          ←
        </button>
      </header>

      {training && (
        <div className="training-info">
          <p className="training-date">{formatDateTime(training.date)}</p>
          <p className="training-location">📍 {training.location}</p>
        </div>
      )}

      <div className="attendance-summary">
        <span>
          {presentCount} de {athletes.length} presentes
        </span>
        <button className="btn btn-secondary btn-small" onClick={handleMarkAll} disabled={isSaving}>
          {athletes.every(a => a.present) ? 'Desmarcar todos' : 'Marcar todos presentes'}
        </button>
      </div>

      <ul className="athletes-list" role="list" aria-label="Lista de atletas para chamada">
        {athletes.map(athlete => (
          <li key={athlete.id} className="athlete-row">
            <div className="athlete-avatar">{athlete.name.charAt(0).toUpperCase()}</div>
            <div className="athlete-info">
              <h2>{athlete.name}</h2>
              <span className="athlete-position">{athlete.position}</span>
            </div>
            <button
              className={`presence-toggle ${athlete.present ? 'present' : 'absent'}`}
              onClick={() => handleToggle(athlete.id)}
              disabled={isSaving}
              aria-pressed={athlete.present}
              aria-label={
                athlete.present
                  ? `${athlete.name}, presente. Toque para marcar como ausente.`
                  : `${athlete.name}, ausente. Toque para marcar como presente.`
              }
            >
              <span className="toggle-icon" aria-hidden="true">
                {athlete.present ? '✓' : '✕'}
              </span>
              <span className="toggle-label">{athlete.present ? 'Presente' : 'Ausente'}</span>
            </button>
          </li>
        ))}
      </ul>

      {saved && (
        <div className="save-success" role="status" aria-live="polite">
          <div className="success-icon">✓</div>
          <h2>Chamada salva!</h2>
          <p>
            {saveResult.present} presentes, {saveResult.absent} ausentes
          </p>
          <button
            className="btn btn-primary"
            onClick={() => navigate(`/teams/${training?.id || 1}/trainings`)}
          >
            Fechar
          </button>
        </div>
      )}

      {!saved && (
        <button
          className="btn btn-primary save-btn"
          onClick={handleSave}
          disabled={isSaving}
          aria-busy={isSaving}
        >
          {isSaving ? 'Salvando...' : 'Salvar chamada'}
        </button>
      )}
    </div>
  );
}
