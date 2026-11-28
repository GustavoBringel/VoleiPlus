/**
 * Módulo único para chamadas à API.
 * A URL base vem da variável de ambiente VITE_API_URL.
 */

const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1').replace(
  /\/$/,
  ''
);

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
  const { headers: optionHeaders, ...requestOptions } = options;

  const config = {
    ...requestOptions,
    headers: {
      'Content-Type': 'application/json',
      ...optionHeaders,
    },
  };

  // Adiciona token de autenticação se existir
  const token = globalThis.localStorage?.getItem('auth_token');
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
    const detail = data.detail;
    const message = Array.isArray(detail)
      ? detail.map(issue => `${issue.loc?.slice(1).join('.')}: ${issue.msg}`).join('; ')
      : typeof detail === 'string'
        ? detail
        : data.message || `Erro ${response.status}`;
    throw new ApiError(message, response.status, data);
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
    list: (teamId, { activeOnly = true, search } = {}) => {
      const params = new URLSearchParams();
      if (teamId != null) params.set('team_id', teamId);
      params.set('active_only', activeOnly);
      if (search) params.set('search', search);
      return request(`/athletes?${params.toString()}`);
    },
    get: id => request(`/athletes/${id}`),
    create: (teamId, athleteData) =>
      request('/athletes', {
        method: 'POST',
        body: JSON.stringify({ ...athleteData, team_id: teamId }),
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
    list: teamId =>
      request(`/trainings${teamId == null ? '' : `?team_id=${encodeURIComponent(teamId)}`}`),
    get: id => request(`/trainings/${id}`),
    create: (teamId, trainingData) =>
      request('/trainings', {
        method: 'POST',
        body: JSON.stringify({ ...trainingData, team_id: teamId }),
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
      request('/attendances', {
        method: 'POST',
        body: JSON.stringify({ ...attendanceData, training_id: trainingId }),
      }),
    registerBulk: (trainingId, attendances) =>
      request('/attendances/bulk', {
        method: 'POST',
        body: JSON.stringify({ training_id: trainingId, attendances }),
      }),
    get: trainingId => request(`/attendances/training/${trainingId}`),
    update: (trainingId, athleteId, attendanceData) =>
      request(`/attendances/${trainingId}/athletes/${athleteId}`, {
        method: 'PUT',
        body: JSON.stringify(attendanceData),
      }),
    stats: athleteId => request(`/attendances/athlete/${athleteId}/stats`),
  },

  // Avaliações
  evaluations: {
    list: athleteId => request(`/evaluations/athlete/${athleteId}`),
    create: (athleteId, evaluationData) =>
      request('/evaluations', {
        method: 'POST',
        body: JSON.stringify({ ...evaluationData, athlete_id: athleteId }),
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
    evolution: athleteId => request(`/evaluations/athlete/${athleteId}/evolution`),
  },
};

export { ApiError };
export default api;
