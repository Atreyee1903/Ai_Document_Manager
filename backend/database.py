"""
Database Module
Manages database for users and metadata (supports SQLite and PostgreSQL)
"""

import re
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

# Import configuration
from .config import get_database_url

# Database configuration from config.json
DATABASE_URL = get_database_url()

# Create SQLAlchemy engine and session factory
# SQLite needs check_same_thread=False for FastAPI's async context
connect_args = {}
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"


class DocumentMetadata(Base):
    """Document metadata model"""
    __tablename__ = "document_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    upload_date = Column(String(255), nullable=False)
    tags = Column(Text, nullable=True)  # JSON string
    skills = Column(Text, nullable=True)  # JSON string
    topic_keywords = Column(Text, nullable=True)  # JSON string
    version = Column(Integer, default=1)
    file_size = Column(Integer, default=0)

    def __repr__(self):
        return f"<DocumentMetadata {self.filename}>"


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate password strength
    Returns: Tuple (is_valid, message)
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"


def register_user(email, password, confirm_password=None):
    """
    Register a new user

    Returns:
        Dictionary with status, message, and user_id
    """
    db = SessionLocal()
    try:
        email = email.lower().strip()

        # Validate email
        if not validate_email(email):
            return {
                "success": False,
                "message": "Invalid email format"
            }

        # Check if email already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return {
                "success": False,
                "message": "Email already registered"
            }

        # Validate password
        is_valid, msg = validate_password(password)
        if not is_valid:
            return {
                "success": False,
                "message": msg
            }

        # Check password confirmation if provided
        if confirm_password and password != confirm_password:
            return {
                "success": False,
                "message": "Passwords do not match"
            }

        # Create new user
        user_id = str(uuid.uuid4())
        new_user = User(
            user_id=user_id,
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.add(new_user)
        db.commit()

        return {
            "success": True,
            "message": "User registered successfully",
            "user_id": user_id,
            "email": email
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "message": f"Registration failed: {str(e)}"
        }
    finally:
        db.close()


def verify_user(email, password):
    """
    Verify user credentials

    Returns:
        Tuple (success: bool, user_id: str or None, message: str)
    """
    db = SessionLocal()
    try:
        email = email.lower().strip()

        # Find user by email
        user = db.query(User).filter(User.email == email).first()

        if user:
            # Check password
            if check_password_hash(user.password_hash, password):
                return True, user.user_id, "Login successful"
            else:
                return False, None, "Invalid password"

        return False, None, "Email not found"
    finally:
        db.close()


def get_user(email):
    """Get user information by email"""
    db = SessionLocal()
    try:
        email = email.lower().strip()
        user = db.query(User).filter(User.email == email).first()

        if user:
            return {
                "user_id": user.user_id,
                "email": user.email,
                "created_date": user.created_date.strftime("%Y-%m-%d %H:%M:%S") if user.created_date else None
            }

        return None
    finally:
        db.close()


def get_user_by_id(user_id):
    """Get user information by user ID"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()

        if user:
            return {
                "user_id": user.user_id,
                "email": user.email,
                "created_date": user.created_date.strftime("%Y-%m-%d %H:%M:%S") if user.created_date else None
            }

        return None
    finally:
        db.close()
