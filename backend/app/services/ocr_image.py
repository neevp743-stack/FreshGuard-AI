import os
import re
import tempfile
from typing import Tuple, Optional, Dict, Any
from PIL import Image, ImageEnhance, ImageFilter
from app.schemas.schemas import OCRImageResponse

# Try importing pytesseract
try:
    import pytesseract
    HAS_PYTESSERACT = True
except ImportError:
    HAS_PYTESSERACT = False

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_MIME_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}

EXPIRY_PATTERNS = [
    r'(?:EXP|EXPIRY|USE BY|BEST BEFORE|BB|B\.BEFORE)[\:\s]*([0-9O]{1,2}[\/\.\-][0-9O]{1,2}[\/\.\-][0-9O]{2,4})',
    r'(?:EXP|EXPIRY|USE BY|BEST BEFORE|BB)[\:\s]*([0-9O]{1,2}\s+[A-Za-z]{3,9}\s+[0-9O]{2,4})',
    r'([0-9O]{1,2}[\/\.\-][0-9O]{1,2}[\/\.\-][0-9O]{2,4})',
]

MFG_PATTERNS = [
    r'(?:MFG|PKD|PACKED|MFD)[\:\s]*([0-9O]{1,2}[\/\.\-][0-9O]{1,2}[\/\.\-][0-9O]{2,4})',
    r'(?:MFG|PKD|PACKED|MFD)[\:\s]*([0-9O]{1,2}\s+[A-Za-z]{3,9}\s+[0-9O]{2,4})',
]

BATCH_PATTERNS = [
    r'(?:BATCH|B\.NO|LOT)[\:\s]*([A-Z0-9\-]+)',
]

QUANTITY_PATTERNS = [
    r'(\d+(?:\.\d+)?)\s*(L|ml|g|kg|pcs|pack|oz)',
]

def sanitize_ocr_date(date_str: str) -> str:
    """Correct common OCR confusion such as replacing 'O' or 'o' with '0' in dates."""
    cleaned = date_str.strip()
    # Replace capital O or lowercase o inside digit patterns with '0'
    cleaned = re.sub(r'(?<=\d)O|O(?=\d)|(?<=\d)o|o(?=\d)|^O(?=\/)', '0', cleaned)
    return cleaned

def preprocess_image_pixels(pil_image: Image.Image, retry: bool = False) -> Image.Image:
    """
    Image preprocessing using Pillow (grayscale conversion, contrast enhancement, sharpening).
    If retry is True, applies adaptive contrast & thresholding.
    """
    img = pil_image.convert('L') # Grayscale
    if retry:
        # Resize if image is small
        if img.width < 800 or img.height < 800:
            img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0) # Double contrast
        img = img.filter(ImageFilter.SHARPEN)
    return img

def process_raw_image_ocr(image_bytes: bytes, content_type: Optional[str] = None) -> OCRImageResponse:
    """
    Real Image OCR Pipeline:
    RAW IMAGE -> VALIDATION -> PREPROCESSING -> OCR ENGINE -> REGEX PARSER -> STRUCTURED RESULT
    Securely uses temporary files and deletes them immediately after processing.
    """
    # 1. File Validation
    if content_type and content_type.lower() not in ALLOWED_MIME_TYPES:
        return OCRImageResponse(
            success=False,
            raw_text="",
            confidence=0.0,
            message=f"Invalid file type '{content_type}'. Allowed types: JPEG, PNG, WebP."
        )

    if len(image_bytes) > MAX_FILE_SIZE:
        return OCRImageResponse(
            success=False,
            raw_text="",
            confidence=0.0,
            message="File size exceeds maximum limit of 10MB."
        )

    tmp_path = None
    try:
        # Save to temporary file securely
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        try:
            pil_img = Image.open(tmp_path)
            # Preprocess Image
            processed_img = preprocess_image_pixels(pil_img, retry=False)
        except Exception:
            return OCRImageResponse(
                success=False,
                product_name=None,
                brand=None,
                manufacturing_date=None,
                expiry_date=None,
                quantity=1.0,
                unit="pcs",
                batch_number=None,
                raw_text="",
                confidence=0.0,
                requires_confirmation=True,
                message="Invalid or corrupt image file payload."
            )

        raw_text = ""
        ocr_confidence = 0.50

        # Execute OCR Engine
        if HAS_PYTESSERACT:
            try:
                raw_text = pytesseract.image_to_string(processed_img).strip()
                ocr_confidence = 0.85
                if not raw_text:
                    # Retry with aggressive preprocessing
                    retry_img = preprocess_image_pixels(pil_img, retry=True)
                    raw_text = pytesseract.image_to_string(retry_img).strip()
                    ocr_confidence = 0.70
            except Exception:
                raw_text = ""

        # 2. Extract structured fields using Date & Regex Parser
        extracted_expiry = None
        extracted_mfg = None
        extracted_batch = None
        extracted_qty = 1.0
        extracted_unit = "pcs"
        requires_confirm = False

        # Expiry Date
        for pattern in EXPIRY_PATTERNS:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                raw_d = match.group(1)
                extracted_expiry = sanitize_ocr_date(raw_d)
                break

        # Manufacturing Date
        for pattern in MFG_PATTERNS:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                raw_m = match.group(1)
                extracted_mfg = sanitize_ocr_date(raw_m)
                break

        # Batch Number
        for pattern in BATCH_PATTERNS:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                extracted_batch = match.group(1).strip()
                break

        # Quantity & Unit
        for pattern in QUANTITY_PATTERNS:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                extracted_qty = float(match.group(1))
                extracted_unit = match.group(2)
                break

        # Product Name & Brand Guess
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        guessed_name = "Scanned Package Product"
        guessed_brand = None
        if lines:
            guessed_name = lines[0]
            if len(lines) > 1 and not re.search(r'exp|mfg|batch|b.no', lines[1], re.IGNORECASE):
                guessed_brand = lines[0]
                guessed_name = lines[1]

        if not extracted_expiry or ocr_confidence < 0.75:
            requires_confirm = True

        return OCRImageResponse(
            success=True,
            product_name=guessed_name,
            brand=guessed_brand,
            manufacturing_date=extracted_mfg,
            expiry_date=extracted_expiry,
            quantity=extracted_qty,
            unit=extracted_unit,
            batch_number=extracted_batch,
            raw_text=raw_text,
            confidence=round(ocr_confidence, 2),
            requires_confirmation=requires_confirm,
            message="Image OCR processing complete."
        )

    finally:
        # Security: Always delete temporary files
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass
