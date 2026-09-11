import sqlite3
import json
from backend.app.core.database import DB_PATH

def save_document_result(document_name: str, document_type: str, status: str, result_dict: dict):
    """Saves or updates the processed document result in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    result_json = json.dumps(result_dict)
    
    cursor.execute("""
        INSERT INTO documents (document_name, document_type, processing_status, extracted_data, created_at)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(document_name) DO UPDATE SET
            document_type=excluded.document_type,
            processing_status=excluded.processing_status,
            extracted_data=excluded.extracted_data,
            created_at=CURRENT_TIMESTAMP
    """, (document_name, document_type, status, result_json))
    
    conn.commit()
    conn.close()

def get_document_by_name(document_name: str) -> dict:
    """Retrieves a specific document's results."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT extracted_data FROM documents WHERE document_name = ?", (document_name,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return json.loads(row[0])
    return None

def get_all_documents() -> list:
    """Retrieves a summary of all processed documents for the dashboard."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT document_name, document_type, processing_status, created_at FROM documents ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {"document_name": r[0], "document_type": r[1], "status": r[2], "processed_at": r[3]}
        for r in rows
    ]