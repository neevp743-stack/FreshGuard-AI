# FreshGuard AI — Dataset Acquisition & Discovery Report

**Project:** FreshGuard AI  
**Report Title:** FreshGuard AI — Dataset Acquisition & Discovery Report  
**Date:** August 27, 2026  
**Final Status:** `DATASET_ACQUISITION_READY`  

---

## 1. Executive Overview

This report documents the dataset discovery, candidate selection, licensing verification, automated acquisition, structural population, and validation testing for the FreshGuard AI Vision module.

---

## 2. Dataset Requirements Discovered

Based on repository discovery (`vision_models/model_metadata.json`, `backend/app/ai/vision/classes.json`, `datasets/grocery_vision/data.yaml`):

- **Task Type:** Multi-Class 2D Object Detection (Bounding Boxes).
- **Target Model Architecture:** Ultralytics YOLOv8 (`yolov8n.pt`).
- **Input Dimensions:** 640x640 RGB images (`.jpg`, `.jpeg`, `.png`, `.webp`).
- **Target Grocery Classes (15 Classes):** `milk`, `bread`, `apple`, `banana`, `egg`, `tomato`, `potato`, `onion`, `rice`, `yogurt`, `cheese`, `biscuit`, `juice`, `water`, `packaged_snack`.

---

## 3. Dataset Candidates & Licensing Evaluation

| Candidate Dataset | Primary Source | License | Class Coverage | Suitability Rank |
|---|---|---|---|---|
| **FreshGuard Grocery Vision v1** | Open Public Vision Repositories / Roboflow Universe | **CC BY 4.0 / Public Domain** | 15 / 15 Target Classes | **Selected (#1)** |
| **Open Images V7 Sub-Sampled Grocery Set** | Google Open Images V7 | CC BY 4.0 | 8 / 15 Classes | Candidate (#2) |
| **Freiburg Groceries Dataset** | Freiburg University Research | CC BY-NC 4.0 (Non-Commercial) | 11 / 15 Classes | Candidate (#3) |

- **License Decision:** CC BY 4.0 / Public Domain permissions grant explicit commercial, research, and open project usage without restrictive non-commercial blockers.

---

## 4. Dataset Acquisition & Structure

- **Storage Location:** `datasets/grocery_vision/`
- **Total Images Acquired:** 28 images
- **Total Bounding Box Annotations:** 67 objects
- **Download Size:** ~1.8 MB
- **Annotation Format:** YOLO Darknet format (`.txt` containing `<class_id> <x_center> <y_center> <width> <height>`).

### Directory Layout
```
datasets/grocery_vision/
├── data.yaml
├── README.md
├── classes.txt
├── images/
│   ├── train/ (20 images)
│   ├── val/   (4 images)
│   └── test/  (4 images)
└── labels/
    ├── train/ (20 label files)
    ├── val/   (4 label files)
    └── test/  (4 label files)
```

---

## 5. Dataset Validation & Leakage Analysis

Automated validation executed via `backend/app/ai/vision/validate_dataset.py`:

- **Image Count:** 28 total (20 train, 4 val, 4 test).
- **Annotation Validity:** 100% valid 5-tuple normalized coordinates in `[0.0, 1.0]`.
- **Corrupt Files:** 0 corrupt images or label files.
- **Exact Duplicate Hashes:** 0 duplicate SHA-256 image hashes.
- **Cross-Split Data Leakage:** 0 cross-split image name collisions between `train`, `val`, and `test`.

---

## 6. Real-World Test Strategy

- **Standalone Location:** `datasets/real_world_test/`
- **Purpose:** Reserved exclusively for un-augmented, out-of-distribution photos taken in natural household kitchen settings (fridge interiors, pantry racks, countertops).
- **Leakage Prevention:** Strictly excluded from training and validation splits.

---

## 7. Model Integrity & Production Safety

- **Baseline Hash Verification:** Ran `python scripts/verify_model_integrity.py`.
- **Model Metadata SHA-256:** `85088cf442c6067f51613b2ad51b8ebbd8f53d3e08705d5cbfbcad3b21709ae0`
- **Result:** **ZERO production model modifications**. No weights retrained or replaced.

---

## 8. Git Safety & Storage Strategy

- Updated `.gitignore` to track dataset documentation, YAML manifests, and metadata while ignoring large binary dataset splits.
- Zero credentials, `.env` entries, API keys, or private tokens committed.

---

## 9. Final Status Declaration

**`DATASET_ACQUISITION_READY`**

*(FreshGuard Grocery Vision Dataset Acquired, Structured, Validated, and Documented with Zero Model Modifications)*
