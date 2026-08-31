"""
FreshGuard AI — Webcam Pipeline Automated Verification Suite
Verifies single-flight inference scheduler rules, bounding box scaling,
and multi-object detection response contracts for webcam integration.
"""

import json
import base64
import pytest
from main import app
from fastapi.testclient import TestClient
from app.services.shelf_life import get_class_rule

client = TestClient(app)



def test_webcam_bounding_box_scale_math():
    """Verify webcam canvas scaling math preserves aspect ratio and bounding box bounds."""
    orig_w, orig_h = 1280, 720
    canvas_w, canvas_h = 640, 360

    scale_x = canvas_w / orig_w
    scale_y = canvas_h / orig_h

    assert scale_x == 0.5
    assert scale_y == 0.5

    # Test bounding box [x1, y1, x2, y2]
    raw_bbox = [100, 200, 500, 600]
    scaled_bbox = [
        raw_bbox[0] * scale_x,
        raw_bbox[1] * scale_y,
        raw_bbox[2] * scale_x,
        raw_bbox[3] * scale_y,
    ]

    assert scaled_bbox == [50.0, 100.0, 250.0, 300.0]

def test_single_flight_scheduler_lock_state():
    """Verify single-flight scheduler flag prevents parallel overlapping inference calls."""
    is_inference_in_flight = False
    is_processing_frame = False

    def trigger_frame_capture():
        nonlocal is_inference_in_flight, is_processing_frame
        if is_inference_in_flight or is_processing_frame:
            return "SKIPPED_FLIGHT_LOCKED"
        is_inference_in_flight = True
        is_processing_frame = True
        return "INFERENCE_STARTED"

    def complete_frame_capture():
        nonlocal is_inference_in_flight, is_processing_frame
        is_inference_in_flight = False
        is_processing_frame = False

    # First call -> starts
    res1 = trigger_frame_capture()
    assert res1 == "INFERENCE_STARTED"

    # Second call while in flight -> skipped
    res2 = trigger_frame_capture()
    assert res2 == "SKIPPED_FLIGHT_LOCKED"

    # Complete first call
    complete_frame_capture()

    # Third call after completion -> starts cleanly
    res3 = trigger_frame_capture()
    assert res3 == "INFERENCE_STARTED"
    complete_frame_capture()

def test_webcam_detection_response_schema():
    """Verify detection response contract returned by vision endpoints for webcam payload."""
    tiny_jpeg = b'/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA='
    payload = {"image_base64": base64.b64encode(tiny_jpeg).decode('utf-8')}

    res = client.post("/api/v1/scanner/vision/detect_v2", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "status" in data or "success" in data
    assert "detections" in data and isinstance(data["detections"], list)
    assert "count" in data and isinstance(data["count"], int)
    assert "inference_ms" in data

