import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import './App.css';

const ProtectedRoute = lazy(() => import('./components/layout/ProtectedRoute'));
const MainLayout = lazy(() => import('./components/layout/MainLayout'));
const AuthLayout = lazy(() => import('./components/layout/AuthLayout'));
const Login = lazy(() => import('./pages/Auth/Login'));
const Register = lazy(() => import('./pages/Auth/Register'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const TeamsList = lazy(() => import('./pages/Teams/TeamsList'));
const TeamForm = lazy(() => import('./pages/Teams/TeamForm'));
const AthletesList = lazy(() => import('./pages/Athletes/AthletesList'));
const AthleteForm = lazy(() => import('./pages/Athletes/AthleteForm'));
const TrainingsList = lazy(() => import('./pages/Trainings/TrainingsList'));
const TrainingForm = lazy(() => import('./pages/Trainings/TrainingForm'));
const Attendance = lazy(() => import('./pages/Attendance/Attendance'));
const EvaluationForm = lazy(() => import('./pages/Evaluations/EvaluationForm'));
const Profile = lazy(() => import('./pages/Profile/Profile'));
const Settings = lazy(() => import('./pages/Settings'));
const Evolution = lazy(() => import('./pages/Evolution'));

function RouteLoading() {
  return (
    <div className="loading-screen" role="status" aria-label="Carregando tela">
      <div className="spinner" aria-hidden="true"></div>
      <p>Carregando...</p>
    </div>
  );
}

function PublicRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <RouteLoading />;
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

import { useAuth } from './context/AuthContext';

function AppRoutes() {
  return (
    <Suspense fallback={<RouteLoading />}>
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
    </Suspense>
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
