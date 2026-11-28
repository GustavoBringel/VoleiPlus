import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './TeamForm.css';

const CATEGORIES = ['Sub-13', 'Sub-15', 'Sub-17', 'Adulto', 'Misto'];

export default function TeamForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditing = !!id;

  const [formData, setFormData] = useState({
    name: '',
    category: '',
    description: '',
  });
  const [formErrors, setFormErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  // Carrega dados se estiver editando
  useEffect(() => {
    if (isEditing) {
      const loadTeam = async () => {
        setIsLoading(true);
        try {
          // Simula API call
          await new Promise(resolve => setTimeout(resolve, 300));
          const mockTeam = {
            id: 1,
            name: 'Falcões',
            category: 'Sub-17',
            description: 'Equipe de vôlei feminino sub-17',
          };
          setFormData(mockTeam);
        } catch {
          setError('Erro ao carregar equipe');
        } finally {
          setIsLoading(false);
        }
      };
      loadTeam();
    }
  }, [isEditing, id]);

  const validateForm = () => {
    const errors = {};
    if (!formData.name.trim()) {
      errors.name = 'Nome da equipe é obrigatório';
    } else if (formData.name.trim().length < 2) {
      errors.name = 'Nome deve ter pelo menos 2 caracteres';
    }
    if (!formData.category) {
      errors.category = 'Categoria é obrigatória';
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
      // Simula API call
      await new Promise(resolve => setTimeout(resolve, 500));
      navigate('/teams', { replace: true });
    } catch (err) {
      setError(err.message || 'Erro ao salvar equipe');
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
      <div className="team-form-container">
        <div className="form-header">
          <h1>{isEditing ? 'Editar Equipe' : 'Nova Equipe'}</h1>
        </div>
        <div className="form-skeleton">
          <div
            className="skeleton"
            style={{ height: '2.5rem', width: '100%', marginBottom: '1.5rem' }}
          ></div>
          <div
            className="skeleton"
            style={{ height: '2.5rem', width: '100%', marginBottom: '1.5rem' }}
          ></div>
          <div
            className="skeleton"
            style={{ height: '2.5rem', width: '100%', marginBottom: '1.5rem' }}
          ></div>
          <div
            className="skeleton"
            style={{ height: '2.5rem', width: '100%', marginBottom: '1.5rem' }}
          ></div>
          <div
            className="skeleton"
            style={{ height: '3rem', width: '100%', marginBottom: '1.5rem' }}
          ></div>
          <div className="skeleton" style={{ height: '3rem', width: '100%' }}></div>
        </div>
      </div>
    );
  }

  return (
    <div className="team-form-container">
      <div className="form-header">
        <h1>{isEditing ? 'Editar Equipe' : 'Nova Equipe'}</h1>
      </div>

      {error && (
        <div className="toast error" role="alert">
          <span className="toast-message">{error}</span>
        </div>
      )}

      <form className="team-form" onSubmit={handleSubmit} noValidate>
        <div className="form-group">
          <label htmlFor="name">Nome da equipe *</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Ex: Falcões Vôlei"
            disabled={isSubmitting}
            aria-invalid={!!formErrors.name}
            aria-describedby={formErrors.name ? 'name-error' : undefined}
            autoFocus
          />
          {formErrors.name && (
            <span id="name-error" className="form-error" role="alert">
              {formErrors.name}
            </span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="category">Categoria *</label>
          <select
            id="category"
            name="category"
            value={formData.category}
            onChange={handleChange}
            disabled={isSubmitting}
            aria-invalid={!!formErrors.category}
            aria-describedby={formErrors.category ? 'category-error' : undefined}
          >
            <option value="">Selecione a categoria</option>
            {CATEGORIES.map(cat => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
          {formErrors.category && (
            <span id="category-error" className="form-error" role="alert">
              {formErrors.category}
            </span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="description">Descrição</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Informações adicionais sobre a equipe..."
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
            {isSubmitting ? 'Salvando...' : isEditing ? 'Atualizar' : 'Criar equipe'}
          </button>
        </div>
      </form>
    </div>
  );
}
