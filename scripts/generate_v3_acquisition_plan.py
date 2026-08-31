import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

OFFICIAL_35_CLASSES = [
    "milk", "bread", "apple", "banana", "egg", "tomato", "potato", "onion", "rice", "yogurt",
    "cheese", "biscuit", "juice", "water", "packaged_snack", "carrot", "cabbage", "cauliflower",
    "capsicum", "cucumber", "brinjal", "broccoli", "spinach", "peas", "corn", "garlic", "ginger",
    "okra", "beetroot", "radish", "pumpkin", "bitter_gourd", "bottle_gourd", "green_chilli", "sweet_potato"
]

# Current dataset counts in datasets/freshguard_35_clean
CURRENT_STATS = {
    "milk": {"images": 43, "objects": 262},
    "bread": {"images": 22, "objects": 30},
    "rice": {"images": 69, "objects": 684},
    "yogurt": {"images": 1, "objects": 1},
    "cheese": {"images": 121, "objects": 1813},
    "water": {"images": 68, "objects": 275}
}

# Per-class acquisition targets based on visual complexity and produce vs packaged goods
CLASS_REQUIREMENTS = {}

for idx, cname in enumerate(OFFICIAL_35_CLASSES):
    cur_img = CURRENT_STATS.get(cname, {}).get("images", 0)
    cur_obj = CURRENT_STATS.get(cname, {}).get("objects", 0)

    # Classify priority & complexity
    if cname in ["potato", "tomato", "onion", "ginger", "carrot", "apple", "banana", "egg", "green_chilli", "cucumber", "capsicum", "spinach"]:
        priority = "HIGH"
        min_img, rec_img, ideal_img = 150, 250, 400
        min_obj, rec_obj, ideal_obj = 500, 800, 1500
    elif cur_img == 0:
        priority = "HIGH" if cname in ["cabbage", "cauliflower", "brinjal", "okra", "peas", "garlic"] else "MEDIUM"
        min_img, rec_img, ideal_img = 120, 200, 350
        min_obj, rec_obj, ideal_obj = 400, 600, 1200
    else:
        priority = "LOW"
        min_img, rec_img, ideal_img = 100, 150, 250
        min_obj, rec_obj, ideal_obj = 300, 500, 1000

    rem_min_img = max(0, min_img - cur_img)
    rem_rec_img = max(0, rec_img - cur_img)

    status = "AVAILABLE" if cur_img >= 40 else ("LIMITED" if cur_img > 0 else "MISSING")

    CLASS_REQUIREMENTS[cname] = {
        "class_id": idx,
        "class_name": cname,
        "status": status,
        "priority": priority,
        "current_images": cur_img,
        "current_objects": cur_obj,
        "target_min_images": min_img,
        "target_recommended_images": rec_img,
        "target_ideal_images": ideal_img,
        "target_min_objects": min_obj,
        "target_recommended_objects": rec_obj,
        "target_ideal_objects": ideal_obj,
        "remaining_min_images_needed": rem_min_img,
        "remaining_rec_images_needed": rem_rec_img
    }

# Write JSON Artifact
json_path = os.path.join(DOCS_DIR, "FRESHGUARD_35_CLASS_DATA_REQUIREMENTS.json")
json_data = {
    "version": "1.0.0",
    "project": "FreshGuard AI",
    "target_model": "FreshGuard Vision V3",
    "total_official_classes": 35,
    "classes_available": sum(1 for v in CLASS_REQUIREMENTS.values() if v["status"] == "AVAILABLE"),
    "classes_limited": sum(1 for v in CLASS_REQUIREMENTS.values() if v["status"] == "LIMITED"),
    "classes_missing": sum(1 for v in CLASS_REQUIREMENTS.values() if v["status"] == "MISSING"),
    "total_current_images": sum(v["current_images"] for v in CLASS_REQUIREMENTS.values()),
    "total_current_objects": sum(v["current_objects"] for v in CLASS_REQUIREMENTS.values()),
    "total_target_min_images": sum(v["target_min_images"] for v in CLASS_REQUIREMENTS.values()),
    "total_target_rec_images": sum(v["target_recommended_images"] for v in CLASS_REQUIREMENTS.values()),
    "total_target_ideal_images": sum(v["target_ideal_images"] for v in CLASS_REQUIREMENTS.values()),
    "training_readiness": "NOT_READY",
    "class_requirements": CLASS_REQUIREMENTS
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2)

# Write Markdown Plan Artifact
md_path = os.path.join(DOCS_DIR, "FRESHGUARD_35_CLASS_DATA_ACQUISITION_PLAN.md")

checklist_table = "| ID | Class Name | Status | Priority | Current Imgs | Current Objs | Min Imgs Needed | Rec Imgs Target | Remaining Needed |\n| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
for cname, req in CLASS_REQUIREMENTS.items():
    checklist_table += f"| {req['class_id']} | `{cname}` | {req['status']} | **{req['priority']}** | {req['current_images']} | {req['current_objects']} | {req['target_min_images']} | {req['target_recommended_images']} | `{req['remaining_rec_images_needed']}` |\n"

md_content = f"""# FreshGuard AI — Phase 3: 35-Class Data Acquisition & Training Readiness Plan

## 1. Executive Summary & Objective

This document defines the comprehensive **Data Acquisition, Annotation, Quality Control, and Training Readiness Plan** for building the future **FreshGuard Vision V3** object-detection dataset.

- **Current Baseline**: `datasets/freshguard_35_clean/` (321 clean images, 3,065 objects across 6 supported classes).
- **Target Goal**: A robust 35-class YOLO object-detection dataset (`datasets/freshguard_35_v3/`) operating reliably across live mobile/webcam streams, dynamic kitchen lighting, multi-item clutter, partial occlusion, and varied orientations.
- **Safety Directive**: **NO MODEL TRAINING** will be conducted until all 35 classes satisfy the minimum data readiness criteria.

---

## 2. Official 35-Class Mapping & Current Status Matrix

{checklist_table}

---

## 3. High-Priority Acquisition Target Breakdown

### High Priority Classes (24 Classes)
Essential fresh produce and everyday household staples currently missing or under-represented:
- **Fresh Vegetables & Roots**: `potato`, `tomato`, `onion`, `carrot`, `ginger`, `garlic`, `green_chilli`, `cucumber`, `capsicum`, `spinach`, `cabbage`, `cauliflower`, `brinjal`, `okra`, `peas`.
- **Fresh Fruits**: `apple`, `banana`.
- **Poultry & Packaged Essentials**: `egg`, `bread`, `yogurt`.

### Medium Priority Classes (5 Classes)
Secondary vegetables and specialty produce:
- `beetroot`, `radish`, `pumpkin`, `bitter_gourd`, `bottle_gourd`, `sweet_potato`, `corn`, `biscuit`, `juice`, `packaged_snack`.

### Low Priority Classes (6 Classes)
Existing supported classes in `freshguard_35_clean` requiring incremental diversity updates:
- `cheese`, `rice`, `water`, `milk`.

---

## 4. Multi-Source Acquisition & Licensing Strategy

1. **Smartphone & Camera Controlled Capture (Primary Source)**:
   - **License**: 100% Permissive / Proprietary FreshGuard AI Ownership.
   - **Focus**: Captured on smartphones and webcams under real kitchen settings, dining tables, counters, and refrigerators.
2. **Permissive Public Datasets (Secondary Source)**:
   - **Sources**: Roboflow Universe, Open Images v7, Kaggle Produce datasets.
   - **License Requirements**: MIT, Apache 2.0, CC-BY 4.0. Requires explicit license verification and class ID re-mapping.
3. **Data Augmentation (Train-Time Only)**:
   - Apply random hue/saturation shifts, horizontal flips, scale scaling (0.8x – 1.2x), HSV jitter, and perspective rotation strictly during YOLO model training.

---

## 5. Real-World Camera & Scene Diversity Matrix

To ensure webcam robustness, acquired images for every class must be distributed across the following 8 environmental parameters:

| Parameter | Required Diversity Conditions |
| :--- | :--- |
| **Surfaces / Backgrounds** | Stainless steel counter, wooden table, marble countertop, refrigerator shelf, grocery tote bag |
| **Lighting Environments** | Direct daylight, warm indoor LED, dim evening kitchen light, directional spotlight |
| **Camera Perspectives** | Overhead top-down (90°), angled (45°), eye-level (0°), slight tilt |
| **Distance & Scale** | Macro close-up (10–20 cm), medium kitchen view (40–60 cm), wide counter view (1 m+) |
| **Occlusion Level** | Unoccluded single item, 20–40% partial overlap, heavy multi-item clutter |
| **Object Quantities** | Single item, small cluster (2–4 items), large batch (5+ items) |
| **Multi-Class Clutter** | Multi-produce scenes containing 3+ distinct food classes in one frame |
| **Physical Condition** | Intact whole produce, sliced/cut produce, peeled vs unpeeled bulbs |

---

## 6. Produce Failure Investigation & Specific Guidance

- **Potato & Ginger**: High visual texture similarity (brown, earthy skin). Require contrasting backgrounds (white/blue surface) and clear lighting to prevent confusing brown cardboard/wood with potato skin.
- **Tomato & Apple**: Specular highlight reflection under kitchen spotlights. Require diffuse ambient lighting samples to ensure bounding boxes encompass the entire fruit boundary without shrinking around highlights.
- **Onion & Garlic**: Loose dry papery skin vs smooth peeled surface. Require annotations covering dry unpeeled bulbs, peeled bulbs, and red vs yellow onion varieties.

---

## 7. Strict YOLO Annotation Standard

Every object annotation file (`.txt`) must strictly adhere to normalized YOLO format:
`<class_id> <x_center> <y_center> <width> <height>`

### Annotation Rules
1. **Tight Fit**: Bounding box must tightly enclose the outer visible boundary of the object.
2. **Separate Multi-Objects**: Every distinct physical object must receive its own bounding box (no grouping 3 potatoes into a single huge box).
3. **Partial Occlusion**: If an object is partially hidden (up to 50%), annotate the visible portion.
4. **Normalized Coordinates**: All coordinates must satisfy $0.0 \\le x, y, w, h \\le 1.0$.

### Concrete YOLO Annotation Examples

#### Example 1: Multi-Item Kitchen Scene (1 Potato, 2 Tomatoes, 1 Onion)
```text
6 0.254120 0.482100 0.184000 0.210000
5 0.582100 0.314200 0.142000 0.165000
5 0.712400 0.410200 0.138000 0.158000
7 0.412500 0.712000 0.165000 0.182000
```

#### Example 2: Packaged Milk & Cheese
```text
0 0.312000 0.521000 0.220000 0.450000
10 0.684000 0.612000 0.195000 0.280000
```

---

## 8. 6-Stage Quality Assurance (QA) Pipeline

```text
RAW IMAGE CAPTURE
      ↓
LABELING & BOUNDING BOX ANNOTATION
      ↓
AUTOMATED SCHEMAS & COORD CHECK (python scripts/verify_yolo_labels.py)
      ↓
VISUAL OVERLAY REVIEW (Random 10% sampling)
      ↓
SHA-256 DUPLICATE & LEAKAGE FILTERING
      ↓
QA APPROVED DATASET WORKSPACE (datasets/freshguard_35_v3/)
```

### Rejection Criteria
- **REJECT**: Bounding box padded with $>15\\%$ empty space.
- **REJECT**: Unannotated food items present in image.
- **REJECT**: Coordinates $<0.0$ or $>1.0$.
- **REJECT**: Blurry or out-of-focus images where produce boundaries are indistinguishable.

---

## 9. Non-Leaking Train / Validation / Test Split Strategy

- **Split Ratio**: 80% Train, 10% Validation, 10% Test.
- **Leakage Protection**: All images captured in the same photographic session or burst must be assigned to the **same split** (using perceptual image hashing and session timestamps) to prevent data leakage.

---

## 10. Dataset Acceptance Criteria

| Criteria | Status Threshold for `READY_FOR_TRAINING` |
| :--- | :--- |
| **Class Representation** | 35 / 35 classes present with $\\ge 100$ images each |
| **Annotation Integrity** | 0 invalid coordinates, 0 malformed rows, 0 empty label files |
| **Class Balance** | Max-to-Min class object ratio $< 10:1$ |
| **Real-World Ratio** | $\\ge 60\\%$ of images captured in real-world kitchen environments |
| **Duplicate Leakage** | 0 exact SHA-256 duplicate images across splits |

---

## 11. Final Training Readiness Verdict

**CURRENT TRAINING READINESS**: `NOT_READY`

> **VERDICT RATIONALE**:  
> Only **6 of 35 official classes** have data in `datasets/freshguard_35_clean/`. 29 essential grocery produce classes are completely missing. Training a model now would cause complete failure on missing produce. Supplemental acquisition must be completed first.
"""

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print("[SUCCESS] Data Acquisition Plan artifacts generated:")
print(f"  - Markdown: {md_path}")
print(f"  - JSON:     {json_path}")
