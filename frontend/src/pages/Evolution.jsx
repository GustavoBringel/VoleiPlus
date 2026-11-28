import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Evolution.css';

const FUNDAMENTALS = [
  { key: 'pass', label: 'Passe', color: '#1a1a2e' },
  { key: 'serve', label: 'Saque', color: '#2d2d4a' },
  { key: 'attack', label: 'Ataque', color: '#3d3d5a' },
  { key: 'block', label: 'Bloqueio', color: '#4d4d6a' },
  { key: 'defense', label: 'Defesa', color: '#5d5d7a' },
];

export default function Evolution() {
  const [athletes, setAthletes] = useState([]);
  const [selectedAthlete, setSelectedAthlete] = useState(null);
  const [evaluations, setEvaluations] = useState([]);
  const [period, setPeriod] = useState('90d');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        await new Promise(resolve => setTimeout(resolve, 500));
        const mockAthletes = [
          { id: 1, name: 'Ana Silva', team: 'Falcões' },
          { id: 2, name: 'Bruno Costa', team: 'Falcões' },
          { id: 3, name: 'Carla Dias', team: 'Águias' },
        ];
        setAthletes(mockAthletes);
        setSelectedAthlete(mockAthletes[0]);
      } catch {
        setError('Erro ao carregar atletas');
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, []);

  useEffect(() => {
    if (!selectedAthlete) return;
    const loadEvaluations = async () => {
      try {
        await new Promise(resolve => setTimeout(resolve, 300));
        // Mock evaluations based on period
        const mockEvaluations = [
          { date: '2026-01-15', pass: 3, serve: 2, attack: 3, block: 2, defense: 3 },
          { date: '2026-02-01', pass: 3, serve: 3, attack: 3, block: 2, defense: 3 },
          { date: '2026-02-15', pass: 4, serve: 3, attack: 4, block: 2, defense: 3 },
          { date: '2026-03-01', pass: 4, serve: 3, attack: 4, block: 3, defense: 4 },
          { date: '2026-03-15', pass: 4, serve: 3, attack: 4, block: 3, defense: 4 },
        ];
        setEvaluations(mockEvaluations);
      } catch {
        console.error('Erro ao carregar avaliações');
      }
    };
    loadEvaluations();
  }, [selectedAthlete, period]);

  if (isLoading) {
    return (
      <div className="evolution-container">
        <header className="evolution-header">
          <h1>Evolução</h1>
        </header>
        <div className="evolution-skeleton">
          <div
            className="skeleton"
            style={{ height: '50px', width: '100%', marginBottom: '1rem' }}
          ></div>
          <div
            className="skeleton"
            style={{ height: '200px', width: '100%', marginBottom: '1rem' }}
          ></div>
          {FUNDAMENTALS.map(f => (
            <div
              key={f.key}
              className="skeleton"
              style={{ height: '200px', width: '100%', marginBottom: '1rem' }}
            ></div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="evolution-container">
        <header className="evolution-header">
          <h1>Evolução</h1>
        </header>
        <div className="error-state">
          <p>{error}</p>
          <button className="btn btn-primary" onClick={() => window.location.reload()}>
            Tentar novamente
          </button>
        </div>
      </div>
    );
  }

  if (!selectedAthlete || evaluations.length === 0) {
    return (
      <div className="evolution-container">
        <header className="evolution-header">
          <h1>Evolução</h1>
        </header>
        <div className="empty-state">
          <div className="empty-icon">📈</div>
          <h2>Selecione um atleta</h2>
          <p>Escolha um atleta na lista para ver sua evolução.</p>
        </div>
      </div>
    );
  }

  if (evaluations.length < 2) {
    return (
      <div className="evolution-container">
        <header className="evolution-header">
          <h1>Evolução</h1>
        </header>
        <div className="athlete-selector">
          <label htmlFor="athlete-select">Atleta</label>
          <select
            id="athlete-select"
            value={selectedAthlete.id}
            onChange={e => setSelectedAthlete(athletes.find(a => a.id === Number(e.target.value)))}
          >
            {athletes.map(a => (
              <option key={a.id} value={a.id}>
                {a.name} ({a.team})
              </option>
            ))}
          </select>
        </div>
        <div className="empty-state">
          <div className="empty-icon">📈</div>
          <h3>Dados insuficientes</h3>
          <p>São necessárias pelo menos 2 avaliações para exibir os gráficos de evolução.</p>
          <Link to={`/athletes/${selectedAthlete.id}/evaluation/new`} className="btn btn-primary">
            Nova Avaliação
          </Link>
        </div>
      </div>
    );
  }

  const getAverage = (evals, key) => {
    if (!evals.length) return 0;
    const sum = evals.reduce((acc, e) => acc + (e[key] || 0), 0);
    return (sum / evals.length).toFixed(1);
  };

  return (
    <div className="evolution-container">
      <header className="evolution-header">
        <h1>Evolução</h1>
      </header>

      <div className="athlete-selector">
        <label htmlFor="athlete-select">Atleta</label>
        <select
          id="athlete-select"
          value={selectedAthlete.id}
          onChange={e => setSelectedAthlete(athletes.find(a => a.id === Number(e.target.value)))}
        >
          {athletes.map(a => (
            <option key={a.id} value={a.id}>
              {a.name} ({a.team})
            </option>
          ))}
        </select>
      </div>

      <div className="period-selector">
        <label htmlFor="period-select">Período</label>
        <select id="period-select" value={period} onChange={e => setPeriod(e.target.value)}>
          <option value="30d">Últimos 30 dias</option>
          <option value="90d">Últimos 90 dias</option>
          <option value="1y">Último ano</option>
        </select>
      </div>

      <div className="averages-summary">
        {FUNDAMENTALS.map(f => (
          <div key={f.key} className="average-card">
            <span className="average-label">{f.label}</span>
            <span className="average-value">{getAverage(evaluations, f.key)}</span>
          </div>
        ))}
      </div>

      <div className="charts-grid">
        {FUNDAMENTALS.map(f => (
          <div key={f.key} className="chart-card">
            <h3>{f.label}</h3>
            <SimpleLineChart
              data={evaluations.map(e => ({
                date: e.date,
                value: e[f.key],
              }))}
              color={f.color}
            />
          </div>
        ))}
      </div>
    </div>
  );
}

function SimpleLineChart({ data, color }) {
  if (!data.length) return null;

  const points = data
    .map((d, i) => {
      const x = (i / Math.max(data.length - 1, 1)) * 100;
      const y = 100 - ((d.value - 1) / 4) * 80;
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
      aria-label={`Gráfico de ${data.length} avaliações`}
    >
      <defs>
        <linearGradient id={`gradient-${color}`} x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor={color} stopOpacity="0.3" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>
      <g className="chart-grid" stroke="#e0e0e0" strokeWidth="0.5">
        {[20, 40, 60, 80].map(y => (
          <line key={y} x1="0" y1={y} x2="100" y2={y} />
        ))}
      </g>
      <path d={`${path} L100 100 L0 100 Z`} fill={`url(#gradient-${color})`} />
      <path
        d={path}
        stroke={color}
        strokeWidth="2"
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <g>
        {data.map((d, i) => {
          const x = (i / Math.max(data.length - 1, 1)) * 100;
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
      <g className="chart-labels" fontSize="8" fill="#666" textAnchor="middle">
        {data.map((d, i) => (
          <text
            key={i}
            x={(i / Math.max(data.length - 1, 1)) * 100 + '%'}
            y="98"
            dominantBaseline="hanging"
          >
            {new Date(d.date).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })}
          </text>
        ))}
      </g>
    </svg>
  );
}
