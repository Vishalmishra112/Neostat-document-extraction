def validate_invoice(extracted_data: dict) -> dict:
    """
    Validates arithmetic relationships on invoice data:
    subtotal + tax_amount - discount ≈ total_amount
    """
    def _extract_num(field):
        if isinstance(field, dict):
            val = field.get("value")
            if isinstance(val, (int, float)):
                return float(val)
        return None

    subtotal = _extract_num(extracted_data.get("subtotal"))
    tax = _extract_num(extracted_data.get("tax_amount")) or 0.0
    discount = _extract_num(extracted_data.get("discount")) or 0.0
    total = _extract_num(extracted_data.get("total_amount"))

    checks = []
    if subtotal is not None and total is not None:
        calculated = round(subtotal + tax - discount, 2)
        variance = round(abs(calculated - total), 2)
        status = "PASS" if variance <= 0.05 else "FAIL"

        checks.append({
            "name": "invoice_total_reconciliation",
            "formula": "subtotal + tax_amount - discount",
            "operands": {"subtotal": subtotal, "tax_amount": tax, "discount": discount},
            "calculated_value": calculated,
            "reported_value": total,
            "variance": variance,
            "status": status
        })
    else:
        checks.append({
            "name": "invoice_total_reconciliation",
            "status": "NOT_APPLICABLE",
            "reason": "Missing required subtotal or total_amount field"
        })

    overall_status = "PASS" if all(c.get("status") in ["PASS", "NOT_APPLICABLE"] for c in checks) else "FAILED"
    return {"checks": checks, "overall_status": overall_status}