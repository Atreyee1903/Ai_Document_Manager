import { useState, useCallback } from 'react';
import api from '../api/axiosClient';

export function useDocuments() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchDocuments = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get('/documents');
      setDocuments(res.data.documents || []);
    } catch (err) {
      console.error('Error fetching documents:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchDocument = useCallback(async (filename) => {
    const res = await api.get('/document/' + encodeURIComponent(filename));
    return res.data;
  }, []);

  const deleteDocument = useCallback(async (filename) => {
    await api.delete('/document/' + encodeURIComponent(filename));
  }, []);

  const fetchDashboard = useCallback(async () => {
    const res = await api.get('/dashboard-data');
    return res.data;
  }, []);

  const fetchSimilar = useCallback(async (filename, topK = 5) => {
    const res = await api.get('/similar/' + encodeURIComponent(filename), { params: { top_k: topK } });
    return res.data.similar_documents || [];
  }, []);

  const fetchPreview = useCallback(async (filename) => {
    const res = await api.get('/preview/' + encodeURIComponent(filename));
    return res.data;
  }, []);

  return { documents, loading, fetchDocuments, fetchDocument, deleteDocument, fetchDashboard, fetchSimilar, fetchPreview };
}
