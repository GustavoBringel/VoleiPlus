import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './AthleteForm.css';

const POSITIONS = ['Ponteira', 'Levantadora', 'Oposta', 'Central', 'Líbero'];

export default function AthleteForm() {
  const navigate = useNavigate();
  const { teamId, id } = useParams();
  const isEditing = !!id;

  const [formData, setFormData] = useState({
    name: '',
    birthDate: '',
    position: '',
    number: '',
  });
  const [formErrors, setFormErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isEditing) {
      const loadAthlete = async () => {
        setIsLoading(true);
        try {
          await new Promise(resolve => setTimeout(resolve, 300));
          const mockAthlete = {
            id: 1,
            name: 'Ana Silva',
            birthDate: '2009-03-15',
            position: 'Ponteira',
            number: '10',
          };
          setFormData(mockAthlete);
        } catch {
          setError('Erro ao carregar atleta');
        } finally {
          setIsLoading(false);
        }
      };
      loadAthlete();
    }
  }, [isEditing, id]);

  const calculateAge = birthDate => {
    if (!birthDate) return '';
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age;
  };

  const validateForm = () => {
    const errors = {};
    if (!formData.name.trim()) {
      errors.name = 'Nome completo é obrigatório';
    } else if (formData.name.trim().length < 3) {
      errors.name = 'Nome deve ter pelo menos 3 caracteres';
    }
    if (!formData.birthDate) {
      errors.birthDate = 'Data de nascimento é obrigatória';
    } else {
      const age = calculateAge(formData.birthDate);
      if (age < 10 || age > 80) {
        errors.birthDate = 'Idade deve estar entre 10 e 80 anos';
      }
    }
    if (!formData.position) {
      errors.position = 'Posição é obrigatória';
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
      navigate(`/teams/${teamId}/athletes`, { replace: true });
    } catch {
      setError('Erro ao salvar atleta');
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

  const age = calculateAge(formData.birthDate);

  if (isLoading) {
    return (
      <div className="athlete-form-container">
        <div className="form-header">
          <h1>{isEditing ? 'Editar Atleta' : 'Novo Atleta'}</h1>
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
          <div className="skeleton" style={{ height: '3rem', width: '100%' }}></div>
        </div>
      </div>
    );
  }

  return (
    <div className="athlete-form-container">
      <div className="form-header">
        <h1>{isEditing ? 'Editar Atleta' : 'Novo Atleta'}</h1>
      </div>

      {error && (
        <div className="toast error" role="alert">
          <span className="toast-message">{error}</span>
        </div>
      )}

      <form className="athlete-form" onSubmit={handleSubmit} noValidate>
        <div className="form-group">
          <label htmlFor="name">Nome completo *</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="João da Silva"
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
          <label htmlFor="birthDate">Data de nascimento *</label>
          <input
            type="date"
            id="birthDate"
            name="birthDate"
            value={formData.birthDate}
            onChange={handleChange}
            max={new Date().toISOString().split('T')[0]}
            disabled={isSubmitting}
            aria-invalid={!!formErrors.birthDate}
            aria-describedby={
              formErrors.birthDate ? 'birthDate-error' : age ? 'age-hint' : undefined
            }
          />
          {formErrors.birthDate && (
            <span id="birthDate-error" className="form-error" role="alert">
              {formErrors.birthDate}
            </span>
          )}
          {age && !formErrors.birthDate && (
            <span id="age-hint" className="form-hint">
              Idade: {age} anos
            </span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="position">Posição *</label>
          <select
            id="position"
            name="position"
            value={formData.position}
            onChange={handleChange}
            disabled={isSubmitting}
            aria-invalid={!!formErrors.position}
            aria-describedby={formErrors.position ? 'position-error' : undefined}
          >
            <option value="">Selecione a posição</option>
            {POSITIONS.map(pos => (
              <option key={pos} value={pos}>
                {pos}
              </option>
            ))}
          </select>
          {formErrors.position && (
            <span id="position-error" className="form-error" role="alert">
              {formErrors.position}
            </span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="number">Número da camisa</label>
          <input
            type="number"
            id="number"
            name="number"
            value={formData.number}
            onChange={handleChange}
            placeholder="Ex: 10"
            min="1"
            max="99"
            disabled={isSubmitting}
          />
          <span className="form-hint">Opcional</span>
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
            {isSubmitting ? 'Salvando...' : isEditing ? 'Atualizar' : 'Cadastrar atleta'}
          </button>
        </div>
      </form>
    </div>
  );
}
