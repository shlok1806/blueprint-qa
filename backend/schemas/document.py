import uuid
from datetime import datetime
from pydantic import BaseModel
from backend.models.document import DocumentStatus


class DocumentBase(BaseModel):
    filename: str


class DocumentCreate(DocumentBase):
    file_path: str
    page_count: int | None = None


class DocumentRead(DocumentBase):
    id: uuid.UUID
    file_path: str
    page_count: int | None
    status: DocumentStatus
    uploaded_at: datetime
    analyzed_at: datetime | None
    issue_count: int = 0

    model_config = {"from_attributes": True}


class DocumentList(BaseModel):
    documents: list[DocumentRead]
    total: int
