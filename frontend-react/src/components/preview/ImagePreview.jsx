import { useState } from 'react';
import PreviewToolbar from './PreviewToolbar';
import styles from './ImagePreview.module.css';

export default function ImagePreview({ filename, downloadUrl, onFullscreen }) {
  const [zoom, setZoom] = useState(1);
  // Use relative URL so browser sends auth cookies automatically
  const src = downloadUrl || '/view/' + encodeURIComponent(filename);

  return (
    <div>
      <PreviewToolbar
        filename={filename}
        zoom={zoom}
        onZoomIn={() => setZoom((z) => Math.min(z + 0.25, 3))}
        onZoomOut={() => setZoom((z) => Math.max(z - 0.25, 0.25))}
        onFullscreen={onFullscreen}
        onDownload={() => window.open('/download/' + encodeURIComponent(filename), '_blank')}
      />
      <div className={styles.container}>
        <img
          className={styles.image}
          src={src}
          alt={filename}
          style={{ transform: 'scale(' + zoom + ')' }}
        />
      </div>
    </div>
  );
}
