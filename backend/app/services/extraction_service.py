import json
from google import genai
from google.genai import types
from backend.app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def extract_document_data(file_bytes: bytes, filename: str, extracted_text: str, json_schema: dict) -> dict:
    mime_type = "application/pdf"
    filename_lower = filename.lower()
    if filename_lower.endswith((".jpg", ".jpeg")):
        mime_type = "image/jpeg"
    elif filename_lower.endswith(".png"):
        mime_type = "image/png"

    prompt = f"""
    You are an expert financial document intelligence and classification system.
    1. Analyze the provided document and automatically classify its type as either "invoice" or "balance_sheet".
    2. Extract all meaningful fields, tables, and financial items.
    3. Provide a confidence score represented as a percentage string from 0% to 100% (e.g., "98%") representing how certain you are of the accuracy of the extracted data.
    
    You MUST return ONLY a strictly valid JSON object matching the template structure below:
    {{
      "document_type": "invoice" (or "balance_sheet"),
      "confidence_score": "98%",
      "extracted_data": {{ ... fill fields according to document type ... }}
    }}
    
    Template Schema Structure:
    {json.dumps(json_schema)}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.0
            )
        )
        
        content = response.text.strip()
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
        
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        raise Exception(f"Failed to extract data: {str(e)}")