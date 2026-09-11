import io
from pypdf import PdfReader

def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extracts raw text from native PDFs to feed to the LLM."""
    if filename.lower().endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file_bytes))
        full_text = ""
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                # Append a clear page marker so the LLM can cite page numbers
                full_text += f"\n--- PAGE {i + 1} ---\n{text}"
        return full_text
    else:
        return "Image OCR not yet implemented for this prototype."