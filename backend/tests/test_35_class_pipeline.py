import os
import sys
import pytest
import numpy as np
from PIL import Image

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

os.environ["FRESHGUARD_VISION_MODEL"] = "v2"

from app.ai.vision.inference import (
    find_v2_onnx_path,
    get_onnx_session,
    _run_onnxruntime_v2_inference,
    _nms_boxes
)

def test_35_class_metadata_alignment():
    onnx_path = find_v2_onnx_path()
    assert onnx_path is not None, "V2 ONNX model path must exist"
    meta_path = os.path.join(os.path.dirname(onnx_path), "classes_metadata.json")
    assert os.path.exists(meta_path), "classes_metadata.json must exist"

    import json
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    classes = meta.get("classes", [])
    assert len(classes) == 35, f"Expected 35 classes, found {len(classes)}"
    assert len(set(classes)) == 35, "Class names must be unique"
    assert classes[0] == "milk"
    assert classes[6] == "potato"
    assert classes[34] == "sweet_potato"

def test_35_class_inference_schema():
    sample_img = os.path.join(BASE_DIR, "datasets", "grocery_vision", "images", "val", "veg_val_001.jpg")
    if not os.path.exists(sample_img):
        pytest.skip("Sample validation image not found")

    with open(sample_img, "rb") as f:
        img_bytes = f.read()

    res = _run_onnxruntime_v2_inference(img_bytes, conf_threshold=0.15)
    assert isinstance(res, dict)
    assert res.get("success") is True
    assert res.get("model") == "grocery_yolov8_v2"
    assert res.get("model_display_name") == "FreshGuard Vision"
    assert "detections" in res
    assert "count" in res
    assert "inference_ms" in res
    assert isinstance(res["inference_ms"], float)

def test_35_class_bounding_box_coordinates():
    sample_img = os.path.join(BASE_DIR, "datasets", "grocery_vision", "images", "val", "veg_val_001.jpg")
    if not os.path.exists(sample_img):
        pytest.skip("Sample validation image not found")

    with open(sample_img, "rb") as f:
        img_bytes = f.read()

    res = _run_onnxruntime_v2_inference(img_bytes, conf_threshold=0.15)
    for det in res.get("detections", []):
        assert "class_id" in det
        assert 0 <= det["class_id"] < 35
        assert "class_name" in det
        assert "confidence" in det
        assert 0.0 <= det["confidence"] <= 1.0
        assert "bbox" in det
        bbox = det["bbox"]
        assert len(bbox) == 4
        x1, y1, x2, y2 = bbox
        assert x1 <= x2
        assert y1 <= y2

def test_nms_boxes_utility():
    boxes = np.array([
        [10, 10, 50, 50],
        [12, 12, 52, 52],
        [100, 100, 200, 200]
    ], dtype=np.float32)
    scores = np.array([0.9, 0.8, 0.95], dtype=np.float32)
    keep = _nms_boxes(boxes, scores, iou_thresh=0.45)
    assert len(keep) == 2
    assert 2 in keep  # highest score for box 3
    assert 0 in keep  # highest score for overlapping box 1 vs box 2
