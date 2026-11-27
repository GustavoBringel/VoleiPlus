import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './EvaluationForm.css';

const FUNDAMENTALS = [
  { key: 'pass', label: 'Passe', icon: '🤲' },
  { key: 'serve', label: 'Saque', icon: '🏐' },
  { key: 'attack', label: 'Ataque', icon: '💥' },
  { key: 'block', label: 'Bloqueio', icon: '🛡️' },
  { key: 'defense', label: 'Defesa', icon: '🤸' },
];

export default function EvaluationForm() {
  const navigate = useNavigate();
  const { athleteId } = useParams();
  const [athlete, setAthlete] = useState(null);
  const [formData, setFormData] = useState({
    date: '',
    pass: 3,
    serve: 3,
    attack: 3,
    block: 3,
    defense: 3,
    notes: '',
  });
  const [formErrors, setFormErrors] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadAthlete = async () => {
      try {
        await new Promise(resolve => setTimeout(resolve, 300));
        setAthlete({ id: 1, name: 'Ana Silva' });
        setFormData(prev => ({ ...prev, date: new Date().toISOString().split('T')[0] }));
      } catch {
        setError('Erro ao carregar atleta');
      } finally {
        setIsLoading(false);
      }
    };
    loadAthlete();
  }, [athleteId]);

  const validateForm = () => {
    const errors = {};
    if (!formData.date) {
      errors.date = 'Data é obrigatória';
    }
    FUNDAMENTALS.forEach(f => {
      if (!formData[f.key] || formData[f.key] < 1 || formData[f.key] > 5) {
        errors[f.key] = `${f.label} deve ser entre 1 e 5`;
      }
    });
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) return;

    setIsSubmitting(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 500));
      navigate(`/athletes/${athleteId}`, { replace: true });
    } catch {
      setError('Erro ao salvar avaliação');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (key, value) => {
    setFormData(prev => ({ ...prev, [key]: value }));
    if (formErrors[key]) {
      setFormErrors(prev => ({ ...prev, [key]: '' }));
    }
  };

  const handleDateChange = e => {
    handleChange('date', e.target.value);
  };

  if (isLoading) {
    return (
      <div className="evaluation-form-container">
        <div className="form-header">
          <h1>Nova Avaliação</h1>
        </div>
        <div className="form-skeleton">
          <div
            className="skeleton"
            style={{ height: '2.5rem', width: '100%', marginBottom: '1.5rem' }}
          ></div>
          {FUNDAMENTALS.map(f => (
            <div
              key={f.key}
              className="skeleton"
              style={{ height: '5rem', width: '100%', marginBottom: '1rem' }}
            ></div>
          ))}
          <div className="skeleton" style={{ height: '5rem', width: '100%' }}></div>
        </div>
      </div>
    );
  }

  return (
    <div className="evaluation-form-container">
      <div className="form-header">
        <h1>Nova Avaliação</h1>
        {athlete && <p className="athlete-name">{athlete.name}</p>}
      </div>

      {error && (
        <div className="toast error" role="alert">
          <span className="toast-message">{error}</span>
        </div>
      )}

      <form className="evaluation-form" onSubmit={handleSubmit} noValidate>
        <div className="form-group">
          <label htmlFor="date">Data da avaliação *</label>
          <input
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleDateChange}
            max={new Date().toISOString().split('T')[0]}
            disabled={isSubmitting}
            aria-invalid={!!formErrors.date}
            aria-describedby={formErrors.date ? 'date-error' : undefined}
          />
          {formErrors.date && (
            <span id="date-error" className="form-error" role="alert">
              {formErrors.date}
            </span>
          )}
        </div>

        <fieldset className="fundamentals-fieldset">
          <legend>Fundamentos (escala 1 a 5) *</legend>
          <div className="fundamentals-grid">
            {FUNDAMENTALS.map(fundamental => (
              <div key={fundamental.key} className="fundamental-item">
                <div className="fundamental-header">
                  <span className="fundamental-icon" aria-hidden="true">
                    {fundamental.icon}
                  </span>
                  <label htmlFor={fundamental.key}>{fundamental.label}</label>
                </div>
                <div
                  className="rating-input"
                  role="radiogroup"
                  aria-label={`${fundamental.label}, nota atual ${formData[fundamental.key]}`}
                >
                  {[1, 2, 3, 4, 5].map(value => (
                    <label key={value} className="rating-label">
                      <input
                        type="radio"
                        name={fundamental.key}
                        value={value}
                        checked={formData[fundamental.key] === value}
                        onChange={() => handleChange(fundamental.key, value)}
                        disabled={isSubmitting}
                        aria-label={`${value} estrela${value > 1 ? 's' : ''}`}
                      />
                      <span className="rating-star" aria-hidden="true">
                        ★
                      </span>
                    </label>
                  ))}
                </div>
                {formErrors[fundamental.key] && (
                  <span className="form-error" role="alert">
                    {formErrors[fundamental.key]}
                  </span>
                )}
              </div>
            ))}
          </div>
        </fieldset>

        <div className="form-group">
          <label htmlFor="notes">Observações</label>
          <textarea
            id="notes"
            name="notes"
            value={formData.notes}
            onChange={e => handleChange('notes', e.target.value)}
            placeholder="Observações sobre a avaliação, pontos fortes, áreas para melhorar..."
            rows={4}
            disabled={isSubmitting}
          />
        </div>

        <div className="form-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate(-1)}
            disabled={isSubmitting}
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={isSubmitting}
            aria-busy={isSubmitting}
          >
            {isSubmitting ? 'Salvando...' : 'Salvar avaliação'}
          </button>
        </div>
      </form>
    </div>
  );
}
