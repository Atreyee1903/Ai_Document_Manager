import { NavLink } from 'react-router-dom';
import { FiHome, FiFolder, FiUpload, FiSearch, FiClock, FiGrid } from 'react-icons/fi';
import styles from './Sidebar.module.css';

const navItems = [
  { to: '/dashboard', icon: FiHome, label: 'Dashboard' },
  { to: '/documents', icon: FiFolder, label: 'Document Library' },
  { to: '/upload', icon: FiUpload, label: 'Upload' },
  { to: '/search', icon: FiSearch, label: 'Search' },
];

export default function Sidebar() {
  return (
    <aside className={styles.sidebar}>
      <div className={styles.section}>
        <div className={styles.sectionTitle}>Navigation</div>
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              styles.navItem + (isActive ? ' ' + styles.navItemActive : '')
            }
          >
            <item.icon className={styles.navIcon} />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </div>
      <div className={styles.section}>
        <div className={styles.sectionTitle}>Library</div>
        <NavLink to="/documents" className={styles.navItem}>
          <FiGrid className={styles.navIcon} />
          <span>My Files</span>
        </NavLink>
        <NavLink to="/documents" className={styles.navItem}>
          <FiClock className={styles.navIcon} />
          <span>Recent</span>
        </NavLink>
      </div>
    </aside>
  );
}
