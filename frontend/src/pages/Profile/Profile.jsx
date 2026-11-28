import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import './Profile.css';

const FUNDAMENTALS = [
  { key: 'pass', label: 'Passe', color: '#1a1a2e' },
  { key: 'serve', label: 'Saque', color: '#2d2d4a' },
  { key: 'attack', label: 'Ataque', color: '#3d3d5a' },
  { key: 'block', label: 'Bloqueio', color: '#4d4d6a' },
  { key: 'defense', label: 'Defesa', color: '#5d5d7a' },
];

export default function Profile() {
  const { athleteId } = useParams();
  const [athlete, setAthlete] = useState(null);
  const [evaluations, setEvaluations] = useState([]);
  const [attendance, setAttendance] = useState({ present: 0, total: 0 });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        await new Promise(resolve => setTimeout(resolve, 500));
        setAthlete({
          id: 1,
          name: 'Ana Silva',
          position: 'Ponteira',
          age: 16,
          number: 10,
          active: true,
        });
        setEvaluations([
          {
            id: 1,
            date: '2026-03-15',
            pass: 4,
            serve: 3,
            attack: 4,
            block: 2,
            defense: 4,
            notes: 'Melhorou no passe',
          },
          {
            id: 2,
            date: '2026-03-01',
            pass: 3,
            serve: 3,
            attack: 3,
            block: 2,
            defense: 3,
            notes: '',
          },
          {
            id: 3,
            date: '2026-02-15',
            pass: 3,
            serve: 2,
            attack: 3,
            block: 2,
            defense: 3,
            notes: '',
          },
        ]);
        setAttendance({ present: 17, total: 20 });
      } catch {
        setError('Erro ao carregar perfil');
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, [athleteId]);

  const attendancePercent =
    attendance.total > 0 ? Math.round((attendance.present / attendance.total) * 100) : 0;

  const latestEvaluation = evaluations[0];

  if (isLoading) {
    return (
      <div className="profile-container">
        <div className="profile-skeleton">
          <div className="skeleton" style={{ height: '120px', width: '100%' }}></div>
          <div
            className="skeleton"
            style={{ height: '100px', width: '100%', marginTop: '1rem' }}
          ></div>
          <div
            className="skeleton"
            style={{ height: '200px', width: '100%', marginTop: '1rem' }}
          ></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="profile-container">
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
    <div className="profile-container">
      <header className="profile-header">
        <div className="athlete-info">
          <div className="athlete-avatar-large">{athlete.name.charAt(0).toUpperCase()}</div>
          <div className="athlete-details">
            <h1>{athlete.name}</h1>
            <div className="athlete-meta">
              <span className="position">{athlete.position}</span>
              <span className="age">{athlete.age} anos</span>
              {athlete.number && <span className="number">Camisa {athlete.number}</span>}
              <span className={`status ${athlete.active ? 'active' : 'inactive'}`}>
                {athlete.active ? 'Ativo' : 'Inativo'}
              </span>
            </div>
          </div>
        </div>
        <div className="profile-actions">
          <Link to={`/athletes/${athleteId}/evaluation/new`} className="btn btn-primary">
            Nova Avaliação
          </Link>
          <Link to={`/teams/1/athletes/${athleteId}/edit`} className="btn btn-secondary">
            Editar
          </Link>
        </div>
      </header>

      <nav className="profile-tabs" role="tablist" aria-label="Abas do perfil">
        <button
          role="tab"
          aria-selected={activeTab === 'overview'}
          aria-controls="overview-panel"
          className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Visão Geral
        </button>
        <button
          role="tab"
          aria-selected={activeTab === 'evaluations'}
          aria-controls="evaluations-panel"
          className={`tab-btn ${activeTab === 'evaluations' ? 'active' : ''}`}
          onClick={() => setActiveTab('evaluations')}
        >
          Avaliações
        </button>
        <button
          role="tab"
          aria-selected={activeTab === 'evolution'}
          aria-controls="evolution-panel"
          className={`tab-btn ${activeTab === 'evolution' ? 'active' : ''}`}
          onClick={() => setActiveTab('evolution')}
        >
          Evolução
        </button>
      </nav>

      <div className="profile-content">
        {activeTab === 'overview' && (
          <div id="overview-panel" role="tabpanel" className="tab-panel">
            <div className="stats-grid">
              <article className="stat-card">
                <div className="stat-icon">📊</div>
                <div className="stat-content">
                  <span className="stat-value-large">{attendancePercent}%</span>
                  <span className="stat-label">Presença</span>
                  <span className="stat-detail">
                    {attendance.present} de {attendance.total} treinos
                  </span>
                </div>
              </article>
              {latestEvaluation && (
                <article className="stat-card">
                  <div className="stat-icon">⭐</div>
                  <div className="stat-content">
                    <span className="stat-value-large">
                      {(
                        Object.keys(latestEvaluation)
                          .filter(k => FUNDAMENTALS.some(f => f.key === k))
                          .reduce((sum, key) => sum + latestEvaluation[key], 0) / 5
                      ).toFixed(1)}
                    </span>
                    <span className="stat-label">Média última avaliação</span>
                    <span className="stat-detail">
                      {new Date(latestEvaluation.date).toLocaleDateString('pt-BR')}
                    </span>
                  </div>
                </article>
              )}
              <article className="stat-card">
                <div className="stat-icon">📝</div>
                <div className="stat-content">
                  <span className="stat-value-large">{evaluations.length}</span>
                  <span className="stat-label">Avaliações</span>
                  <span className="stat-detail">Total registrado</span>
                </div>
              </article>
            </div>

            {latestEvaluation && (
              <section className="latest-evaluation">
                <h2>Última Avaliação</h2>
                <div className="evaluation-summary">
                  <p className="evaluation-date">
                    {new Date(latestEvaluation.date).toLocaleDateString('pt-BR', {
                      weekday: 'long',
                      day: '2-digit',
                      month: 'long',
                    })}
                  </p>
                  <div className="fundamentals-mini">
                    {FUNDAMENTALS.map(f => (
                      <div key={f.key} className="fundamental-mini">
                        <span className="fundamental-label">{f.label}</span>
                        <div className="stars">
                          {[1, 2, 3, 4, 5].map(v => (
                            <span key={v} className={v <= latestEvaluation[f.key] ? 'filled' : ''}>
                              ★
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                  {latestEvaluation.notes && (
                    <p className="evaluation-notes">{latestEvaluation.notes}</p>
                  )}
                </div>
                <Link
                  to={`/athletes/${athleteId}/evaluation/${latestEvaluation.id}`}
                  className="btn btn-secondary btn-full"
                >
                  Ver detalhes
                </Link>
              </section>
            )}

            {evaluations.length === 0 && (
              <div className="empty-state-inline">
                <p>Nenhuma avaliação registrada ainda.</p>
                <Link to={`/athletes/${athleteId}/evaluation/new`} className="btn btn-primary">
                  Criar primeira avaliação
                </Link>
              </div>
            )}
          </div>
        )}

        {activeTab === 'evaluations' && (
          <div id="evaluations-panel" role="tabpanel" className="tab-panel">
            {evaluations.length === 0 ? (
              <div className="empty-state-inline">
                <p>Nenhuma avaliação registrada.</p>
                <Link to={`/athletes/${athleteId}/evaluation/new`} className="btn btn-primary">
                  Criar primeira avaliação
                </Link>
              </div>
            ) : (
              <ul className="evaluations-list">
                {evaluations.map(evaluation => (
                  <li key={evaluation.id} className="evaluation-item">
                    <div className="evaluation-header">
                      <span className="evaluation-date">
                        {new Date(evaluation.date).toLocaleDateString('pt-BR', {
                          weekday: 'short',
                          day: '2-digit',
                          month: 'short',
                        })}
                      </span>
                      <span className="evaluation-average">
                        Média:{' '}
                        {(
                          Object.keys(evaluation)
                            .filter(k => FUNDAMENTALS.some(f => f.key === k))
                            .reduce((sum, k) => sum + evaluation[k], 0) / 5
                        ).toFixed(1)}
                      </span>
                    </div>
                    <div className="fundamentals-mini">
                      {FUNDAMENTALS.map(f => (
                        <div key={f.key} className="fundamental-mini">
                          <span className="fundamental-label">{f.label.charAt(0)}</span>
                          <div className="stars">
                            {[1, 2, 3, 4, 5].map(v => (
                              <span key={v} className={v <= evaluation[f.key] ? 'filled' : ''}>
                                ★
                              </span>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                    {evaluation.notes && <p className="evaluation-notes">{evaluation.notes}</p>}
                    <Link
                      to={`/athletes/${athleteId}/evaluation/${evaluation.id}`}
                      className="btn btn-secondary btn-small"
                    >
                      Ver
                    </Link>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}

        {activeTab === 'evolution' && (
          <div id="evolution-panel" role="tabpanel" className="tab-panel">
            {evaluations.length < 2 ? (
              <div className="empty-state-inline">
                <div className="empty-icon-large">📈</div>
                <h3>Dados insuficientes</h3>
                <p>São necessárias pelo menos 2 avaliações para exibir os gráficos de evolução.</p>
                <Link to={`/athletes/${athleteId}/evaluation/new`} className="btn btn-primary">
                  Nova Avaliação
                </Link>
              </div>
            ) : (
              <div className="evolution-charts">
                {FUNDAMENTALS.map(f => (
                  <div key={f.key} className="chart-card">
                    <h3>{f.label}</h3>
                    <SimpleLineChart
                      data={evaluations
                        .map(e => ({
                          date: e.date,
                          value: e[f.key],
                        }))
                        .reverse()}
                      color={f.color}
                    />
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function SimpleLineChart({ data, color }) {
  const points = data
    .map((d, i) => {
      const x = (i / (data.length - 1)) * 100;
      const y = 100 - ((d.value - 1) / 4) * 80; // 1-5 scale to 80% height with 10% margin
      return `${x}% ${y}%`;
    })
    .join(', ');

  const path = `M${points
    .split(', ')
    .map((p, i) => (i === 0 ? p : `L${p}`))
    .join(' ')}`;

  return (
    <svg
      className="chart-svg"
      viewBox="0 0 100 100"
      preserveAspectRatio="none"
      aria-label={`Gráfico de evolução, ${data.length} pontos`}
    >
      <defs>
        <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor={color} stopOpacity="0.3" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>
      {/* Grid lines */}
      <g className="chart-grid" stroke="#e0e0e0" strokeWidth="0.5">
        {[20, 40, 60, 80].map(y => (
          <line key={y} x1="0" y1={y} x2="100" y2={y} />
        ))}
      </g>
      {/* Area */}
      <path d={`${path} L100 100 L0 100 Z`} fill="url(#gradient)" />
      {/* Line */}
      <path
        d={path}
        stroke={color}
        strokeWidth="2"
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Points */}
      <g>
        {data.map((d, i) => {
          const x = (i / (data.length - 1)) * 100;
          const y = 100 - ((d.value - 1) / 4) * 80;
          return (
            <circle
              key={i}
              cx={x + '%'}
              cy={y + '%'}
              r="3"
              fill={color}
              stroke="white"
              strokeWidth="2"
            />
          );
        })}
      </g>
      {/* Labels */}
      <g className="chart-labels" fontSize="8" fill="#666" textAnchor="middle">
        {data.map((d, i) => (
          <text key={i} x={(i / (data.length - 1)) * 100 + '%'} y="98" dominantBaseline="hanging">
            {new Date(d.date).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })}
          </text>
        ))}
      </g>
    </svg>
  );
}
