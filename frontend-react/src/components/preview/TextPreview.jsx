import { useState } from 'react';
import PreviewToolbar from './PreviewToolbar';
import styles from './TextPreview.module.css';

export default function TextPreview({ filename, text, downloadUrl, onFullscreen }) {
  const [zoom, setZoom] = useState(1);

  return (
    <div>
      <PreviewToolbar
        filename={filename}
        zoom={zoom}
        onZoomIn={() => setZoom((z) => Math.min(z + 0.5, 3))}
        onZoomOut={() => setZoom((z) => Math.max(z - 0.5, 0.5))}
        onFullscreen={onFullscreen}
        onDownload={() => window.open('/download/' + encodeURIComponent(filename), '_blank')}
      />
      <div className={styles.container} style={{ fontSize: (14 * zoom) + 'px' }}>
        {text ? (
          <div className={styles.text}>{text}</div>
        ) : (
          <div className={styles.empty}>No extracted text available for preview.</div>
        )}
      </div>
    </div>
  );
}
