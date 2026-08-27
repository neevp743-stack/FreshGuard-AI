# FreshGuard AI

> **AI-Powered Freshness & Food Intelligence Platform**  
> *"Know. Use. Refill. Waste Less."*

FreshGuard AI is an AI-powered household food, freshness, and grocery management platform. It tracks kitchen inventory, detects expiry dates via raw packaging image OCR, scans barcodes using live mobile camera hardware, performs multi-object grocery vision detection using a bounded YOLOv8 object detection pipeline, predicts product run-out dates using consumption velocity analytics, dispatches 24h-deduplicated FCM push notifications, and automates smart grocery refills.

---

## 🌟 System Architecture

```
+-------------------------------------------------------------------------+
|                          CLIENT PRESENTATION                            |
|  +-----------------------------------+  +----------------------------+  |
|  | Flutter Mobile & Desktop Client   |  | Web App (HTML5/JS/CSS)     |  |
|  +-----------------------------------+  +----------------------------+  |
+------------------------------------+------------------------------------+
                                     | (REST API / JSON / HTTP 2.0)
                                     v
+-------------------------------------------------------------------------+
|                        BACKEND API & SECURITY LAYER                     |
|  FastAPI Application Server (Uvicorn / Python 3.11+)                    |
|  - API Gateway & Versioning (/api/v1)                                   |
|  - PBKDF2-HMAC-SHA256 Auth & JWT Tokens                                 |
|  - Role-Based Access Control (RBAC: USER, ADMIN)                        |
|  - Configurable CORS Security Middleware                                |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                      CORE SERVICES & BUSINESS LOGIC                     |
|  +-----------------------+  +-------------------+  +-----------------+  |
|  | Inventory Engine      |  | Scanner Service   |  | Notification    |  |
|  | (Status & Days Calc)  |  | (Barcode + OCR)   |  | Engine (FCM)    |  |
|  +-----------------------+  +-------------------+  +-----------------+  |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                         AI / ML INFERENCE PIPELINE                      |
|  +-----------------------+  +-------------------+  +-----------------+  |
|  | YOLOv8 Vision Model   |  | Consumption       |  | Reorder &       |  |
|  | (Bounded Lazy Cache)  |  | Trend Analytics   |  | AI Assistant    |  |
|  +-----------------------+  +-------------------+  +-----------------+  |
+------------------------------------+------------------------------------+
```

---

## 🔒 Security & Engineering Highlights

1. **PBKDF2 Password Security & Legacy Re-Hashing**: Passwords stored using PBKDF2-HMAC-SHA256 (100,000 iterations + random salt). Legacy SHA-256 password hashes are automatically and transparently upgraded to PBKDF2 upon successful login.
2. **Role-Based Access Control (RBAC)**: User roles (`USER`, `ADMIN`). Protected `/api/v1/admin/diagnostics` endpoint returns HTTP 403 Forbidden to standard `USER` accounts.
3. **Lightweight Operational Health Probe (`/health` & `/api/v1/health`)**: Extremely fast health endpoints distinguishing `PROCESS_ALIVE` from `APPLICATION_READY` without loading heavy ML models or querying databases.
4. **Lazy Bounded ML Model Caching**: `get_cached_yolo_model()` caches loaded model weights in memory to avoid repeated disk I/O on every inference request.
5. **No AI Prediction Fabrication**: Hardcoded OCR fallback text mocks removed. If OCR fails or contains no readable text, an honest `success: false` response is returned.
6. **Automated SHA-256 Model Integrity Verification**: Baseline model hashes verified before and after code changes (`scripts/verify_model_integrity.py`).

---

## 🚀 Running & Local Setup

### 1. Launch FastAPI Backend
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```
- Interactive API Documentation: `http://127.0.0.1:8000/docs`
- Health Probe: `http://127.0.0.1:8000/health`

### 2. Verify Model Integrity
```bash
python scripts/verify_model_integrity.py
```

### 3. Run Pytest Test Suite (26 Unit & Integration Tests)
```bash
cd backend
python -m pytest
```

### 4. Run Docker Compose Deployment
```bash
docker-compose up -d --build
```

---

## 📚 Complete Technical Documentation

- [`docs/ARCHITECTURE_AUDIT.md`](docs/ARCHITECTURE_AUDIT.md) — Comprehensive Engineering Audit
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — System Architecture Specification
- [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md) — REST API Reference
- [`docs/SECURITY_AUDIT.md`](docs/SECURITY_AUDIT.md) — Security & Controls Audit
- [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) — Deployment & Docker Guide
- [`docs/TESTING.md`](docs/TESTING.md) — QA & Automated Test Suite Reference
- [`docs/PRODUCTION_RELIABILITY.md`](docs/PRODUCTION_RELIABILITY.md) — Failure Isolation & Resiliency
- [`docs/PRODUCTION_READINESS_REPORT.md`](docs/PRODUCTION_READINESS_REPORT.md) — Final Readiness Verification
