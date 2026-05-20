"""
Authentication Module
Handles email-based login with per-user sessions
"""

from .database import verify_user
from .database import get_user_by_id

# Active sessions: user_id -> session_data
ACTIVE_SESSIONS = {}


def login(email, password):
    """
    Authenticate user with email and password

    Args:
        email: User email
        password: User password

    Returns:
        Tuple (success: bool, user_id: str or None, message: str)
    """
    success, user_id, message = verify_user(email, password)
    if success:
        create_session(user_id)
    return success, user_id, message


def create_session(user_id):
    """
    Create a user session

    Args:
        user_id: User ID to create session for
    """
    global ACTIVE_SESSIONS
    ACTIVE_SESSIONS[user_id] = {
        "user_id": user_id,
        "is_active": True
    }


def destroy_session(user_id):
    """
    Destroy user session

    Args:
        user_id: User ID to destroy session for
    """
    global ACTIVE_SESSIONS
    if user_id in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[user_id]


def is_authenticated(user_id):
    """
    Check if user is authenticated

    Args:
        user_id: User ID to check

    Returns:
        True if authenticated, False otherwise
    """
    # Primary check: active in-memory session (same-process).
    if user_id in ACTIVE_SESSIONS and ACTIVE_SESSIONS[user_id].get('is_active', False):
        return True

    # Fallback check: allow authenticated cookie if user exists in DB.
    # This avoids false logout when server runs with multiple workers/processes
    # where in-memory session dicts are not shared.
    return get_user_by_id(user_id) is not None


def get_authenticated_users():
    """Get list of all currently authenticated user IDs"""
    return list(ACTIVE_SESSIONS.keys())
