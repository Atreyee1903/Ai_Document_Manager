export function formatFileSize(bytes) {
  if (!bytes || bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

export function formatDate(dateString) {
  if (!dateString) return '-';
  const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString(undefined, options);
}

export function truncateText(text, length = 100) {
  if (!text) return '';
  if (text.length <= length) return text;
  return text.substring(0, length) + '...';
}

export function getFileExtension(filename) {
  if (!filename) return '';
  return filename.toLowerCase().split('.').pop();
}

export function getTagColor(tag) {
  const colors = {
    Finance: 'var(--danger)',
    Career: 'var(--alfresco-blue)',
    Health: 'var(--success)',
    Legal: 'var(--warning)',
    Education: 'var(--info)',
    Technology: '#546E7A',
    Research: '#3E2723',
  };
  return colors[tag] || '#757575';
}
