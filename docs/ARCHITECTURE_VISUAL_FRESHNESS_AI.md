# FreshGuard AI — Architectural Separation: Vision Detection vs. Freshness Intelligence

## Executive Summary & System Boundaries

FreshGuard AI enforces a strict architectural boundary between object identification, date-based inventory freshness tracking, and future computer vision visual spoilage estimation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FRESHGUARD AI ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐
│       SYSTEM 1        │  │       SYSTEM 2        │  │       SYSTEM 3        │
│   FreshGuard Vision   │  │Freshness Intelligence │  │ Future Visual Spoilage│
│   (Object Detector)   │  │(Date & Rules Engine)  │  │   (Visual Estimate)   │
├───────────────────────┤  ├───────────────────────┤  ├───────────────────────┤
│ • 35-Class YOLOv8/ONNX│  │ • Expiry Date Tracking│  │ • Optional Multimodal │
│ • Bounding Box Loc.   │  │ • Category Rules      │  │ • Surface Mold/Browning│
│ • Class Identification│  │ • Timezone-Safe Math  │  │ • Visual Estimate ONLY│
│                       │  │ • Use-First Engine    │  │ • Explicit Warning    │
└───────────────────────┘  └───────────────────────┘  └───────────────────────┘
```

---

## 1. System Definitions & Principles

### System 1: FreshGuard Vision (Object Detection)
- **Role**: Locates and classifies 35 common grocery and vegetable items from camera frames or image uploads.
- **Model**: `grocery_yolov8_v2` (ONNX deployment runtime).
- **Output**: Class IDs (`0–34`), class names, bounding box coordinates `[x1, y1, x2, y2]`, and confidence scores.
- **Safety Boundary**: Object detection identifies *what* the item is (e.g. `okra`, `tomato`), but does **NOT** determine physical or chemical food safety.

### System 2: Freshness Intelligence Engine (Primary Safe Mechanism)
- **Role**: Deterministic, date-based food freshness tracking and consumption priority recommendation engine.
- **Location**: `backend/app/services/freshness.py` & `backend/app/services/shelf_life.py`.
- **Inputs**: Manufacturer expiration dates, user purchase dates, and 35-class estimated shelf-life rules.
- **Statuses**:
  - `FRESH`: Item is well within safe consumption timeframe (> 2 days remaining).
  - `USE_SOON`: Item is approaching expiry (0 to 2 days remaining).
  - `EXPIRED`: Current date is past the expiration date. Item is flagged as **"Review / Remove"** and NEVER recommended as safe to eat.
  - `UNKNOWN`: Dates are unavailable. Prompts user to input an expiry date.

### System 3: Future Visual Freshness AI (Optional Auxiliary System)
- **Role**: Optional future visual analysis for surface defect or browning estimation.
- **Strict Policy**: Any future visual freshness model MUST be explicitly labeled in the UI as a **Visual Estimate** and NEVER as a food safety guarantee.

---

## 2. Safety & Disclosure Guarantees

1. **Camera Detection Limitation**: Real-time camera detection identifies food items but does not measure bacterial growth, internal rot, or chemical spoilage.
2. **Date Hierarchy**:
   - Manufacturer/User Expiry Date > Estimated Shelf-Life Rules > `UNKNOWN`
3. **Expired Food Policy**: Expired items are strictly excluded from "Eat Now" lists and flagged with safety instructions to inspect for spoilage before discarding or composting.
