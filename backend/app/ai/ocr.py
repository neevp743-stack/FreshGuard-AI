import re
from datetime import datetime
from typing import Optional, Dict, Any
from app.schemas.schemas import OCRScanResponse

EXPIRY_REGEX_PATTERNS = [
    r'(?:EXP|EXPIRY|USE BY|BEST BEFORE|BB|B\.BEFORE)[\:\s]*([0-9O]{1,2}[\/\.\-][0-9O]{1,2}[\/\.\-][0-9O]{2,4})',
    r'(?:EXP|EXPIRY|USE BY|BEST BEFORE|BB)[\:\s]*([0-9O]{1,2}\s+[A-Za-z]{3,9}\s+[0-9O]{2,4})',
    r'([0-9O]{1,2}[\/\.\-][0-9O]{1,2}[\/\.\-][0-9O]{2,4})',
]

MFG_REGEX_PATTERNS = [
    r'(?:MFG|PKD|PACKED|MFD)[\:\s]*([0-9O]{1,2}[\/\.\-][0-9O]{1,2}[\/\.\-][0-9O]{2,4})',
    r'(?:MFG|PKD|PACKED|MFD)[\:\s]*([0-9O]{1,2}\s+[A-Za-z]{3,9}\s+[0-9O]{2,4})',
]

BATCH_REGEX_PATTERNS = [
    r'(?:BATCH|B\.NO|LOT)[\:\s]*([A-Z0-9\-]+)',
]

QUANTITY_REGEX_PATTERNS = [
    r'(\d+(?:\.\d+)?)\s*(L|ml|g|kg|pcs|pack|oz)',
]

def sanitize_ocr_date(date_str: str) -> str:
    """Correct common OCR confusion such as replacing 'O' or 'o' with '0' in dates."""
    cleaned = date_str.strip()
    cleaned = re.sub(r'(?<=\d)O|O(?=\d)|(?<=\d)o|o(?=\d)|^O(?=\/)', '0', cleaned)
    return cleaned

def parse_package_ocr_text(raw_text: str) -> OCRScanResponse:
    """
    Intelligent packaging OCR parser.
    Extracts product details, expiry dates, mfg dates, quantity, and batch numbers.
    Never silently trusts OCR: returns extracted data with a calculated confidence score.
    """
    text = raw_text.strip()
    if not text:
        return OCRScanResponse(
            detected=False,
            confidence_score=0.0
        )
    
    extracted_expiry = None
    extracted_mfg = None
    extracted_batch = None
    extracted_qty = None
    extracted_unit = None
    confidence = 0.50

    # 1. Extract Expiry Date
    for pattern in EXPIRY_REGEX_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw_d = match.group(1).strip()
            extracted_expiry = sanitize_ocr_date(raw_d)
            confidence += 0.25
            break
            
    # 2. Extract Manufacturing Date
    for pattern in MFG_REGEX_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw_m = match.group(1).strip()
            extracted_mfg = sanitize_ocr_date(raw_m)
            confidence += 0.10
            break

    # 3. Extract Batch Number
    for pattern in BATCH_REGEX_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted_batch = match.group(1).strip()
            break

    # 4. Extract Quantity/Unit
    for pattern in QUANTITY_REGEX_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted_qty = float(match.group(1))
            extracted_unit = match.group(2)
            confidence += 0.10
            break

    # 5. Extract Product Name guess (First line or keywords)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    guessed_name = "Scanned Grocery Item"
    guessed_brand = None

    if lines:
        guessed_name = lines[0]
        if len(lines) > 1 and not re.search(r'exp|mfg|batch|b.no', lines[1], re.IGNORECASE):
            guessed_brand = lines[0]
            guessed_name = lines[1]

    confidence = min(0.96, confidence)

    return OCRScanResponse(
        detected=True,
        product_name=guessed_name,
        brand=guessed_brand,
        expiry_date=extracted_expiry,
        mfg_date=extracted_mfg,
        quantity=extracted_qty or 1.0,
        unit=extracted_unit or "pcs",
        batch_number=extracted_batch,
        confidence_score=round(confidence * 100, 1),
        raw_text=text
    )
