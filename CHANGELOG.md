# Changelog

All notable changes to FreshGuard AI are documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [3.0.0] - 2026-09-01

### Added
- **FreshGuard Vision V3 ONNX Pipeline**: Upgraded object recognition model supporting 35 produce and packaged grocery classes (`vision_models/v3/freshguard_vision_v3.onnx`).
- **Phase 8 Scientific Confidence Policy**: Three-tier classification system (`HIGH >= 0.50`, `MEDIUM 0.30–0.49`, `LOW < 0.30` with `requires_confirmation: true`).
- **Webcam Real-Time Pipeline**: Frame-rate throttle (1.5s interval), single-flight request lock, and HTML5 Canvas overlay for real-time bounding boxes.
- **Universal Multi-Item Inventory Flow**: Automated aggregation (`[ADD +X]`), new batch separation (`[NEW BATCH]`), and item skipping (`[SKIP]`).
- **35-Class Shelf Life Rules**: Full 1:1 mapped database rules engine for calculate days to expiry and freshness state (`FRESH`, `USE_SOON`, `EXPIRED`, `UNKNOWN`).
- **Production Cloud Deployment**: Backend deployed to Render Web Services (`https://freshguard-ai-auef.onrender.com`), Frontend web application deployed to Vercel Edge (`https://fresh-guard-ai-delta.vercel.app`).
- **Automated SHA-256 Model Integrity Verification**: Integrated `scripts/verify_model_integrity.py` to prevent unauthorized model weight modifications.

### Changed
- **API Endpoints**: Standardized API v1 endpoint versioning (`/api/v1/*`).
- **Database Engine**: Migrated database session management to SQLAlchemy 2.0 with strict household user isolation (`user_id`).
- **Password Security**: Upgraded authentication to PBKDF2-HMAC-SHA256 (100,000 iterations) with transparent automatic re-hashing for legacy credentials.

### Security
- Added RBAC middleware returning HTTP 403 Forbidden for non-admin accounts on `/admin/diagnostics`.
- Enforced strict CORS domain origin controls for production frontend deployment.
- Added privacy-first vision feedback handling storing only metadata logs (`vision_feedback_metadata.jsonl`) without raw user images.

---

## [2.0.0] - 2026-08-28

### Added
- **Vision V2 YOLOv8 Pipeline**: Initial multi-object grocery recognition model supporting produce detection.
- **Barcode & OCR Service**: Integration of barcode scanner lookup andpackaging text OCR extraction via Tesseract OCR engine.
- **Consumption Velocity Analytics**: Basic prediction service for household inventory run-out dates and reorder recommendations.
- **FCM Notification Dispatcher**: 24-hour deduplicated notification queue for expiring products.

---

## [1.0.0] - 2026-08-15

### Added
- **Core FastAPI Backend**: Initial setup of FastAPI server with SQLite database models (`User`, `InventoryItem`, `Product`).
- **Frontend Prototype**: HTML5/JS frontend dashboard for manual inventory tracking.
- **Authentication**: JWT token generation and basic user registration/login.
