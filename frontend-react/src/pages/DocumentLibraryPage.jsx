import { useEffect, useState } from 'react';
import { useDocuments } from '../hooks/useDocuments';
import DocumentToolbar from '../components/documents/DocumentToolbar';
import DocumentListView from '../components/documents/DocumentListView';
import DocumentGridView from '../components/documents/DocumentGridView';
import styles from './DocumentLibraryPage.module.css';

export default function DocumentLibraryPage() {
  const { documents, loading, fetchDocuments } = useDocuments();
  const [view, setView] = useState('list');
  const [sortBy, setSortBy] = useState('name');

  useEffect(() => { fetchDocuments(); }, [fetchDocuments]);

  const sorted = [...documents].sort((a, b) => {
    if (sortBy === 'name') return (a.file_name || '').localeCompare(b.file_name || '');
    if (sortBy === 'date') return new Date(b.upload_date || 0) - new Date(a.upload_date || 0);
    if (sortBy === 'size') return (b.file_size || 0) - (a.file_size || 0);
    return 0;
  });

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <h2 className={styles.title}>Document Library</h2>
      </div>
      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>Loading documents...</div>
      ) : (
        <>
          <DocumentToolbar view={view} onViewChange={setView} count={sorted.length} sortBy={sortBy} onSortChange={setSortBy} />
          {view === 'list' ? <DocumentListView documents={sorted} /> : <DocumentGridView documents={sorted} />}
        </>
      )}
    </div>
  );
}
