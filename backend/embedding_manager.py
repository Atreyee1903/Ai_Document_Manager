"""
Embedding Manager Module
Manages embeddings for semantic search using Sentence Transformers
"""

import pickle
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from .utils.file_handler import get_user_embeddings_path, ensure_user_directories_exist


MODEL_NAME = "all-MiniLM-L6-v2"


def load_model():
    """Load the sentence transformer model"""
    try:
        model = SentenceTransformer(MODEL_NAME)
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None


def create_embedding(text):
    """
    Create embedding for given text

    Args:
        text: Text to embed

    Returns:
        Embedding vector or None
    """
    try:
        if not text or len(text.strip()) == 0:
            return None

        model = load_model()
        if model is None:
            return None

        embedding = model.encode(text, convert_to_tensor=False)
        return embedding.tolist()

    except Exception as e:
        print(f"Error creating embedding: {str(e)}")
        return None


def load_embeddings(user_id):
    """Load all embeddings from pickle file for a user"""
    embeddings_file = get_user_embeddings_path(user_id)
    if os.path.exists(embeddings_file):
        try:
            with open(embeddings_file, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading embeddings: {str(e)}")

    return {}


def save_embeddings(embeddings_dict, user_id):
    """Save embeddings to pickle file for a user"""
    try:
        ensure_user_directories_exist(user_id)
        embeddings_file = get_user_embeddings_path(user_id)
        os.makedirs(os.path.dirname(embeddings_file), exist_ok=True)
        with open(embeddings_file, 'wb') as f:
            pickle.dump(embeddings_dict, f)
        return True
    except Exception as e:
        print(f"Error saving embeddings: {str(e)}")
    return False


def add_embedding(filename, text, user_id):
    """
    Add embedding for a document

    Args:
        filename: Document filename
        text: Document text to embed
        user_id: User ID

    Returns:
        True if successful
    """
    embedding = create_embedding(text)

    if embedding is None:
        return False

    embeddings = load_embeddings(user_id)
    embeddings[filename] = {
        "embedding": embedding,
        "text_preview": text[:200]  # Store preview of text
    }

    return save_embeddings(embeddings, user_id)


def get_embedding(filename, user_id):
    """Get embedding for a document"""
    embeddings = load_embeddings(user_id)
    return embeddings.get(filename, None)


def delete_embedding(filename, user_id):
    """Delete embedding for a document"""
    embeddings = load_embeddings(user_id)
    if filename in embeddings:
        del embeddings[filename]
        return save_embeddings(embeddings, user_id)
    return True


def update_embedding(filename, text, user_id):
    """Update embedding for a document"""
    return delete_embedding(filename, user_id) and add_embedding(filename, text, user_id)


def get_all_embeddings(user_id):
    """Get all embeddings for a user"""
    return load_embeddings(user_id)


def embedding_exists(filename, user_id):
    """Check if embedding exists for a document"""
    embeddings = load_embeddings(user_id)
    return filename in embeddings

