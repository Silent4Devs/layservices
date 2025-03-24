from sqlalchemy import Column, Integer, String, DateTime, Enum, UniqueConstraint
from .base import Base
import enum
import sqlalchemy as sa

class DocumentClassification(enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

class ProcessedDocument(Base):
    __tablename__ = 'processed_documents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False, unique=True)
    checksum = Column(String(64), unique=True)
    status = Column(
        Enum(
            DocumentClassification,
            name="documentsclassifcation",  
            create_constraint=True,
            validate_strings=True
        ),
        nullable=False
    )
    created_at = Column(DateTime, server_default=sa.text('now()'))

    __table_args__ = (
        UniqueConstraint('checksum', name='uq_processed_documents_checksum'),
    )
