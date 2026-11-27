import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const isAuthenticated = !!user;

  // Verifica se há token salvo e valida ao carregar
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        try {
          const userData = await api.auth.me();
          setUser(userData);
        } catch {
          // Token inválido/expirado
          localStorage.removeItem('auth_token');
          setUser(null);
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = useCallback(async credentials => {
    setError(null);
    try {
      const response = await api.auth.login(credentials);
      const { token, user: userData } = response;
      localStorage.setItem('auth_token', token);
      setUser(userData);
      return { success: true };
    } catch (err) {
      setError(err.message || 'Erro ao fazer login');
      return { success: false, error: err.message };
    }
  }, []);

  const register = useCallback(async userData => {
    setError(null);
    try {
      const response = await api.auth.register(userData);
      const { token, user: newUser } = response;
      localStorage.setItem('auth_token', token);
      setUser(newUser);
      return { success: true };
    } catch (err) {
      setError(err.message || 'Erro ao cadastrar');
      return { success: false, error: err.message };
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await api.auth.logout();
    } catch (err) {
      // Ignora erro de logout no servidor
      console.warn('Logout server error:', err);
    } finally {
      localStorage.removeItem('auth_token');
      setUser(null);
    }
  }, []);

  const clearError = useCallback(() => setError(null), []);

  const value = {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
}
