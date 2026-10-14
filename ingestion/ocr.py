from typing import List
from pdf2image import convert_from_path
import pytesseract
from config.settings import settings

pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD


def ocr_pdf_fallback(file_path: str) -> List[dict]:
    results = []
    try:
        images = convert_from_path(file_path)
        for page_idx, img in enumerate(images, start=1):
            text = pytesseract.image_to_string(img)
            if text.strip():
                results.append({"page": page_idx, "text": text.strip()})
    except Exception as e:
        print(f"OCR execution failure on {file_path}: {e}")
    return results