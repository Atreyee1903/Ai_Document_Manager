import { Routes, Route, Navigate } from 'react-router-dom';
import AuthenticatedLayout from './components/layout/AuthenticatedLayout';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import DocumentLibraryPage from './pages/DocumentLibraryPage';
import DocumentDetailsPage from './pages/DocumentDetailsPage';
import UploadPage from './pages/UploadPage';
import SearchPage from './pages/SearchPage';
import PreviewFullscreenPage from './pages/PreviewFullscreenPage';

export default function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Authenticated routes */}
      <Route element={<AuthenticatedLayout />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/documents" element={<DocumentLibraryPage />} />
        <Route path="/documents/:filename" element={<DocumentDetailsPage />} />
        <Route path="/documents/:filename/preview" element={<PreviewFullscreenPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/search" element={<SearchPage />} />
      </Route>

      {/* Default redirect */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

