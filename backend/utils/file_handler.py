"""
File Handler Module
Manages file operations and validation
"""

import os
from pathlib import Path

from backend.config import get_storage_config

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.jpg', '.jpeg', '.png'}
STORAGE_CONFIG = get_storage_config()
DOCUMENTS_DIR = STORAGE_CONFIG["documents_dir"]
EXTRACTED_TEXT_DIR = STORAGE_CONFIG["extracted_text_dir"]
METADATA_DIR = STORAGE_CONFIG["metadata_dir"]
EMBEDDINGS_DIR = STORAGE_CONFIG["embeddings_dir"]

# Users directory for multi-user support
USERS_DIR = STORAGE_CONFIG["users_dir"]
USER_DOCUMENTS_SUBDIR = STORAGE_CONFIG["user_documents_subdir"]
USER_EXTRACTED_TEXT_SUBDIR = STORAGE_CONFIG["user_extracted_text_subdir"]
USER_METADATA_SUBDIR = STORAGE_CONFIG["user_metadata_subdir"]
USER_EMBEDDINGS_SUBDIR = STORAGE_CONFIG["user_embeddings_subdir"]


def get_user_path(user_id):
    """Get base path for user data"""
    return os.path.join(USERS_DIR, user_id)


def get_user_documents_dir(user_id):
    """Get documents directory for user"""
    return os.path.join(get_user_path(user_id), USER_DOCUMENTS_SUBDIR)


def get_user_extracted_text_dir(user_id):
    """Get extracted text directory for user"""
    return os.path.join(get_user_path(user_id), USER_EXTRACTED_TEXT_SUBDIR)


def get_user_metadata_dir(user_id):
    """Get metadata directory for user"""
    return os.path.join(get_user_path(user_id), USER_METADATA_SUBDIR)


def get_user_embeddings_dir(user_id):
    """Get embeddings directory for user"""
    return os.path.join(get_user_path(user_id), USER_EMBEDDINGS_SUBDIR)


def get_user_metadata_path(user_id):
    """Get metadata.json file path for user"""
    return os.path.join(get_user_metadata_dir(user_id), "metadata.json")


def get_user_embeddings_path(user_id):
    """Get embeddings.pkl file path for user"""
    return os.path.join(get_user_embeddings_dir(user_id), "embeddings.pkl")


def ensure_directories_exist():
    """Create necessary directories if they don't exist"""
    directories = [
        DOCUMENTS_DIR,
        EXTRACTED_TEXT_DIR,
        METADATA_DIR,
        EMBEDDINGS_DIR,
        USERS_DIR
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def ensure_user_directories_exist(user_id):
    """Create user-specific directories if they don't exist"""
    directories = [
        get_user_documents_dir(user_id),
        get_user_extracted_text_dir(user_id),
        get_user_metadata_dir(user_id),
        get_user_embeddings_dir(user_id)
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def is_allowed_file(filename):
    """Check if file has an allowed extension"""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


def get_file_size(file_path):
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        return 0


def delete_file(file_path):
    """Delete a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"Error deleting file: {str(e)}")
    return False


def get_file_extension(filename):
    """Get file extension"""
    return os.path.splitext(filename)[1].lower()


def list_files_in_directory(directory):
    """List all files in a directory"""
    try:
        if os.path.exists(directory):
            return os.listdir(directory)
    except Exception as e:
        print(f"Error listing files: {str(e)}")
    return []


def get_extracted_text_path(filename, user_id=None):
    """
    Get path for extracted text file

    Args:
        filename: Original filename
        user_id: User ID (if None, uses global path for backward compatibility)

    Returns:
        Path to extracted text file
    """
    base_name = os.path.splitext(filename)[0]
    if user_id:
        return os.path.join(get_user_extracted_text_dir(user_id), f"{base_name}.txt")
    else:
        return os.path.join(EXTRACTED_TEXT_DIR, f"{base_name}.txt")

def save_text_file(file_path, content):
    """Save text content to file"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving file: {str(e)}")
    return False


def read_text_file(file_path):
    """Read text content from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {str(e)}")
    return ""
