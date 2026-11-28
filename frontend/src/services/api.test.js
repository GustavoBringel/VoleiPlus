import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { ApiError, api } from './api';

const jsonResponse = (body, status = 200) => ({
  ok: status >= 200 && status < 300,
  status,
  json: async () => body,
});

describe('API client', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.stubGlobal('fetch', vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('uses the backend v1 URL and sends JSON credentials to login', async () => {
    fetch.mockResolvedValue(jsonResponse({ access_token: 'jwt', token_type: 'bearer' }));

    await api.auth.login({ email: 'coach@example.com', password: 'password123' });

    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/auth/login',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ email: 'coach@example.com', password: 'password123' }),
      })
    );
  });

  it('uses the backend bulk attendance route and includes the bearer token', async () => {
    localStorage.setItem('auth_token', 'jwt');
    fetch.mockResolvedValue(jsonResponse({ training_id: 8, saved: 2, updated: 0 }));

    await api.attendance.registerBulk(8, [
      { training_id: 8, athlete_id: 3, present: true },
      { training_id: 8, athlete_id: 4, present: false },
    ]);

    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/attendances/bulk',
      expect.objectContaining({
        headers: expect.objectContaining({ Authorization: 'Bearer jwt' }),
        body: expect.stringContaining('"training_id":8'),
      })
    );
  });

  it('turns FastAPI validation details into a readable API error', async () => {
    fetch.mockResolvedValue(
      jsonResponse(
        {
          detail: [
            { loc: ['body', 'email'], msg: 'value is not a valid email', type: 'value_error' },
          ],
        },
        422
      )
    );

    await expect(api.auth.me()).rejects.toMatchObject({
      name: 'ApiError',
      status: 422,
      message: 'email: value is not a valid email',
    });
    await expect(api.auth.me()).rejects.toBeInstanceOf(ApiError);
  });
});
