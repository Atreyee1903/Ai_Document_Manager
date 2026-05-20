import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FiFile, FiUpload, FiSearch, FiClock } from 'react-icons/fi';
import { useDocuments } from '../hooks/useDocuments';
import DocumentListView from '../components/documents/DocumentListView';
import styles from './DashboardPage.module.css';

export default function DashboardPage() {
  const { fetchDashboard } = useDocuments();
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchDashboard().then(setData).catch(console.error);
  }, [fetchDashboard]);

  return (
    <div>
      <div className={styles.welcome}>
        <h2>Welcome to AI Document Manager</h2>
        <p>Manage and search documents with AI-powered tagging, skills detection, and semantic search.</p>
      </div>

      <div className={styles.grid}>
        <div className={styles.statCard}>
          <div className={styles.statIcon} style={{ color: 'var(--alfresco-blue)' }}><FiFile size={32} /></div>
          <div className={styles.statValue}>{data?.total_documents ?? 0}</div>
          <div className={styles.statLabel}>Total Documents</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statIcon} style={{ color: 'var(--success)' }}><FiUpload size={32} /></div>
          <div className={styles.statValue}>{data?.recent_files?.length ?? 0}</div>
          <div className={styles.statLabel}>Recent Uploads</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statIcon} style={{ color: 'var(--info)' }}><FiSearch size={32} /></div>
          <Link to="/search" style={{ fontSize: 'var(--font-size-sm)', fontWeight: 600 }}>Try Search</Link>
          <div className={styles.statLabel}>AI-Powered Search</div>
        </div>
      </div>

      <div className={styles.actions}>
        <Link to="/upload" className={styles.actionBtn} style={{ background: 'var(--alfresco-blue)' }}>
          <FiUpload /> Upload Document
        </Link>
        <Link to="/search" className={styles.actionBtn} style={{ background: 'var(--info)' }}>
          <FiSearch /> Search Documents
        </Link>
      </div>

      <h3 className={styles.sectionTitle}><FiClock style={{ marginRight: 8 }} /> Recent Uploads</h3>
      <DocumentListView documents={data?.recent_files || []} />
    </div>
  );
}
