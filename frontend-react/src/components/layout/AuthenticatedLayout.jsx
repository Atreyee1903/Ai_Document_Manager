import { Outlet, Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import AppHeader from './AppHeader';
import Sidebar from './Sidebar';
import Breadcrumb from './Breadcrumb';
import styles from './AuthenticatedLayout.module.css';

export default function AuthenticatedLayout() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
        <div>Loading...</div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <>
      <AppHeader />
      <div className={styles.wrapper}>
        <Sidebar />
        <main className={styles.main}>
          <Breadcrumb />
          <Outlet />
        </main>
      </div>
    </>
  );
}
