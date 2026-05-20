"""
Metadata Manager Module
Manages document metadata (title, tags, upload date, version, etc.)
"""

from datetime import datetime
from .utils.json_handler import (
    load_metadata, save_metadata, update_document_metadata,
    get_document_metadata, delete_document_metadata
)
from .utils.file_handler import get_user_documents_dir, DOCUMENTS_DIR
import os


def create_document_metadata(filename, tags=None, user_id=None):
    """
    Create metadata for a new document

    Args:
        filename: Filename with version
        tags: List of tags
        user_id: User ID

    Returns:
        Metadata dictionary
    """
    if tags is None:
        tags = []

    metadata = {
        "file_name": filename,
        "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tags": tags,
        "version": extract_version_number(filename),
        "file_size": get_file_size(filename, user_id)
    }

    return metadata


def extract_version_number(filename):
    """
    Extract version number from filename

    Example:
        resume_v2.pdf -> 2
        resume.pdf -> 1

    Args:
        filename: Filename

    Returns:
        Version number
    """
    base_name = os.path.splitext(filename)[0]

    if '_v' in base_name:
        try:
            version = int(base_name.rsplit('_v', 1)[1])
            return version
        except ValueError:
            return 1

    return 1


def get_file_size(filename, user_id=None):
    """Get file size in KB"""
    try:
        if user_id:
            file_path = os.path.join(get_user_documents_dir(user_id), filename)
        else:
            file_path = os.path.join(DOCUMENTS_DIR, filename)
        size_bytes = os.path.getsize(file_path)
        return round(size_bytes / 1024, 2)  # Convert to KB
    except Exception as e:
        print(f"Error getting file size: {str(e)}")
        return 0


def update_tags(filename, tags, user_id):
    """
    Update tags for a document

    Args:
        filename: Filename
        tags: List of tags
        user_id: User ID

    Returns:
        True if successful
    """
    metadata = get_document_metadata(filename, user_id)
    if metadata:
        metadata['tags'] = tags
        return update_document_metadata(filename, metadata, user_id)
    return False


def add_tag(filename, tag, user_id):
    """
    Add a tag to a document

    Args:
        filename: Filename
        tag: Tag to add
        user_id: User ID

    Returns:
        True if successful
    """
    metadata = get_document_metadata(filename, user_id)
    if metadata:
        if tag not in metadata.get('tags', []):
            metadata['tags'].append(tag)
            return update_document_metadata(filename, metadata, user_id)
    return False


def get_tags(filename, user_id):
    """
    Get tags for a document

    Args:
        filename: Filename
        user_id: User ID

    Returns:
        List of tags
    """
    metadata = get_document_metadata(filename, user_id)
    return metadata.get('tags', []) if metadata else []


def delete_document(filename, user_id):
    """
    Delete document and its metadata

    Args:
        filename: Filename
        user_id: User ID

    Returns:
        True if successful
    """
    return delete_document_metadata(filename, user_id)


def get_document_info(filename, user_id):
    """
    Get complete information for a document

    Args:
        filename: Filename
        user_id: User ID

    Returns:
        Document information dictionary
    """
    metadata = get_document_metadata(filename, user_id)

    if not metadata:
        return None

    return {
        "file_name": metadata.get("file_name"),
        "upload_date": metadata.get("upload_date"),
        "tags": metadata.get("tags", []),
        "version": metadata.get("version", 1),
        "file_size": metadata.get("file_size", 0)
    }
