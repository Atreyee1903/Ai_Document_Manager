import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/login': 'http://127.0.0.1:8000',
      '/register': 'http://127.0.0.1:8000',
      '/logout': 'http://127.0.0.1:8000',
      '/auth-status': 'http://127.0.0.1:8000',
      '/upload': 'http://127.0.0.1:8000',
      '/documents': 'http://127.0.0.1:8000',
      '/document': 'http://127.0.0.1:8000',
      '/download': 'http://127.0.0.1:8000',
      '/view': 'http://127.0.0.1:8000',
      '/preview': 'http://127.0.0.1:8000',
      '/search': 'http://127.0.0.1:8000',
      '/keyword-search': 'http://127.0.0.1:8000',
      '/semantic-search': 'http://127.0.0.1:8000',
      '/topic-search': 'http://127.0.0.1:8000',
      '/similar': 'http://127.0.0.1:8000',
      '/dashboard-data': 'http://127.0.0.1:8000',
      '/health': 'http://127.0.0.1:8000',
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
});

