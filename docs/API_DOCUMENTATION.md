# FreshGuard AI — API Specification & Integration Reference

**Base URL:** `/api/v1` (with `/api` legacy backward compatibility aliases)  
**Authentication:** Bearer JWT Header (`Authorization: Bearer <token>`)  

---

## 1. System & Health Endpoints

### `GET /health` & `GET /api/v1/health`
Lightweight application probe suitable for load balancers and external uptime monitors.

- **Auth Required:** No
- **Response (200 OK):**
```json
{
  "status": "READY",
  "process_alive": true,
  "database_connected": true,
  "version": "1.0.0",
  "timestamp": "2026-08-27T16:15:00+00:00"
}
```

---

## 2. Authentication Endpoints

### `POST /api/v1/auth/register`
Registers a new user, creates a primary household, and returns JWT access token.

- **Auth Required:** No
- **Request Body:**
```json
{
  "email": "user@freshguard.ai",
  "password": "SecurePassword123!",
  "full_name": "Jane Morgan",
  "household_name": "Morgan Kitchen"
}
```
- **Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "user@freshguard.ai",
  "full_name": "Jane Morgan",
  "role": "USER",
  "household_id": 1,
  "household_name": "Morgan Kitchen"
}
```

### `POST /api/v1/auth/login`
Authenticates credentials. Transparently re-hashes legacy SHA-256 password hashes to PBKDF2.

- **Auth Required:** No
- **Request Body:**
```json
{
  "email": "user@freshguard.ai",
  "password": "SecurePassword123!"
}
```

### `GET /api/v1/auth/me`
Retrieves authenticated user identity, role, and assigned household details.

- **Auth Required:** Yes (`USER` or `ADMIN`)
- **Response (200 OK):**
```json
{
  "user_id": 1,
  "email": "user@freshguard.ai",
  "full_name": "Jane Morgan",
  "role": "USER",
  "household_id": 1,
  "household_name": "Morgan Kitchen",
  "join_code": "FG-A1B2C3"
}
```

---

## 3. Inventory Management Endpoints

### `GET /api/v1/inventory`
Retrieves household inventory items with optional filtering by location, category, status, and search query.

- **Auth Required:** Yes
- **Query Parameters:** `location`, `category`, `status`, `search`
- **Response (200 OK):**
```json
[
  {
    "id": 12,
    "user_id": 1,
    "household_id": 1,
    "product_name": "Amul Taaza Toned Milk",
    "category": "Dairy",
    "quantity": 1.0,
    "unit": "L",
    "storage_location": "Refrigerator",
    "expiry_date": "2026-08-29T00:00:00",
    "status": "Expiring Soon",
    "days_until_expiry": 2
  }
]
```

### `POST /api/v1/inventory`
Creates a new inventory item and updates purchase history.

- **Auth Required:** Yes
- **Request Body:**
```json
{
  "product_name": "Organic Tomatoes",
  "category": "Vegetables",
  "quantity": 1.5,
  "unit": "kg",
  "storage_location": "Refrigerator"
}
```

---

## 4. Vision AI & Multi-Modal Scanner Endpoints

### `GET /api/v1/scanner/vision/status`
Returns vision model lifecycle state (`NOT_TRAINED`, `READY`, `FAILED`) and availability.

### `POST /api/v1/scanner/ocr/image`
Processes package image uploads using Tesseract & Regex Date Parser.
- **Auth Required:** Yes
- **Request:** `multipart/form-data` with `file` payload.
- **Response (200 OK - Success):**
```json
{
  "success": true,
  "product_name": "Amul Pure Butter",
  "expiry_date": "20/08/2026",
  "confidence": 0.85,
  "requires_confirmation": false
}
```
- **Response (200 OK - No Text Detected):**
```json
{
  "success": false,
  "raw_text": "",
  "confidence": 0.0,
  "requires_confirmation": true,
  "message": "OCR text extraction unavailable or no readable text detected on image."
}
```

---

## 5. Admin Diagnostics Endpoints

### `GET /api/v1/admin/diagnostics`
ADMIN-only operational monitoring endpoint.

- **Auth Required:** Yes (`ADMIN` role required)
- **Response (200 OK - ADMIN):**
```json
{
  "status": "OPERATIONAL",
  "process_alive": true,
  "memory_usage_mb": 42.15,
  "database_status": "HEALTHY",
  "ai_vision_status": "STANDBY",
  "ai_vision_lifecycle": "NOT_TRAINED",
  "error_count_24h": 0,
  "timestamp": "2026-08-27T16:15:00+00:00"
}
```
- **Response (403 Forbidden - Standard USER):**
```json
{
  "detail": "Forbidden: Admin diagnostics access required"
}
```
