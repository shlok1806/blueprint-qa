import uuid
from datetime import datetime
from pydantic import BaseModel
from backend.models.issue import IssueSeverity


class IssueBase(BaseModel):
    page_number: int
    issue_type: str
    severity: IssueSeverity
    description: str
    location_hint: str | None = None
    raw_ocr_text: str | None = None


class IssueCreate(IssueBase):
    document_id: uuid.UUID


class IssueRead(IssueBase):
    id: uuid.UUID
    document_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class IssueSummary(BaseModel):
    total: int
    by_severity: dict[str, int]
    by_type: dict[str, int]
