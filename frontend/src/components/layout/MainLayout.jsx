import { Outlet, NavLink, useLocation } from 'react-router-dom';
import './MainLayout.css';

const NAV_ITEMS = [
  { path: '/dashboard', label: 'Início', icon: '🏠' },
  { path: '/teams', label: 'Equipes', icon: '👥' },
  { path: '/evolution', label: 'Evolução', icon: '📊' },
  { path: '/settings', label: 'Config', icon: '⚙️' },
];

export default function MainLayout() {
  const location = useLocation();

  return (
    <div className="main-layout">
      <header className="header">
        <h1>Vôlei+</h1>
      </header>

      <main className="main-content" role="main">
        <Outlet />
      </main>

      <nav className="bottom-nav" aria-label="Navegação principal">
        <ul className="nav-list">
          {NAV_ITEMS.map(item => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                aria-current={location.pathname === item.path ? 'page' : undefined}
              >
                <span className="nav-icon" aria-hidden="true">
                  {item.icon}
                </span>
                <span className="nav-label">{item.label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}
