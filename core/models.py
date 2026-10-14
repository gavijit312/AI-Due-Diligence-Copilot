import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from core.database import Base


class DocumentRecord(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    doc_type = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    page_count = Column(String(50), default="0")
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class AuditRun(Base):
    __tablename__ = "audit_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    target_company = Column(String(255), nullable=True)
    status = Column(String(50), default="PENDING")
    risk_score = Column(String(50), nullable=True)
    report = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)