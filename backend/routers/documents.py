"""
IntelCredit - Document Upload & Parsing Routes
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import os
import shutil

from services.document_parser import document_parser
from models.database import db
import config

router = APIRouter(prefix="/api/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form("other"),
    company_id: Optional[str] = Form(None),
):
    """
    Upload and parse a document (PDF, Excel, CSV, JSON).
    Extracts structured data based on document type.
    """
    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in config.ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"File type {ext} not supported. Allowed: {config.ALLOWED_EXTENSIONS}")
    
    # Save file
    file_path = os.path.join(config.UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Parse document
    try:
        extracted_data = await document_parser.parse_document(file_path, document_type)
    except Exception as e:
        raise HTTPException(500, f"Failed to parse document: {str(e)}")
    
    # Store in database
    doc_id = db.store_document(file.filename, document_type, extracted_data)
    
    return {
        "status": "success",
        "document_id": doc_id,
        "filename": file.filename,
        "document_type": document_type,
        "extracted_data": extracted_data,
    }


@router.get("/list")
async def list_documents():
    """List all uploaded/parsed documents."""
    return {"documents": list(db.documents.values())}


@router.get("/{doc_id}")
async def get_document(doc_id: str):
    """Get a specific document's extraction data."""
    doc = db.documents.get(doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    return doc
