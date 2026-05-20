"""
JSON Handler Module
Manages metadata storage in PostgreSQL
"""

import json
from .file_handler import get_user_metadata_path
from backend.database import SessionLocal, DocumentMetadata


def load_metadata(user_id):
    """Load all metadata for a user from database"""
    db = SessionLocal()
    try:
        documents = db.query(DocumentMetadata).filter(
            DocumentMetadata.user_id == user_id
        ).all()

        metadata = {}
        for doc in documents:
            metadata[doc.filename] = {
                "file_name": doc.filename,
                "upload_date": doc.upload_date,
                "tags": json.loads(doc.tags) if doc.tags else [],
                "skills": json.loads(doc.skills) if doc.skills else [],
                "topic_keywords": json.loads(doc.topic_keywords) if doc.topic_keywords else [],
                "version": doc.version,
                "file_size": doc.file_size
            }

        return metadata
    finally:
        db.close()


def save_metadata(data, user_id):
    """Save metadata to database (bulk update)"""
    db = SessionLocal()
    try:
        # Delete existing metadata for user
        db.query(DocumentMetadata).filter(
            DocumentMetadata.user_id == user_id
        ).delete()

        # Add new metadata
        for filename, doc_data in data.items():
            doc = DocumentMetadata(
                user_id=user_id,
                filename=filename,
                upload_date=doc_data.get("upload_date", ""),
                tags=json.dumps(doc_data.get("tags", [])),
                skills=json.dumps(doc_data.get("skills", [])),
                topic_keywords=json.dumps(doc_data.get("topic_keywords", [])),
                version=doc_data.get("version", 1),
                file_size=doc_data.get("file_size", 0)
            )
            db.add(doc)

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error saving metadata: {str(e)}")
        return False
    finally:
        db.close()


def get_document_metadata(filename, user_id):
    """Get metadata for a specific document"""
    db = SessionLocal()
    try:
        doc = db.query(DocumentMetadata).filter(
            DocumentMetadata.user_id == user_id,
            DocumentMetadata.filename == filename
        ).first()

        if doc:
            return {
                "file_name": doc.filename,
                "upload_date": doc.upload_date,
                "tags": json.loads(doc.tags) if doc.tags else [],
                "skills": json.loads(doc.skills) if doc.skills else [],
                "topic_keywords": json.loads(doc.topic_keywords) if doc.topic_keywords else [],
                "version": doc.version,
                "file_size": doc.file_size
            }

        return None
    finally:
        db.close()


def update_document_metadata(filename, doc_metadata, user_id):
    """Update or create metadata for a document"""
    db = SessionLocal()
    try:
        # Check if document exists
        existing_doc = db.query(DocumentMetadata).filter(
            DocumentMetadata.user_id == user_id,
            DocumentMetadata.filename == filename
        ).first()

        if existing_doc:
            # Update existing
            existing_doc.upload_date = doc_metadata.get("upload_date", "")
            existing_doc.tags = json.dumps(doc_metadata.get("tags", []))
            existing_doc.skills = json.dumps(doc_metadata.get("skills", []))
            existing_doc.topic_keywords = json.dumps(doc_metadata.get("topic_keywords", []))
            existing_doc.version = doc_metadata.get("version", 1)
            existing_doc.file_size = doc_metadata.get("file_size", 0)
        else:
            # Create new
            new_doc = DocumentMetadata(
                user_id=user_id,
                filename=filename,
                upload_date=doc_metadata.get("upload_date", ""),
                tags=json.dumps(doc_metadata.get("tags", [])),
                skills=json.dumps(doc_metadata.get("skills", [])),
                topic_keywords=json.dumps(doc_metadata.get("topic_keywords", [])),
                version=doc_metadata.get("version", 1),
                file_size=doc_metadata.get("file_size", 0)
            )
            db.add(new_doc)

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error updating metadata: {str(e)}")
        return False
    finally:
        db.close()


def delete_document_metadata(filename, user_id):
    """Delete metadata for a document"""
    db = SessionLocal()
    try:
        db.query(DocumentMetadata).filter(
            DocumentMetadata.user_id == user_id,
            DocumentMetadata.filename == filename
        ).delete()

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error deleting metadata: {str(e)}")
        return False
    finally:
        db.close()


def get_all_documents(user_id):
    """Get list of all documents for a user"""
    db = SessionLocal()
    try:
        documents = db.query(DocumentMetadata).filter(
            DocumentMetadata.user_id == user_id
        ).all()

        return [doc.filename for doc in documents]
    finally:
        db.close()


def get_document_count(user_id):
    """Get total number of documents for a user"""
    db = SessionLocal()
    try:
        count = db.query(DocumentMetadata).filter(
            DocumentMetadata.user_id == user_id
        ).count()

        return count
    finally:
        db.close()


def get_recent_documents(user_id, count=5):
    """Get recent documents sorted by upload date"""
    db = SessionLocal()
    try:
        documents = db.query(DocumentMetadata).filter(
            DocumentMetadata.user_id == user_id
        ).order_by(DocumentMetadata.upload_date.desc()).limit(count).all()

        result = []
        for doc in documents:
            result.append({
                "file_name": doc.filename,
                "upload_date": doc.upload_date,
                "tags": json.loads(doc.tags) if doc.tags else [],
                "skills": json.loads(doc.skills) if doc.skills else [],
                "topic_keywords": json.loads(doc.topic_keywords) if doc.topic_keywords else [],
                "version": doc.version,
                "file_size": doc.file_size
            })

        return result
    finally:
        db.close()
