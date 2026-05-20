import { getFileExtension } from '../../utils/formatters';
import PdfPreview from './PdfPreview';
import ImagePreview from './ImagePreview';
import TextPreview from './TextPreview';

export default function DocumentPreview({ filename, previewData, onFullscreen }) {
  const ext = getFileExtension(filename);
  const downloadUrl = previewData?.download_url;

  if (ext === 'pdf') {
    return <PdfPreview filename={filename} downloadUrl={downloadUrl} onFullscreen={onFullscreen} />;
  }

  if (['jpg', 'jpeg', 'png'].includes(ext)) {
    return <ImagePreview filename={filename} downloadUrl={downloadUrl} onFullscreen={onFullscreen} />;
  }

  // DOCX and others - show extracted text
  return (
    <TextPreview
      filename={filename}
      text={previewData?.extracted_text || ''}
      downloadUrl={downloadUrl}
      onFullscreen={onFullscreen}
    />
  );
}
