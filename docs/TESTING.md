# FreshGuard AI — Testing & Quality Assurance Suite

**Framework:** Pytest 9.1+ & FastAPI TestClient  
**Total Test Cases:** 26  
**Suite Execution Time:** ~3.1 seconds  
**Pass Rate:** 100% (26 / 26 passed)  

---

## 1. Test Suite Coverage Overview

### A. Authentication & Password Security
- `test_auth_register_and_login`: Verifies user registration, JWT generation, and login authorization.
- `test_unauthorized_access`: Verifies protected routes return HTTP 401 Unauthorized without Bearer tokens.
- `test_pbkdf2_password_hashing_and_legacy_migration`: Validates PBKDF2 hash generation (`pbkdf2_sha256$...`) and transparent migration from legacy SHA-256 hashes upon login.

### B. User Roles & RBAC (Role-Based Access Control)
- `test_rbac_user_admin_access_control`: Enforces permission boundaries:
  - Unauthenticated -> **401 Unauthorized**
  - Standard `USER` role -> **403 Forbidden** on Admin diagnostics
  - Authorized `ADMIN` role -> **200 OK** on `/api/v1/admin/diagnostics`

### C. Health & System Monitoring
- `test_lightweight_health_endpoints`: Validates `/health` and `/api/v1/health` return status `READY` without loading ML models or executing heavy queries.

### D. Multi-Modal Identity & Vision AI
- `test_vision_status_endpoint`: Verifies active Vision lifecycle state (`NOT_TRAINED`), threshold, and class metadata.
- `test_vision_detect_no_model_graceful`: Ensures inference returns structured status without fabricating false detections.
- `test_vision_feedback_privacy_first`: Verifies prediction feedback logging without retaining raw household photos.
- `test_multimodal_barcode_vision_conflict_flagging`: Verifies multi-modal identity priority and conflict resolution.
- `test_ocr_failure_without_hardcoded_mock`: Verifies OCR processing returns an honest `success: false` response on corrupt payload without fallback text mocks.

### E. Inventory & Consumption Analytics
- `test_add_and_delete_product`: Verifies item creation, status calculation, and purchase history recording.
- `test_expiry_calculation_and_expired_item`: Verifies expiry date status evaluation (Healthy, Expiring Soon, Expired).
- `test_consumption_prediction_and_reorder`: Verifies consumption velocity calculation and reorder recommendations.

---

## 2. Running Automated Tests

To execute the full test suite locally:

```bash
cd backend
python -m pytest
```

Expected Output:
```text
collected 26 items

tests\test_main.py ..........................                           [100%]

============================== 26 passed in 3.11s ==============================
```
