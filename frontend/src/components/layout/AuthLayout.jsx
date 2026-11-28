import { Outlet } from 'react-router-dom';
import './AuthLayout.css';

export default function AuthLayout() {
  return (
    <div className="auth-layout">
      <main className="auth-main" role="main">
        <Outlet />
      </main>
    </div>
  );
}
