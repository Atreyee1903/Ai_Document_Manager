import { useLocation, Link } from 'react-router-dom';
import styles from './Breadcrumb.module.css';

const labelMap = {
  dashboard: 'Dashboard',
  documents: 'Document Library',
  upload: 'Upload',
  search: 'Search',
  preview: 'Preview',
};

export default function Breadcrumb() {
  const location = useLocation();
  const parts = location.pathname.split('/').filter(Boolean);

  const crumbs = parts.map((part, idx) => {
    const path = '/' + parts.slice(0, idx + 1).join('/');
    const label = labelMap[part] || decodeURIComponent(part);
    const isLast = idx === parts.length - 1;
    return { path, label, isLast };
  });

  return (
    <nav className={styles.breadcrumb}>
      <Link to="/dashboard" className={styles.crumb}>Home</Link>
      {crumbs.map((c, i) => (
        <span key={i}>
          <span className={styles.separator}> / </span>
          {c.isLast ? (
            <span className={styles.current}>{c.label}</span>
          ) : (
            <Link to={c.path} className={styles.crumb}>{c.label}</Link>
          )}
        </span>
      ))}
    </nav>
  );
}
