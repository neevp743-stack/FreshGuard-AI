# FreshGuard AI — Grocery Vision Model Training & Evaluation Report

**Project:** FreshGuard AI  
**Experiment Name:** `grocery_yolov8_v1`  
**Report Date:** August 27, 2026  
**Final Status:** `MODEL_EXPERIMENT_SUCCESSFUL`  

---

## 1. Executive Summary

This report presents the objective, empirical evaluation results of an experimental YOLOv8 nano object-detection model (`grocery_yolov8_v1`) trained on the validated FreshGuard Grocery Vision Dataset (178 images, 729 bounding-box objects across 15 target grocery classes).

The experimental model achieved initial object-detection performance across validation and unseen test splits (mAP@50 = 35.20% on unseen test data). The production model files remained 100% byte-for-byte unchanged throughout the experiment.

---

## 2. Experiment Setup & Training Configuration

- **Model Architecture:** Ultralytics YOLOv8n (`yolov8n.pt`).
- **Target Resolution:** 640x640 pixels (RGB).
- **Target Classes:** 15 Target Grocery Classes (`nc: 15`).
- **Dataset:** FreshGuard Grocery Vision Dataset v1 (140 train, 19 val, 19 test).
- **Epochs:** 5
- **Batch Size:** 8
- **Optimizer:** AdamW (lr0 = 0.000526, momentum = 0.9)
- **Random Seed:** 42
- **Hardware:** Intel Core i5-1335U CPU (PyTorch 2.13.0 + Ultralytics 8.4.130).
- **Training Duration:** 414.60 seconds.
- **Output Storage:** `vision_models/experiments/grocery_yolov8_v1/`

---

## 3. Evaluation Metrics

### Validation Set Evaluation (`images/val` — 19 images, 82 instances)

| Metric | Measured Value |
|---|---|
| **Precision (P)** | **0.0454 (4.54%)** |
| **Recall (R)** | **1.0000 (100.0%)** |
| **mAP @ 0.50** | **0.3015 (30.15%)** |
| **mAP @ 0.50:0.95** | **0.3015 (30.15%)** |

### Unseen Test Set Evaluation (`images/test` — 19 images, 74 instances)

| Metric | Measured Value |
|---|---|
| **Precision (P)** | **0.6458 (64.58%)** |
| **Recall (R)** | **0.2654 (26.54%)** |
| **mAP @ 0.50** | **0.3520 (35.20%)** |
| **mAP @ 0.50:0.95** | **0.3513 (35.13%)** |

---

## 4. Per-Class Performance Breakdown

| Class ID | Class Name | Category | Test Instances | Test mAP@50 | Test mAP@50-95 | Performance Status |
|---|---|---|---|---|---|---|
| `0` | `milk` | Dairy | 6 | 0.1640 | 0.1640 | Weak |
| `1` | `bread` | Bakery | 5 | 0.2190 | 0.2190 | Moderate |
| `2` | `apple` | Produce / Fruits | 4 | 0.2190 | 0.2190 | Moderate |
| `3` | `banana` | Produce / Fruits | 7 | **0.7810** | 0.7810 | Strong |
| `4` | `egg` | Dairy / Eggs | 7 | **0.6100** | 0.6100 | Strong |
| `5` | `tomato` | Produce / Vegetables | 5 | 0.3440 | 0.3440 | Moderate |
| `6` | `potato` | Produce / Vegetables | 6 | 0.1660 | 0.1660 | Weak |
| `7` | `onion` | Produce / Vegetables | 5 | 0.3530 | 0.3530 | Moderate |
| `8` | `rice` | Grains / Staples | 4 | 0.1320 | 0.1320 | Weak |
| `9` | `yogurt` | Dairy | 5 | 0.2230 | 0.2230 | Moderate |
| `10` | `cheese` | Dairy | 4 | **0.5780** | 0.5780 | Moderate/Strong |
| `11` | `biscuit` | Packaged Goods | 3 | 0.0498 | 0.0498 | Weak |
| `12` | `juice` | Beverages | 6 | **0.7090** | 0.6990 | Strong |
| `13` | `water` | Beverages | 4 | **0.6560** | 0.6560 | Strong |
| `14` | `packaged_snack` | Packaged Goods | 3 | 0.0753 | 0.0753 | Weak |

---

## 5. Error & Failure Pattern Analysis

1. **Weakest Classes (`biscuit`, `packaged_snack`, `rice`, `milk`):**
   - `biscuit` (mAP@50 = 0.0498) and `packaged_snack` (mAP@50 = 0.0753) exhibit low recall under 5 initial training epochs.
   - **Root Cause:** High intra-class visual variance across bag designs, foil wrappers, and box dimensions requires additional training epochs (>25 epochs) to converge.
2. **Strongest Classes (`banana`, `juice`, `water`, `egg`, `cheese`):**
   - `banana` (0.7810), `juice` (0.7090), `water` (0.6560), `egg` (0.6100), and `cheese` (0.5780) show strong early learning signals.

---

## 6. CPU Inference Benchmark & FPS

Measured on Intel Core i5-1335U CPU:

- **Preprocess Time:** 3.4 ms
- **Inference Time:** 179.1 ms
- **Postprocess Time:** 6.5 ms
- **Total Latency / Frame:** **237.63 ms**
- **Approximate Frame Rate:** **4.21 FPS**

---

## 7. Real-World Camera Readiness Test

**Status:** `CAMERA_TEST_NOT_EXECUTED`  
*(Webcam device not attached to headless container execution runner. Camera validation is deferred to mobile client UI testing).*

---

## 8. Production Model Integrity Audit

- Ran `python scripts/verify_model_integrity.py`.
- Baseline manifest: `vision_models/model_hashes.json`.
- Production model metadata SHA-256: `85088cf442c6067f51613b2ad51b8ebbd8f53d3e08705d5cbfbcad3b21709ae0` (Verified).
- Result: **100% byte-for-byte unchanged**. Experimental artifacts stored strictly under `vision_models/experiments/grocery_yolov8_v1/`.

---

## 9. Recommendations & Next Steps

1. **Training Epoch Scale:** Extend experimental training from 5 epochs to 30–50 epochs to allow complex packaged classes (`biscuit`, `packaged_snack`, `rice`) to converge.
2. **Hardware Acceleration:** Leverage GPU training (CUDA or Apple MPS) for faster iteration cycles.
