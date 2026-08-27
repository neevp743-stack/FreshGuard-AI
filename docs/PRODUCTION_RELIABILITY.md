# FreshGuard AI — Production Reliability & Failure Isolation

**System:** FreshGuard AI  
**Scope:** Resiliency, External Dependency Protection, Memory Safety  

---

## 1. Failure Isolation Architecture

FreshGuard AI is designed so that non-critical external service failures do NOT cause backend crashes or cascade into system outage.

```
                  +--------------------------------+
                  |  FastAPI Application Backend   |
                  +---------------+----------------+
                                  |
         +------------------------+------------------------+
         |                        |                        |
         v                        v                        v
+------------------+     +------------------+     +------------------+
| Open Food Facts  |     | Firebase FCM     |     | Tesseract OCR    |
| External API     |     | Push Service     |     | Native Engine    |
+--------+---------+     +--------+---------+     +--------+---------+
         |                        |                        |
  Timeout / Fail           Not Configured           Missing Binary
         |                        |                        |
         v                        v                        v
[ Fallback Local DB ]    [ Safe Mock Log ]        [ Honest Error ]
 (No Crash / 200 OK)     (No Crash / Enqueue)     (success: false)
```

### Dependency Failure Strategy

1. **Open Food Facts API Timeout / Network Failure:**
   - Handled with explicit 3.5s HTTP timeout.
   - If API fails or times out, resolution falls back to `LOCAL_PRODUCT_DATABASE` or returns `found: false` allowing manual user entry without crashing the endpoint.

2. **Firebase Cloud Messaging (FCM) Configuration Absence:**
   - `FIREBASE_INITIALIZED` state defaults safely to `False` if environment keys are missing.
   - Notifications remain enqueued in database while push dispatch logs a safe mock message.

3. **OCR Native Engine Absence / Failure:**
   - If Tesseract is not installed or returns empty text, `process_raw_image_ocr` returns an honest `success: false` response (`"OCR text extraction unavailable"`). Zero predictions are fabricated.

---

## 2. Memory & Performance Guardrails

- **Lazy Bounded ML Model Caching:** `get_cached_yolo_model()` caches loaded model weights in `_MODEL_CACHE` to avoid repeated disk reading on every request while capping memory growth.
- **Immediate File Cleanup:** Uploaded images processed during OCR or Vision detection use `tempfile.NamedTemporaryFile` and are deleted immediately in `finally` blocks.
- **Database Connection Lifecycle:** Connections are managed per-request via SQLAlchemy `get_db()` yield generators with explicit session closure to prevent connection pool exhaustion.
