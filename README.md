# AI Document Manager

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running the System](#running-the-system)
7. [Features](#features)
8. [Document Preview](#document-preview)
9. [Usage Guide](#usage-guide)
10. [API Documentation](#api-documentation)
11. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

**AI Document Manager** is an AI-powered document management system inspired by **Alfresco Share**, built with a FastAPI (Python) backend and a **React.js** single-page application frontend. It allows you to:

- Upload and manage documents (PDF, DOCX, JPG, PNG)
- **Preview documents in-browser** (PDF viewer, image viewer, extracted-text viewer)
- Automatically extract text from documents
- Perform keyword, semantic, and topic-based search
- Auto-tag documents by category with AI
- Detect skills and topic keywords
- Maintain document versions
- Browse a professional document library with list/grid views

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────┐
│                  React SPA (Vite)                   │
│  ┌──────────┐ ┌────────────┐ ┌──────────────────┐  │
│  │  Sidebar  │ │   Header   │ │  Document Views  │  │
│  │  (nav)    │ │  (search)  │ │  Preview / Grid  │  │
│  └──────────┘ └────────────┘ └──────────────────┘  │
│         Axios ──── API Proxy (Vite dev) ──────►     │
└──────────────────────┬─────────────────────────────┘
                       │  HTTP / REST
┌──────────────────────▼─────────────────────────────┐
│                 FastAPI Backend                      │
│  ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌────────┐  │
│  │  Auth   │ │  Upload  │ │  Search │ │Preview │  │
│  │  Module │ │  + Tags  │ │  Engine │ │  API   │  │
│  └─────────┘ └──────────┘ └─────────┘ └────────┘  │
│       │           │             │           │       │
│  ┌────▼───────────▼─────────────▼───────────▼───┐  │
│  │         PostgreSQL + File Storage             │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**Frontend**: React 18 + Vite + React Router 6 + Axios + CSS Modules  
**Backend**: FastAPI + SQLAlchemy + Sentence Transformers + PyPDF2 + python-docx  
**Styling**: Alfresco Share-inspired UI with sidebar navigation, header search, breadcrumbs, and document library views

---

## 🔧 System Requirements

### Hardware
- CPU: Any modern processor
- RAM: Minimum 4GB (8GB recommended for AI models)
- Disk: At least 2GB free space

### Software
- **Python**: 3.9 or higher
- **Node.js**: 18 or higher (for React frontend)
- **npm**: 9+ (comes with Node.js)
- **pip**: Python package manager (comes with Python)
- **OS**: Windows, macOS, or Linux

### Optional (for OCR on images)
- **Tesseract OCR**: Download from https://github.com/UB-Mannheim/tesseract/wiki

---

## 📦 Installation Guide

### Step 1: Clone or Download the Project

```bash
git clone <repository-url>
cd Ai_Document_Manager-main
```

### Step 2: Create a Python Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The first time you run the system, it will download the sentence-transformers models (~500MB). This may take a few minutes.

### Step 4: Install React Frontend Dependencies

```bash
cd frontend-react
npm install
cd ..
```

### Step 5: Build the React Frontend (for production)

```bash
cd frontend-react
npm run build
cd ..
```

This creates a `frontend-react/dist/` folder that the FastAPI backend serves automatically.

### Step 6: Install Tesseract (Optional - for OCR)

**On Windows:**
- Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
- Run the installer
- Remember the installation path (default: `C:\Program Files\Tesseract-OCR`)
- Add this environment variable:
  ```
  TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata
  ```

**On macOS:**
```bash
brew install tesseract
```

**On Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

---

## ⚙️ Configuration

### Default Credentials

```
Username: admin
Password: 1234
```

To change credentials, edit `backend/auth.py`:

```python
USERNAME = "admin"  # Change this
PASSWORD = "1234"   # Change this
```

### API Port

Default: `8000`

To change, edit the main.py file at the bottom:

```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port here
```

### Backup and Configuration Files

- **Metadata**: `metadata/metadata.json`
- **Embeddings**: `embeddings/embeddings.pkl`
- **Documents**: `documents/`
- **Extracted Text**: `extracted_text/`
- **Summaries**: `summaries/`

---

## 🚀 Running the System

### Option A: Production Mode (Built React Frontend)

1. Build the frontend (if not already done):
```bash
cd frontend-react && npm run build && cd ..
```

2. Start the backend:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

3. Open: [http://localhost:8000](http://localhost:8000)

The backend automatically serves the React build when it detects `frontend-react/dist/`.

### Option B: Development Mode (Hot Reload)

**Terminal 1 – Backend:**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 – React Dev Server (with hot reload):**
```bash
cd frontend-react
npm run dev
```

Open: [http://localhost:5173](http://localhost:5173)

The Vite dev server automatically proxies all API calls to `localhost:8000`.

### Option C: Legacy Frontend (Original HTML/Bootstrap)

The original vanilla HTML frontend is still available at:
```
http://localhost:8000/frontend/templates/login.html
```


---

## ✨ Key Features

### 1. **Alfresco Share-style UI** 🖥️
- Enterprise document management layout with sidebar navigation
- Global search bar in the header
- Breadcrumb navigation across all pages
- Document library with list and grid views
- Properties panel with tags, skills, metadata, and similar documents

### 2. **Document Preview** 👁️
- **PDF Preview**: In-browser PDF rendering with zoom controls
- **Image Preview**: View JPG/PNG files directly with zoom in/out
- **Text Preview**: View extracted text from DOCX and other document types
- **Fullscreen Mode**: Dedicated fullscreen preview page per document
- Preview toolbar with zoom controls, download button, and fullscreen toggle

### 3. **Login System** 🔐
- Email/password authentication
- Session-based auth with cookies
- Registration with password validation
- Auto-redirect for protected routes

### 4. **Document Upload** 📤
- Supports: PDF, DOCX, JPG, PNG
- Drag and drop upload area
- Upload progress bar
- Automatic versioning
- Real-time processing results (tags, skills, keywords)

### 5. **Text Extraction** 📖
- PDF → PyPDF2
- DOCX → python-docx
- Images → pytesseract (OCR)
- Extracted text available for preview

### 6. **Auto-Tagging** 🏷️
- Automatic categorization
- Categories: Finance, Career, Health, Legal, Education, Technology, Research
- Color-coded tag badges

### 7. **Semantic Search** 🔍
- AI-powered embeddings using Sentence Transformers
- Understands meaning, not just keywords
- Cosine similarity matching
- Topic/skills-based search
- Keyword exact-match search

### 8. **Document Versioning** 🔄
- Automatic version control
- Never overwrites original files
- Example: `resume.pdf` → `resume_v1.pdf` → `resume_v2.pdf`

### 9. **Document Library** 📚
- List view with sortable columns (name, date, size)
- Grid view with file type icons
- Click-through to document details and preview
- Similar documents discovery

### 10. **Dashboard** 🏠
- Overview statistics (total docs, recent uploads)
- Quick action buttons
- Recent uploads table

---

## 👁️ Document Preview

The document preview feature provides Alfresco Share-style in-browser document viewing:

### PDF Preview
- Renders PDFs directly in an embedded viewer
- Zoom in/out controls with percentage indicator
- Click fullscreen to view in a dedicated page
- Download directly from the preview toolbar

### Image Preview (JPG, PNG)
- Displays images inline with zoom controls
- Supports drag-to-zoom and fit-to-width
- Fullscreen mode for detailed inspection

### DOCX / Text Preview
- Extracts text from DOCX files via the backend `/preview/{filename}` API
- Renders extracted text in a readable monospace format
- Zoom control adjusts font size for readability

### Fullscreen Preview
- Navigate to `/documents/{filename}/preview` for an immersive view
- Dark background with centered content
- Close button returns to document details

---

## 📚 Usage Guide

### Uploading a Document

1. Click **"Upload Document"** on Dashboard
2. Select or drag-and-drop your file
3. Click **"Upload & Process"**
4. Wait for automatic processing:
   - Text extraction
   - Summary generation
   - Tag assignment
   - Embedding creation
5. View results and confirm

### Searching Documents

#### Keyword Search
- Best for: Finding exact terms
- Example: Search "invoice" finds all documents containing "invoice"

#### Semantic Search
- Best for: Understanding meaning
- Example: Search "medical records" finds documents about health, even if they don't use those exact words
- Shows similarity score (0-100%)

#### Combined Search
- Gets results from both methods
- Most comprehensive results

### Viewing Document Details

- Click on any document to view:
  - Summary
  - Tags
  - Upload date
  - Version history
  - Similar documents
  - Download link
  - Delete option

### Managing Versions

- Upload the same file twice
- System automatically creates versions:
  - `document_v1.pdf`
  - `document_v2.pdf`
- All versions are preserved

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication Endpoints

#### Login
```
POST /login
Content-Type: application/json

{
  "username": "admin",
  "password": "1234"
}

Response:
{
  "status": "success",
  "message": "Login successful",
  "username": "admin"
}
```

#### Logout
```
GET /logout

Response:
{
  "status": "success",
  "message": "Logout successful"
}
```

#### Check Auth Status
```
GET /auth-status

Response:
{
  "authenticated": true
}
```

### Document Endpoints

#### Upload Document
```
POST /upload
Content-Type: multipart/form-data

Body: File upload

Response:
{
  "success": true,
  "message": "Document uploaded successfully",
  "file_name": "resume_v1.pdf",
  "summary": "AI generated summary...",
  "tags": ["Career"],
  "metadata": {...}
}
```

#### Get Dashboard Data
```
GET /dashboard-data

Response:
{
  "total_documents": 5,
  "recent_files": [{...}, ...],
  "timestamp": "2026-03-26T10:30:00"
}
```

#### List All Documents
```
GET /documents

Response:
{
  "documents": [{...}, {...}, ...]
}
```

#### Get Document Details
```
GET /document/{filename}

Response:
{
  "file_name": "resume_v1.pdf",
  "upload_date": "2026-03-26",
  "tags": ["Career"],
  "version": 1,
  "file_size": 245,
  "summary": "...",
  "download_url": "/download/resume_v1.pdf"
}
```

#### Delete Document
```
DELETE /document/{filename}

Response:
{
  "success": true,
  "message": "Document deleted successfully"
}
```

#### Download Document
```
GET /download/{filename}

Response: File download
```

#### Preview Document
```
GET /preview/{filename}

Response:
{
  "filename": "resume_v1.pdf",
  "content_type": "application/pdf",
  "extracted_text": "Full extracted text content...",
  "download_url": "/download/resume_v1.pdf",
  "file_extension": ".pdf"
}
```

### Search Endpoints

#### Keyword Search
```
GET /keyword-search?q=invoice

Response:
{
  "query": "invoice",
  "results": [
    {
      "file": "bill_march.pdf",
      "type": "keyword",
      "relevance": 3,
      "preview": "..."
    }
  ],
  "count": 1
}
```

#### Semantic Search
```
GET /semantic-search?q=medical+records&top_k=10

Response:
{
  "query": "medical records",
  "results": [
    {
      "file": "health_report.pdf",
      "type": "semantic",
      "similarity": 0.892,
      "preview": "..."
    }
  ],
  "count": 1
}
```

#### Combined Search
```
POST /search
Content-Type: application/json

{
  "query": "financial report",
  "search_type": "combined",
  "top_k": 10
}

Response:
{
  "query": "financial report",
  "search_type": "combined",
  "results": [...],
  "count": 2
}
```

#### Find Similar Documents
```
GET /similar/resume_v1.pdf?top_k=5

Response:
{
  "reference_file": "resume_v1.pdf",
  "similar_documents": [
    {
      "file": "cover_letter.pdf",
      "similarity": 0.756
    }
  ],
  "count": 1
}
```

### System Endpoints

#### Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "timestamp": "2026-03-26T10:30:00"
}
```

---

## 📁 Project Structure

```
ai_document_manager/
├── backend/
│   ├── main.py                 # FastAPI application + preview endpoint
│   ├── auth.py                 # Authentication
│   ├── config.py               # Configuration management
│   ├── database.py             # Database models
│   ├── upload.py               # Document upload
│   ├── search.py               # Search functionality
│   ├── tagging.py              # Auto-tagging
│   ├── versioning.py           # Version control
│   ├── metadata_manager.py     # Metadata handling
│   ├── embedding_manager.py    # Embeddings management
│   └── utils/
│       ├── text_extractor.py   # Text extraction
│       ├── file_handler.py     # File operations
│       └── json_handler.py     # JSON/DB handling
├── frontend-react/             # React SPA (Alfresco Share-style)
│   ├── package.json            # Node.js dependencies
│   ├── vite.config.js          # Vite configuration + API proxy
│   ├── index.html              # SPA entry point
│   └── src/
│       ├── main.jsx            # React entry point
│       ├── App.jsx             # Route definitions
│       ├── api/
│       │   └── axiosClient.js  # Axios API client
│       ├── context/
│       │   └── AuthContext.jsx  # Authentication context
│       ├── hooks/
│       │   ├── useDocuments.js # Document operations hook
│       │   └── useSearch.js    # Search hook
│       ├── utils/
│       │   ├── formatters.js   # Utility functions
│       │   └── toast.js        # Toast notifications
│       ├── styles/
│       │   ├── variables.css   # Alfresco design tokens
│       │   └── global.css      # Global styles
│       ├── components/
│       │   ├── layout/
│       │   │   ├── AppHeader.jsx       # Header with search
│       │   │   ├── Sidebar.jsx         # Navigation sidebar
│       │   │   ├── Breadcrumb.jsx      # Breadcrumb navigation
│       │   │   └── AuthenticatedLayout.jsx # Auth guard layout
│       │   ├── documents/
│       │   │   ├── FileIcon.jsx        # File type icons
│       │   │   ├── DocumentToolbar.jsx # List/grid toggle + sort
│       │   │   ├── DocumentListView.jsx # Table view
│       │   │   ├── DocumentGridView.jsx # Grid/card view
│       │   │   └── PropertiesPanel.jsx  # Right-side properties
│       │   └── preview/
│       │       ├── DocumentPreview.jsx  # Preview router
│       │       ├── PdfPreview.jsx       # PDF viewer
│       │       ├── ImagePreview.jsx     # Image viewer
│       │       ├── TextPreview.jsx      # Extracted text viewer
│       │       └── PreviewToolbar.jsx   # Zoom/download controls
│       └── pages/
│           ├── LoginPage.jsx
│           ├── RegisterPage.jsx
│           ├── DashboardPage.jsx
│           ├── DocumentLibraryPage.jsx
│           ├── DocumentDetailsPage.jsx
│           ├── PreviewFullscreenPage.jsx
│           ├── UploadPage.jsx
│           └── SearchPage.jsx
├── frontend/                   # Legacy vanilla HTML frontend
│   ├── templates/              # HTML pages
│   └── static/                 # JS + CSS
├── requirements.txt            # Python dependencies
├── config.example.json         # Configuration template
└── README.md                   # This file
```

---

## 🐛 Troubleshooting

### Problem: Port 8000 already in use

**Solution**: 
```bash
# Use a different port
uvicorn backend.main:app --port 8001
```

### Problem: ModuleNotFoundError

**Solution**: 
```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Tesseract not found (OCR for images)

**Solution**:
```python
# Add to backend/utils/text_extractor.py:
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Problem: Slow first run

**Reason**: Models are downloading (~500MB)
**Solution**: This is normal. Be patient on first run.

### Problem: Login page not loading

**Solution**:
1. Make sure backend server is running on port 8000
2. Check browser console for errors (F12)
3. Try: `http://0.0.0.0:8000/frontend/templates/login.html`

### Problem: Upload fails silently

**Solution**:
1. Check browser console (F12)
2. Ensure file size < 50MB
3. Try uploading a different file type
4. Check backend terminal for error messages

### Problem: Search returns no results

**Solution**:
1. Upload at least one document first
2. Try with simpler search terms
3. Use keyword search first to verify documents exist
4. Try semantic search with different query

---

## 📊 Performance Tips

### For 100-200 Documents
- System handles this easily
- First semantic search may take 2-3 seconds
- Embeddings file (~100MB+ depending on documents)

### Optimize for Speed
1. Use keyword search for exact matches
2. Keep document count reasonable
3. Ensure sufficient RAM (8GB+)
4. Close other applications

---

## 🔒 Security Notes

This is a **prototype system**. For production:

1. **Change default credentials** in `auth.py`
2. **Never deploy publicly** without authentication
3. **Use HTTPS** instead of HTTP
4. **Add database** instead of JSON files
5. **Implement user management**
6. **Use proper session management**
7. **Add rate limiting**
8. **Validate all file uploads**

---

## 📝 Sample Test Files

Create test files to explore the system:

1. **PDF**: Any PDF document
2. **DOCX**: Create in Microsoft Word
3. **Images**: Screenshots or photos with text
4. **Test files**: Use documents from your computer

---

## 🎓 Learning Outcomes

By using this system, you'll learn:

- **React.js**: Modern component-based SPA with hooks, context, and routing
- **FastAPI**: Modern Python web framework with async support
- **CSS Modules**: Scoped component styling with design tokens
- **AI/ML**: Transformers, embeddings, semantic search
- **Document Processing**: Text extraction, OCR, in-browser preview
- **Full Stack Development**: React frontend + Python backend
- **Enterprise UI Patterns**: Alfresco Share-inspired sidebar, breadcrumbs, document library
- **Version Control**: Document versioning
- **API Design**: RESTful endpoints with proxy configuration

---

## 📞 Support

For issues:
1. Check the Troubleshooting section
2. Review error messages in terminal
3. Check browser console (F12)
4. Verify all dependencies are installed
5. Ensure Python 3.9+ and Node.js 18+

---

## 📄 License

This is a student project. Use freely for learning purposes.

---

**Happy Managing! 📚**

**Last Updated**: March 29, 2026
**Version**: 2.0.0 (React Frontend)
