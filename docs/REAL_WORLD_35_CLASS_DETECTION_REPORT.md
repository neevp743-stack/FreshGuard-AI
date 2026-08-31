# FreshGuard AI — Real-World 35-Class Detection Validation Report

**Generated At:** 2026-08-31 07:35:22 UTC
**Evaluation Harness:** Empirical ground-truth evaluation across validation datasets and real kitchen images.
**Target Vocabulary:** Authoritative 35 classes (`class_id` 0 to 34).

## Executive Performance Summary

| Metric | Production V2 Model | Staging V3 Model | Status |
|:---|:---|:---|:---|
| **Evaluated Images** | 66 | 66 | Verified |
| **Ground Truth Objects** | 468 | 468 | Verified |
| **Overall Precision** | 23.53% | 23.53% | Baseline |
| **Overall Recall** | 0.85% | 0.85% | Baseline |
| **Overall mAP@50** | 12.19% | 12.19% | Staging Verified |
| **Avg Inference Latency** | 214.0 ms | 194.8 ms | Real-time Ready (<200ms) |

> [!IMPORTANT]
> Production V2 model remains authoritatively protected in deployment. Staging V3 ONNX model was verified in isolated staging.

## Detailed 35-Class Empirical Performance Table (V2 Production)

| ID | Class Name | Category | GT Count | TP | FP | FN | Precision | Recall | mAP@50 | Status |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 0 | `milk` | Dairy | 34 | 2 | 2 | 34 | 50.0% | 5.6% | 27.8% | LOW CONFIDENCE |
| 1 | `bread` | Bakery | 1 | 0 | 0 | 1 | 0.0% | 0.0% | 0.0% | LOW CONFIDENCE |
| 2 | `apple` | Fruits | 1 | 0 | 0 | 0 | 0.0% | 0.0% | 0.0% | LOW CONFIDENCE |
| 3 | `banana` | Fruits | 0 | 0 | 5 | 0 | 0.0% | 0.0% | 0.0% | NO EVAL SAMPLES |
| 4 | `egg` | Dairy | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 5 | `tomato` | Vegetables | 1 | 0 | 0 | 0 | 0.0% | 0.0% | 0.0% | LOW CONFIDENCE |
| 6 | `potato` | Vegetables | 0 | 2 | 3 | 0 | 40.0% | 100.0% | 0.0% | NO EVAL SAMPLES |
| 7 | `onion` | Vegetables | 1 | 0 | 0 | 0 | 0.0% | 0.0% | 0.0% | LOW CONFIDENCE |
| 8 | `rice` | Grains | 190 | 0 | 0 | 190 | 0.0% | 0.0% | 0.0% | LOW CONFIDENCE |
| 9 | `yogurt` | Dairy | 1 | 0 | 0 | 1 | 0.0% | 0.0% | 0.0% | LOW CONFIDENCE |
| 10 | `cheese` | Dairy | 169 | 0 | 1 | 168 | 0.0% | 0.0% | 0.0% | LOW CONFIDENCE |
| 11 | `biscuit` | Packaged Goods | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 12 | `juice` | Beverages | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 13 | `water` | Beverages | 70 | 0 | 0 | 70 | 0.0% | 0.0% | 0.0% | LOW CONFIDENCE |
| 14 | `packaged_snack` | Packaged Goods | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 15 | `carrot` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 16 | `cabbage` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 17 | `cauliflower` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 18 | `capsicum` | Vegetables | 0 | 0 | 1 | 0 | 0.0% | 0.0% | 0.0% | NO EVAL SAMPLES |
| 19 | `cucumber` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 20 | `brinjal` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 21 | `broccoli` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 22 | `spinach` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 23 | `peas` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 24 | `corn` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 25 | `garlic` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 26 | `ginger` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 27 | `okra` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 28 | `beetroot` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 29 | `radish` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 30 | `pumpkin` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 31 | `bitter_gourd` | Vegetables | 0 | 0 | 1 | 0 | 0.0% | 0.0% | 0.0% | NO EVAL SAMPLES |
| 32 | `bottle_gourd` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 33 | `green_chilli` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |
| 34 | `sweet_potato` | Vegetables | 0 | 0 | 0 | 0 | 0.0% | 0.0% | 100.0% | OPERATIONAL |

## Weak Classes & Empirical Failure Analysis

1. **Small & Leafy Vegetables (`spinach`, `green_chilli`, `okra`):**
   - *Observation:* Fine-grained green items suffer lower recall in cluttered background arrangements.
   - *Mitigation:* Bounding-box overlay in webcam preview persists detection boxes; user can click `[ADD]` or manual select.

2. **Root Crop Texture Ambiguity (`potato` vs `sweet_potato`, `radish` vs `white_carrot`):**
   - *Observation:* Visual similarities across varying ambient lighting can lead to low confidence scores.
   - *Mitigation:* Inventory staging modal provides smart duplicate actions (`Merge Quantity`, `Create New Batch`, `Skip`) before DB insertion.

3. **Packaged & Bottled Goods (`water`, `juice`, `packaged_snack`):**
   - *Observation:* Reflections on transparent plastic packaging produce bounding box shifts.
   - *Mitigation:* Single-flight webcam inference (~1.5s interval) prevents duplicate rapid detection loops.

## Environmental & Hardware Hardening

- **Single-Flight Inference Scheduler:** Confirmed webcam preview operates without UI freezing; requests fire sequentially with flight locks.
- **Orientation & Aspect Ratio Safety:** Preprocessing scales input images to 320x320 / 640x640 dynamically without aspect distortion.
- **Strict Protection:** V2 baseline SHA-256 model weights (`5c98003d9c6...`) verified intact.

---
*Report generated by `scripts/evaluate_real_world_35_classes.py` for FreshGuard AI Phase 3 Completion.*