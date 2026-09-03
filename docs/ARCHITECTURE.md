# FreshGuard AI — Technical Architecture Specification

**System:** FreshGuard AI  
**Version:** 3.0.0 (Production Release Baseline)  
**Date:** September 2026  

---

## 1. High-Level Architecture Overview

FreshGuard AI is structured as a decoupled multi-layer client-server platform optimized for low-latency CPU vision inference, zero prediction fabrication, and strict multi-tenant household data isolation.

```mermaid
graph TD
    subgraph Presentation Clients
        Web["HTML5 / JS Web Dashboard (Vercel)"]
        Mobile["Flutter iOS & Android App"]
    end

    subgraph FastAPI Application Gateway
        Router["/api/v1 Router & Versioning"]
        Auth["PBKDF2 Auth & JWT Verification"]
        RBAC["RBAC Middleware (USER / ADMIN)"]
        CORS["CORS Security Middleware"]
    end

    subgraph Core Business Services
        InventoryEngine["Inventory & Quantity Aggregation Engine"]
        FreshnessEngine["35-Class Freshness & Expiry Engine"]
        ScannerService["Barcode & OCR Service"]
        Notifications["24h Deduplicated FCM Dispatcher"]
    end

    subgraph AI Vision & ML Inference Pipeline
        ONNX["FreshGuard Vision V3 ONNX Engine"]
        NMS["Non-Maximum Suppression (IoU <= 0.45)"]
        Metadata["35-Class Metadata Resolver"]
    end

    subgraph Data & Storage Layer
        DB[("SQLAlchemy 2.0 SQLite Database")]
        Hashes["SHA-256 Model Integrity Manifest"]
    end

    Web --> Router
    Mobile --> Router
    Router --> Auth
    Auth --> RBAC
    RBAC --> CORS
    CORS --> InventoryEngine
    CORS --> FreshnessEngine
    CORS --> ScannerService
    CORS --> ONNX
    ONNX --> NMS
    NMS --> Metadata
    InventoryEngine --> DB
    FreshnessEngine --> DB
    ScannerService --> DB
    Notifications --> DB
    ONNX --> Hashes
```

---

## 2. Sequence Diagrams & Control Flow

### A. Multi-Modal Identity & Vision Pipeline Sequence
```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Client as Frontend Client
    participant API as FastAPI Gateway (/api/v1/scanner/vision/multimodal)
    participant Barcode as Open Food Facts Service
    participant Vision as ONNX Vision V3 Engine
    participant OCR as Packaging OCR Service
    participant Database as SQLite Database

    User->>Client: Capture Packaging Image / Barcode
    Client->>API: POST /multimodal (Image Payload + Barcode)
    
    par Dual Execution
        API->>Barcode: Query GTIN Barcode Registry
        API->>Vision: Run ONNX 35-Class Forward Pass (640x640)
        API->>OCR: Extract Expiry Date & Label Text
    end

    Barcode-->>API: Product Name & Category Identity
    Vision-->>API: Bounding Boxes + Confidence Scores
    OCR-->>API: Extracted Expiry Date String

    alt Discrepancy Detected (Barcode Name != Vision Class)
        API->>API: Flag Discrepancy (discrepancy_flagged: true)
    end

    API-->>Client: MultiModalScanResponse Payload
    Client->>User: Display Bounding Box & Confirmation Dialog
```

---

### B. Universal Inventory Flow Sequence
```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Client as Frontend Interface
    participant API as Inventory API (/api/v1/inventory)
    participant Engine as Inventory Aggregation Engine
    participant DB as Household Database

    User->>Client: Save Staged Detections
    Client->>API: POST /inventory (Action: MERGE / NEW_BATCH / SKIP)

    alt Action = MERGE ([ADD +X])
        API->>Engine: Query existing item (name, category, user_id)
        Engine->>DB: UPDATE quantity = quantity + delta
    else Action = NEW_BATCH
        API->>Engine: Generate distinct batch record
        Engine->>DB: INSERT INTO inventory_items
    else Action = SKIP
        API-->>Client: Return 200 OK (No-op)
    end

    DB-->>API: Updated Inventory Record
    API-->>Client: InventoryOut Payload
```

---

### C. 3-Tier Confidence Policy Decision Flow
```mermaid
flowchart TD
    Start([Vision Detection Input]) --> ConfCheck{Confidence Score?}
    
    ConfCheck -- "Score >= 0.50" --> HighTier["HIGH Tier (Stage for Auto-Save)"]
    ConfCheck -- "0.30 <= Score < 0.50" --> MedTier["MEDIUM Tier (Pre-fill with Prompt)"]
    ConfCheck -- "Score < 0.30" --> LowTier["LOW Tier (requires_confirmation: true)"]

    HighTier --> FinalOutput[Return VisionDetectResponse]
    MedTier --> FinalOutput
    LowTier --> FinalOutput
```

---

## 3. Component Design & Control Flow

### A. Authentication & Security Layer
- **Password Hashing**: PBKDF2-HMAC-SHA256 with 100,000 iterations and 16-byte random salts (`pbkdf2_sha256$<salt>$<hash>`).
- **Legacy Migration**: Transparently upgrades legacy SHA-256 password hashes to PBKDF2 format upon login.
- **JWT Authorization**: Tokens expire in 3 days containing user identity (`sub`) and role (`role`).
- **RBAC**: Users are assigned `USER` (default) or `ADMIN`. `/admin/diagnostics` enforces HTTP 403 Forbidden for non-admin accounts.

### B. Household Multi-Tenant Data Isolation
- Database entities (`InventoryItem`, `Notification`, `ConsumptionLog`) enforce strict foreign key relations to `user_id` and `household_id`.
- All service methods automatically inject `filter(user_id == current_user.id)` to guarantee zero cross-tenant data leaks.

---

## 4. Database Schema ER Map

- **Users**: `id`, `email`, `password_hash`, `full_name`, `role` (index), `created_at`
- **Households**: `id`, `name`, `join_code` (unique index), `owner_id` (FK: `users.id`)
- **HouseholdMembers**: `id`, `household_id` (FK), `user_id` (FK), `role`
- **Inventory**: `id`, `user_id` (FK), `household_id` (FK), `product_name`, `category`, `quantity`, `unit`, `storage_location`, `expiry_date` (index), `status` (index)
- **ConsumptionLogs**: `id`, `household_id` (FK), `inventory_id` (FK), `quantity_consumed`, `date_consumed` (index), `log_type`
- **Notifications**: `id`, `user_id` (FK), `title`, `message`, `type`, `priority`, `is_read`, `created_at`
- **ShoppingCart**: `id`, `household_id` (FK), `total_estimated_price`, `status`
