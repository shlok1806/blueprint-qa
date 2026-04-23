import logging
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from backend.models.document import Document, DocumentStatus
from backend.models.issue import Issue, IssueSeverity
from backend.services.ocr_service import extract_text_from_pdf
from backend.services.llm_service import analyze_page
from backend.config import get_settings
from backend.storage import get_storage

logger = logging.getLogger(__name__)
settings = get_settings()

VALID_ISSUE_TYPES = {
    "missing_tag",
    "dimension_mismatch",
    "unlabeled_element",
    "inconsistent_annotation",
    "missing_scale",
    "incomplete_detail",
}

VALID_SEVERITIES = {"low", "medium", "high"}


async def run_analysis(document_id: uuid.UUID, db: AsyncSession) -> list[Issue]:
    """
    Full QA pipeline:
    1. Load document from DB
    2. OCR all pages
    3. Analyze each page with LLM
    4. Save issues to DB
    5. Update document status
    """
    # Mark as processing
    await db.execute(
        update(Document)
        .where(Document.id == document_id)
        .values(status=DocumentStatus.processing)
    )
    await db.commit()

    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()
    if not document:
        raise ValueError(f"Document {document_id} not found")

    storage = get_storage()
    file_path = storage.get_path(document.file_path)

    try:
        page_data = extract_text_from_pdf(file_path, max_pages=settings.max_pages_per_document)
    except Exception as e:
        logger.error(f"OCR failed for document {document_id}: {e}")
        await db.execute(
            update(Document)
            .where(Document.id == document_id)
            .values(status=DocumentStatus.failed)
        )
        await db.commit()
        raise

    total_pages = len(page_data)

    # Update page count
    await db.execute(
        update(Document)
        .where(Document.id == document_id)
        .values(page_count=total_pages)
    )
    await db.commit()

    all_issues: list[Issue] = []

    for page_num, image, ocr_text in page_data:
        try:
            raw_issues = await analyze_page(image, ocr_text, page_num, total_pages)
        except Exception as e:
            logger.error(f"LLM analysis failed for document {document_id} page {page_num}: {e}")
            await db.execute(
                update(Document)
                .where(Document.id == document_id)
                .values(status=DocumentStatus.failed)
            )
            await db.commit()
            raise

        for raw in raw_issues:
            issue_type = raw.get("issue_type", "").strip()
            severity_str = raw.get("severity", "low").strip()
            description = raw.get("description", "").strip()
            location_hint = raw.get("location_hint", "").strip() or None

            if issue_type not in VALID_ISSUE_TYPES:
                logger.warning(f"Unknown issue_type '{issue_type}', skipping")
                continue
            if severity_str not in VALID_SEVERITIES:
                severity_str = "low"

            issue = Issue(
                id=uuid.uuid4(),
                document_id=document_id,
                page_number=page_num,
                issue_type=issue_type,
                severity=IssueSeverity(severity_str),
                description=description,
                location_hint=location_hint,
                raw_ocr_text=ocr_text[:4000] if ocr_text else None,
                created_at=datetime.utcnow(),
            )
            db.add(issue)
            all_issues.append(issue)

    # Mark as completed
    await db.execute(
        update(Document)
        .where(Document.id == document_id)
        .values(status=DocumentStatus.completed, analyzed_at=datetime.utcnow())
    )
    await db.commit()

    logger.info(f"Analysis complete for document {document_id}: {len(all_issues)} issues found")
    return all_issues


async def get_issues(document_id: uuid.UUID, db: AsyncSession) -> list[Issue]:
    result = await db.execute(select(Issue).where(Issue.document_id == document_id))
    return list(result.scalars().all())
