# FreshGuard AI — Phase 3: 35-Class Data Acquisition & Training Readiness Plan

## 1. Executive Summary & Objective

This document defines the comprehensive **Data Acquisition, Annotation, Quality Control, and Training Readiness Plan** for building the future **FreshGuard Vision V3** object-detection dataset.

- **Current Baseline**: `datasets/freshguard_35_clean/` (321 clean images, 3,065 objects across 6 supported classes).
- **Target Goal**: A robust 35-class YOLO object-detection dataset (`datasets/freshguard_35_v3/`) operating reliably across live mobile/webcam streams, dynamic kitchen lighting, multi-item clutter, partial occlusion, and varied orientations.
- **Safety Directive**: **NO MODEL TRAINING** will be conducted until all 35 classes satisfy the minimum data readiness criteria.

---

## 2. Official 35-Class Mapping & Current Status Matrix

| ID | Class Name | Status | Priority | Current Imgs | Current Objs | Min Imgs Needed | Rec Imgs Target | Remaining Needed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | `milk` | AVAILABLE | **LOW** | 43 | 262 | 100 | 150 | `107` |
| 1 | `bread` | LIMITED | **LOW** | 22 | 30 | 100 | 150 | `128` |
| 2 | `apple` | MISSING | **HIGH** | 0 | 0 | 150 | 250 | `250` |
| 3 | `banana` | MISSING | **HIGH** | 0 | 0 | 150 | 250 | `250` |
| 4 | `egg` | MISSING | **HIGH** | 0 | 0 | 150 | 250 | `250` |
| 5 | `tomato` | MISSING | **HIGH** | 0 | 0 | 150 | 250 | `250` |
| 6 | `potato` | MISSING | **HIGH** | 0 | 0 | 150 | 250 | `250` |
| 7 | `onion` | MISSING | **HIGH** | 0 | 0 | 150 | 250 | `250` |
| 8 | `rice` | AVAILABLE | **LOW** | 69 | 684 | 100 | 150 | `81` |
| 9 | `yogurt` | LIMITED | **LOW** | 1 | 1 | 100 | 150 | `149` |
| 10 | `cheese` | AVAILABLE | **LOW** | 121 | 1813 | 100 | 150 | `29` |
| 11 | `biscuit` | MISSING | **MEDIUM** | 0 | 0 | 120 | 200 | `200` |
| 12 | `juice` | MISSING | **MEDIUM** | 0 | 0 | 120 | 200 | `200` |
| 13 | `water` | AVAILABLE | **LOW** | 68 | 275 | 100 | 150 | `82` |
| 14 | `packaged_snack` | MISSING | **MEDIUM** | 0 | 0 | 120 | 200 | `200` |
| 15 | `carrot` | MISSING | **HIGH** | 0 | 0 | 150 | 250 | `250` |
| 16 | `cabbage` | MISSING | **HIGH** | 0 | 0 | 120 | 200 | `200` |
| 17 | `cauliflower` | MISSING | **HIGH** | 0 | 0 | 120 | 200 | `200` |
| 18 | `capsicum` | MISSING | **HIGH** | 0 | 0 | 150 | 250 | `250` |
| 19 | `cucumber` | MISSING | **HIGH** | 0 | 0 | 150 | 250 | `250` |
| 20 | `brinjal` | MISSING | **HIGH** | 0 | 0 | 120 | 200 | `200` |
| 21 | `broccoli` | MISSING | **MEDIUM** | 0 | 0 | 120 | 200 | `200` |
| 22 | `spinach` | MISSING | **HIGH** | 0 | 0 | 150 | 250 | `250` |
| 23 | `peas` | MISSING | **HIGH** | 0 | 0 | 120 | 200 | `200` |
| 24 | `corn` | MISSING | **MEDIUM** | 0 | 0 | 120 | 200 | `200` |
| 25 | `garlic` | MISSING | **HIGH** | 0 | 0 | 120 | 200 | `200` |
| 26 | `ginger` | MISSING | **HIGH** | 0 | 0 | 150 | 250 | `250` |
| 27 | `okra` | MISSING | **HIGH** | 0 | 0 | 120 | 200 | `200` |
| 28 | `beetroot` | MISSING | **MEDIUM** | 0 | 0 | 120 | 200 | `200` |
| 29 | `radish` | MISSING | **MEDIUM** | 0 | 0 | 120 | 200 | `200` |
| 30 | `pumpkin` | MISSING | **MEDIUM** | 0 | 0 | 120 | 200 | `200` |
| 31 | `bitter_gourd` | MISSING | **MEDIUM** | 0 | 0 | 120 | 200 | `200` |
| 32 | `bottle_gourd` | MISSING | **MEDIUM** | 0 | 0 | 120 | 200 | `200` |
| 33 | `green_chilli` | MISSING | **HIGH** | 0 | 0 | 150 | 250 | `250` |
| 34 | `sweet_potato` | MISSING | **MEDIUM** | 0 | 0 | 120 | 200 | `200` |


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
4. **Normalized Coordinates**: All coordinates must satisfy $0.0 \le x, y, w, h \le 1.0$.

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
- **REJECT**: Bounding box padded with $>15\%$ empty space.
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
| **Class Representation** | 35 / 35 classes present with $\ge 100$ images each |
| **Annotation Integrity** | 0 invalid coordinates, 0 malformed rows, 0 empty label files |
| **Class Balance** | Max-to-Min class object ratio $< 10:1$ |
| **Real-World Ratio** | $\ge 60\%$ of images captured in real-world kitchen environments |
| **Duplicate Leakage** | 0 exact SHA-256 duplicate images across splits |

---

## 11. Final Training Readiness Verdict

**CURRENT TRAINING READINESS**: `NOT_READY`

> **VERDICT RATIONALE**:  
> Only **6 of 35 official classes** have data in `datasets/freshguard_35_clean/`. 29 essential grocery produce classes are completely missing. Training a model now would cause complete failure on missing produce. Supplemental acquisition must be completed first.
