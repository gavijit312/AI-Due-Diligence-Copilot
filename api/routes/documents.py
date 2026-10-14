import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.deps import get_db
from config.settings import settings
from core.models import DocumentRecord
from core.vector_store import vector_service
from ingestion.parser import parse_file
from ingestion.chunker import chunk_extracted_pages

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form(..., description="Category: legal, financial, compliance, or general"),
    db: Session = Depends(get_db)
):
    category = category.lower().strip()
    if category not in ["legal", "financial", "compliance", "general"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category must be one of: legal, financial, compliance, general"
        )

    ext = Path(file.filename).suffix.lower()
    if ext not in [".pdf", ".docx", ".xlsx", ".xls"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported format '{ext}'. Allowed: .pdf, .docx, .xlsx"
        )

    saved_path = settings.UPLOAD_DIR / file.filename
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        pages = parse_file(str(saved_path))
        chunks = chunk_extracted_pages(pages, source_filename=file.filename, category=category)
        if chunks:
            vector_service.add_documents(chunks)

        doc = DocumentRecord(
            filename=file.filename,
            file_path=str(saved_path),
            doc_type=ext.replace(".", ""),
            category=category,
            page_count=str(len(pages))
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        return {
            "id": str(doc.id),
            "filename": doc.filename,
            "category": doc.category,
            "total_pages": len(pages),
            "indexed_chunks": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(DocumentRecord).order_by(DocumentRecord.uploaded_at.desc()).all()
    return [
        {
            "id": str(d.id),
            "filename": d.filename,
            "category": d.category,
            "doc_type": d.doc_type,
            "pages": d.page_count,
            "uploaded_at": d.uploaded_at.isoformat()
        }
        for d in docs
    ]