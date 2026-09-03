# FreshGuard AI — Testing & Quality Assurance Suite Reference

**Framework:** Pytest 9.1+ & FastAPI TestClient  
**Total Verified Test Cases:** 60 Passed / 0 Failed  
**Suite Execution Time:** ~18-19 seconds  
**Pass Rate:** 100% (60 / 60 passed)  

---

## 1. Test Suite Architecture & Breakdown

The FreshGuard AI test suite consists of 60 automated unit and integration test cases distributed across three core test modules:

```
backend/tests/
├── test_main.py                        # Core Auth, Vision V2, OCR, Barcode, RBAC, Health & Inventory (46 tests)
├── test_universal_inventory.py         # Inventory Merge, Separate Batch, Skip, and Isolation Logic (9 tests)
└── test_v3_multi_object_recognition.py # Vision V3 35-Class NMS, Bounding Box & Class Metadata (5 tests)
```

---

## 2. Comprehensive Test Module Mapping

### Module 1: `test_main.py` (46 Test Cases)
- **Authentication & Security**:
  - `test_auth_register_and_login`: Verifies user account creation, JWT issuance, and login authorization.
  - `test_unauthorized_access`: Verifies HTTP 401 Unauthorized for unauthenticated requests.
  - `test_pbkdf2_password_hashing_and_legacy_migration`: Validates PBKDF2-HMAC-SHA256 password hashing (100,000 iterations) and transparent migration from legacy SHA-256 hashes upon login.
  - `test_rbac_user_admin_access_control`: Enforces RBAC boundaries (`USER` receive 403 Forbidden on `/admin/diagnostics`, `ADMIN` receives 200 OK).

- **Operational Health**:
  - `test_lightweight_health_endpoints`: Validates `/health` and `/api/v1/health` probes return `READY` in < 10 ms without loading ML models.

- **OCR, Barcode & Multi-Modal Pipeline**:
  - `test_barcode_lookup`: Verifies Open Food Facts product barcode identification.
  - `test_unknown_barcode_fallback`: Verifies graceful fallback on unregistered barcodes.
  - `test_ocr_parsing`: Verifies label packaging text and expiry date extraction.
  - `test_ocr_image_endpoint_valid` / `test_ocr_image_invalid_file_type` / `test_ocr_image_oversized_file`: Input validation and payload size checks.
  - `test_ocr_date_extraction_parsing` / `test_ocr_ambiguous_expiry_date`: Multi-format date parsing validation.
  - `test_ocr_failure_without_hardcoded_mock`: Ensures honest error payloads on unreadable OCR images.
  - `test_multimodal_barcode_vision_conflict_flagging`: Verifies discrepancy flagging when Barcode and Vision identities diverge.

- **Vision V2 & Active Learning**:
  - `test_vision_status_endpoint`: Verifies active vision model lifecycle state and metadata.
  - `test_vision_detect_no_model_graceful`: Ensures graceful degradation if model weights are unavailable.
  - `test_vision_feedback_privacy_first`: Verifies privacy-first active learning feedback logging without retaining raw household photos.
  - `test_live_webcam_v2_detection_endpoint` / `test_live_webcam_v2_json_base64_payload_endpoint`: Web camera frame ingestion via multipart and Base64 payloads.

- **Inventory, Freshness & Analytics**:
  - `test_add_and_delete_product`: Item creation, purchase logging, and status tracking.
  - `test_expiry_calculation_and_expired_item`: Date-calculated freshness evaluation (`FRESH`, `USE_SOON`, `EXPIRED`).
  - `test_consumption_prediction_and_reorder`: Velocity calculation and smart refill recommendations.
  - `test_notification_creation_and_deduplication`: FCM 24h deduplicated notification dispatch.
  - `test_user_notification_preferences_filtering`: User notification preference filtering.
  - `test_35_class_shelf_life_rules`: Full 35-class produce & grocery rules verification.
  - `test_freshness_engine_status_calculations` / `test_freshness_summary_and_use_first_endpoints` / `test_freshness_user_isolation`: Freshness aggregation and household isolation.

### Module 2: `test_universal_inventory.py` (9 Test Cases)
- `test_check_existing_inventory_and_duplicate_prevention`: Verifies existing inventory detection.
- `test_merge_existing_inventory_quantity`: Verifies `[ADD +X]` quantity merging into existing item record.
- `test_keep_separate_batch_creation`: Verifies `[NEW BATCH]` creation for separate expiry dates.
- `test_skip_item_action`: Verifies no-op behavior on `[SKIP]`.
- `test_user_inventory_isolation`: Enforces multi-tenant database boundary between households.
- `test_invalid_class_id_rejection`: Rejects invalid class IDs outside `0–34`.

### Module 3: `test_v3_multi_object_recognition.py` (5 Test Cases)
- `test_product_name_origin_strictly_from_class_id_metadata`: Ensures product labels originate strictly from `v3_classes_metadata.json` without hardcoded hacks.
- `test_multi_object_bounding_box_non_overlapping_nms`: Verifies Non-Maximum Suppression (NMS) bounding box calculation.
- `test_v3_multi_object_detection_endpoint_schema`: Verifies Vision V3 detection schema and confidence policy output.

---

## 3. Running Automated Tests

### Execute Full Pytest Suite
```bash
python -m pytest backend/tests -v
```

Expected Terminal Summary:
```text
====================== 60 passed, 0 failed in 18.98s ======================
```

### Run Model Integrity Verification
Verify SHA-256 cryptographic hashes of vision model binaries:
```bash
python scripts/verify_model_integrity.py
```

Expected Terminal Output:
```text
--- MODEL INTEGRITY AUDIT ---
[VERIFIED] model_metadata.json: 85088cf442c6067f...

[SUCCESS] MODEL INTEGRITY VERIFIED: NO UNEXPECTED MODEL CHANGES.
```

### Run Production Smoke Tests & Health Checks
```bash
python scripts/smoke_test_api.py
```
