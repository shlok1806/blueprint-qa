import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database import get_db
from backend.models.document import Document, DocumentStatus
from backend.schemas.issue import IssueRead, IssueSummary
from backend.services.qa_service import run_analysis, get_issues

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.post("/{document_id}/run", response_model=list[IssueRead])
async def trigger_analysis(document_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    if document.status == DocumentStatus.processing:
        raise HTTPException(status_code=409, detail="Analysis already in progress.")

    try:
        issues = await run_analysis(document_id, db)
        return [IssueRead.model_validate(i) for i in issues]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/{document_id}/issues", response_model=list[IssueRead])
async def fetch_issues(document_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == document_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Document not found.")

    issues = await get_issues(document_id, db)
    return [IssueRead.model_validate(i) for i in issues]


@router.get("/{document_id}/summary", response_model=IssueSummary)
async def fetch_summary(document_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == document_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Document not found.")

    issues = await get_issues(document_id, db)
    by_severity: dict[str, int] = {}
    by_type: dict[str, int] = {}
    for issue in issues:
        sev = issue.severity.value
        by_severity[sev] = by_severity.get(sev, 0) + 1
        by_type[issue.issue_type] = by_type.get(issue.issue_type, 0) + 1

    return IssueSummary(total=len(issues), by_severity=by_severity, by_type=by_type)
