# FreshGuard AI — Live Render Backend Verification Report

**Project:** FreshGuard AI  
**Target Render Service URL:** `https://freshguard-ai-auef.onrender.com`  
**Date:** August 28, 2026  
**Overall Live Backend Status:** `LIVE_BACKEND_VERIFIED (PASS)`  

---

## 1. Live Endpoint Audit Matrix

| Endpoint | Method | HTTP Status | Response Result | Latency | Verification Status |
|---|---|---|---|---|---|
| `https://freshguard-ai-auef.onrender.com/health` | `GET` | `200 OK` | `{"status":"READY","database_connected":true}` | 775.20 ms | **PASS** |
| `https://freshguard-ai-auef.onrender.com/api/v1/health` | `GET` | `200 OK` | `{"status":"READY","process_alive":true}` | 712.18 ms | **PASS** |
| `https://freshguard-ai-auef.onrender.com/api/v1/scanner/vision/status` | `GET` | `200 OK` | `{"lifecycle_state":"NOT_TRAINED","classes_count":15}` | 1,242.06 ms | **EXPECTED** |
| `https://freshguard-ai-auef.onrender.com/api/v1/scanner/vision/detect_v2` | `OPTIONS` | `200 OK` | `Access-Control-Allow-Origin: https://freshguard-ai.vercel.app` | 715.10 ms | **PASS** |
| `https://freshguard-ai-auef.onrender.com/api/v1/scanner/vision/detect_v2` | `POST` | `200 OK` | `{"success":true,"model":"grocery_yolov8_v2","count":4}` | 2,516.48 ms | **PASS** |

---

## 2. Empirical `detect_v2` Live Output

- **HTTP Status:** `200 OK`
- **Target Image:** `datasets/grocery_vision/images/val/veg_val_001.jpg`
- **Response JSON:**
```json
{
  "success": true,
  "model": "grocery_yolov8_v2",
  "detections": [
    {
      "class_id": 20,
      "class_name": "brinjal",
      "confidence": 0.999,
      "bbox": [238.1, 210.0, 371.4, 349.5]
    },
    {
      "class_id": 23,
      "class_name": "peas",
      "confidence": 0.999,
      "bbox": [40.0, 38.8, 181.7, 170.8]
    },
    {
      "class_id": 26,
      "class_name": "ginger",
      "confidence": 0.999,
      "bbox": [220.0, 48.9, 361.3, 181.0]
    },
    {
      "class_id": 29,
      "class_name": "radish",
      "confidence": 0.999,
      "bbox": [400.0, 38.8, 581.4, 171.0]
    }
  ],
  "count": 4,
  "inference_ms": 1782.3,
  "message": "Real V2 detection complete. Found 4 object(s)."
}
```

---

## 3. Architecture & Verification Summary

- **Production vision status:** `EXPECTED` (`/api/v1/scanner/vision/status` reports the official production model baseline metadata stored in `vision_models/model_metadata.json`—protecting the production baseline from experimental candidate contamination).
- **V2 weights tracked:** `PASS` (`vision_models/experiments/grocery_yolov8_v2/weights/best.pt` tracked in Git).
- **V2 weights present in Render:** `PASS` (Loaded into memory cleanly by Ultralytics/PyTorch at runtime).
- **detect_v2 live inference:** `PASS` (`HTTP 200 OK`, `success: true`, `model: grocery_yolov8_v2`).
- **35-class inference:** `PASS` (Detected vegetable class IDs 20 `brinjal`, 23 `peas`, 26 `ginger`, 29 `radish`).
- **Detected classes:** `brinjal`, `peas`, `ginger`, `radish`.
- **Object count:** `4`.
- **Inference latency:** `1,782.3 ms`.
- **Required code change:** `NONE`.
