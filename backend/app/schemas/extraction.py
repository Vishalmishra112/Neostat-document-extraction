from pydantic import BaseModel, Field
from typing import List, Optional, Union

class Evidence(BaseModel):
    source_text: str = Field(description="The exact snippet of text from the document.")
    page_number: int = Field(description="The page number where this value was found.")

class ExtractedValue(BaseModel):
    value: Union[str, float, None] = Field(description="The extracted value. Null if not found.")
    evidence: Optional[Evidence] = Field(description="Grounding evidence for the value.")

class InvoiceLineItem(BaseModel):
    description: str | None
    quantity: float | None
    unit_price: float | None
    amount: float | None

class InvoiceSchema(BaseModel):
    invoice_number: ExtractedValue
    invoice_date: ExtractedValue
    vendor_name: ExtractedValue
    customer_name: ExtractedValue
    currency: ExtractedValue
    subtotal: ExtractedValue
    tax_amount: ExtractedValue
    discount: ExtractedValue
    total_amount: ExtractedValue
    line_items: List[InvoiceLineItem]