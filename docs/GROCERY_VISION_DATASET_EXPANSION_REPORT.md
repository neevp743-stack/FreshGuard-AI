# FreshGuard AI — Grocery Vision Dataset Expansion Report

**Project:** FreshGuard AI  
**Report Title:** FreshGuard AI — Grocery Vision Dataset Expansion Report  
**Date:** August 27, 2026  
**Final Classification:** `DATASET_EXPANDED_TRAINING_READY`  

---

## 1. Executive Summary

The FreshGuard AI Grocery Vision Dataset has been expanded from a baseline prototype into a robust multi-class object detection dataset.

- **Baseline Images:** 28 images
- **Expanded Images:** 178 images (**+535.7% increase**)
- **Baseline Bounding Box Objects:** 67 objects
- **Expanded Bounding Box Objects:** 729 objects (**+988.1% increase**)
- **Class Coverage:** 15 / 15 Target Classes (mean 48.6 objects per class)
- **Annotation Validation:** 100% valid YOLO Darknet 5-tuple normalized coordinates in `[0.0, 1.0]`

---

## 2. Quantitative Comparison (Before vs After)

| Metric | Before Expansion | After Expansion | Growth | Status |
|---|---|---|---|---|
| **Total Images** | 28 | **178** | +150 (+535.7%) | **VERIFIED** |
| **Total Bounding Box Objects** | 67 | **729** | +662 (+988.1%) | **VERIFIED** |
| **Average Objects / Image** | 2.39 | **4.10** | +1.71 objects/img | **VERIFIED** |
| **Train Set Images** | 20 (71.4%) | **140 (78.7%)** | +120 | **VERIFIED** |
| **Validation Set Images** | 4 (14.3%) | **19 (10.7%)** | +15 | **VERIFIED** |
| **Test Set Images** | 4 (14.3%) | **19 (10.6%)** | +15 | **VERIFIED** |
| **Invalid Labels** | 0 | **0** | 0 errors | **VERIFIED** |
| **Corrupt Files** | 0 | **0** | 0 corrupt | **VERIFIED** |
| **Cross-Split Leakage Warnings** | 0 | **0** | 0 leakage | **VERIFIED** |

---

## 3. Class Distribution Comparison (15 Classes)

| Class ID | Class Name | Category | Objects Before | Objects After | Growth |
|---|---|---|---|---|---|
| `0` | `milk` | Dairy | 6 | **57** | +850.0% |
| `1` | `bread` | Bakery | 6 | **47** | +683.3% |
| `2` | `apple` | Produce / Fruits | 6 | **41** | +583.3% |
| `3` | `banana` | Produce / Fruits | 6 | **58** | +866.7% |
| `4` | `egg` | Dairy / Eggs | 5 | **50** | +900.0% |
| `5` | `tomato` | Produce / Vegetables | 5 | **43** | +760.0% |
| `6` | `potato` | Produce / Vegetables | 5 | **58** | +1060.0% |
| `7` | `onion` | Produce / Vegetables | 5 | **49** | +880.0% |
| `8` | `rice` | Grains / Staples | 5 | **42** | +740.0% |
| `9` | `yogurt` | Dairy | 3 | **55** | +1733.3% |
| `10` | `cheese` | Dairy | 3 | **47** | +1466.7% |
| `11` | `biscuit` | Packaged Goods | 3 | **38** | +1166.7% |
| `12` | `juice` | Beverages | 3 | **55** | +1733.3% |
| `13` | `water` | Beverages | 3 | **47** | +1466.7% |
| `14` | `packaged_snack` | Packaged Goods | 3 | **42** | +1300.0% |

---

## 4. Quality Control & Anti-Leakage Protocol

1. **Staging & Quality Filter (`datasets/_acquisition/`):**
   - PIL byte stream verification rejected corrupt files.
   - SHA-256 duplicate image hash check prevented identical image inclusion.
2. **Session / Burst Isolation:**
   - Multi-frame burst captures from single camera sessions are grouped strictly inside one split directory (`train`, `val`, or `test`).
   - Zero filename collisions or image hash overlap detected across splits.

---

## 5. Environmental & Scene Diversity

The expanded dataset introduces diverse household contexts:
- **Refrigerator Scenes:** Internal shelf glass, door racks, dim interior LED lighting.
- **Pantry Racks:** Wooden and metal wire shelving, layered product placement.
- **Kitchen Countertops:** Granite and tile surfaces with ambient lighting.
- **Shopping Bags:** Grocery paper/tote bags with partial top-down product views.
- **Multi-Object Density:** Average of 4.1 objects per scene with varying degrees of partial occlusion (30% to 100% visible area).

---

## 6. Model Integrity & Production Safety

- Checked baseline model hashes via `python scripts/verify_model_integrity.py`.
- Result: **100% byte-for-byte unchanged** (`model_metadata.json`: `85088cf442c6067f51613b2ad51b8ebbd8f53d3e08705d5cbfbcad3b21709ae0`).
- No ML models were retrained or altered during this dataset expansion task.

---

## 7. Final Classification

**`DATASET_EXPANDED_TRAINING_READY`**

*(Expanded FreshGuard Grocery Vision Dataset validated with 178 images, 729 objects across 15 target classes; dataset is ready for controlled model training)*
