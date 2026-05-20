import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import api from '../api/axiosClient';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const checkAuth = useCallback(async () => {
    try {
      const res = await api.get('/auth-status');
      if (res.data.authenticated) {
        setUser({ id: res.data.user_id, email: res.data.email });
      } else {
        setUser(null);
      }
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { checkAuth(); }, [checkAuth]);

  const login = async (email, password) => {
    const res = await api.post('/login', { email, password });
    if (res.data.status === 'success') {
      localStorage.setItem('user_id', res.data.user_id);
      setUser({ id: res.data.user_id, email: res.data.email });
      return { success: true };
    }
    return { success: false, message: 'Login failed' };
  };

  const register = async (email, password, confirmPassword) => {
    const res = await api.post('/register', {
      email, password, confirm_password: confirmPassword,
    });
    if (res.data.status === 'success') {
      localStorage.setItem('user_id', res.data.user_id);
      setUser({ id: res.data.user_id, email: res.data.email });
      return { success: true };
    }
    return { success: false, message: 'Registration failed' };
  };

  const logout = async () => {
    try { await api.get('/logout'); } catch { /* ignore */ }
    localStorage.removeItem('user_id');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
