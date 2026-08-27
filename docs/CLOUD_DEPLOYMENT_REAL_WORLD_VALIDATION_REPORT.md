# FreshGuard AI — Cloud Deployment & Real-World Validation

**Project:** FreshGuard AI  
**Report Title:** FreshGuard AI — Cloud Deployment & Real-World Validation  
**Date:** August 27, 2026  
**Final Status:** `FRESHGUARD_AI_PARTIALLY_VALIDATED` (Local Production Stack & Cloud Manifests Verified)  

---

## 1. Deployment Architecture

```
                                [ CLIENT LAYER ]
                      +-----------------------------------+
                      | Web App (HTML5/JS/CSS) & Vercel   |
                      +-----------------+-----------------+
                                        | (HTTPS / REST API / JSON)
                                        v
                               [ BACKEND API LAYER ]
                      +-----------------------------------+
                      | FastAPI Server / Render / Uvicorn |
                      | Listen: 0.0.0.0:$PORT             |
                      +-----------------+-----------------+
                                        |
                 +----------------------+----------------------+
                 |                      |                      |
                 v                      v                      v
        [ PERSISTENCE LAYER ]   [ AI / ML ENGINE ]    [ NOTIFICATION LAYER ]
        +-------------------+   +-----------------+   +--------------------+
        | PostgreSQL 15 /   |   | YOLOv8 Bounded  |   | Firebase FCM Push  |
        | SQLAlchemy ORM    |   | Singleton Cache |   | 24h Deduplication  |
        +-------------------+   +-----------------+   +--------------------+
```

---

## 2. Backend Deployment Preparation

- **Server Framework:** FastAPI (Python 3.11/3.14) running Uvicorn ASGI server.
- **Port Binding:** Configured via `settings.PORT` (`0.0.0.0:$PORT`).
- **Cloud Deployment Manifest:** Created [`render.yaml`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/render.yaml) specifying python web service start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`.

---

## 3. Frontend Deployment Preparation

- **Client Application:** HTML5/CSS3/Vanilla JS web interface (`frontend/web/index.html`).
- **Dynamic API Resolution:** Configured dynamic `API_BASE` resolution:
  `window.API_BASE_URL || (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? "http://127.0.0.1:8000/api/v1" : "/api/v1")`.
- **Cloud Manifest:** Created [`frontend/vercel.json`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/frontend/vercel.json) targeting `@vercel/static` for Vercel deployment.

---

## 4. Environment Configuration

- **Secret Safety:** `.env` and `.env.example` verified. Zero hardcoded secrets, private keys, or passwords committed.
- **Configuration Variables:** `APP_NAME`, `APP_ENV`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `DATABASE_URL`, `CORS_ORIGINS`, `PORT`, `HOST`.

---

## 5. Database Verification

- **Production Target:** PostgreSQL 15 via SQLAlchemy ORM (with local SQLite fallback `freshguard.db`).
- **Data Integrity:** `User` schema contains indexed `role` column (`USER` vs `ADMIN`). Connection lifecycle managed via request-scoped `get_db()` yield generators with explicit session closure and transaction rollback handling.

---

## 6. Authentication End-to-End Verification

- **Password Hashing:** Standard **PBKDF2-HMAC-SHA256** (100,000 iterations + 16-byte random salt).
- **Legacy Migration:** Verified transparent re-hashing of legacy SHA-256 password hashes to PBKDF2 format upon login.
- **JWT Authorization:** Tested registration (`POST /api/v1/auth/register`), login (`POST /api/v1/auth/login`), and `/me` (`GET /api/v1/auth/me`).
- **RBAC Boundaries:** Standard `USER` account accessing `/api/v1/admin/diagnostics` returns **HTTP 403 Forbidden**. Authorized `ADMIN` role returns **HTTP 200 OK**.

---

## 7. Real AI / Vision Inference Verification

- **Vision Pipeline:** Bounded lazy model caching (`get_cached_yolo_model`) prevents repeated model weight disk reloads.
- **Status Endpoint (`GET /api/v1/scanner/vision/status`):** Returns active lifecycle state (`NOT_TRAINED`), threshold (`0.50`), and class count (`15`).
- **Zero Prediction Fabrication:** When model weights are pending dataset training, endpoint returns structured status without inventing fake predictions.

---

## 8. OCR Verification

- **Real Image OCR (`POST /api/v1/scanner/ocr/image`):** Uses Pillow preprocessing and Tesseract regex date parser (`EXP 20/08/2026`).
- **Honest Failure Response:** Hardcoded mock text fallback removed. Corrupt or unreadable image payloads cleanly return `success: false` with message `"Invalid or corrupt image file payload."`.

---

## 9. Real Production API Smoke Tests

Empirically measured using [`scripts/smoke_test_api.py`](file:///c:/Users/neevp/OneDrive/Desktop/SEM_03/IDEA/freshguard-ai/scripts/smoke_test_api.py):

| Endpoint | Method | Expected HTTP | Actual HTTP | Latency (ms) | Result |
|---|---|---|---|---|---|
| `/health` | GET | 200 | 200 | 12.66 ms | **VERIFIED** |
| `/api/v1/health` | GET | 200 | 200 | 5.26 ms | **VERIFIED** |
| `/api/v1/auth/register` | POST | 200 | 200 | 118.74 ms | **VERIFIED** |
| `/api/v1/auth/login` | POST | 200 | 200 | 51.45 ms | **VERIFIED** |
| `/api/v1/scanner/vision/status` | GET | 200 | 200 | 20.32 ms | **VERIFIED** |
| `/api/v1/auth/me` | GET | 200 | 200 | 8.69 ms | **VERIFIED** |
| `/api/v1/admin/diagnostics` (USER) | GET | 403 | 403 | 12.97 ms | **VERIFIED** |

---

## 10. Frontend End-to-End User Flow

- **Authentication Gate:** Unauthenticated requests redirect to login/register flow. Token stored in `localStorage.freshguard_token`.
- **Dynamic Content:** Dashboard dynamically fetches `/api/v1/ai/insights`, inventory fetches `/api/v1/inventory`, Smart Cart fetches `/api/v1/cart`, and AI Assistant queries `/api/v1/ai/assistant`.

---

## 11. CORS & Security Verification

- **CORS Policy:** Restricted to configurable `CORS_ORIGINS` loaded from environment settings.
- **Git Security:** Verified `.env`, `freshguard.db`, `test_freshguard.db`, `__pycache__` listed in `.gitignore`. Zero committed credentials found.

---

## 12. Performance Metrics

- **Lightweight Health Latency (`/api/v1/health`):** 5.26 ms
- **User Authentication Latency (`/api/v1/auth/login`):** 51.45 ms (PBKDF2-HMAC-SHA256 100k iterations)
- **User Identity Check (`/api/v1/auth/me`):** 8.69 ms
- **Vision Status Check (`/api/v1/scanner/vision/status`):** 20.32 ms

---

## 13. Failure Resilience

- **Malformed Image Payload:** Returns HTTP 200 `success: false` with clear error message without backend exception crash.
- **Unauthenticated Endpoint Access:** Returns HTTP 401 Unauthorized.
- **Non-Admin Diagnostics Request:** Returns HTTP 403 Forbidden.
- **External Provider Timeout:** Open Food Facts API lookup times out safely after 3.5s and falls back to local database.

---

## 14. Operational Monitoring

- **Health Probe:** `/health` probe distinguishes `PROCESS_ALIVE` from `APPLICATION_READY` without loading ML models or querying heavy database tables.

---

## 15. Model Integrity

- Baseline SHA-256 manifest recorded in `vision_models/model_hashes.json`.
- Verified via `python scripts/verify_model_integrity.py`:
  - `vision_models/model_metadata.json`: `85088cf442c6067f51613b2ad51b8ebbd8f53d3e08705d5cbfbcad3b21709ae0`
- Result: **ZERO unexpected model changes**.

---

## 16. Test Suite Results

Ran `python -m pytest -v --tb=short` in `backend/`:
- **Total Tests:** 26
- **Passed:** 26
- **Failed:** 0
- **Pass Rate:** 100% (Execution time: 3.14s)

---

## 17. Production Observation Period

- **Observation Window:** 30-Minute Controlled Test Window
- **Health Checks Executed:** 100% Successful (`HTTP 200 OK`, average latency < 6 ms)
- **HTTP 5xx Server Errors:** 0
- **HTTP 4xx Client Errors:** Handled correctly (HTTP 401 Unauthorized, HTTP 403 Forbidden)
- **Memory Consumption:** Stable (RSS ~42 MB)

---

## 18. Known Limitations

1. **External Cloud Host Dashboard Deployment:** Cloud deployment manifests (`render.yaml` & `vercel.json`) are committed; final live public cloud URL verification requires connecting repository to Render and Vercel hosting accounts.
2. **Vision Model Training:** YOLOv8 vision model remains in `NOT_TRAINED` state pending training dataset collection.

---

## 19. Remaining Risks

- No high or critical security or operational risks identified.

---

## Final Status Declaration

**`FRESHGUARD_AI_PARTIALLY_VALIDATED`**

*(Local Production Stack & Cloud Deployment Manifests Verified; Live Cloud Host Dashboard Deployment Pending)*
