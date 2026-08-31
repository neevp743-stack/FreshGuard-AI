"""
FreshGuard AI — 35-Class Identity Verification Automated Test Suite
Verifies authoritative class_id 0–34 mapping consistency across model metadata,
shelf life rules engine, vision classes config, and boundary validations.
"""

import json
import os
import pytest
from app.services.shelf_life import CLASS_MAPPING_RULES, CLASS_NAME_TO_ID, get_class_rule

def test_35_class_shelf_life_rules_completeness():
    """Verify CLASS_MAPPING_RULES contains exactly 35 entries (0 to 34)."""
    assert len(CLASS_MAPPING_RULES) == 35, f"Expected 35 classes, found {len(CLASS_MAPPING_RULES)}"
    for cid in range(35):
        assert cid in CLASS_MAPPING_RULES, f"Missing class_id {cid} in CLASS_MAPPING_RULES"
        rule = CLASS_MAPPING_RULES[cid]
        assert "name" in rule and isinstance(rule["name"], str)
        assert "display_name" in rule and isinstance(rule["display_name"], str)
        assert "category" in rule and isinstance(rule["category"], str)
        assert "default_location" in rule and rule["default_location"] in ["Fridge", "Pantry", "Freezer"]
        assert "shelf_life_days" in rule and isinstance(rule["shelf_life_days"], int) and rule["shelf_life_days"] > 0

def test_35_class_name_to_id_mapping():
    """Verify bidirectional CLASS_NAME_TO_ID mapping consistency."""
    assert len(CLASS_NAME_TO_ID) == 35, f"Expected 35 entries in CLASS_NAME_TO_ID, found {len(CLASS_NAME_TO_ID)}"
    for cid, rule in CLASS_MAPPING_RULES.items():
        name = rule["name"]
        assert CLASS_NAME_TO_ID.get(name) == cid, f"Mismatch for class_name '{name}': expected {cid}, got {CLASS_NAME_TO_ID.get(name)}"

def test_backend_vision_classes_json_alignment():
    """Verify backend/app/ai/vision/classes.json aligns 1:1 with 35 class IDs."""
    classes_json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/ai/vision/classes.json"))
    assert os.path.exists(classes_json_path), f"classes.json not found at {classes_json_path}"
    with open(classes_json_path, "r") as f:
        data = json.load(f)
    assert data.get("classes_count") == 35
    classes_list = data.get("classes", [])
    assert len(classes_list) == 35, f"classes.json has {len(classes_list)} items, expected 35"
    for idx, cname in enumerate(classes_list):
        expected_name = CLASS_MAPPING_RULES[idx]["name"]
        assert cname == expected_name, f"Index {idx} mismatch in classes.json: expected {expected_name}, got {cname}"

def test_v2_model_metadata_json_alignment():
    """Verify vision_models/deployment/grocery_yolov8_v2_web/classes_metadata.json aligns 1:1 with 35 class IDs."""
    v2_meta_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../vision_models/deployment/grocery_yolov8_v2_web/classes_metadata.json"))
    assert os.path.exists(v2_meta_path), f"V2 classes_metadata.json not found at {v2_meta_path}"
    with open(v2_meta_path, "r") as f:
        data = json.load(f)
    assert data.get("classes_count") == 35
    classes_list = data.get("classes", [])
    assert len(classes_list) == 35, f"V2 classes_metadata.json has {len(classes_list)} items, expected 35"
    for idx, cname in enumerate(classes_list):
        expected_name = CLASS_MAPPING_RULES[idx]["name"]
        assert cname == expected_name, f"Index {idx} mismatch in V2 metadata: expected {expected_name}, got {cname}"

def test_v3_model_metadata_json_alignment():
    """Verify vision_models/v3/v3_classes_metadata.json aligns 1:1 with 35 class IDs."""
    v3_meta_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../vision_models/v3/v3_classes_metadata.json"))
    assert os.path.exists(v3_meta_path), f"V3 metadata not found at {v3_meta_path}"
    with open(v3_meta_path, "r") as f:
        data = json.load(f)
    assert data.get("num_classes") == 35
    v3_classes = data.get("classes", {})
    assert len(v3_classes) == 35, f"V3 classes dictionary has {len(v3_classes)} items, expected 35"
    for cid in range(35):
        cname = v3_classes.get(str(cid))
        expected_name = CLASS_MAPPING_RULES[cid]["name"]
        assert cname == expected_name, f"Class ID {cid} mismatch in V3 metadata: expected {expected_name}, got {cname}"

def test_class_rule_boundary_validations():
    """Verify get_class_rule returns rules for 0..34 and None for invalid IDs."""
    for cid in range(35):
        rule_by_id = get_class_rule(cid)
        assert rule_by_id is not None, f"get_class_rule({cid}) returned None"
        rule_by_name = get_class_rule(rule_by_id["name"])
        assert rule_by_name is not None and rule_by_name["name"] == rule_by_id["name"]

    assert get_class_rule(35) is None, "get_class_rule(35) should return None for out-of-bounds class ID"
    assert get_class_rule(-1) is None, "get_class_rule(-1) should return None for negative class ID"
    assert get_class_rule("non_existent_food_item") is None, "get_class_rule for unknown string should return None"
