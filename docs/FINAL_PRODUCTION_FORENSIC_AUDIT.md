# FreshGuard AI — Final Production Forensic Audit

**Document Status:** COMPLETE  
**Audit Target:** FreshGuard AI Complete Repository & End-to-End Architecture  
**Audit Date:** 2026-08-31  

---

## Executive Summary

This forensic audit covers all 18 architectural components of FreshGuard AI prior to production hardening and live validation. Application behavior was preserved during this audit.

---

## 1. Frontend Entry Points
- **Production SPA:** [`frontend/web/index.html`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/frontend/web/index.html) and [`frontend/index.html`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/frontend/index.html) — Single-page HTML5/JS web application incorporating interactive camera feed, real-time bounding box overlay, 35-class inventory management, duplicate modal workflow, and date-based freshness dashboard.
- **Vercel Routing Destination:** [`frontend/vercel.json`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/frontend/vercel.json) rewrites `/` and `/index.html` to `/web/index.html`.
- **Standalone AI Demo:** [`frontend/web/vision_demo.html`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/frontend/web/vision_demo.html) and [`frontend/vision_demo.html`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/frontend/vision_demo.html) — Vision inference testing utility with confidence and NMS sliders.
- **Flutter Mobile App:** [`frontend/lib/main.dart`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/frontend/lib/main.dart) — Cross-platform Flutter client entry point for mobile devices.

---

## 2. Backend FastAPI Entry Points
- **Primary Application Entry Point:** [`backend/main.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/main.py)
- **Framework & Config:** FastAPI app with configurable CORS via `CORS_ORIGINS`.
- **Startup Warmup:** Warmup hooks pre-load the ONNX Runtime session (`get_onnx_session()`) into memory during container startup to avoid cold-start latency spikes.
- **API Versioning:** Routers registered under both `/api/v1` and `/api` (backward compatibility alias):
  - `auth`: `/api/v1/auth`
  - `inventory`: `/api/v1/inventory`
  - `freshness`: `/api/v1/freshness`
  - `scanner`: `/api/v1/scanner`
  - `vision`: `/api/v1/scanner/vision`
  - `ai`: `/api/v1/ai`
  - `cart`: `/api/v1/cart`
  - `notifications`: `/api/v1/notifications`
  - `analytics`: `/api/v1/analytics`
  - `health`: `/health` and `/api/v1/health`

---

## 3. Vision Inference Routes
Located in [`backend/app/api/vision_router.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/app/api/vision_router.py):
- `POST /api/v1/scanner/vision/detect`: Multipart image upload endpoint (PyTorch baseline).
- `POST /api/v1/scanner/vision/detect_v2`: High-speed webcam frame & upload detection route supporting multipart form data and base64 JSON payload. Powered by ONNX Runtime V2 (35-class).
- `POST /api/v1/scanner/vision/detect_direct`: Alias for `detect_v2`.
- `GET /api/v1/scanner/vision/status`: Model status and lifecycle state endpoint (`READY`, `NOT_TRAINED`, etc.).
- `POST /api/v1/scanner/vision/feedback`: Privacy-preserving active learning feedback endpoint.
- `POST /api/v1/scanner/vision/multimodal`: Barcode + Vision + OCR multi-modal identity pipeline.
- `POST /api/v1/scanner/vision/detect_v3`: Isolated evaluation route for V3 staging model.

---

## 4. Model Loading & Inference Engine
- **Inference Service Module:** [`backend/app/ai/vision/inference.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/app/ai/vision/inference.py)
- **Active Production Model (V2):** `vision_models/deployment/grocery_yolov8_v2_web/model.onnx` (12,292,329 bytes, 35 classes, ONNX float32).
- **Fallback PyTorch Model (V2):** `vision_models/deployment/grocery_yolov8_v2_web/model.pt` (6,259,306 bytes).
- **Staging Model (V3):** `vision_models/v3/freshguard_vision_v3.onnx` (12,292,329 bytes, 35 classes).
- **Experimental Model (V5):** `training/v5/deployment/model.onnx` (644 classes).
- **Model Resolution Logic:** `find_v2_onnx_path()` inspects candidates relative to file location and working directory. Cached singleton ONNX Runtime session in `_ONNX_SESSION_CACHE` with `CPUExecutionProvider`.
- **Pre/Post-processing:** PIL decode -> RGB resize (640x640) -> CHW float32 normalization (`/ 255.0`) -> ONNX output tensor `[1, 39, 8400]` -> Confidence thresholding -> Custom Non-Maximum Suppression (`_nms_boxes`).

---

## 5. Class Metadata & Identity Rules
Authoritative 35-class mapping (`class_id` 0–34):
- [`backend/app/ai/vision/classes.json`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/app/ai/vision/classes.json)
- [`vision_models/deployment/grocery_yolov8_v2_web/classes_metadata.json`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/vision_models/deployment/grocery_yolov8_v2_web/classes_metadata.json)
- [`vision_models/v3/v3_classes_metadata.json`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/vision_models/v3/v3_classes_metadata.json)
- [`backend/app/services/shelf_life.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/app/services/shelf_life.py) (`CLASS_MAPPING_RULES` dictionary)

Class Index | Name | Display Name | Category | Default Location | Shelf Life (Days)
---|---|---|---|---|---
0 | milk | Milk | Dairy | Fridge | 7
1 | bread | Bread | Bakery | Pantry | 5
2 | apple | Apple | Fruits | Pantry | 14
3 | banana | Banana | Fruits | Pantry | 6
4 | egg | Egg | Dairy | Fridge | 21
5 | tomato | Tomato | Vegetables | Fridge | 7
6 | potato | Potato | Vegetables | Pantry | 30
7 | onion | Onion | Vegetables | Pantry | 30
8 | rice | Rice | Grains | Pantry | 180
9 | yogurt | Yogurt | Dairy | Fridge | 10
10 | cheese | Cheese | Dairy | Fridge | 14
11 | biscuit | Biscuit | Packaged Goods | Pantry | 60
12 | juice | Juice | Beverages | Fridge | 7
13 | water | Water | Beverages | Pantry | 365
14 | packaged_snack | Packaged Snack | Packaged Goods | Pantry | 90
15 | carrot | Carrot | Vegetables | Fridge | 14
16 | cabbage | Cabbage | Vegetables | Fridge | 14
17 | cauliflower | Cauliflower | Vegetables | Fridge | 7
18 | capsicum | Capsicum | Vegetables | Fridge | 7
19 | cucumber | Cucumber | Vegetables | Fridge | 7
20 | brinjal | Brinjal | Vegetables | Fridge | 5
21 | broccoli | Broccoli | Vegetables | Fridge | 5
22 | spinach | Spinach | Vegetables | Fridge | 4
23 | peas | Peas | Vegetables | Fridge | 5
24 | corn | Corn | Vegetables | Fridge | 5
25 | garlic | Garlic | Vegetables | Pantry | 60
26 | ginger | Ginger | Vegetables | Fridge | 21
27 | okra | Okra | Vegetables | Fridge | 5
28 | beetroot | Beetroot | Vegetables | Fridge | 14
29 | radish | Radish | Vegetables | Fridge | 10
30 | pumpkin | Pumpkin | Vegetables | Pantry | 30
31 | bitter_gourd | Bitter Gourd | Vegetables | Fridge | 5
32 | bottle_gourd | Bottle Gourd | Vegetables | Fridge | 7
33 | green_chilli | Green Chilli | Vegetables | Fridge | 10
34 | sweet_potato | Sweet Potato | Vegetables | Pantry | 21

---

## 6. Inventory Database & Schema
- **Database Engine:** SQLite / SQLAlchemy ([`backend/app/core/database.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/app/core/database.py)). DB file at `backend/freshguard.db`.
- **Database Models:** [`backend/app/models/models.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/app/models/models.py)
  - `User`: `id`, `email`, `password_hash`, `full_name`, `role`, `created_at`
  - `Household`: `id`, `name`, `join_code`, `owner_id`, `created_at`
  - `HouseholdMember`: `id`, `household_id`, `user_id`, `role`
  - `Inventory`: `id`, `user_id`, `household_id`, `product_name`, `category`, `brand`, `quantity`, `unit`, `storage_location`, `purchase_date`, `expiry_date`, `opened_date`, `estimated_remaining_quantity`, `barcode`, `image_url`, `notes`, `status`, `created_at`, `updated_at`
  - Additional tables: `ConsumptionLog`, `PurchaseHistory`, `ExpiryEvent`, `Notification`, `DeviceToken`, `Recommendation`, `ShoppingCart`, `ShoppingCartItem`, `UserPreference`.

---

## 7. Freshness Engine
- **Core Service:** [`backend/app/services/freshness.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/app/services/freshness.py)
- **Status Determination:** `calculate_freshness_status(expiry_date, purchase_date)`
  - `days < 0`: `"EXPIRED"`
  - `0 <= days <= 2`: `"USE_SOON"`
  - `days > 2`: `"FRESH"`
  - `expiry_date is None`: `"UNKNOWN"`
- **Aggregations & Guidance:**
  - `get_freshness_summary()`: Counts total, fresh, use_soon, expired, unknown.
  - `get_use_first_recommendations()`: Prioritizes items. Expired items are strictly flagged as `"Review / Remove"` (never safe to eat).
  - `get_freshness_alerts()`: Generates urgent dashboard notifications.

---

## 8. Shelf-Life Engine
- **Service:** [`backend/app/services/shelf_life.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/app/services/shelf_life.py)
- **Function:** `calculate_estimated_expiry(class_identifier, purchase_date)`
- Adds exact shelf-life days from `CLASS_MAPPING_RULES` to purchase date or `datetime.utcnow()`.
- Default storage location (Fridge/Pantry) and category auto-assigned per class ID.

---

## 9. Security & Household User Isolation
- **Security Core:** [`backend/app/core/security.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/app/core/security.py) (JWT Bearer tokens, passlib/bcrypt hashing).
- **Authentication Guard:** `get_current_user` FastAPI dependency.
- **Household Scoping:** Inventory queries verify user household membership:
  ```python
  member = db.query(HouseholdMember).filter(HouseholdMember.user_id == current_user.id).first()
  items = db.query(Inventory).filter(Inventory.household_id == member.household_id).all()
  ```
  Users cannot view, add, modify, or delete inventory belonging to another household.

---

## 10. Webcam Capture Pipeline
- **Frontend Camera Logic:** In `frontend/web/index.html` & `frontend/index.html`:
  - Access camera stream via `navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })`.
  - Continuous loop captures video frame to hidden `<canvas>` element (640x480).
  - Converts frame to JPEG Base64 (`canvas.toDataURL('image/jpeg', 0.8)`).
  - Single-flight throttle flag (`isProcessingFrame = true`) prevents request flooding.
  - Target minimum inference interval: ~1.5 seconds.
  - Canvas overlay redraws bounding boxes without clearing previous state until new inference results arrive.

---

## 11. Image Upload Pipeline
- **Frontend:** Upload input accepts JPG/PNG images -> converts to file form data or base64.
- **Backend:** `POST /api/v1/scanner/vision/detect_v2` accepts both `multipart/form-data` and `{ "image_base64": "..." }`. Reads binary stream directly into PIL -> passes bytes to `_run_onnxruntime_v2_inference()` -> returns detections JSON.

---

## 12. Detection Response Schema
Response model structure:
```json
{
  "success": true,
  "model": "grocery_yolov8_v2",
  "model_display_name": "FreshGuard Vision",
  "detections": [
    {
      "class_id": 6,
      "class_name": "potato",
      "confidence": 0.892,
      "bbox": [120.5, 80.0, 340.2, 310.4]
    }
  ],
  "count": 1,
  "inference_ms": 18.5,
  "message": "Real FreshGuard Vision ONNX detection complete. Found 1 object(s)."
}
```

---

## 13. Frontend Detection Rendering
- **Canvas Rendering:** `drawDetectionsOverlay(detections, videoElement, canvasElement)` maps normalized/scaled bounding box coordinates to live preview canvas.
- **Visual Palette:** Crisp neon bounding box outlines, semi-transparent label tag background, bold class display name, and confidence score badge.
- **Detection Summary Panel:** Lists detected item cards with class display name, confidence percentage, and count controls.

---

## 14. Inventory Creation Workflow
- Endpoints in [`backend/app/api/inventory.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/backend/app/api/inventory.py):
  - `POST /api/v1/inventory`: Manual single item creation.
  - `POST /api/v1/inventory/bulk`: Atomic creation of multiple items.
  - `POST /api/v1/inventory/from-detections`: Processing detected scanner objects with explicit user action ([ADD], [NEW BATCH], [SKIP]).

---

## 15. Duplicate Prevention Workflow
- **Pre-Check Endpoint:** `POST /api/v1/inventory/check-existing`
- Accepts payload of detected `class_ids`.
- Performs user-isolated lookup for existing inventory matching `class_id` -> `display_name`.
- Returns matching existing inventory details (`existing_quantity`, `existing_location`, `existing_expiry_date`).
- Frontend presents interactive modal requiring explicit user choice:
  - **[ADD / MERGE]:** `existing_quantity += detected_quantity`
  - **[NEW BATCH]:** Creates distinct inventory record for separate expiry tracking.
  - **[SKIP]:** Discards detection without altering database.

---

## 16. Render & Vercel Environment Configuration
- **Render Backend Configuration:** [`render.yaml`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/render.yaml)
  - Service Type: Web Service (Docker runtime).
  - Port: `10000`
  - Env Vars: `FRESHGUARD_VISION_MODEL=v2`, `CORS_ORIGINS=["*"]`
- **Vercel Frontend Configuration:** [`frontend/vercel.json`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/frontend/vercel.json)
  - Static site rewrites `/` to `/web/index.html`.

---

## 17. Existing Automated Test Suite
- `backend/tests/test_35_class_pipeline.py`: 35-class metadata alignment, ONNX inference schema, bbox sanity, NMS.
- `backend/tests/test_main.py`: Full API test suite covering auth, inventory endpoints, scanner, and freshness routes.
- `backend/tests/test_universal_inventory.py`: Unit tests for 35-class inventory creation and duplicate handling.
- `scripts/verify_model_integrity.py`: SHA-256 model integrity hash baseline script.

---

## 18. Existing Deployment Configuration
- **Backend Build:** `backend/Dockerfile` using Python 3.10-slim runtime.
- **Deployed Backend URL:** `https://freshguard-ai.onrender.com`
- **Deployed Frontend URL:** Vercel edge deployment.

---

**Forensic Audit Conclusion:** All 18 repository components are identified, mapped, and verified. Baseline model integrity is intact. Phase 1 complete.
