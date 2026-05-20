import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { FiSearch } from 'react-icons/fi';
import { useSearch } from '../hooks/useSearch';
import FileIcon from '../components/documents/FileIcon';
import styles from './SearchPage.module.css';

export default function SearchPage() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const { results, loading, search } = useSearch();
  const [query, setQuery] = useState(params.get('q') || '');
  const [searchType, setSearchType] = useState('topic');
  const [searched, setSearched] = useState(false);

  useEffect(() => {
    const q = params.get('q');
    if (q) {
      setQuery(q);
      search(q, searchType);
      setSearched(true);
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const handleSearch = (e) => {
    e?.preventDefault();
    if (!query.trim()) return;
    search(query.trim(), searchType);
    setSearched(true);
  };

  return (
    <div>
      <h2 style={{ marginBottom: 'var(--space-lg)', fontWeight: 600 }}>Search Documents</h2>

      <div className={styles.searchBox}>
        <form className={styles.searchRow} onSubmit={handleSearch}>
          <input
            className={styles.searchInput}
            type="text"
            placeholder="Enter search query..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <select className={styles.typeSelect} value={searchType} onChange={(e) => setSearchType(e.target.value)}>
            <option value="topic">Topic / Skills</option>
            <option value="keyword">Keyword Only</option>
            <option value="semantic">Semantic</option>
          </select>
          <button className={styles.searchBtn} type="submit"><FiSearch style={{ marginRight: 4 }} /> Search</button>
        </form>
      </div>

      {loading && <div className={styles.loading}>Searching documents...</div>}

      {!loading && searched && results.length === 0 && (
        <div className={styles.empty}>
          <FiSearch size={32} style={{ marginBottom: 8, opacity: 0.4 }} />
          <div>No results found. Try different keywords.</div>
        </div>
      )}

      {!loading && results.length > 0 && (
        <>
          <div className={styles.info}>Found <strong>{results.length}</strong> result{results.length !== 1 ? 's' : ''} for "{query}"</div>
          {results.map((r, i) => (
            <div key={i} className={styles.resultCard} onClick={() => navigate('/documents/' + encodeURIComponent(r.file))}>
              <div className={styles.resultHeader}>
                <FileIcon filename={r.file} />
                <span className={styles.resultName}>{r.file}</span>
                {r.match_ratio != null && (
                  <span className={styles.badge} style={{ background: 'var(--success)' }}>{Math.round(r.match_ratio * 100)}% match</span>
                )}
                {r.similarity != null && (
                  <span className={styles.badge} style={{ background: 'var(--success)' }}>{Math.round(r.similarity * 100)}% similar</span>
                )}
              </div>
              <div className={styles.resultPreview}>{r.preview || 'No preview available'}</div>
              <div className={styles.resultMeta}>
                {(r.matched_keywords || []).map((kw) => (
                  <span key={kw} className={styles.badge} style={{ background: 'var(--info)' }}>{kw}</span>
                ))}
              </div>
            </div>
          ))}
        </>
      )}
    </div>
  );
}
