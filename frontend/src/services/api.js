/**
 * Módulo único para chamadas à API.
 * A URL base vem da variável de ambiente VITE_API_URL.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api';

class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;

  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Adiciona token de autenticação se existir
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(url, config);

  // Trata respostas sem conteúdo (ex: 204 No Content)
  if (response.status === 204) {
    return null;
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new ApiError(data.message || `Erro ${response.status}`, response.status, data);
  }

  return data;
}

export const api = {
  // Autenticação
  auth: {
    register: userData =>
      request('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData),
      }),
    login: credentials =>
      request('/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      }),
    logout: () => request('/auth/logout', { method: 'POST' }),
    me: () => request('/auth/me'),
  },

  // Equipes
  teams: {
    list: () => request('/teams'),
    get: id => request(`/teams/${id}`),
    create: teamData =>
      request('/teams', {
        method: 'POST',
        body: JSON.stringify(teamData),
      }),
    update: (id, teamData) =>
      request(`/teams/${id}`, {
        method: 'PUT',
        body: JSON.stringify(teamData),
      }),
    delete: id => request(`/teams/${id}`, { method: 'DELETE' }),
  },

  // Atletas
  athletes: {
    list: teamId => request(`/teams/${teamId}/athletes`),
    get: id => request(`/athletes/${id}`),
    create: (teamId, athleteData) =>
      request(`/teams/${teamId}/athletes`, {
        method: 'POST',
        body: JSON.stringify(athleteData),
      }),
    update: (id, athleteData) =>
      request(`/athletes/${id}`, {
        method: 'PUT',
        body: JSON.stringify(athleteData),
      }),
    deactivate: id => request(`/athletes/${id}`, { method: 'DELETE' }),
  },

  // Treinos
  trainings: {
    list: teamId => request(`/teams/${teamId}/trainings`),
    get: id => request(`/trainings/${id}`),
    create: (teamId, trainingData) =>
      request(`/teams/${teamId}/trainings`, {
        method: 'POST',
        body: JSON.stringify(trainingData),
      }),
    update: (id, trainingData) =>
      request(`/trainings/${id}`, {
        method: 'PUT',
        body: JSON.stringify(trainingData),
      }),
    delete: id => request(`/trainings/${id}`, { method: 'DELETE' }),
  },

  // Presença
  attendance: {
    register: (trainingId, attendanceData) =>
      request(`/trainings/${trainingId}/attendance`, {
        method: 'POST',
        body: JSON.stringify(attendanceData),
      }),
    get: trainingId => request(`/trainings/${trainingId}/attendance`),
    update: (trainingId, attendanceData) =>
      request(`/trainings/${trainingId}/attendance`, {
        method: 'PUT',
        body: JSON.stringify(attendanceData),
      }),
  },

  // Avaliações
  evaluations: {
    list: athleteId => request(`/athletes/${athleteId}/evaluations`),
    create: (athleteId, evaluationData) =>
      request(`/athletes/${athleteId}/evaluations`, {
        method: 'POST',
        body: JSON.stringify(evaluationData),
      }),
    update: (id, evaluationData) =>
      request(`/evaluations/${id}`, {
        method: 'PUT',
        body: JSON.stringify(evaluationData),
      }),
    delete: id => request(`/evaluations/${id}`, { method: 'DELETE' }),
  },

  // Perfil e evolução do atleta
  profile: {
    get: athleteId => request(`/athletes/${athleteId}/profile`),
    evolution: athleteId => request(`/athletes/${athleteId}/evolution`),
  },
};

export { ApiError };
export default api;
