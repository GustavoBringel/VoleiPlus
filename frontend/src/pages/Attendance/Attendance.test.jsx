import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { describe, expect, it } from 'vitest';
import Attendance from './Attendance';

describe('attendance flow', () => {
  it('marks the whole team present and confirms the saved call', async () => {
    const user = userEvent.setup();

    render(
      <MemoryRouter initialEntries={['/trainings/1/attendance']}>
        <Routes>
          <Route path="/trainings/:trainingId/attendance" element={<Attendance />} />
        </Routes>
      </MemoryRouter>
    );

    await user.click(await screen.findByRole('button', { name: 'Marcar todos presentes' }));
    expect(screen.getByText('6 de 6 presentes')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Salvar chamada' }));
    expect(await screen.findByRole('heading', { name: 'Chamada salva!' })).toBeInTheDocument();
    expect(screen.getByText('6 presentes, 0 ausentes')).toBeInTheDocument();
  });
});
