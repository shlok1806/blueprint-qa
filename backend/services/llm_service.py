import base64
import json
import logging
import io
from PIL import Image
import anthropic
from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

SYSTEM_PROMPT = """You are an expert construction drawing QA inspector. You analyze engineering drawings (mechanical, electrical, structural, civil) for quality issues. You are precise, technical, and thorough."""

USER_PROMPT_TEMPLATE = """Analyze this engineering drawing page (page {page_num} of {total_pages}) for QA issues.

OCR Text extracted from this page:
---
{ocr_text}
---

Look for these categories of issues:
- missing_tag: Elements that should have labels/tags but don't (equipment tags, room numbers, pipe labels, etc.)
- dimension_mismatch: Dimensions that appear inconsistent or contradictory
- unlabeled_element: Symbols, components, or areas that are unidentified
- inconsistent_annotation: Notes or callouts that conflict with drawing content
- missing_scale: No scale bar or scale reference present
- incomplete_detail: Sections or details referenced elsewhere but missing or truncated

Return ONLY a JSON array. Each item must have:
{{
  "issue_type": "<category from above>",
  "severity": "low" | "medium" | "high",
  "description": "<clear explanation of the issue>",
  "location_hint": "<where on the page, e.g. top-right, center, room 204>"
}}

If no issues are found, return an empty array: []"""


def _image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


async def analyze_page(
    image: Image.Image,
    ocr_text: str,
    page_num: int,
    total_pages: int,
) -> list[dict]:
    """
    Send a drawing page image + OCR text to Claude for QA analysis.
    Returns a list of issue dicts, or [] on failure.
    """
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    image_b64 = _image_to_base64(image)
    user_content = USER_PROMPT_TEMPLATE.format(
        page_num=page_num,
        total_pages=total_pages,
        ocr_text=ocr_text or "(no text extracted)",
    )

    try:
        response = await client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_b64,
                            },
                        },
                        {"type": "text", "text": user_content},
                    ],
                }
            ],
        )
        raw = response.content[0].text.strip()

        # Strip markdown code fences if present
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

        issues = json.loads(raw)
        if not isinstance(issues, list):
            logger.warning(f"LLM returned non-list for page {page_num}: {raw[:200]}")
            return []
        return issues

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM JSON for page {page_num}: {e}")
        return []
    except Exception as e:
        logger.error(f"LLM call failed for page {page_num}: {e}")
        return []
