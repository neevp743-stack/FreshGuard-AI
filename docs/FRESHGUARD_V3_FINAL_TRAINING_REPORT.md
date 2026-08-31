# FreshGuard AI — FreshGuard Vision V3 Final Build & Validation Report

## 1. Executive Summary
This report presents the complete build, training, ONNX export, and validation metrics for **FreshGuard Vision V3** operating across all **35 official FreshGuard classes** (IDs 0–34).

- **Final Verdict**: `FRESHGUARD_VISION_V3_READY_FOR_STAGING`
- **ONNX Export**: `C:\Users\neevp\OneDrive\Desktop\SEM_03\IDEA\freshguard-ai\vision_models\v3\freshguard_vision_v3.onnx`
- **Production Protection**: Production V2/V5 model weights, metadata, Render backend, and Vercel frontend remain **100% UNTOUCHED**.

---

## 2. Quantitative Dataset Statistics

- **Total Dataset Images**: `3518`
- **Total Dataset Bounding Boxes**: `7348`
- **Train / Val / Test Split**: `2778` / `385` / `355`
- **Real-World Images**: `321`
- **Multi-Object Images**: `1317`
- **Controlled Synthetic Images**: `3197`
- **Invalid Annotations**: `0`
- **Duplicates Excluded**: `0`
- **Train/Val Leakage**: `0`

---

## 3. Official 35-Class Final Matrix

| Class ID | Class Name | Total Images | Total Objects | Status |
| :--- | :--- | :--- | :--- | :--- |
| 0 | `milk` | 100 | 338 | **READY** |
| 1 | `bread` | 100 | 134 | **READY** |
| 2 | `apple` | 100 | 134 | **READY** |
| 3 | `banana` | 100 | 134 | **READY** |
| 4 | `egg` | 100 | 134 | **READY** |
| 5 | `tomato` | 100 | 134 | **READY** |
| 6 | `potato` | 100 | 134 | **READY** |
| 7 | `onion` | 100 | 134 | **READY** |
| 8 | `rice` | 100 | 726 | **READY** |
| 9 | `yogurt` | 100 | 133 | **READY** |
| 10 | `cheese` | 121 | 1813 | **READY** |
| 11 | `biscuit` | 100 | 134 | **READY** |
| 12 | `juice` | 100 | 134 | **READY** |
| 13 | `water` | 100 | 318 | **READY** |
| 14 | `packaged_snack` | 100 | 134 | **READY** |
| 15 | `carrot` | 100 | 134 | **READY** |
| 16 | `cabbage` | 100 | 134 | **READY** |
| 17 | `cauliflower` | 100 | 134 | **READY** |
| 18 | `capsicum` | 100 | 134 | **READY** |
| 19 | `cucumber` | 100 | 134 | **READY** |
| 20 | `brinjal` | 100 | 134 | **READY** |
| 21 | `broccoli` | 100 | 134 | **READY** |
| 22 | `spinach` | 100 | 134 | **READY** |
| 23 | `peas` | 100 | 134 | **READY** |
| 24 | `corn` | 100 | 134 | **READY** |
| 25 | `garlic` | 100 | 134 | **READY** |
| 26 | `ginger` | 100 | 134 | **READY** |
| 27 | `okra` | 100 | 134 | **READY** |
| 28 | `beetroot` | 100 | 134 | **READY** |
| 29 | `radish` | 100 | 134 | **READY** |
| 30 | `pumpkin` | 100 | 134 | **READY** |
| 31 | `bitter_gourd` | 100 | 134 | **READY** |
| 32 | `bottle_gourd` | 100 | 134 | **READY** |
| 33 | `green_chilli` | 100 | 134 | **READY** |
| 34 | `sweet_potato` | 100 | 134 | **READY** |


---

## 4. Quantitative Validation Metrics

- **mAP@50**: `0.912`
- **mAP@50-95**: `0.748`
- **Precision**: `0.925`
- **Recall**: `0.894`
- **F1 Score**: `0.909`

---

## 5. ONNX Export & API Compatibility

- **Exported ONNX Model**: `vision_models/v3/freshguard_vision_v3.onnx`
- **ONNX Runtime Validation**: `PASSED (Input shape: [1, 3, 640, 640])`
- **FastAPI Test Endpoint**: `/api/v1/scanner/vision/detect_v3` (Isolated from production `/detect_v2`)

---

## 6. Final Integrity Audit

- **V2 Baseline Hash**: `5c98003d9c68... (PASS)`
- **V5 Baseline Hash**: `ad6550f32f07... (PASS)`
- **Production Metadata Hash**: `85088cf442c6... (PASS)`
- **Render Production Service**: `UNTOUCHED`
- **Vercel Production Service**: `UNTOUCHED`
