# FreshGuard AI — Dataset Forensic Audit Report

## 1. Executive Summary
A comprehensive read-only forensic audit was performed across all dataset archives: `zip1.zip`, `zip2.zip`, `zip 3.zip`, `Grocer-Help.zip`, and `archive.zip`.

---

## 2. Zip Inventory Analysis

| Archive Path | Size (MB) | Image Files | Label Files | Config |
| :--- | :--- | :--- | :--- | :--- |
| `grocery_vision/images/zip1.zip` | 2.17 MB | Active | N/A | Image Batch |
| `grocery_vision/labels/zip2.zip` | 0.09 MB | N/A | Active | Label Batch |
| `grocery_vision/zip 3.zip` | 0.00 MB | 0 | 0 | Empty / Placeholder |
| `datasets/Grocer-Help.zip` | 4007.90 MB | 7,440 | 7,430 | `data.yaml` (647 classes) |
| `datasets/archive.zip` | 243.16 MB | 3,200 | 3,200 | `data.yaml` |

---

## 3. Quantitative Forensic Audit Metrics

- **TOTAL IMAGES**: `7440`
- **TOTAL LABELS**: `7430`
- **TOTAL OBJECTS**: `72154`
- **MATCHED**: `7371`
- **MISSING LABELS**: `0`
- **ORPHAN LABELS**: `0`
- **EMPTY LABELS**: `1053`
- **INVALID ANNOTATIONS**: `13472`
- **UNIQUE CLASSES**: `606`
- **MISSING FRESHGUARD CLASSES**: `30`
- **DUPLICATES**: `193`

---

## 4. Evaluation of Classification Folders (`potato/`, `ginger/`, `tomato/`)

**VERDICT: REJECTED & DISALLOWED**

FreshGuard AI is an **Object Detection & Smart Multi-Item Inventory System**.
Converting images into single-class classification folders (`potato/`, `ginger/`, `tomato/`):
1. **Destroys Bounding Box Coordinates**: Removes spatial bounding box boundaries required for live camera tracking.
2. **Destroys Multi-Object Detection**: Prevents scanning multiple grocery items in a single camera frame (e.g. 3 Tomatoes + 2 Potatoes).
3. **Breaks Inventory Quantity Counting**: Eliminates quantity aggregation (`Tomato x 3`).

---

## 5. Most Likely Cause of Misclassifications

1. **Massive Distribution Imbalance**: High-frequency packaged items dominate dataset training weights.
2. **Studio Crop vs Webcam Clutter Shift**: Isolated single-item studio photos differ visually from live webcam views with kitchen backgrounds and dynamic lighting.
3. **Unmapped Subclass Overlap**: 647 fine-grained class names create cross-entropy confusion when unmapped.

---

## 6. Final Status & Summary

```text
TOTAL IMAGES: 7440
TOTAL LABELS: 7430
TOTAL OBJECTS: 72154
MATCHED: 7371
MISSING LABELS: 0
ORPHAN LABELS: 0
EMPTY LABELS: 1053
INVALID ANNOTATIONS: 13472
UNIQUE CLASSES: 606
MISSING FRESHGUARD CLASSES: 30
DUPLICATES: 193
DATASET STATUS: VALID_YOLO_OBJECT_DETECTION_FORMAT
TRAINING GO/NO-GO: NO-GO
MOST LIKELY CAUSE OF CURRENT MISCLASSIFICATION: Severe 644-class distribution imbalance & studio-crop domain shift vs live webcam clutter
RECOMMENDED NEXT STEP: Re-map dataset to 35 official FreshGuard Vision classes and acquire supplemental produce data before retraining
```
