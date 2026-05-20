import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDocuments } from '../hooks/useDocuments';
import { getFileExtension } from '../utils/formatters';
import styles from './PreviewFullscreenPage.module.css';

export default function PreviewFullscreenPage() {
  const { filename } = useParams();
  const navigate = useNavigate();
  const { fetchPreview } = useDocuments();
  const [data, setData] = useState(null);
  const decoded = decodeURIComponent(filename || '');

  useEffect(() => {
    if (decoded) fetchPreview(decoded).then(setData).catch(() => {});
  }, [decoded, fetchPreview]);

  const ext = getFileExtension(decoded);
  // Use relative URL so browser sends auth cookies automatically
  const viewUrl = '/view/' + encodeURIComponent(decoded);

  return (
    <div className={styles.page}>
      <div className={styles.topBar}>
        <span className={styles.title}>{decoded}</span>
        <button className={styles.closeBtn} onClick={() => navigate(-1)}>Close</button>
      </div>
      <div className={styles.content}>
        {ext === 'pdf' && <iframe className={styles.pdfFrame} src={viewUrl} title={decoded} />}
        {['jpg', 'jpeg', 'png'].includes(ext) && <img className={styles.image} src={viewUrl} alt={decoded} />}
        {!['pdf', 'jpg', 'jpeg', 'png'].includes(ext) && (
          <div className={styles.text}>{data?.extracted_text || 'Loading preview...'}</div>
        )}
      </div>
    </div>
  );
}
