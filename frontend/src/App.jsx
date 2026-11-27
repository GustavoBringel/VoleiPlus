import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/layout/ProtectedRoute';
import MainLayout from './components/layout/MainLayout';
import AuthLayout from './components/layout/AuthLayout';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import Dashboard from './pages/Dashboard';
import TeamsList from './pages/Teams/TeamsList';
import TeamForm from './pages/Teams/TeamForm';
import AthletesList from './pages/Athletes/AthletesList';
import AthleteForm from './pages/Athletes/AthleteForm';
import TrainingsList from './pages/Trainings/TrainingsList';
import TrainingForm from './pages/Trainings/TrainingForm';
import Attendance from './pages/Attendance/Attendance';
import EvaluationForm from './pages/Evaluations/EvaluationForm';
import Profile from './pages/Profile/Profile';
import Settings from './pages/Settings';
import Evolution from './pages/Evolution';
import './App.css';

function PublicRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="loading-screen" role="status" aria-label="Verificando autenticação">
        <div className="spinner" aria-hidden="true"></div>
        <p>Carregando...</p>
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

import { useAuth } from './context/AuthContext';

function AppRoutes() {
  return (
    <Routes>
      {/* Public Routes (Auth) */}
      <Route element={<AuthLayout />}>
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          }
        />
      </Route>

      {/* Protected Routes */}
      <Route
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/evolution" element={<Evolution />} />
        <Route path="/settings" element={<Settings />} />

        {/* Teams */}
        <Route path="/teams" element={<TeamsList />} />
        <Route path="/teams/new" element={<TeamForm />} />
        <Route path="/teams/:teamId/edit" element={<TeamForm />} />
        <Route path="/teams/:teamId/trainings" element={<TrainingsList />} />
        <Route path="/teams/:teamId/trainings/new" element={<TrainingForm />} />
        <Route path="/teams/:teamId/trainings/:trainingId/edit" element={<TrainingForm />} />
        <Route path="/teams/:teamId/athletes" element={<AthletesList />} />
        <Route path="/teams/:teamId/athletes/new" element={<AthleteForm />} />
        <Route path="/teams/:teamId/athletes/:athleteId/edit" element={<AthleteForm />} />

        {/* Attendance */}
        <Route path="/trainings/:trainingId/attendance" element={<Attendance />} />

        {/* Evaluations */}
        <Route path="/athletes/:athleteId/evaluation/new" element={<EvaluationForm />} />
        <Route
          path="/athletes/:athleteId/evaluation/:evaluationId/edit"
          element={<EvaluationForm />}
        />

        {/* Profile */}
        <Route path="/athletes/:athleteId" element={<Profile />} />
      </Route>

      {/* Redirect root to dashboard or login */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
