import os
import json
import tempfile
import logging
from typing import List, Dict, Any, Optional
from PIL import Image
from app.core.config import settings
from app.schemas.schemas import VisionDetection, VisionDetectResponse, VisionStatusResponse

logger = logging.getLogger(__name__)

VISION_MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../vision_models"))
METADATA_PATH = os.path.join(VISION_MODELS_DIR, "model_metadata.json")
BEST_WEIGHTS_PATH = os.path.join(VISION_MODELS_DIR, "grocery_vision_v1", "weights", "best.pt")

_MODEL_CACHE: Dict[str, Any] = {}

def get_cached_yolo_model(weights_path: str):
    """
    Lazy bounded singleton model instance cache.
    Prevents repeated expensive disk model loading on every inference request.
    """
    if weights_path not in _MODEL_CACHE:
        from ultralytics import YOLO
        logger.info(f"Loading YOLO model weights into memory cache from: {weights_path}")
        _MODEL_CACHE[weights_path] = YOLO(weights_path)
    return _MODEL_CACHE[weights_path]

def get_vision_model_status() -> VisionStatusResponse:
    """
    Returns active vision model lifecycle state and configuration status.
    Lifecycle states: NOT_TRAINED, TRAINING, READY, FAILED, DEPRECATED.
    """
    lifecycle_state = "NOT_TRAINED"
    classes_count = 15
    model_version = "0.1.0"
    message = "Vision model integration is ready; training is pending the real grocery dataset."

    if os.path.exists(METADATA_PATH):
        try:
            with open(METADATA_PATH, "r") as f:
                data = json.load(f)
                lifecycle_state = data.get("lifecycle_state", "NOT_TRAINED")
                classes_count = data.get("classes_count", 15)
                model_version = data.get("version", "0.1.0")
                message = data.get("message", message)
        except Exception:
            pass

    is_ready = (lifecycle_state == "READY" and os.path.exists(BEST_WEIGHTS_PATH))

    return VisionStatusResponse(
        lifecycle_state=lifecycle_state,
        model_available=is_ready,
        model_version=model_version,
        classes_count=classes_count,
        confidence_threshold=settings.VISION_CONFIDENCE_THRESHOLD,
        message=message
    )

def run_vision_inference(image_bytes: bytes) -> VisionDetectResponse:
    """
    Executes Vision Object Detection on raw image bytes.
    Privacy-first: Processes image in memory / secure temporary file and deletes it immediately.
    Filters detections against VISION_CONFIDENCE_THRESHOLD.
    If no trained model is available, returns lifecycle_state NOT_TRAINED without fabricating detections.
    """
    status = get_vision_model_status()
    threshold = settings.VISION_CONFIDENCE_THRESHOLD

    if not status.model_available:
        return VisionDetectResponse(
            success=False,
            lifecycle_state=status.lifecycle_state,
            model_version=status.model_version,
            confidence_threshold=threshold,
            image_width=0,
            image_height=0,
            detections=[],
            message="Vision model integration is ready; training is pending the real grocery dataset."
        )

    tmp_path = None
    try:
        # Secure temporary file creation
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        img = Image.open(tmp_path)
        img_w, img_h = img.size

        model = get_cached_yolo_model(BEST_WEIGHTS_PATH)

        results = model.predict(source=tmp_path, conf=threshold, imgsz=640)
        detections: List[VisionDetection] = []

        if results and len(results) > 0:
            boxes = results[0].boxes
            for box in boxes:
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                cls_name = model.names.get(cls_id, f"class_{cls_id}")
                xyxy = box.xyxy[0].tolist()

                is_low_conf = conf < threshold

                detections.append(VisionDetection(
                    class_id=cls_id,
                    class_name=cls_name,
                    confidence=round(conf, 3),
                    bounding_box={
                        "x1": round(xyxy[0], 1),
                        "y1": round(xyxy[1], 1),
                        "x2": round(xyxy[2], 1),
                        "y2": round(xyxy[3], 1),
                    },
                    requires_confirmation=is_low_conf
                ))

        return VisionDetectResponse(
            success=True,
            lifecycle_state="READY",
            model_version=status.model_version,
            confidence_threshold=threshold,
            image_width=img_w,
            image_height=img_h,
            detections=detections,
            message=f"Vision detection complete. Found {len(detections)} object(s)."
        )

    except Exception as ex:
        logger.error(f"Vision inference error: {ex}")
        return VisionDetectResponse(
            success=False,
            lifecycle_state="FAILED",
            model_version=status.model_version,
            confidence_threshold=threshold,
            image_width=0,
            image_height=0,
            detections=[],
            message=f"Vision inference error: {ex}"
        )

    finally:
        # Privacy-first: Immediate temporary file deletion
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass


V2_WEIGHTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../vision_models/experiments/grocery_yolov8_v2/weights/best.pt"))

def run_experimental_v2_inference(image_bytes: bytes, conf_threshold: float = 0.25, iou_threshold: float = 0.45) -> Dict[str, Any]:
    """
    Executes real YOLOv8 V2 (35-class) experimental model inference on image frame.
    Returns real predictions, class names, bounding boxes, object count, and latency.
    """
    candidates = [
        V2_WEIGHTS_PATH,
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../vision_models/experiments/grocery_yolov8_v2/results/run_v2/weights/best.pt")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../vision_models/deployment/grocery_yolov8_v2_web/model.pt")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../vision_models/deployment/grocery_yolov8_v2_web/model.onnx")),
    ]

    weights_path = None
    for cand in candidates:
        if os.path.exists(cand):
            weights_path = cand
            break

    if not weights_path:
        return {
            "success": False,
            "model": "grocery_yolov8_v2",
            "detections": [],
            "count": 0,
            "inference_ms": 0.0,
            "message": f"Vision inference unavailable: V2 model weights not found in candidates {[os.path.basename(c) for c in candidates]}."
        }

    tmp_path = None
    t0 = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    try:
        t0.write(image_bytes)
        tmp_path = t0.name
        t0.close()

        import time
        t_start = time.perf_counter()

        model = get_cached_yolo_model(weights_path)
        results = model.predict(source=tmp_path, conf=conf_threshold, iou=iou_threshold, imgsz=640, verbose=False)

        t_end = time.perf_counter()
        inference_ms = round((t_end - t_start) * 1000, 1)

        detections = []
        if results and len(results) > 0:
            boxes = results[0].boxes
            for box in boxes:
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                cls_name = model.names.get(cls_id, f"class_{cls_id}")
                xyxy = box.xyxy[0].tolist()

                detections.append({
                    "class_id": cls_id,
                    "class_name": cls_name,
                    "confidence": round(conf, 3),
                    "bbox": [round(c, 1) for c in xyxy]
                })

        return {
            "success": True,
            "model": "grocery_yolov8_v2",
            "detections": detections,
            "count": len(detections),
            "inference_ms": inference_ms,
            "message": f"Real V2 detection complete. Found {len(detections)} object(s)."
        }
    except Exception as ex:
        logger.error(f"Experimental V2 vision inference error: {ex}")
        return {
            "success": False,
            "model": "grocery_yolov8_v2",
            "detections": [],
            "count": 0,
            "inference_ms": 0.0,
            "message": f"Vision inference unavailable: {ex}"
        }
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

