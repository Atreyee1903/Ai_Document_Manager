import { useState, useCallback } from 'react';
import api from '../api/axiosClient';

export function useSearch() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const search = useCallback(async (query, searchType = 'keyword', topK = 10) => {
    setLoading(true);
    try {
      let res;
      if (searchType === 'keyword') {
        res = await api.get('/keyword-search', { params: { q: query, top_k: topK } });
      } else if (searchType === 'semantic') {
        res = await api.get('/semantic-search', { params: { q: query, top_k: topK } });
      } else {
        res = await api.get('/topic-search', { params: { q: query, top_k: topK } });
      }
      setResults(res.data.results || []);
      return res.data.results || [];
    } catch (err) {
      console.error('Search error:', err);
      setResults([]);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  return { results, loading, search };
}
