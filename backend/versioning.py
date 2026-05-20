"""
Versioning Module
Handles document versioning - creates new versions instead of overwriting
"""

import os
from .utils.file_handler import DOCUMENTS_DIR


def get_next_version(filename):
    """
    Get the next version number for a file
    
    Example:
        resume.pdf -> resume_v1.pdf
        resume_v1.pdf -> resume_v2.pdf
        
    Args:
        filename: Original filename
        
    Returns:
        New versioned filename
    """
    base_name = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    
    # If file has _vX pattern, increment version
    if '_v' in base_name:
        parts = base_name.rsplit('_v', 1)
        try:
            version = int(parts[1])
            base = parts[0]
            next_version = version + 1
        except ValueError:
            # If can't parse version, start with v1
            base = base_name
            next_version = 1
    else:
        # First version
        base = base_name
        next_version = 1
    
    return f"{base}_v{next_version}{extension}"


def get_all_versions(base_filename, documents_path=None):
    """
    Get all versions of a file
    
    Args:
        base_filename: Base filename without version
        
    Returns:
        List of all versions of the file
    """
    base_name = os.path.splitext(base_filename)[0]
    extension = os.path.splitext(base_filename)[1]
    
    versions = []
    documents_path = documents_path or DOCUMENTS_DIR
    
    if os.path.exists(documents_path):
        for file in os.listdir(documents_path):
            # Check if file matches the base name pattern
            if file.startswith(base_name):
                versions.append(file)
    
    # Sort versions
    versions.sort()
    return versions


def get_latest_version(base_filename):
    """Get the latest version of a file"""
    versions = get_all_versions(base_filename)
    return versions[-1] if versions else None


def create_versioned_filename(filename, documents_path=None):
    """
    Create a versioned filename if file already exists
    
    Args:
        filename: Original filename
        
    Returns:
        Versioned filename
    """
    documents_path = documents_path or DOCUMENTS_DIR
    full_path = os.path.join(documents_path, filename)
    
    if os.path.exists(full_path):
        # File exists, create new version
        return get_next_version(filename)
    else:
        # File doesn't exist, use original name
        return filename


def get_base_filename(versioned_filename):
    """
    Extract base filename from versioned filename
    
    Example:
        resume_v2.pdf -> resume
        
    Args:
        versioned_filename: Versioned filename
        
    Returns:
        Base filename without version and extension
    """
    base_name = os.path.splitext(versioned_filename)[0]
    
    if '_v' in base_name:
        return base_name.rsplit('_v', 1)[0]
    
    return base_name
