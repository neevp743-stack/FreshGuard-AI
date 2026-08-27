from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Auth Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    household_name: Optional[str] = "My Household"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    full_name: Optional[str] = None
    role: str = "USER"
    household_id: int
    household_name: str

class HouseholdOut(BaseModel):
    id: int
    name: str
    join_code: str
    owner_id: int
    created_at: datetime
    member_count: Optional[int] = 1

    class Config:
        from_attributes = True

# --- Inventory Schemas ---
class InventoryCreate(BaseModel):
    product_name: str
    brand: Optional[str] = None
    category: str = "Other"
    quantity: float = 1.0
    unit: str = "pcs"
    storage_location: str = "Pantry"
    purchase_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    opened_date: Optional[datetime] = None
    barcode: Optional[str] = None
    image_url: Optional[str] = None
    notes: Optional[str] = None

class InventoryUpdate(BaseModel):
    product_name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    storage_location: Optional[str] = None
    expiry_date: Optional[datetime] = None
    opened_date: Optional[datetime] = None
    estimated_remaining_quantity: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class InventoryOut(BaseModel):
    id: int
    user_id: int
    household_id: int
    product_name: str
    category: str
    brand: Optional[str] = None
    quantity: float
    unit: str
    storage_location: str
    purchase_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    opened_date: Optional[datetime] = None
    estimated_remaining_quantity: Optional[float] = None
    barcode: Optional[str] = None
    image_url: Optional[str] = None
    notes: Optional[str] = None
    status: str
    days_until_expiry: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Consumption Log Schemas ---
class ConsumptionLogCreate(BaseModel):
    inventory_id: Optional[int] = None
    product_name: str
    category: Optional[str] = "Other"
    quantity_consumed: float
    unit: str = "pcs"
    log_type: str = "consumed" # consumed, wasted, expired, donated
    waste_value: Optional[float] = 0.0

class ConsumptionLogOut(BaseModel):
    id: int
    household_id: int
    product_name: str
    category: Optional[str] = None
    quantity_consumed: float
    unit: str
    date_consumed: datetime
    log_type: str
    waste_value: float

    class Config:
        from_attributes = True

# --- Scanner Schemas ---
class BarcodeLookupRequest(BaseModel):
    barcode: str

class BarcodeLookupResponse(BaseModel):
    found: bool
    barcode: str
    product_name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    default_unit: Optional[str] = "pcs"

class OCRScanResponse(BaseModel):
    detected: bool
    product_name: Optional[str] = None
    brand: Optional[str] = None
    expiry_date: Optional[str] = None
    mfg_date: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    batch_number: Optional[str] = None
    confidence_score: float
    requires_confirmation: bool = False
    raw_text: Optional[str] = None

class OCRImageResponse(BaseModel):
    success: bool
    product_name: Optional[str] = None
    brand: Optional[str] = None
    manufacturing_date: Optional[str] = None
    expiry_date: Optional[str] = None
    quantity: Optional[float] = 1.0
    unit: Optional[str] = "pcs"
    batch_number: Optional[str] = None
    raw_text: str
    confidence: float
    requires_confirmation: bool = False
    message: Optional[str] = None

# --- Vision Schemas ---
class VisionDetection(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    bounding_box: Dict[str, float] # {x1, y1, x2, y2}
    requires_confirmation: bool = False

class VisionDetectResponse(BaseModel):
    success: bool
    lifecycle_state: str # NOT_TRAINED, TRAINING, READY, FAILED, DEPRECATED
    model_version: str
    confidence_threshold: float
    image_width: int
    image_height: int
    detections: List[VisionDetection] = []
    message: str

class VisionStatusResponse(BaseModel):
    lifecycle_state: str
    model_available: bool
    model_version: str
    classes_count: int
    confidence_threshold: float
    message: str

class VisionFeedbackRequest(BaseModel):
    predicted_class: str
    confidence: float
    corrected_class: str
    opt_in_image_retention: bool = False
    comments: Optional[str] = None

class MultiModalScanResponse(BaseModel):
    barcode_identity: Optional[Dict[str, Any]] = None
    vision_detections: List[VisionDetection] = []
    ocr_result: Optional[Dict[str, Any]] = None
    discrepancy_flagged: bool = False
    discrepancy_message: Optional[str] = None
    final_suggested_item: Dict[str, Any]

# --- AI & Recommendation Schemas ---
class ConsumptionPrediction(BaseModel):
    product_name: str
    current_quantity: float
    unit: str
    avg_daily_consumption: float
    estimated_days_remaining: float
    predicted_runout_date: Optional[str]
    confidence_score: float
    status_message: str

class AIRecommendationOut(BaseModel):
    id: int
    product_name: str
    category: str
    suggested_quantity: float
    unit: str
    reason: str
    urgency: str
    added_to_cart: bool

class AIInsightSummary(BaseModel):
    healthy_count: int
    expiring_soon_count: int
    expired_count: int
    running_low_count: int
    food_waste_estimate: float
    top_consumed_category: str
    recent_insight_message: str

class AIAssistantRequest(BaseModel):
    query: str

class AIAssistantResponse(BaseModel):
    query: str
    answer: str
    related_items: List[str] = []

# --- Smart Cart Schemas ---
class CartItemCreate(BaseModel):
    product_name: str
    quantity: float = 1.0
    unit: str = "pcs"
    estimated_price: float = 0.0
    reason: Optional[str] = "User added"
    priority: Optional[str] = "Normal"

class CartItemOut(BaseModel):
    id: int
    product_name: str
    quantity: float
    unit: str
    estimated_price: float
    reason: Optional[str] = None
    priority: str
    confirmed: bool

    class Config:
        from_attributes = True

class CartOut(BaseModel):
    id: int
    household_id: int
    total_estimated_price: float
    status: str
    items: List[CartItemOut] = []

    class Config:
        from_attributes = True

# --- Notification & Device Token Schemas ---
class DeviceTokenCreate(BaseModel):
    token: str
    platform: Optional[str] = "android"

class DeviceTokenOut(BaseModel):
    id: int
    user_id: int
    token: str
    platform: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationOut(BaseModel):
    id: int
    title: str
    message: str
    type: str
    priority: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Health & Admin Schemas ---
class HealthCheckResponse(BaseModel):
    status: str # READY, DEGRADED, INITIALIZING, UNAVAILABLE
    process_alive: bool = True
    database_connected: bool = True
    version: str = "1.0.0"
    timestamp: str

class AdminDiagnosticsResponse(BaseModel):
    status: str
    process_alive: bool
    memory_usage_mb: float
    database_status: str
    ai_vision_status: str
    ai_vision_lifecycle: str
    error_count_24h: int
    timestamp: str

