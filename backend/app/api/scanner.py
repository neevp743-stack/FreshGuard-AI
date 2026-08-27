from fastapi import APIRouter, Depends, HTTPException, Body, File, UploadFile
from app.services.scanner import lookup_barcode
from app.ai.ocr import parse_package_ocr_text
from app.services.ocr_image import process_raw_image_ocr
from app.schemas.schemas import BarcodeLookupRequest, BarcodeLookupResponse, OCRScanResponse, OCRImageResponse

router = APIRouter(prefix="/scanner", tags=["Scanner & OCR"])

@router.post("/barcode", response_model=BarcodeLookupResponse)
def scan_barcode(req: BarcodeLookupRequest):
    if not req.barcode:
        raise HTTPException(status_code=400, detail="Barcode string required")
    return lookup_barcode(req.barcode)

@router.post("/ocr", response_model=OCRScanResponse)
def scan_ocr_text(raw_text: str = Body(..., embed=True)):
    return parse_package_ocr_text(raw_text)

@router.post("/ocr/image", response_model=OCRImageResponse)
async def scan_ocr_image(file: UploadFile = File(...)):
    """
    Multipart/form-data Raw Image Package OCR Endpoint.
    Accepts raw packaging image upload, validates file type & size, preprocesses image pixels,
    and returns structured OCR date and product metadata.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No image file uploaded")

    contents = await file.read()
    return process_raw_image_ocr(contents, file.content_type)
