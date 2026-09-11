import io
from pypdf import PdfReader

def validate_file(file_bytes: bytes, filename: str) -> dict:
    """Validates file type, size, and page limits."""
    if not file_bytes:
        return {"status": "FAILED", "is_readable": False, "error": "Empty file"}

    filename_lower = filename.lower()
    is_pdf = filename_lower.endswith(".pdf")
    is_img = filename_lower.endswith((".jpg", ".jpeg", ".png"))

    if not (is_pdf or is_img):
        return {"status": "FAILED", "is_supported": False, "error": "Unsupported file format"}

    page_count = 1
    if is_pdf:
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            page_count = len(reader.pages)
            if page_count > 3:
                return {
                    "status": "FAILED", 
                    "page_count": page_count, 
                    "error": "Page limit exceeded (max 3 pages)"
                }
        except Exception:
            return {"status": "FAILED", "is_readable": False, "error": "Corrupted or unreadable PDF"}

    return {
        "file_type": "application/pdf" if is_pdf else f"image/{filename_lower.split('.')[-1]}",
        "is_supported": True,
        "is_readable": True,
        "page_count": page_count,
        "status": "PASS"
    }