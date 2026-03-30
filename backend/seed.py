"""
Seed script — inserts 2 dummy completed documents with 5 issues each.
Run from project root: python -m backend.seed
"""
import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.config import get_settings
from backend.models.document import Document, DocumentStatus
from backend.models.issue import Issue, IssueSeverity

settings = get_settings()

engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

DUMMY_DOCS = [
    {
        "filename": "structural_plan_floor1.pdf",
        "file_path": "./uploads/seed_structural_plan_floor1.pdf",
        "page_count": 4,
    },
    {
        "filename": "mechanical_hvac_layout.pdf",
        "file_path": "./uploads/seed_mechanical_hvac_layout.pdf",
        "page_count": 6,
    },
]

DUMMY_ISSUES = [
    {
        "page_number": 1,
        "issue_type": "missing_tag",
        "severity": IssueSeverity.high,
        "description": "HVAC diffuser in room 102 is missing equipment tag. All diffusers require a DIF-XXXX tag per spec section 15820.",
        "location_hint": "top-right quadrant, room 102",
        "raw_ocr_text": "ROOM 102 OFFICE 450 SF  DIFFUSER (no tag) CFM: 200",
    },
    {
        "page_number": 1,
        "issue_type": "dimension_mismatch",
        "severity": IssueSeverity.high,
        "description": "Corridor width shown as 4'-0\" on plan but referenced as 5'-0\" in section cut A/S-3. Dimensions must be reconciled.",
        "location_hint": "center corridor, between grids C and D",
        "raw_ocr_text": "CORRIDOR W=4'-0\"  REF: SEE SECTION A/S-3 (5'-0\")",
    },
    {
        "page_number": 2,
        "issue_type": "missing_scale",
        "severity": IssueSeverity.medium,
        "description": "Page 2 detail sheet has no scale bar or written scale reference. All detail sheets must include a graphic scale.",
        "location_hint": "bottom title block",
        "raw_ocr_text": "DETAIL 3  STAIR NOSING CONDITION  NTS",
    },
    {
        "page_number": 2,
        "issue_type": "unlabeled_element",
        "severity": IssueSeverity.medium,
        "description": "Unidentified rectangular element (approx 600x400mm) in plant room with no label, tag, or reference note.",
        "location_hint": "plant room, bottom-left corner",
        "raw_ocr_text": "PLANT ROOM  AHU-1  [unlabeled box]  PUMP-1",
    },
    {
        "page_number": 3,
        "issue_type": "inconsistent_annotation",
        "severity": IssueSeverity.low,
        "description": "General note 7 states 'all exposed piping to be insulated' but detail 4B shows uninsulated pipe in ceiling space. Conflict requires clarification.",
        "location_hint": "top-left notes block",
        "raw_ocr_text": "GENERAL NOTES: 7. ALL EXPOSED PIPING TO BE INSULATED PER SPEC 15080",
    },
]


async def seed():
    async with AsyncSessionLocal() as db:
        for i, doc_data in enumerate(DUMMY_DOCS):
            doc_id = uuid.uuid4()
            document = Document(
                id=doc_id,
                filename=doc_data["filename"],
                file_path=doc_data["file_path"],
                page_count=doc_data["page_count"],
                status=DocumentStatus.completed,
                uploaded_at=datetime.utcnow() - timedelta(hours=i * 3 + 1),
                analyzed_at=datetime.utcnow() - timedelta(hours=i * 3),
            )
            db.add(document)
            await db.flush()

            for issue_data in DUMMY_ISSUES:
                issue = Issue(
                    id=uuid.uuid4(),
                    document_id=doc_id,
                    page_number=issue_data["page_number"],
                    issue_type=issue_data["issue_type"],
                    severity=issue_data["severity"],
                    description=issue_data["description"],
                    location_hint=issue_data["location_hint"],
                    raw_ocr_text=issue_data["raw_ocr_text"],
                    created_at=datetime.utcnow(),
                )
                db.add(issue)

        await db.commit()
        print("Seed complete: 2 documents, 5 issues each inserted.")


if __name__ == "__main__":
    asyncio.run(seed())
