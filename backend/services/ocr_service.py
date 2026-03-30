import logging
from pathlib import Path
from PIL import Image

logger = logging.getLogger(__name__)


def pdf_to_images(file_path: str, max_pages: int = 10) -> list[Image.Image]:
    """Convert a PDF to a list of PIL images (one per page, up to max_pages)."""
    try:
        from pdf2image import convert_from_path
    except ImportError:
        raise RuntimeError("pdf2image is not installed. Run: pip install pdf2image")

    images = convert_from_path(file_path, dpi=150, first_page=1, last_page=max_pages)
    return images


def ocr_image(image: Image.Image) -> str:
    """Extract text from a PIL image using pytesseract."""
    try:
        import pytesseract
    except ImportError:
        raise RuntimeError("pytesseract is not installed. Run: pip install pytesseract")

    try:
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        return ""


def extract_text_from_pdf(file_path: str, max_pages: int = 10) -> list[tuple[int, Image.Image, str]]:
    """
    Returns list of (page_number, image, ocr_text) tuples.
    page_number is 1-indexed.
    """
    images = pdf_to_images(file_path, max_pages=max_pages)
    results = []
    for idx, image in enumerate(images):
        page_num = idx + 1
        ocr_text = ocr_image(image)
        results.append((page_num, image, ocr_text))
        logger.info(f"OCR complete for page {page_num}, extracted {len(ocr_text)} chars")
    return results
