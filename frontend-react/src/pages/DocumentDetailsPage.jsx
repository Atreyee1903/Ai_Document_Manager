import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FiArrowLeft, FiEye } from 'react-icons/fi';
import { useDocuments } from '../hooks/useDocuments';
import FileIcon from '../components/documents/FileIcon';
import PropertiesPanel from '../components/documents/PropertiesPanel';
import DocumentPreview from '../components/preview/DocumentPreview';
import { showToast } from '../utils/toast';
import styles from './DocumentDetailsPage.module.css';

export default function DocumentDetailsPage() {
  const { filename } = useParams();
  const navigate = useNavigate();
  const { fetchDocument, fetchSimilar, fetchPreview, deleteDocument } = useDocuments();
  const [doc, setDoc] = useState(null);
  const [similar, setSimilar] = useState([]);
  const [previewData, setPreviewData] = useState(null);
  const [showDelete, setShowDelete] = useState(false);

  useEffect(() => {
    if (!filename) return;
    const decoded = decodeURIComponent(filename);
    fetchDocument(decoded).then(setDoc).catch(() => {
      showToast('Error loading document', 'danger');
      navigate('/documents');
    });
    fetchSimilar(decoded).then(setSimilar).catch(() => {});
    fetchPreview(decoded).then(setPreviewData).catch(() => {});
  }, [filename, fetchDocument, fetchSimilar, fetchPreview, navigate]);

  const handleDelete = async () => {
    try {
      await deleteDocument(decodeURIComponent(filename));
      showToast('Document deleted successfully', 'success');
      navigate('/documents');
    } catch {
      showToast('Error deleting document', 'danger');
    }
    setShowDelete(false);
  };

  const handleDownload = () => {
    window.open('/download/' + encodeURIComponent(decodeURIComponent(filename)), '_blank');
  };

  if (!doc) {
    return <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>Loading document...</div>;
  }

  return (
    <>
      <div className={styles.page}>
        <div className={styles.main}>
          <button className={styles.backBtn} onClick={() => navigate(-1)}>
            <FiArrowLeft /> Back
          </button>
          <div className={styles.docHeader}>
            <FileIcon filename={doc.file_name} size={24} />
            <span className={styles.docTitle}>{doc.file_name}</span>
          </div>

          <div className={styles.previewSection}>
            <div className={styles.previewTitle}>
              <FiEye style={{ marginRight: 6, verticalAlign: 'middle' }} />
              Document Preview
            </div>
            <DocumentPreview
              filename={doc.file_name}
              previewData={previewData}
              onFullscreen={() => navigate('/documents/' + encodeURIComponent(doc.file_name) + '/preview')}
            />
          </div>
        </div>

        <div className={styles.sidebar}>
          <PropertiesPanel
            document={doc}
            similar={similar}
            onDelete={() => setShowDelete(true)}
            onDownload={handleDownload}
          />
        </div>
      </div>

      {showDelete && (
        <div className={styles.modal} onClick={() => setShowDelete(false)}>
          <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <div className={styles.modalTitle}>Delete Document</div>
            <p>Are you sure you want to delete this document? This action cannot be undone.</p>
            <div className={styles.modalActions}>
              <button className={styles.modalBtn + ' ' + styles.cancelBtn} onClick={() => setShowDelete(false)}>Cancel</button>
              <button className={styles.modalBtn + ' ' + styles.deleteBtn} onClick={handleDelete}>Delete</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
