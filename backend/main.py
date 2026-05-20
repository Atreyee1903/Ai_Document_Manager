"""
Main FastAPI Application
Central backend server for AI Document Manager
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Cookie, Response, Header, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from datetime import datetime
from typing import Optional

# Import backend modules
from .auth import create_session, destroy_session, is_authenticated
from .database import register_user, verify_user, init_db, get_user_by_id
from .config import get_api_config, get_paths_config
from .upload import upload_document, delete_document, get_document, get_all_documents
from .search import keyword_search, semantic_search, combined_search, get_similar_documents
from .utils.json_handler import get_document_count, get_recent_documents
from .utils.file_handler import ensure_directories_exist, ensure_user_directories_exist, get_extracted_text_path, get_user_documents_dir, get_file_extension


# Initialize FastAPI app
app = FastAPI(title="AI Document Manager", version="1.0.0")

# Load API config
api_config = get_api_config()
paths_config = get_paths_config()
cors_origins = api_config.get(
    "cors_origins",
    [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://0.0.0.0:8000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://0.0.0.0:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "null",
    ],
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|0\.0\.0\.0)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.middleware("http")
async def canonical_localhost_middleware(request: Request, call_next):
    """
    Redirect UI page requests from 0.0.0.0 to 127.0.0.1.
    Using 0.0.0.0 in browser can lead to inconsistent cookie/session behavior.
    """
    if request.url.hostname == "0.0.0.0" and request.method == "GET":
        path = request.url.path or "/"
        if path == "/":
            redirected = str(request.url).replace("://0.0.0.0", "://127.0.0.1", 1)
            return RedirectResponse(url=redirected, status_code=307)
    return await call_next(request)


# ==================== Pydantic Models ====================

class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    confirm_password: str


class SearchRequest(BaseModel):
    query: str
    search_type: str = "keyword"  # keyword/topic/semantic/combined
    top_k: int = 10


class TagRequest(BaseModel):
    filename: str
    tag: str


# ==================== Dependency Injection ====================

def get_current_user_id(
    user_id: Optional[str] = Cookie(None),
    x_user_id: Optional[str] = Header(None)
) -> str:
    """
    Extract current user ID from cookie

    Args:
        user_id: User ID from cookie

    Returns:
        User ID string

    Raises:
        HTTPException: If user is not authenticated
    """
    resolved_user_id = user_id or x_user_id
    if not resolved_user_id or not is_authenticated(resolved_user_id):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return resolved_user_id


# ==================== Authentication Endpoints ====================

@app.post("/login")
def login_endpoint(credentials: LoginRequest, response: Response):
    """Login endpoint with email and password"""
    # Verify user credentials
    success, user_id, message = verify_user(credentials.email, credentials.password)

    if success:
        print(f"[AUTH] Login success for email={credentials.email} user_id={user_id}")
        # Create session
        create_session(user_id)
        # Set user_id as cookie
        response.set_cookie(
            key="user_id",
            value=user_id,
            httponly=True,
            samesite="lax",
            secure=False,
            max_age=60 * 60 * 24
        )
        return {
            "status": "success",
            "message": "Login successful",
            "user_id": user_id,
            "email": credentials.email
        }
    else:
        print(f"[AUTH] Login failed for email={credentials.email}: {message}")
        raise HTTPException(status_code=401, detail=message)


@app.post("/register")
def register_endpoint(request: RegisterRequest, response: Response):
    """Register a new user"""
    # Register user
    result = register_user(request.email, request.password, request.confirm_password)

    if result["success"]:
        # Auto-login after registration
        user_id = result["user_id"]
        create_session(user_id)
        ensure_user_directories_exist(user_id)
        # Set user_id as cookie
        response.set_cookie(
            key="user_id",
            value=user_id,
            httponly=True,
            samesite="lax",
            secure=False,
            max_age=60 * 60 * 24
        )
        return {
            "status": "success",
            "message": "Registration successful",
            "user_id": user_id,
            "email": result["email"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["message"])


@app.get("/logout")
def logout(response: Response, user_id: str = Depends(get_current_user_id)):
    """Logout endpoint"""
    destroy_session(user_id)
    # Clear the user_id cookie
    response.delete_cookie(key="user_id", samesite="lax", secure=False)
    return {
        "status": "success",
        "message": "Logout successful"
    }


@app.get("/auth-status")
def auth_status(
    user_id: Optional[str] = Cookie(None),
    x_user_id: Optional[str] = Header(None)
):
    """Check authentication status"""
    resolved_user_id = user_id or x_user_id
    if resolved_user_id and is_authenticated(resolved_user_id):
        user_info = get_user_by_id(resolved_user_id)
        return {
            "authenticated": True,
            "user_id": resolved_user_id,
            "email": user_info.get("email") if user_info else None
        }
    if user_id or x_user_id:
        print(f"[AUTH] auth-status rejected: cookie_user_id={user_id}, header_user_id={x_user_id}")
    return {
        "authenticated": False
    }


# ==================== Upload Endpoints ====================

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), user_id: str = Depends(get_current_user_id)):
    """Upload and process a document"""
    temp_file_path = None
    try:
        print(f"[UPLOAD] Starting upload for file: {file.filename} by user: {user_id}")

        # Save uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        content = await file.read()
        with open(temp_file_path, "wb") as f:
            f.write(content)

        print(f"[UPLOAD] File saved temporarily: {temp_file_path}")

        # Create a file-like object wrapper with proper methods
        class FileObj:
            def __init__(self, path, filename):
                self.path = path
                self.filename = filename

            def save(self, dest):
                """Save file to destination"""
                import shutil
                shutil.copy(self.path, dest)

            def read(self):
                with open(self.path, "rb") as f:
                    return f.read()

        file_obj = FileObj(temp_file_path, file.filename)
        result = upload_document(file_obj, user_id)

        print(f"[UPLOAD] Processing complete: {result}")

        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result["message"])

    except HTTPException:
        raise
    except Exception as e:
        print(f"[UPLOAD ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    finally:
        # Clean up temp file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass


# ==================== Document Endpoints ====================

@app.get("/dashboard-data")
def get_dashboard_data(user_id: str = Depends(get_current_user_id)):
    """Get dashboard statistics and recent documents"""
    try:
        total_documents = get_document_count(user_id)
        recent_files = get_recent_documents(user_id, count=5)

        return {
            "total_documents": total_documents,
            "recent_files": recent_files,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents")
def list_documents(user_id: str = Depends(get_current_user_id)):
    """Get list of all documents"""
    try:
        documents = get_all_documents(user_id)
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/document/{filename}")
def get_document_details(filename: str, user_id: str = Depends(get_current_user_id)):
    """Get details for a specific document"""
    try:
        document = get_document(filename, user_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/document/{filename}")
def delete_document_endpoint(filename: str, user_id: str = Depends(get_current_user_id)):
    """Delete a document"""
    try:
        result = delete_document(filename, user_id)
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
def download_document(filename: str, user_id: str = Depends(get_current_user_id)):
    """Download a document"""
    try:
        from .utils.file_handler import get_user_documents_dir
        user_documents_dir = get_user_documents_dir(user_id)
        file_path = os.path.join(user_documents_dir, filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/octet-stream"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/view/{filename}")
def view_document_inline(filename: str, user_id: str = Depends(get_current_user_id)):
    """Serve a document inline for in-browser preview (PDF, images).
    Unlike /download, this uses the correct MIME type and Content-Disposition: inline
    so browsers render the file instead of downloading it."""
    try:
        user_documents_dir = get_user_documents_dir(user_id)
        file_path = os.path.join(user_documents_dir, filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        ext = get_file_extension(filename)
        mime_map = {
            ".pdf": "application/pdf",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".doc": "application/msword",
        }
        media_type = mime_map.get(ext, "application/octet-stream")

        return FileResponse(
            path=file_path,
            media_type=media_type,
            headers={"Content-Disposition": f"inline; filename=\"{filename}\""},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/preview/{filename}")
def preview_document(filename: str, user_id: str = Depends(get_current_user_id)):
    """Get document preview data (extracted text and content type)"""
    try:
        # Determine content type from file extension
        ext = get_file_extension(filename)
        content_type_map = {
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".doc": "application/msword",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
        }
        content_type = content_type_map.get(ext, "application/octet-stream")

        # Get extracted text
        text_path = get_extracted_text_path(filename, user_id)
        extracted_text = ""
        if os.path.exists(text_path):
            with open(text_path, "r", encoding="utf-8") as f:
                extracted_text = f.read()

        # Get download URL for binary preview (PDF/images)
        download_url = f"/view/{filename}"

        return {
            "filename": filename,
            "content_type": content_type,
            "extracted_text": extracted_text,
            "download_url": download_url,
            "file_extension": ext,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Search Endpoints ====================

@app.post("/search")
def search_documents(request: SearchRequest, user_id: str = Depends(get_current_user_id)):
    """Search documents"""
    try:
        if request.search_type == "keyword":
            results = keyword_search(request.query, user_id=user_id, top_k=request.top_k)
        elif request.search_type == "topic":
            results = keyword_search(request.query, user_id=user_id, top_k=request.top_k)
        elif request.search_type == "semantic":
            results = semantic_search(request.query, user_id=user_id, top_k=request.top_k)
        else:  # combined
            results = combined_search(request.query, user_id=user_id, top_k=request.top_k)

        return {
            "query": request.query,
            "search_type": request.search_type,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/keyword-search")
def keyword_search_endpoint(q: str, top_k: int = 10, user_id: str = Depends(get_current_user_id)):
    """Keyword search endpoint"""
    try:
        results = keyword_search(q, user_id=user_id, top_k=top_k)
        return {
            "query": q,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/semantic-search")
def semantic_search_endpoint(q: str, top_k: int = 10, user_id: str = Depends(get_current_user_id)):
    """Semantic search endpoint"""
    try:
        results = semantic_search(q, user_id=user_id, top_k=top_k)
        return {
            "query": q,
            "search_type": "topic_keyword",
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/topic-search")
def topic_search_endpoint(q: str, top_k: int = 10, user_id: str = Depends(get_current_user_id)):
    """Topic/keyword search endpoint"""
    try:
        results = keyword_search(q, user_id=user_id, top_k=top_k)
        return {
            "query": q,
            "search_type": "topic_keyword",
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/similar/{filename}")
def get_similar_documents_endpoint(filename: str, top_k: int = 5, user_id: str = Depends(get_current_user_id)):
    """Get documents similar to a given document"""
    try:
        results = get_similar_documents(filename, user_id=user_id, top_k=top_k)
        return {
            "reference_file": filename,
            "similar_documents": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Health Check ====================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/")
def root():
    """Serve React frontend"""
    react_build = os.path.join(
        paths_config.get("project_root", ""), "frontend-react", "dist", "index.html"
    )
    if os.path.exists(react_build):
        return FileResponse(react_build, media_type="text/html")
    raise HTTPException(
        status_code=503,
        detail="Frontend not built. Run 'cd frontend-react && npm run build' first."
    )


# ==================== Startup ====================

@app.on_event("startup")
async def startup_event():
    """Initialize database and directories on startup"""
    try:
        # Initialize database tables
        init_db()
        print("✓ Database tables initialized")
    except Exception as e:
        print(f"✗ Database initialization error: {str(e)}")

    # Initialize directories
    ensure_directories_exist()

    # Mount React build if available
    react_build_dir = os.path.join(
        paths_config.get("project_root", ""), "frontend-react", "dist"
    )
    if os.path.exists(react_build_dir):
        app.mount("/assets", StaticFiles(directory=os.path.join(react_build_dir, "assets")), name="react-assets")
        print(f"✓ React frontend build mounted from {react_build_dir}")
    else:
        print("ℹ React frontend build not found - using legacy frontend")

    print("✓ Application started - Directories initialized")


if __name__ == "__main__":
    import uvicorn
    init_db()
    ensure_directories_exist()

    # Load API config
    api_config = get_api_config()
    host = api_config.get("host", "0.0.0.0")
    port = api_config.get("port", 8000)

    print(f"\n🚀 Starting API server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
