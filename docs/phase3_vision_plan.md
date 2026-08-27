# FreshGuard AI — Phase 3 Refined Vision Architecture & Dataset Strategy Plan

## 1. Overview & Vision Pipeline Architecture
FreshGuard AI Phase 3 introduces a privacy-first, custom Computer Vision pipeline capable of multi-class, multi-object grocery detection from a single camera frame or uploaded packaging image.

```
+------------------+     Multipart File Upload      +------------------------+
|  Flutter Client  | ---------------------------->  |  FastAPI Backend API   |
| (Camera / Upload)|                                | /scanner/vision/detect |
+------------------+                                +------------------------+
         |                                                       |
         v                                                       v
+------------------+                                +------------------------+
| Render Bounding  |  <---------------------------  |  YOLOv8n Inference     |
| Boxes & Checklist|     JSON Detections Payload    |  (ultralytics==8.1.24) |
+------------------+                                +------------------------+
         |
         v
+------------------+     Combined Multi-modal       +------------------------+
| User Approval    | ---------------------------->  | Inventory & Expiry DB  |
| & Confirm Items  |                                | (OCR Date + Vision ID) |
+------------------+                                +------------------------+
```

---

## 2. Model Architecture & Pinned Dependencies
- **Pinned Model**: **Ultralytics YOLOv8 Nano (`yolov8n.pt`)** exclusively.
- **Pinned Dependency**: `ultralytics==8.1.24` and `torch==2.2.1` in `backend/requirements.txt`.
- **Input Resolution**: 640x640 RGB image tensor.
- **Output Format**: Array of detections with `class_id`, `class_name`, `confidence` score, and normalized pixel bounding box coordinates `[x1, y1, x2, y2]`.

---

## 3. Explicit Dataset Pipeline Stages
```
Image Collection
       ↓
Bounding Box Annotation (LabelImg / CVAT)
       ↓
Label Validation (validate_dataset.py)
       ↓
Dataset Split (70% train / 20% val / 10% test)
       ↓
Training (train.py)
```
> `collect_dataset.py` explicitly marks unannotated raw images as `UNANNOTATED` and will **NOT** claim images are training-ready until corresponding `.txt` label annotation files are validated.

---

## 4. Dataset Format & Directory Structure
- **Format**: Standard YOLO Darknet annotation text format (`<class_id> <x_center> <y_center> <width> <height>`).
- **Directory Structure**:
  ```
  datasets/grocery_vision/
  ├── images/
  │   ├── train/
  │   ├── val/
  │   └── test/
  ├── labels/
  │   ├── train/
  │   ├── val/
  │   └── test/
  ├── raw_unannotated/
  ├── data.yaml
  ├── classes.txt
  └── README.md
  ```

---

## 5. Configurable Initial Classes (15 Classes)
Defined in `backend/app/ai/vision/classes.json`:
1. `0`: `milk`
2. `1`: `bread`
3. `2`: `apple`
4. `3`: `banana`
5. `4`: `egg`
6. `5`: `tomato`
7. `6`: `potato`
8. `7`: `onion`
9. `8`: `rice`
10. `9`: `yogurt`
11. `10`: `cheese`
12. `11`: `biscuit`
13. `12`: `juice`
14. `13`: `water`
15. `14`: `packaged_snack`

---

## 6. Dataset Balance & Anti-Leakage Prevention
- **Dynamic Balance Reporting**: Calculates real class distributions, reporting total images, total objects per class, and balance ratios without enforcing arbitrary fixed quotas (e.g. 300 images/class).
- **Dataset Leakage Prevention**: Session/scene-based grouping ensures that burst captures or multiple photos of the same physical item/countertop scene are assigned exclusively to a single split (train, validation, or test) to prevent data leakage.

---

## 7. Model Lifecycle States & Status API
The vision system tracks 5 explicit model lifecycle states:
- `NOT_TRAINED`: Initial state before dataset collection and training.
- `TRAINING`: Active background training process running.
- `READY`: Trained model weights validated and ready for inference.
- `FAILED`: Training or validation failure encountered.
- `DEPRECATED`: Model version retired.

Returned by `GET /api/scanner/vision/status`:
```json
{
    "lifecycle_state": "NOT_TRAINED",
    "model_available": false,
    "model_version": "0.1.0",
    "classes_count": 15,
    "confidence_threshold": 0.50,
    "message": "Vision model integration is ready; training is pending the real grocery dataset."
}
```

---

## 8. Multi-Modal Identity Priority & Conflict Resolution
1. **Barcode**: Highest-confidence product identity when valid barcode detected.
2. **Vision**: Fallback or additional product identity verification.
3. **OCR**: Primarily used for date extraction (expiry/mfg/batch) and net weight/quantity.
4. **Conflict Resolution**: If Barcode identity and Vision detection disagree (e.g. Barcode = "Organic Whole Milk", Vision = "Juice"), **DO NOT** automatically pick a winner. Flag the discrepancy and require explicit user confirmation.

---

## 9. Privacy-First Active Learning Architecture
- **No Default Image Retention**: Raw household/fridge images uploaded to `/api/scanner/vision/detect` are processed temporarily in memory/temp directory and deleted immediately after inference.
- **Privacy-First Feedback**: User corrections submitted via `POST /api/scanner/vision/feedback` store prediction metadata (predicted class, confidence score, user correction, timestamp) **without** retaining raw images unless the user explicitly toggles `opt_in_image_retention: true`.

---

## 10. Zero False Claims Policy
- No fabricated images, annotations, metrics, accuracy figures, or false claims of a trained model.
- If dataset is missing/unannotated, system reports state `NOT_TRAINED` and returns structured status: *"Vision model integration is ready; training is pending the real grocery dataset."*
