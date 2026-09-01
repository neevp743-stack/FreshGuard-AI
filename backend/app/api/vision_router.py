import os
import json
import logging
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query, Body, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User
from app.services.scanner import lookup_barcode
from app.services.ocr_image import process_raw_image_ocr
from app.ai.vision.inference import get_vision_model_status, run_vision_inference
from app.schemas.schemas import (
    VisionStatusResponse, VisionDetectResponse, VisionFeedbackRequest, MultiModalScanResponse, VisionDetectPayload
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scanner/vision", tags=["Vision AI & Multi-Modal Scanner"])

FEEDBACK_LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../vision_feedback_metadata.jsonl"))

@router.get("/status", response_model=VisionStatusResponse)
def get_vision_status():
    """
    Returns active Vision Model Lifecycle State (NOT_TRAINED, TRAINING, READY, FAILED, DEPRECATED),
    model availability, class counts, and confidence threshold.
    """
    return get_vision_model_status()

@router.post("/detect", response_model=VisionDetectResponse)
async def detect_grocery_vision_objects(file: UploadFile = File(...)):
    """
    Multipart/form-data Raw Packaging / Fridge Photo Object Detection Endpoint.
    Privacy-first: Processes image in memory/temp directory and deletes temporary file immediately after inference.
    Filters detections against VISION_CONFIDENCE_THRESHOLD.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No image file uploaded")

    contents = await file.read()
    return run_vision_inference(contents)

@router.post("/detect_v2")
async def detect_v2_webcam_frame(
    request: Request,
    conf: float = Query(0.25),
    iou: float = Query(0.45)
):
    """
    Real 644-Class / 35-Class YOLOv8 Object Detection Endpoint for Live Web Camera Stream & Uploads.
    Supports both multipart image upload and JSON Base64 image payload seamlessly.
    Returns real detections, class names, bounding boxes, object count, and latency.
    """
    import base64
    image_bytes = None
    content_type = request.headers.get("content-type", "")

    # 1. Check multipart/form-data or form upload
    if "multipart" in content_type or "form" in content_type:
        try:
            form_data = await request.form()
            if "file" in form_data:
                f_item = form_data["file"]
                if hasattr(f_item, "read"):
                    image_bytes = await f_item.read()
            elif "image_base64" in form_data:
                b64 = str(form_data["image_base64"])
                if "," in b64:
                    b64 = b64.split(",")[1]
                image_bytes = base64.b64decode(b64)
        except Exception:
            pass

    # 2. Check JSON payload
    if not image_bytes:
        try:
            body_data = await request.json()
            if isinstance(body_data, dict) and "image_base64" in body_data:
                b64 = body_data["image_base64"]
                if "," in b64:
                    b64 = b64.split(",")[1]
                image_bytes = base64.b64decode(b64)
        except Exception:
            pass

    # 3. Fallback form check
    if not image_bytes:
        try:
            form_data = await request.form()
            if "file" in form_data:
                f_item = form_data["file"]
                if hasattr(f_item, "read"):
                    image_bytes = await f_item.read()
            elif "image_base64" in form_data:
                b64 = str(form_data["image_base64"])
                if "," in b64:
                    b64 = b64.split(",")[1]
                image_bytes = base64.b64decode(b64)
        except Exception:
            pass

    if not image_bytes:
        raise HTTPException(status_code=400, detail="No image file or image_base64 payload provided")

    from app.ai.vision.inference import run_experimental_v2_inference
    return run_experimental_v2_inference(image_bytes, conf_threshold=conf, iou_threshold=iou)

# Direct Route Aliases for Live Web Camera Inference API
@router.post("/detect_direct")
async def detect_direct_alias(
    request: Request,
    conf: float = Query(0.25),
    iou: float = Query(0.45)
):
    return await detect_v2_webcam_frame(request=request, conf=conf, iou=iou)

@router.post("/feedback")
def submit_vision_feedback(
    req: VisionFeedbackRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Privacy-First Active Learning Feedback Endpoint.
    Stores prediction metadata and user correction strictly WITHOUT storing raw household images
    unless the user explicitly toggles `opt_in_image_retention: true`.
    """
    record = {
        "user_id": current_user.id,
        "predicted_class": req.predicted_class,
        "confidence": req.confidence,
        "corrected_class": req.corrected_class,
        "opt_in_image_retention": req.opt_in_image_retention,
        "comments": req.comments,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        with open(FEEDBACK_LOG_PATH, "a") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as ex:
        logger.warning(f"Error logging vision feedback: {ex}")

    return {
        "status": "success",
        "message": "Vision prediction feedback recorded. Thank you for contributing to model accuracy!"
    }

@router.post("/multimodal", response_model=MultiModalScanResponse)
async def scan_multimodal_pipeline(
    barcode: Optional[str] = Query(None),
    file: Optional[UploadFile] = File(None)
):
    """
    Intelligent Multi-Modal Identity Pipeline (Barcode + Vision + OCR).
    Priority Rules:
    1. Barcode: Highest-confidence product identity when valid.
    2. Vision: Fallback or verification product identity.
    3. OCR: Expiry date, manufacturing date, and batch extraction.
    4. Conflict Resolution: If Barcode and Vision disagree, flags discrepancy for user confirmation.
    """
    barcode_res = None
    ocr_res = None
    vision_detections = []
    discrepancy_flagged = False
    discrepancy_msg = None

    # 1. Barcode Lookup
    if barcode and barcode.strip():
        lookup = lookup_barcode(barcode.strip())
        if lookup.found:
            barcode_res = {
                "barcode": lookup.barcode,
                "product_name": lookup.product_name,
                "brand": lookup.brand,
                "category": lookup.category
            }

    # 2. Vision & OCR Processing
    if file:
        contents = await file.read()

        # Image OCR Execution
        ocr_obj = process_raw_image_ocr(contents, file.content_type)
        if ocr_obj.success:
            ocr_res = {
                "product_name": ocr_obj.product_name,
                "expiry_date": ocr_obj.expiry_date,
                "manufacturing_date": ocr_obj.manufacturing_date,
                "quantity": ocr_obj.quantity,
                "unit": ocr_obj.unit,
                "batch_number": ocr_obj.batch_number,
                "confidence": ocr_obj.confidence
            }

        # Vision Inference Execution
        v_res = run_vision_inference(contents)
        if v_res.success:
            vision_detections = v_res.detections

    # 3. Determine Final Identity & Conflict Check
    final_name = "Scanned Grocery Item"
    final_brand = None
    final_category = "Other"

    if barcode_res:
        final_name = barcode_res["product_name"]
        final_brand = barcode_res.get("brand")
        final_category = barcode_res.get("category", "Other")

        # Conflict check with Vision top detection
        if vision_detections:
            top_v = vision_detections[0].class_name.lower()
            b_name = final_name.lower()
            if top_v not in b_name and b_name not in top_v:
                discrepancy_flagged = True
                discrepancy_msg = f"Barcode identity '{final_name}' disagrees with Vision detection '{vision_detections[0].class_name}'. Please verify."
    elif vision_detections:
        final_name = vision_detections[0].class_name.title()
        final_category = "Produce" if vision_detections[0].class_name in ["apple", "banana", "tomato", "potato", "onion"] else "Other"
    elif ocr_res and ocr_res.get("product_name"):
        final_name = ocr_res["product_name"]

    final_suggested = {
        "product_name": final_name,
        "brand": final_brand,
        "category": final_category,
        "quantity": ocr_res.get("quantity", 1.0) if ocr_res else 1.0,
        "unit": ocr_res.get("unit", "pcs") if ocr_res else "pcs",
        "expiry_date": ocr_res.get("expiry_date") if ocr_res else None,
        "storage_location": "Refrigerator"
    }

    return MultiModalScanResponse(
        barcode_identity=barcode_res,
        vision_detections=vision_detections,
        ocr_result=ocr_res,
        discrepancy_flagged=discrepancy_flagged,
        discrepancy_message=discrepancy_msg,
        final_suggested_item=final_suggested
    )


@router.post("/detect_v3")
async def detect_vision_v3(payload: VisionDetectPayload, db: Session = Depends(get_db)):
    """Isolated FreshGuard Vision V3 detection endpoint for 35-class evaluation."""
    if payload.image_base64:
        try:
            import base64
            image_bytes = base64.b64decode(payload.image_base64)
            from app.core.config import settings
            from app.ai.vision.inference import run_experimental_v2_inference
            orig_setting = settings.FRESHGUARD_VISION_MODEL
            try:
                settings.FRESHGUARD_VISION_MODEL = "v3"
                res = run_experimental_v2_inference(image_bytes)
                res["model_version"] = "v3.0.0"
                return res
            finally:
                settings.FRESHGUARD_VISION_MODEL = orig_setting
        except Exception as e:
            return {
                "success": False,
                "model_version": "v3.0.0",
                "error": str(e),
                "detections": [],
                "count": 0,
                "inference_ms": 0.0
            }
    return {
        "success": True,
        "model_version": "v3.0.0",
        "detections": [],
        "count": 0,
        "inference_ms": 0.0,
        "message": "No image payload provided."
    }
