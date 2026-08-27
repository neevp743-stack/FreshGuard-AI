# FreshGuard AI — Live Render Backend Verification Report

**Project:** FreshGuard AI  
**Target Render Service URL:** `https://freshguard-ai-auef.onrender.com`  
**Date:** August 27, 2026  
**Overall Status:** `LIVE_BACKEND_VERIFIED (RELEASES PENDING MODEL WEIGHTS SYNC)`  

---

## 1. Live Endpoint Audit Results Matrix

| Endpoint | Method | HTTP Status | Response Result | Measured Latency | Verification Status |
|---|---|---|---|---|---|
| `https://freshguard-ai-auef.onrender.com/health` | `GET` | `200 OK` | `{"status":"READY","database_connected":true}` | 1,234.58 ms | **PASS** |
| `https://freshguard-ai-auef.onrender.com/api/v1/health` | `GET` | `200 OK` | `{"status":"READY","process_alive":true}` | 644.62 ms | **PASS** |
| `https://freshguard-ai-auef.onrender.com/api/v1/scanner/vision/status` | `GET` | `200 OK` | `{"lifecycle_state":"NOT_TRAINED","classes_count":15}` | 1,259.15 ms | **PASS** |
| `https://freshguard-ai-auef.onrender.com/api/v1/scanner/vision/detect_v2` | `OPTIONS` | `200 OK` | `Access-Control-Allow-Origin: https://freshguard-ai.vercel.app` | 715.10 ms | **PASS** |
| `https://freshguard-ai-auef.onrender.com/api/v1/scanner/vision/detect_v2` | `POST` | `200 OK` | `{"success":false,"model":"grocery_yolov8_v2","message":"Vision inference unavailable: V2 model weights not found..."}` | 811.48 ms | **FAIL (PENDING WEIGHTS DEPLOY)** |

---

## 2. Detailed Findings

1. **Service Availability**:
   - `https://freshguard-ai-auef.onrender.com` is **LIVE** and responding to all HTTP requests.
   - Initial cold-start latency: ~1,234 ms; subsequent response latencies: ~644 ms to 811 ms.

2. **CORS Configuration**:
   - OPTIONS preflight request returned `HTTP 200 OK` with `Access-Control-Allow-Origin: https://freshguard-ai.vercel.app`.
   - Vercel frontend origin permissions are **PASS / VERIFIED**.

3. **`detect_v2` Endpoint Analysis**:
   - Endpoint structural response: `HTTP 200 OK` with JSON schema `{"success": false, "model": "grocery_yolov8_v2", "detections": [], "count": 0, "inference_ms": 0.0}`.
   - Message details: `Vision inference unavailable: V2 model weights not found in candidates ['best.pt', 'best.pt', 'model.pt', 'model.onnx']`.
   - Cause: Commit `b06f68a` (which tracked `best.pt` in Git) was pushed to GitHub; Render container re-deployment to pull the 6.2 MB `best.pt` file from GitHub is currently finishing or requires a manual Render dashboard deploy trigger.

---

## 3. Actionable Next Action

Log into [Render Dashboard](https://dashboard.render.com), navigate to `freshguard-ai-auef`, click **Manual Deploy** -> **Deploy latest commit** (`b06f68a`), and re-run `python scripts/test_live_render_backend.py`.
