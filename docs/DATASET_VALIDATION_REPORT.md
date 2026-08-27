# FreshGuard AI — Dataset Validation Report

**Dataset:** FreshGuard Grocery Vision Dataset v1  
**Validation Date:** August 27, 2026  
**Validator Script:** `backend/app/ai/vision/validate_dataset.py`  
**Overall Result:** **VALID [OK]**  

---

## 1. Measured Dataset Summary

| Metric | Measured Value | Requirement Status |
|---|---|---|
| **Total Images** | 28 | **VERIFIED** |
| **Annotated Images** | 28 | **VERIFIED** |
| **Total Bounding Box Objects** | 67 | **VERIFIED** |
| **Training Set (`images/train`)** | 20 images (71.4%) | **VERIFIED** |
| **Validation Set (`images/val`)** | 4 images (14.3%) | **VERIFIED** |
| **Testing Set (`images/test`)** | 4 images (14.3%) | **VERIFIED** |
| **Invalid Labels** | 0 | **VERIFIED** |
| **Missing Label Files** | 0 | **VERIFIED** |
| **Cross-Split Leakage Warnings** | 0 | **VERIFIED** |
| **Corrupt Image Files** | 0 | **VERIFIED** |

---

## 2. Object Class Distribution (15 Classes)

| Class ID | Class Name | Category | Bounding Box Objects Count |
|---|---|---|---|
| `0` | `milk` | Dairy | 6 |
| `1` | `bread` | Bakery | 6 |
| `2` | `apple` | Produce / Fruits | 6 |
| `3` | `banana` | Produce / Fruits | 6 |
| `4` | `egg` | Dairy / Eggs | 5 |
| `5` | `tomato` | Produce / Vegetables | 5 |
| `6` | `potato` | Produce / Vegetables | 5 |
| `7` | `onion` | Produce / Vegetables | 5 |
| `8` | `rice` | Grains / Staples | 5 |
| `9` | `yogurt` | Dairy | 3 |
| `10` | `cheese` | Dairy | 3 |
| `11` | `biscuit` | Packaged Goods | 3 |
| `12` | `juice` | Beverages | 3 |
| `13` | `water` | Beverages | 3 |
| `14` | `packaged_snack` | Packaged Goods | 3 |

---

## 3. Data Leakage & Duplicate Hash Inspection

- **Exact Duplicate SHA-256 Hashes:** 0 duplicate image hashes detected.
- **Cross-Split File Name Collisions:** 0 cross-split duplicates found between `train`, `val`, and `test`.
- **Anti-Leakage Rule Compliance:** Images captured in the same session remain strictly isolated within a single directory split.

---

## 4. Annotation Integrity Audit

- **Coordinate Bounds:** 100% of bounding box normalized coordinates `(x_center, y_center, width, height)` satisfy `0.0 <= val <= 1.0`.
- **Item Count Per Line:** 100% of annotation lines contain exactly 5 space-separated items (`class_id x_center y_center width height`).
- **Class ID Ranges:** All class IDs fall strictly in the integer range `[0, 14]`.
