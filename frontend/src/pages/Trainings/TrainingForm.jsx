import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './TrainingForm.css';

export default function TrainingForm() {
  const navigate = useNavigate();
  const { teamId, id } = useParams();
  const isEditing = !!id;

  const today = new Date().toISOString().split('T')[0];

  const [formData, setFormData] = useState({
    date: today,
    startTime: '',
    endTime: '',
    location: '',
    notes: '',
  });
  const [formErrors, setFormErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isEditing) {
      const loadTraining = async () => {
        setIsLoading(true);
        try {
          await new Promise(resolve => setTimeout(resolve, 300));
          const mockTraining = {
            id: 1,
            date: '2026-03-15',
            startTime: '19:00',
            endTime: '21:00',
            location: 'Quadra 2',
            notes: 'Foco em passe e saque',
          };
          setFormData(mockTraining);
        } catch {
          setError('Erro ao carregar treino');
        } finally {
          setIsLoading(false);
        }
      };
      loadTraining();
    }
  }, [isEditing, id]);

  const validateForm = () => {
    const errors = {};
    if (!formData.date) {
      errors.date = 'Data é obrigatória';
    }
    if (!formData.startTime) {
      errors.startTime = 'Horário de início é obrigatório';
    }
    if (!formData.endTime) {
      errors.endTime = 'Horário de fim é obrigatório';
    } else if (formData.startTime && formData.endTime <= formData.startTime) {
      errors.endTime = 'Horário de fim deve ser posterior ao início';
    }
    if (!formData.location.trim()) {
      errors.location = 'Local é obrigatório';
    }
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
      navigate(`/teams/${teamId}/trainings`, { replace: true });
    } catch (err) {
      setError(err.message || 'Erro ao salvar treino');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (formErrors[name]) {
      setFormErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  if (isLoading) {
    return (
      <div className="training-form-container">
        <div className="form-header">
          <h1>{isEditing ? 'Editar Treino' : 'Novo Treino'}</h1>
        </div>
        <div className="form-skeleton">
          <div
            className="skeleton"
            style={{ height: '2.5rem', width: '100%', marginBottom: '1.5rem' }}
          ></div>
          <div
            className="skeleton"
            style={{ height: '2.5rem', width: '48%', marginBottom: '1.5rem' }}
          ></div>
          <div
            className="skeleton"
            style={{ height: '2.5rem', width: '48%', marginBottom: '1.5rem' }}
          ></div>
          <div
            className="skeleton"
            style={{ height: '2.5rem', width: '100%', marginBottom: '1.5rem' }}
          ></div>
          <div className="skeleton" style={{ height: '5rem', width: '100%' }}></div>
        </div>
      </div>
    );
  }

  return (
    <div className="training-form-container">
      <div className="form-header">
        <h1>{isEditing ? 'Editar Treino' : 'Novo Treino'}</h1>
      </div>

      {error && (
        <div className="toast error" role="alert">
          <span className="toast-message">{error}</span>
        </div>
      )}

      <form className="training-form" onSubmit={handleSubmit} noValidate>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="date">Data *</label>
            <input
              type="date"
              id="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              min={new Date().toISOString().split('T')[0]}
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

          <div className="form-group">
            <label htmlFor="startTime">Início *</label>
            <input
              type="time"
              id="startTime"
              name="startTime"
              value={formData.startTime}
              onChange={handleChange}
              disabled={isSubmitting}
              aria-invalid={!!formErrors.startTime}
              aria-describedby={formErrors.startTime ? 'startTime-error' : undefined}
            />
            {formErrors.startTime && (
              <span id="startTime-error" className="form-error" role="alert">
                {formErrors.startTime}
              </span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="endTime">Fim *</label>
            <input
              type="time"
              id="endTime"
              name="endTime"
              value={formData.endTime}
              onChange={handleChange}
              disabled={isSubmitting}
              aria-invalid={!!formErrors.endTime}
              aria-describedby={formErrors.endTime ? 'endTime-error' : undefined}
            />
            {formErrors.endTime && (
              <span id="endTime-error" className="form-error" role="alert">
                {formErrors.endTime}
              </span>
            )}
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="location">Local *</label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleChange}
            placeholder="Ex: Quadra 2, Ginásio Municipal"
            disabled={isSubmitting}
            aria-invalid={!!formErrors.location}
            aria-describedby={formErrors.location ? 'location-error' : undefined}
          />
          {formErrors.location && (
            <span id="location-error" className="form-error" role="alert">
              {formErrors.location}
            </span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="notes">Observações</label>
          <textarea
            id="notes"
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            placeholder="Detalhes do treino, foco, materiais necessários..."
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
            {isSubmitting ? 'Salvando...' : isEditing ? 'Atualizar' : 'Criar treino'}
          </button>
        </div>
      </form>
    </div>
  );
}
