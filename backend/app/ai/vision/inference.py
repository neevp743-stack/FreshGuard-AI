import os
import numpy as np
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

    is_ready = (lifecycle_state == "READY") and os.path.exists(BEST_WEIGHTS_PATH)

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
    Executes production baseline vision inference on incoming binary image payload.
    """
    status = get_vision_model_status()
    if not status.model_available:
        return VisionDetectResponse(
            success=False,
            lifecycle_state=status.lifecycle_state,
            model_version=status.model_version,
            confidence_threshold=status.confidence_threshold,
            image_width=0,
            image_height=0,
            detections=[],
            message=f"Production vision inference unavailable: {status.message}"
        )

    tmp_path = None
    t0 = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    try:
        t0.write(image_bytes)
        tmp_path = t0.name
        t0.close()

        model = get_cached_yolo_model(BEST_WEIGHTS_PATH)
        results = model.predict(source=tmp_path, conf=status.confidence_threshold, imgsz=640, verbose=False)

        detections = []
        if results and len(results) > 0:
            boxes = results[0].boxes
            for box in boxes:
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                cls_name = model.names.get(cls_id, f"class_{cls_id}")
                xyxy = box.xyxy[0].tolist()

                detections.append(VisionDetection(
                    class_id=cls_id,
                    class_name=cls_name,
                    confidence=round(conf, 3),
                    bounding_box={"x1": round(xyxy[0], 1), "y1": round(xyxy[1], 1), "x2": round(xyxy[2], 1), "y2": round(xyxy[3], 1)}
                ))

        return VisionDetectResponse(
            success=True,
            lifecycle_state=status.lifecycle_state,
            model_version=status.model_version,
            confidence_threshold=status.confidence_threshold,
            image_width=640,
            image_height=640,
            detections=detections,
            message=f"Production vision inference complete. Found {len(detections)} object(s)."
        )
    except Exception as ex:
        logger.error(f"Production vision inference error: {ex}")
        return VisionDetectResponse(
            success=False,
            lifecycle_state=status.lifecycle_state,
            model_version=status.model_version,
            confidence_threshold=status.confidence_threshold,
            image_width=0,
            image_height=0,
            detections=[],
            message=f"Production vision inference error: {ex}"
        )
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass


V2_WEIGHTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../vision_models/experiments/grocery_yolov8_v2/weights/best.pt"))

FRESHGUARD_VISION_DISPLAY_NAME = "FreshGuard Vision"
_ONNX_SESSION_CACHE = None
_LAST_ONNX_ERROR = None

def find_v2_onnx_path() -> Optional[str]:
    candidates = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../vision_models/deployment/grocery_yolov8_v2_web/model.onnx")),
        os.path.abspath(os.path.join(os.getcwd(), "vision_models/deployment/grocery_yolov8_v2_web/model.onnx")),
        os.path.abspath(os.path.join(os.getcwd(), "../vision_models/deployment/grocery_yolov8_v2_web/model.onnx")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../vision_models/deployment/grocery_yolov8_v2_web/model.onnx")),
    ]
    for cand in candidates:
        if os.path.exists(cand):
            return cand
    return None

def get_onnx_session():
    global _ONNX_SESSION_CACHE, _LAST_ONNX_ERROR
    if _ONNX_SESSION_CACHE is None:
        onnx_path = find_v2_onnx_path()
        if not onnx_path:
            _LAST_ONNX_ERROR = "model.onnx file not found in any candidate path"
            return None
        try:
            import onnxruntime as ort
            logger.info(f"Initializing ONNX Runtime session with CPUExecutionProvider from: {onnx_path}")
            _ONNX_SESSION_CACHE = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
            _LAST_ONNX_ERROR = None
        except Exception as e:
            _LAST_ONNX_ERROR = f"Failed to load ONNX session: {e}"
            logger.error(_LAST_ONNX_ERROR)
            _ONNX_SESSION_CACHE = None
    return _ONNX_SESSION_CACHE


def _nms_boxes(boxes_xyxy: np.ndarray, scores: np.ndarray, iou_thresh: float) -> List[int]:
    if len(boxes_xyxy) == 0:
        return []
    x1 = boxes_xyxy[:, 0]
    y1 = boxes_xyxy[:, 1]
    x2 = boxes_xyxy[:, 2]
    y2 = boxes_xyxy[:, 3]
    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter + 1e-6)
        inds = np.where(ovr <= iou_thresh)[0]
        order = order[inds + 1]
    return keep

def _run_onnxruntime_v2_inference(image_bytes: bytes, conf_threshold: float = 0.25, iou_threshold: float = 0.45) -> Dict[str, Any]:
    """
    Executes ONNX Runtime inference using exported 35-class model.onnx artifact.
    Bypasses PyTorch C++ NumPy binding dependencies cleanly on Linux runtimes.
    """
    onnx_path = find_v2_onnx_path()
    if not onnx_path:
        return {
            "success": False,
            "model": "grocery_yolov8_v2",
            "detections": [],
            "count": 0,
            "inference_ms": 0.0,
            "message": f"ONNX Runtime V2 error: File model.onnx not found in candidate paths."
        }

    try:
        import io
        import time
        from PIL import Image

        t_start = time.perf_counter()

        session = get_onnx_session()
        if session is None:
            return {
                "success": False,
                "model": "grocery_yolov8_v2",
                "detections": [],
                "count": 0,
                "inference_ms": 0.0,
                "message": f"ONNX Runtime session initialization failed: {_LAST_ONNX_ERROR or 'Unknown session error'}"
            }

        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        orig_w, orig_h = img.size

        # Resize and normalize image for YOLOv8 (640x640)
        img_resized = img.resize((640, 640))
        img_np = np.array(img_resized).astype(np.float32) / 255.0
        img_np = np.transpose(img_np, (2, 0, 1))  # HWC to CHW
        img_np = np.expand_dims(img_np, axis=0)   # Add batch dimension [1, 3, 640, 640]

        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: img_np})

        # YOLOv8 output shape: [1, 39, 8400] where 39 = 4 (bbox) + 35 (classes)
        predictions = outputs[0][0]  # shape: [39, 8400]
        
        # Load 35 class names metadata
        class_names = []
        meta_path = os.path.join(os.path.dirname(onnx_path), "classes_metadata.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                meta = json.load(f)
                class_names = meta.get("classes", [])

        boxes = predictions[:4, :]      # [4, 8400] (xc, yc, w, h)
        scores = predictions[4:, :]     # [35, 8400]

        max_scores = np.max(scores, axis=0)      # [8400]
        class_ids = np.argmax(scores, axis=0)     # [8400]

        mask = max_scores >= conf_threshold
        filtered_boxes = boxes[:, mask]
        filtered_scores = max_scores[mask]
        filtered_class_ids = class_ids[mask]

        if len(filtered_scores) == 0:
            t_end = time.perf_counter()
            return {
                "success": True,
                "model": "grocery_yolov8_v2",
                "model_display_name": FRESHGUARD_VISION_DISPLAY_NAME,
                "detections": [],
                "count": 0,
                "inference_ms": round((t_end - t_start) * 1000, 1),
                "message": f"Real {FRESHGUARD_VISION_DISPLAY_NAME} ONNX detection complete. Found 0 object(s)."
            }

        # Convert xc,yc,w,h to x1,y1,x2,y2 for NMS
        scale_x = orig_w / 640.0
        scale_y = orig_h / 640.0

        xc = filtered_boxes[0, :]
        yc = filtered_boxes[1, :]
        w = filtered_boxes[2, :]
        h = filtered_boxes[3, :]

        x1_arr = (xc - w / 2.0) * scale_x
        y1_arr = (yc - h / 2.0) * scale_y
        x2_arr = (xc + w / 2.0) * scale_x
        y2_arr = (yc + h / 2.0) * scale_y

        boxes_xyxy = np.column_stack((x1_arr, y1_arr, x2_arr, y2_arr))
        keep_indices = _nms_boxes(boxes_xyxy, filtered_scores, iou_threshold)

        detections = []
        for idx in keep_indices:
            conf = float(filtered_scores[idx])
            cls_id = int(filtered_class_ids[idx])
            cls_name = class_names[cls_id] if cls_id < len(class_names) else f"class_{cls_id}"

            box = boxes_xyxy[idx]
            detections.append({
                "class_id": cls_id,
                "class_name": cls_name,
                "confidence": float(round(conf, 3)),
                "bbox": [float(round(box[0], 1)), float(round(box[1], 1)), float(round(box[2], 1)), float(round(box[3], 1))]
            })

        t_end = time.perf_counter()
        inference_ms = round((t_end - t_start) * 1000, 1)

        return {
            "success": True,
            "model": "grocery_yolov8_v2",
            "model_display_name": FRESHGUARD_VISION_DISPLAY_NAME,
            "detections": detections,
            "count": len(detections),
            "inference_ms": inference_ms,
            "message": f"Real {FRESHGUARD_VISION_DISPLAY_NAME} ONNX detection complete. Found {len(detections)} object(s)."
        }
    except Exception as ex:
        logger.error(f"ONNX Runtime V2 inference error: {ex}")
        return {
            "success": False,
            "model": "grocery_yolov8_v2",
            "detections": [],
            "count": 0,
            "inference_ms": 0.0,
            "message": f"ONNX Runtime V2 error [{type(ex).__name__}]: {ex}"
        }

def run_experimental_v2_inference(image_bytes: bytes, conf_threshold: float = 0.25, iou_threshold: float = 0.45) -> Dict[str, Any]:
    """
    Executes real YOLOv8 V2 (35-class) experimental model inference on image frame.
    Prefers ONNX Runtime for zero-dependency high speed Linux execution, with PyTorch fallback.
    """
    # 1. Try ONNX Runtime inference first
    onnx_res = _run_onnxruntime_v2_inference(image_bytes, conf_threshold=conf_threshold, iou_threshold=iou_threshold)
    if onnx_res and onnx_res.get("success"):
        return onnx_res

    onnx_msg = onnx_res.get("message", "Unknown ONNX error") if onnx_res else str(_LAST_ONNX_ERROR)

    # 2. PyTorch PyPI fallback
    candidates = [
        V2_WEIGHTS_PATH,
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../vision_models/experiments/grocery_yolov8_v2/results/run_v2/weights/best.pt")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../vision_models/deployment/grocery_yolov8_v2_web/model.pt")),
        os.path.abspath(os.path.join(os.getcwd(), "vision_models/deployment/grocery_yolov8_v2_web/model.pt")),
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
            "message": f"Vision inference unavailable: V2 model weights not found in candidates {[os.path.basename(c) for c in candidates]} | ONNX: {onnx_msg}"
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
            "model_display_name": FRESHGUARD_VISION_DISPLAY_NAME,
            "detections": detections,
            "count": len(detections),
            "inference_ms": inference_ms,
            "message": f"Real V2 detection complete. Found {len(detections)} object(s)."
        }
    except Exception as ex:
        import traceback
        tb_str = traceback.format_exc()
        logger.error(f"Experimental V2 vision inference error: {ex}\n{tb_str}")
        return {
            "success": False,
            "model": "grocery_yolov8_v2",
            "detections": [],
            "count": 0,
            "inference_ms": 0.0,
            "message": f"Vision inference error [{type(ex).__name__}]: {ex} | ONNX: {onnx_msg}"
        }
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

