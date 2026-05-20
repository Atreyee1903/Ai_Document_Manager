import { FiZoomIn, FiZoomOut, FiMaximize, FiDownload } from 'react-icons/fi';
import styles from './PreviewToolbar.module.css';

export default function PreviewToolbar({ filename, zoom, onZoomIn, onZoomOut, onFullscreen, onDownload }) {
  return (
    <div className={styles.toolbar}>
      <div className={styles.left}>
        <span className={styles.info}>{filename}</span>
      </div>
      <div className={styles.right}>
        <button className={styles.btn} onClick={onZoomOut} title="Zoom out"><FiZoomOut /></button>
        <span className={styles.info}>{Math.round(zoom * 100)}%</span>
        <button className={styles.btn} onClick={onZoomIn} title="Zoom in"><FiZoomIn /></button>
        {onFullscreen && (
          <button className={styles.btn} onClick={onFullscreen} title="Fullscreen"><FiMaximize /></button>
        )}
        <button className={styles.btn} onClick={onDownload} title="Download"><FiDownload /></button>
      </div>
    </div>
  );
}
