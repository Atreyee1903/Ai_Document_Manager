"""
Configuration Management Module
Loads database and application settings from config.json
"""

import json
from pathlib import Path

DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATHS_CONFIG = {
    "project_root": str(DEFAULT_PROJECT_ROOT),
}
DEFAULT_STORAGE_CONFIG = {
    "users_dir": "users",
    "documents_dir": "documents",
    "extracted_text_dir": "extracted_text",
    "metadata_dir": "metadata",
    "embeddings_dir": "embeddings",
    "user_documents_subdir": "documents",
    "user_extracted_text_subdir": "extracted_text",
    "user_metadata_subdir": "metadata",
    "user_embeddings_subdir": "embeddings"
}


def load_config(config_file="config.json"):
    """
    Load configuration from JSON file

    Args:
        config_file: Path to config.json file

    Returns:
        Dictionary with configuration settings

    Raises:
        FileNotFoundError: If config file doesn't exist
    """
    config_path = Path(config_file)
    if not config_path.is_absolute():
        config_path = DEFAULT_PROJECT_ROOT / config_path

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_file}\n"
            f"Please copy config.example.json to config.json and update with your settings"
        )

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {config_file}: {str(e)}")


def get_database_url():
    """Get database URL from config"""
    config = load_config()
    return config.get("database", {}).get("url")


def get_api_config():
    """Get API configuration from config"""
    config = load_config()
    return config.get("api", {})


def get_security_config():
    """Get security configuration from config"""
    config = load_config()
    return config.get("security", {})


def get_storage_config():
    """
    Get resolved storage configuration from config.

    Directory values are resolved relative to project root when provided
    as relative paths.
    """
    config = load_config()
    user_storage = config.get("storage", {})
    storage = {**DEFAULT_STORAGE_CONFIG, **user_storage}
    paths = get_paths_config()
    project_root = Path(paths["project_root"])

    resolved = dict(storage)
    for key in ["users_dir", "documents_dir", "extracted_text_dir", "metadata_dir", "embeddings_dir"]:
        raw_path = Path(storage[key])
        resolved[key] = str(raw_path if raw_path.is_absolute() else (project_root / raw_path))

    return resolved


def get_paths_config():
    """Get resolved project paths from config."""
    config = load_config()
    user_paths = config.get("paths", {})
    paths = {**DEFAULT_PATHS_CONFIG, **user_paths}

    project_root = Path(paths["project_root"])
    if not project_root.is_absolute():
        project_root = DEFAULT_PROJECT_ROOT / project_root

    resolved = dict(paths)
    resolved["project_root"] = str(project_root)


    return resolved
