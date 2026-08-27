# FreshGuard AI — Technical Architecture Specification

**System:** FreshGuard AI  
**Version:** 1.0.0 (Production Engineering Foundation)  
**Date:** August 27, 2026  

---

## 1. High-Level Architecture Overview

FreshGuard AI is structured as a decoupled multi-layer client-server platform optimized for low latency, zero prediction fabrication, and high operational reliability.

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
                                     |
                                     v
+-------------------------------------------------------------------------+
|                           PERSISTENCE LAYER                             |
|  SQLAlchemy ORM (SQLite / PostgreSQL 15)                                |
|  - Users, Inventory, Consumption Logs, Notifications, Shopping Cart     |
+-------------------------------------------------------------------------+
```

---

## 2. Component Design & Control Flow

### A. Authentication & Security Layer
- **Password Security:** Hashes passwords using `pbkdf2_hmac` with `sha256`, 100,000 iterations, and 16-byte random salts (`pbkdf2_sha256$<salt>$<hash>`).
- **Legacy Password Migration:** Transparently upgrades legacy SHA-256 password hashes to PBKDF2 format upon successful user authentication.
- **JWT Authorization:** Tokens expire in 3 days (4320 minutes default) containing user identity (`sub`) and role (`role`).
- **Role-Based Access Control (RBAC):** Users are assigned `USER` (default) or `ADMIN`. The `get_current_admin_user` guard enforces HTTP 403 Forbidden for non-admin attempts on operational diagnostics.

### B. Multi-Modal Identity Pipeline
```
INPUT DATA -> BARCODE LOOKUP -> VISION DETECTION -> OCR PACKAGE PARSING -> CONFLICT RESOLUTION -> SUGGESTED ITEM
```
1. **Barcode Resolution:** Resolves GTIN/UPC codes against local database and Open Food Facts API with fallback.
2. **Vision Object Detection:** Lazy-caches YOLOv8 model instance to execute bounding box prediction without repeated disk loading.
3. **Package OCR:** Preprocesses images (grayscale, contrast, sharpening), executes regex date/batch parsing, and returns honest status (`success: false` if no readable text detected).
4. **Discrepancy Resolution:** Flags identity mismatches (e.g. Barcode identity vs Vision detection) for explicit user verification.

### C. Operational & Health Monitoring
- **`/health` & `/api/v1/health`:** Lightweight probes returning process status and DB ping (`READY` vs `DEGRADED`) without invoking ML models or heavy queries.
- **`/api/v1/admin/diagnostics`:** Protected ADMIN endpoint reporting RSS memory usage (`psutil`), DB state, and AI engine status.

---

## 3. Database Schema Entity Relationship Map

- **Users:** `id`, `email`, `password_hash`, `full_name`, `role` (index), `created_at`
- **Households:** `id`, `name`, `join_code` (unique index), `owner_id` (FK: `users.id`)
- **HouseholdMembers:** `id`, `household_id` (FK), `user_id` (FK), `role`
- **Inventory:** `id`, `user_id` (FK), `household_id` (FK), `product_name`, `category`, `quantity`, `unit`, `storage_location`, `expiry_date` (index), `status` (index)
- **ConsumptionLogs:** `id`, `household_id` (FK), `inventory_id` (FK), `quantity_consumed`, `date_consumed` (index), `log_type`
- **Notifications:** `id`, `user_id` (FK), `title`, `message`, `type`, `priority`, `is_read`, `created_at`
- **ShoppingCart:** `id`, `household_id` (FK), `total_estimated_price`, `status`
