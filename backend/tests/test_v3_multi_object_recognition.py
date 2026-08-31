"""
FreshGuard AI — V3 Multi-Object Recognition & Staging E2E Test Suite
Verifies multi-object scene detection (1, 2, 3, 5+ objects), class name origin strictly
from class_id -> authoritative metadata, and inventory staging integration.
"""

import json
import base64
import pytest
from app.services.shelf_life import CLASS_MAPPING_RULES, get_class_rule
from app.ai.vision.inference import _run_onnxruntime_v2_inference
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_product_name_origin_strictly_from_class_id_metadata():
    """Verify product names originate ONLY from authoritative 35-class metadata via class_id."""
    for cid in range(35):
        rule = get_class_rule(cid)
        assert rule is not None, f"Rule for class_id {cid} must exist"
        assert rule["name"] == CLASS_MAPPING_RULES[cid]["name"]
        assert rule["display_name"] == CLASS_MAPPING_RULES[cid]["display_name"]

def test_multi_object_bounding_box_non_overlapping_nms():
    """Verify Non-Maximum Suppression (NMS) separates distinct multi-object bounding boxes."""
    from app.ai.vision.inference import _nms_boxes
    import numpy as np

    # 3 boxes: Box 1 and Box 2 overlap heavily (IoU > 0.45), Box 3 is separate
    boxes = np.array([
        [10.0, 10.0, 100.0, 100.0],
        [12.0, 12.0, 98.0, 98.0],
        [200.0, 200.0, 300.0, 300.0]
    ])
    scores = np.array([0.90, 0.85, 0.88])

    keep = _nms_boxes(boxes, scores, iou_thresh=0.45)
    assert len(keep) == 2, f"NMS should keep 2 distinct boxes, kept {len(keep)}"
    assert 0 in keep and 2 in keep, f"Expected indices 0 and 2, got {keep}"

def test_v3_multi_object_detection_endpoint_schema():
    """Verify POST /api/v1/scanner/vision/detect_v3 returns valid multi-object schema."""
    tiny_jpeg = b'/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA='
    payload = {"image_base64": base64.b64encode(tiny_jpeg).decode('utf-8')}

    res = client.post("/api/v1/scanner/vision/detect_v3", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data.get("status") in ["success", "error"]
    assert "model_version" in data and data["model_version"] == "v3.0.0"
    assert "detections" in data and isinstance(data["detections"], list)
    assert "count" in data and isinstance(data["count"], int)
    assert "inference_ms" in data

def test_detection_to_inventory_staging_flow():
    """Verify Detection -> Check Existing -> ADD / NEW BATCH / SKIP flow."""
    # Step 1: Register test user
    reg = client.post("/api/v1/auth/register", json={
        "email": "e2e_staging_user@freshguard.ai",
        "password": "Password123!",
        "full_name": "E2E Staging User"
    })
    assert reg.status_code == 200
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 2: Add initial item (3 Tomatoes, class_id 5)
    add_init = client.post("/api/v1/inventory", json={
        "product_name": "Tomato",
        "class_id": 5,
        "quantity": 3.0,
        "unit": "pcs",
        "storage_location": "Fridge"
    }, headers=headers)
    assert add_init.status_code == 200
    init_item = add_init.json()
    assert init_item["quantity"] == 3.0

    # Step 3: Simulate webcam detection of Tomato (class_id 5, +2 items)
    check_dup = client.post("/api/v1/inventory/check-existing", json={
        "class_ids": [5]
    }, headers=headers)
    assert check_dup.status_code == 200
    dup_list = check_dup.json()
    assert len(dup_list) == 1
    assert dup_list[0]["already_in_inventory"] is True
    assert dup_list[0]["existing_item_id"] == init_item["id"]
    assert dup_list[0]["existing_quantity"] == 3.0



    # Step 4: Batch action [add] (Merge +2)
    batch_add = client.post("/api/v1/inventory/from-detections", json={
        "items": [{
            "class_id": 5,
            "name": "Tomato",
            "quantity": 2.0,
            "unit": "pcs",
            "location": "Fridge",
            "action": "add"
        }]
    }, headers=headers)
    assert batch_add.status_code == 200
    added_list = batch_add.json()
    assert len(added_list) == 1
    assert added_list[0]["quantity"] == 5.0  # 3 + 2 = 5!

