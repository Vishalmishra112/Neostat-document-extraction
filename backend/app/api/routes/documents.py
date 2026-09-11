import time
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from backend.app.services.extraction_service import extract_document_data

router = APIRouter(prefix="/documents", tags=["Documents"])

MASTER_SCHEMA = {
    "document_type": "invoice or balance_sheet",
    "confidence_score": "95%",
    "extracted_data": {}
}

@router.post("/process")
async def process_document(
    file: UploadFile = File(...)
):
    start_time = time.time()
    file_bytes = await file.read()
    
    try:
        result = extract_document_data(
            file_bytes=file_bytes,
            filename=file.filename,
            extracted_text="",
            json_schema=MASTER_SCHEMA
        )
        
        processing_time = round(time.time() - start_time, 2)
        
        return {
            "status": "success",
            "filename": file.filename,
            "processing_time_seconds": processing_time,
            "result": result
        }
    except Exception as e:
        print(f"Extraction Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during AI extraction."
        )