# FreshGuard Vision V3 — Safe Production Migration Plan

## 1. Executive Overview
This document outlines the **Safe Production Migration Procedure** for transitioning FreshGuard AI from the 35-class V2 model baseline to the 42-class V3 model candidate.

> [!IMPORTANT]
> **Production Safety Guarantees**:
> - The V2 model weights (`grocery_yolov8_v2_web/model.onnx`) are **NEVER deleted or overwritten**.
> - Model selection is dynamically controlled by environment variable `FRESHGUARD_VISION_MODEL`.
> - System defaults to `FRESHGUARD_VISION_MODEL=v2` until deployment verification passes.
> - Full rollback to V2 is instantaneous, zero-code, and 100% non-destructive.

---

## 2. Model Architecture Comparison

| Dimension | Current V2 Production | V3 Candidate |
| :--- | :--- | :--- |
| **Model Architecture** | YOLOv8 Nano (`grocery_yolov8_v2_web/model.onnx`) | YOLOv8 Nano (`v3_training/deployment/model.onnx`) |
| **Input Shape** | `[1, 3, 640, 640]` | `[1, 3, 320, 320]` (Optimized low-latency webcam shape) |
| **Output Shape** | `[1, 39, 8400]` (4 box + 35 classes) | `[1, 46, 2100]` (4 box + 42 classes) |
| **Vocabulary Count** | 35 Classes (IDs 0–34) | **42 Classes** (IDs 0–41) |
| **V2 ID Preserved** | IDs 0–34 Preserved | **IDs 0–34 Byte-Matched & Preserved** |
| **New Classes Added** | N/A | `avocado`, `beans`, `beet`, `celery`, `fasol`, `salad`, `squash-patisson` |

---

## 3. Cryptographic Hashes & Artifact Locations

| Component | Path | SHA-256 Hash |
| :--- | :--- | :--- |
| **V2 Production Model** | `vision_models/deployment/grocery_yolov8_v2_web/model.onnx` | `5c98003d9c686dcc0733e095143d09fe0bd382b2a7e3b6171fd6c7d76b9dcd7a` |
| **V2 Model Metadata** | `vision_models/model_metadata.json` | `85088cf442c6067f51613b2ad51b8ebbd8f53d3e08705d5cbfbcad3b21709ae0` |
| **V2 Rollback Backup** | `vision_models/rollback_v2/` | **Verified Copy** |
| **V3 Candidate Model** | `training/vision_models/v3_training/deployment/model.onnx` | `59d2a8ef652329c33f901c5fb757580b356cceaabd0a505ae759091b333249de` |
| **V3 Candidate Metadata** | `training/vision_models/v3_training/deployment/v3_classes_metadata.json` | **Verified Metadata** |

---

## 4. Reversible Model Selection Mechanism

Model selection is controlled in `backend/app/core/config.py` and `backend/app/ai/vision/inference.py`:

```bash
# Environment Variable in Render Dashboard / local .env
FRESHGUARD_VISION_MODEL=v2   # Default (loads V2 production model.onnx)
FRESHGUARD_VISION_MODEL=v3   # Candidate (loads V3 model.onnx with 42 classes)
```

- **Default Behavior**: When unset or set to `v2`, `find_v2_onnx_path()` loads `grocery_yolov8_v2_web/model.onnx`.
- **V3 Behavior**: When set to `v3`, `find_v2_onnx_path()` loads `training/vision_models/v3_training/deployment/model.onnx`.

---

## 5. Affected Code Files

- [`backend/app/core/config.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/app/core/config.py): Added `FRESHGUARD_VISION_MODEL: str = os.getenv("FRESHGUARD_VISION_MODEL", "v2").lower()`.
- [`backend/app/ai/vision/inference.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/app/ai/vision/inference.py): Updated `find_v2_onnx_path()` and class metadata candidates array.
- [`vision_models/rollback_v2/`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/vision_models/rollback_v2/): Production backup folder.

---

## 6. Deployment Procedure

1. **Staging Verification**:
   Ensure `FRESHGUARD_VISION_MODEL=v2` locally and verify unit tests pass.
2. **Environment Variable Configuration**:
   In Render Dashboard $\rightarrow$ Environment Settings $\rightarrow$ Add `FRESHGUARD_VISION_MODEL=v3`.
3. **Trigger Zero-Downtime Deploy**:
   Trigger deployment. Render builds container and pre-loads V3 ONNX model session at startup.
4. **Run Production Smoke Tests**:
   - `GET /health` $\rightarrow$ `200 OK`
   - `GET /api/v1/scanner/vision/status` $\rightarrow$ `200 OK`
   - `POST /api/v1/scanner/vision/detect_v2` $\rightarrow$ Test image detection

---

## 7. Zero-Code Rollback Procedure

If any unexpected latency, error, or degradation occurs:

1. Go to **Render Dashboard** $\rightarrow$ **Environment Variables**.
2. Change `FRESHGUARD_VISION_MODEL` back to `v2`.
3. Save changes.
4. Uvicorn reloads in < 5 seconds; system immediately reverts to V2 production baseline (`5c98003d...`).

---

## 8. Failure Conditions Triggering Rollback

- Any HTTP 500 error on `/detect_v2` endpoint.
- ONNX Runtime initialization failure (`_LAST_ONNX_ERROR`).
- Latency exceeding 1000ms per frame request.
- Invalid bounding box coordinates or unmapped class IDs.
