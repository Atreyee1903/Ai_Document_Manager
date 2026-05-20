"""
Upload Module
Handles file upload and processing pipeline
"""

import os
from werkzeug.utils import secure_filename

from .utils.text_extractor import extract_text
from .utils.file_handler import (
    is_allowed_file
)
from .versioning import create_versioned_filename
from .metadata_manager import create_document_metadata
from .tagging import generate_tags, detect_skills, extract_topic_keywords
from .utils.json_handler import update_document_metadata


def upload_document(file, user_id):
    """
    Main upload pipeline

    Performs:
    1. Save file with versioning
    2. Extract text
    3. Generate tags and skill/topic classification
    4. Update metadata

    Args:
        file: File object from upload
        user_id: User ID for data isolation

    Returns:
        Result dictionary
    """
    try:
        # Ensure user directories exist
        from .utils.file_handler import ensure_user_directories_exist, get_user_documents_dir
        ensure_user_directories_exist(user_id)

        # Get original filename
        original_filename = secure_filename(file.filename)

        # Check if file type is allowed
        if not is_allowed_file(original_filename):
            return {
                "success": False,
                "message": f"File type not allowed. Supported: .pdf, .docx, .jpg, .png"
            }

        # Create versioned filename
        versioned_filename = create_versioned_filename(
            original_filename,
            documents_path=get_user_documents_dir(user_id)
        )

        # Save file to user-specific documents directory
        document_path = os.path.join(get_user_documents_dir(user_id), versioned_filename)
        os.makedirs(get_user_documents_dir(user_id), exist_ok=True)
        file.save(document_path)
        
        # Extract text
        extracted_text = extract_text(document_path)
        
        # Check for critical SYSTEM SETUP errors
        if "[SYSTEM SETUP REQUIRED]" in extracted_text:
            # Clean up the file since we can't process it
            os.remove(document_path)
            return {
                "success": False,
                "message": f"System setup required: {extracted_text}"
            }
        
        # If extraction had errors but we have some content, log warning but continue
        extraction_warning = ""
        if "Error" in extracted_text or "error" in extracted_text.lower():
            extraction_warning = f" (Warning: {extracted_text})"
            # Use a placeholder for text if extraction failed completely
            if len(extracted_text) < 50:
                extracted_text = f"[Document uploaded but text extraction had issues. Manual review recommended. Original error: {extracted_text}]"
        
        # Generate tags and classification metadata
        tags = generate_tags(extracted_text)
        skills = detect_skills(extracted_text)
        topic_keywords = extract_topic_keywords(extracted_text, limit=25)

        # Save extracted text
        from backend.utils.file_handler import save_text_file, get_extracted_text_path
        extracted_text_path = get_extracted_text_path(versioned_filename, user_id)
        save_text_file(extracted_text_path, extracted_text)

        # Create and save metadata
        metadata = create_document_metadata(versioned_filename, tags, user_id)
        metadata["skills"] = skills
        metadata["topic_keywords"] = topic_keywords
        update_document_metadata(versioned_filename, metadata, user_id)

        return {
            "success": True,
            "message": "Document uploaded successfully" + extraction_warning,
            "file_name": versioned_filename,
            "tags": tags,
            "skills": skills,
            "topic_keywords": topic_keywords,
            "metadata": metadata
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Upload failed: {str(e)}"
        }


def delete_document(filename, user_id):
    """
    Delete a document and its associated files

    Args:
        filename: Filename to delete
        user_id: User ID

    Returns:
        Result dictionary
    """
    try:
        # Delete main document
        from .utils.file_handler import get_user_documents_dir
        user_documents_dir = get_user_documents_dir(user_id)
        document_path = os.path.join(user_documents_dir, filename)
        if os.path.exists(document_path):
            os.remove(document_path)

        # Delete extracted text
        from backend.utils.file_handler import get_extracted_text_path
        extracted_path = get_extracted_text_path(filename, user_id)
        if os.path.exists(extracted_path):
            os.remove(extracted_path)

        # Delete metadata
        from backend.metadata_manager import delete_document as delete_doc_metadata
        delete_doc_metadata(filename, user_id)

        return {
            "success": True,
            "message": "Document deleted successfully"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Delete failed: {str(e)}"
        }


def get_document(filename, user_id):
    """
    Get document details including all associated data

    Args:
        filename: Filename
        user_id: User ID

    Returns:
        Document details dictionary
    """
    try:
        from .utils.file_handler import get_user_documents_dir
        user_documents_dir = get_user_documents_dir(user_id)
        document_path = os.path.join(user_documents_dir, filename)

        if not os.path.exists(document_path):
            return None

        # Get metadata
        from backend.utils.json_handler import get_document_metadata
        metadata = get_document_metadata(filename, user_id)

        if metadata is None:
            return None

        return {
            "file_name": filename,
            "upload_date": metadata.get("upload_date"),
            "tags": metadata.get("tags", []),
            "skills": metadata.get("skills", []),
            "topic_keywords": metadata.get("topic_keywords", []),
            "version": metadata.get("version", 1),
            "file_size": metadata.get("file_size", 0),
            "download_url": f"/download/{filename}"
        }

    except Exception as e:
        print(f"Error getting document: {str(e)}")
        return None


def get_all_documents(user_id):
    """Get list of all documents for a user"""
    try:
        from backend.utils.json_handler import get_all_documents as get_docs
        documents = get_docs(user_id)

        result = []
        for doc_file in documents:
            doc_info = get_document(doc_file, user_id)
            if doc_info:
                result.append(doc_info)

        return result

    except Exception as e:
        print(f"Error getting documents: {str(e)}")
        return []
