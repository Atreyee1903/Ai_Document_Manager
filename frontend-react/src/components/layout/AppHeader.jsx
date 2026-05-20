import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { FiSearch, FiFileText } from 'react-icons/fi';
import { useAuth } from '../../context/AuthContext';
import styles from './AppHeader.module.css';

export default function AppHeader() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [query, setQuery] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      navigate('/search?q=' + encodeURIComponent(query.trim()));
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <header className={styles.header}>
      <a href="/dashboard" className={styles.logo} onClick={(e) => { e.preventDefault(); navigate('/dashboard'); }}>
        <FiFileText size={22} />
        <span>Document Manager</span>
      </a>

      <form className={styles.searchBar} onSubmit={handleSearch}>
        <FiSearch className={styles.searchIcon} />
        <input
          className={styles.searchInput}
          type="text"
          placeholder="Search documents..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </form>

      <div className={styles.userMenu}>
        <span className={styles.userEmail}>{user?.email || ''}</span>
        <button className={styles.logoutBtn} onClick={handleLogout}>Logout</button>
      </div>
    </header>
  );
}
