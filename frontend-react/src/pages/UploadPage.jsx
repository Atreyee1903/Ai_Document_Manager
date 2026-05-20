import { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import { FiUploadCloud } from 'react-icons/fi';
import api from '../api/axiosClient';
import FileIcon from '../components/documents/FileIcon';
import { getTagColor } from '../utils/formatters';
import { showToast } from '../utils/toast';
import styles from './UploadPage.module.css';

const ALLOWED = ['.pdf', '.docx', '.jpg', '.jpeg', '.png'];

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const inputRef = useRef(null);

  const validateFile = (f) => {
    const ext = '.' + f.name.split('.').pop().toLowerCase();
    return ALLOWED.includes(ext);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files.length > 0 && validateFile(e.dataTransfer.files[0])) {
      setFile(e.dataTransfer.files[0]);
      setResult(null);
    } else {
      showToast('Invalid file type. Supported: PDF, DOCX, JPG, PNG', 'warning');
    }
  };

  const handleSelect = (e) => {
    if (e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    if (!validateFile(file)) {
      showToast('Invalid file type', 'warning');
      return;
    }
    setUploading(true);
    setProgress(0);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await api.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (e) => {
          const pct = Math.round((e.loaded * 100) / e.total);
          setProgress(pct);
        },
      });
      setResult(res.data);
      showToast('Document uploaded successfully!', 'success');
    } catch (err) {
      showToast(err.response?.data?.detail || 'Upload failed', 'danger');
    } finally {
      setUploading(false);
    }
  };

  const reset = () => {
    setFile(null);
    setResult(null);
    setProgress(0);
    if (inputRef.current) inputRef.current.value = '';
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Upload Document</h2>

      {!result && (
        <>
          <div
            className={styles.dropzone + (dragOver ? ' ' + styles.dropzoneActive : '')}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
          >
            <div className={styles.dropIcon}><FiUploadCloud size={48} /></div>
            <div className={styles.dropText}>Drag and drop your file here</div>
            <div className={styles.dropHint}>or click to select &mdash; PDF, DOCX, JPG, PNG</div>
            <input ref={inputRef} type="file" accept=".pdf,.docx,.jpg,.jpeg,.png" hidden onChange={handleSelect} />
          </div>

          {file && (
            <>
              <div className={styles.fileInfo}>
                <div className={styles.fileName}>
                  <FileIcon filename={file.name} /> {file.name}
                </div>
                <button className={styles.changeBtn} onClick={() => inputRef.current?.click()}>Change</button>
              </div>
              {!uploading ? (
                <button className={styles.uploadBtn} onClick={handleUpload}>Upload &amp; Process</button>
              ) : (
                <div className={styles.progressBar}>
                  <div className={styles.progressFill} style={{ width: progress + '%' }}>{progress}%</div>
                </div>
              )}
            </>
          )}
        </>
      )}

      {result && (
        <div className={styles.result}>
          <div className={styles.resultTitle}>Upload Successful!</div>
          <div className={styles.resultSection}>
            <div className={styles.resultLabel}>File Name</div>
            <div>{result.file_name}</div>
          </div>
          <div className={styles.resultSection}>
            <div className={styles.resultLabel}>Tags</div>
            <div>
              {(result.tags || []).length > 0
                ? result.tags.map((t) => <span key={t} className={styles.badge} style={{ background: getTagColor(t) }}>{t}</span>)
                : <span style={{ color: 'var(--text-muted)' }}>No tags</span>}
            </div>
          </div>
          <div className={styles.resultSection}>
            <div className={styles.resultLabel}>Skills</div>
            <div>
              {(result.skills || []).length > 0
                ? result.skills.map((s) => <span key={s} className={styles.badge} style={{ background: 'var(--info)' }}>{s}</span>)
                : <span style={{ color: 'var(--text-muted)' }}>No skills detected</span>}
            </div>
          </div>
          <div className={styles.resultSection}>
            <div className={styles.resultLabel}>Topic Keywords</div>
            <div>
              {(result.topic_keywords || []).length > 0
                ? result.topic_keywords.map((k) => <span key={k} className={styles.badge} style={{ background: '#757575' }}>{k}</span>)
                : <span style={{ color: 'var(--text-muted)' }}>No topic keywords</span>}
            </div>
          </div>
          <div className={styles.resultActions}>
            <Link to="/dashboard" className={styles.linkBtn} style={{ background: 'var(--alfresco-blue)', color: '#fff' }}>Dashboard</Link>
            <button className={styles.linkBtn} style={{ background: 'var(--border-color)', color: 'var(--text-primary)' }} onClick={reset}>Upload Another</button>
          </div>
        </div>
      )}
    </div>
  );
}
