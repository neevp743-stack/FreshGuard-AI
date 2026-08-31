# FreshGuard AI — V3 Dataset Readiness & Preparation Report

## 1. Executive Summary
This report documents the compilation, quality filtering, non-leaking 80/20 train/val split, and readiness audit of the **FreshGuard Vision V3 Training Dataset** (`datasets/freshguard_v3/`).

- **Target Location**: `C:\Users\neevp\OneDrive\Desktop\SEM_03\IDEA\freshguard-ai\datasets\freshguard_v3`
- **YOLO Format**: Normalized `<class_id> <x_center> <y_center> <width> <height>` (IDs 0..34)
- **Model Integrity Safeguard**: Production ONNX models, metadata, and live Render/Vercel services remain **100% UNTOUCHED**.

---

## 2. Quantitative Dataset Statistics

- **Official Classes**: `35`
- **Classes Meeting Minimum Readiness**: `1 / 35`
- **Classes Missing / Insufficient**: `34 / 35`
- **Total Compiled Images**: `321` (Train: `257`, Val: `64`)
- **Total Compiled Bounding Boxes**: `3065` (Train: `2602`, Val: `463`)
- **Invalid Annotations Rejected**: `0`
- **Duplicate Images Excluded**: `0`
- **Train/Val Leakage**: `0`

---

## 3. Official 35-Class Readiness Matrix

| Class ID | Class Name | Train Imgs | Val Imgs | Train Objs | Val Objs | Total Objs | Min Target | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | `milk` | 33 | 10 | 229 | 33 | 262 | 100 | **NEEDS_MORE_DATA** |
| 1 | `bread` | 22 | 0 | 30 | 0 | 30 | 100 | **NEEDS_MORE_DATA** |
| 2 | `apple` | 0 | 0 | 0 | 0 | 0 | 150 | **MISSING** |
| 3 | `banana` | 0 | 0 | 0 | 0 | 0 | 150 | **MISSING** |
| 4 | `egg` | 0 | 0 | 0 | 0 | 0 | 150 | **MISSING** |
| 5 | `tomato` | 0 | 0 | 0 | 0 | 0 | 150 | **MISSING** |
| 6 | `potato` | 0 | 0 | 0 | 0 | 0 | 150 | **MISSING** |
| 7 | `onion` | 0 | 0 | 0 | 0 | 0 | 150 | **MISSING** |
| 8 | `rice` | 50 | 19 | 494 | 190 | 684 | 100 | **NEEDS_MORE_DATA** |
| 9 | `yogurt` | 0 | 1 | 0 | 1 | 1 | 100 | **NEEDS_MORE_DATA** |
| 10 | `cheese` | 101 | 20 | 1644 | 169 | 1813 | 100 | **READY** |
| 11 | `biscuit` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 12 | `juice` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 13 | `water` | 54 | 14 | 205 | 70 | 275 | 100 | **NEEDS_MORE_DATA** |
| 14 | `packaged_snack` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 15 | `carrot` | 0 | 0 | 0 | 0 | 0 | 150 | **MISSING** |
| 16 | `cabbage` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 17 | `cauliflower` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 18 | `capsicum` | 0 | 0 | 0 | 0 | 0 | 150 | **MISSING** |
| 19 | `cucumber` | 0 | 0 | 0 | 0 | 0 | 150 | **MISSING** |
| 20 | `brinjal` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 21 | `broccoli` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 22 | `spinach` | 0 | 0 | 0 | 0 | 0 | 150 | **MISSING** |
| 23 | `peas` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 24 | `corn` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 25 | `garlic` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 26 | `ginger` | 0 | 0 | 0 | 0 | 0 | 150 | **MISSING** |
| 27 | `okra` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 28 | `beetroot` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 29 | `radish` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 30 | `pumpkin` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 31 | `bitter_gourd` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 32 | `bottle_gourd` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |
| 33 | `green_chilli` | 0 | 0 | 0 | 0 | 0 | 150 | **MISSING** |
| 34 | `sweet_potato` | 0 | 0 | 0 | 0 | 0 | 120 | **MISSING** |


---

## 4. Missing Classes & Acquisition Requirements

- **`milk` (ID 0)**: 43 / 100 images (Requires **+57 additional images**)
- **`bread` (ID 1)**: 22 / 100 images (Requires **+78 additional images**)
- **`apple` (ID 2)**: 0 / 150 images (Requires **+150 additional images**)
- **`banana` (ID 3)**: 0 / 150 images (Requires **+150 additional images**)
- **`egg` (ID 4)**: 0 / 150 images (Requires **+150 additional images**)
- **`tomato` (ID 5)**: 0 / 150 images (Requires **+150 additional images**)
- **`potato` (ID 6)**: 0 / 150 images (Requires **+150 additional images**)
- **`onion` (ID 7)**: 0 / 150 images (Requires **+150 additional images**)
- **`rice` (ID 8)**: 69 / 100 images (Requires **+31 additional images**)
- **`yogurt` (ID 9)**: 1 / 100 images (Requires **+99 additional images**)
- **`biscuit` (ID 11)**: 0 / 120 images (Requires **+120 additional images**)
- **`juice` (ID 12)**: 0 / 120 images (Requires **+120 additional images**)
- **`water` (ID 13)**: 68 / 100 images (Requires **+32 additional images**)
- **`packaged_snack` (ID 14)**: 0 / 120 images (Requires **+120 additional images**)
- **`carrot` (ID 15)**: 0 / 150 images (Requires **+150 additional images**)
- **`cabbage` (ID 16)**: 0 / 120 images (Requires **+120 additional images**)
- **`cauliflower` (ID 17)**: 0 / 120 images (Requires **+120 additional images**)
- **`capsicum` (ID 18)**: 0 / 150 images (Requires **+150 additional images**)
- **`cucumber` (ID 19)**: 0 / 150 images (Requires **+150 additional images**)
- **`brinjal` (ID 20)**: 0 / 120 images (Requires **+120 additional images**)
- **`broccoli` (ID 21)**: 0 / 120 images (Requires **+120 additional images**)
- **`spinach` (ID 22)**: 0 / 150 images (Requires **+150 additional images**)
- **`peas` (ID 23)**: 0 / 120 images (Requires **+120 additional images**)
- **`corn` (ID 24)**: 0 / 120 images (Requires **+120 additional images**)
- **`garlic` (ID 25)**: 0 / 120 images (Requires **+120 additional images**)
- **`ginger` (ID 26)**: 0 / 150 images (Requires **+150 additional images**)
- **`okra` (ID 27)**: 0 / 120 images (Requires **+120 additional images**)
- **`beetroot` (ID 28)**: 0 / 120 images (Requires **+120 additional images**)
- **`radish` (ID 29)**: 0 / 120 images (Requires **+120 additional images**)
- **`pumpkin` (ID 30)**: 0 / 120 images (Requires **+120 additional images**)
- **`bitter_gourd` (ID 31)**: 0 / 120 images (Requires **+120 additional images**)
- **`bottle_gourd` (ID 32)**: 0 / 120 images (Requires **+120 additional images**)
- **`green_chilli` (ID 33)**: 0 / 150 images (Requires **+150 additional images**)
- **`sweet_potato` (ID 34)**: 0 / 120 images (Requires **+120 additional images**)


---

## 5. Final Training Gate Verdict

**TRAINING VERDICT**: `TRAINING_NOT_READY`

> **GATE DECISION RATIONALE**:  
> V3 model training is **STRICTLY BLOCKED / NOT READY**. Although `1` classes have clean, validated YOLO annotations, **34 essential FreshGuard produce classes** have insufficient data. Executing YOLO training now would lead to immediate detection regression for missing fresh produce. Supplemental acquisition must be completed before training V3.
