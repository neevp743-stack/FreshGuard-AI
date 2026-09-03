import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api import auth, inventory, freshness_router, scanner, vision_router, ai_router, cart, notifications_router, analytics, health, admin

# Create database tables automatically
Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Operational Health Probes",
        "description": "Ultra-fast liveness and application readiness health status endpoints."
    },
    {
        "name": "Authentication & User Access",
        "description": "User registration, PBKDF2 authentication, JWT access token generation, and user profile management."
    },
    {
        "name": "Inventory Management Engine",
        "description": "Household food inventory tracking, quantity merging, batch management, and status updates."
    },
    {
        "name": "Freshness & Expiry Engine",
        "description": "Dynamic shelf-life calculations, freshness state tracking (FRESH, USE_SOON, EXPIRED), and consumption priority."
    },
    {
        "name": "Vision AI & Multi-Modal Scanner",
        "description": "YOLOv8 35-class ONNX vision object detection, multi-modal barcode+vision+OCR identity pipeline, and active learning feedback."
    },
    {
        "name": "Barcode & OCR Scanner Service",
        "description": "Open Food Facts barcode metadata lookup and packaging label text/date OCR parsing."
    },
    {
        "name": "Smart Cart & Grocery Assistant",
        "description": "Automated grocery refill recommendations and AI shopping cart management."
    },
    {
        "name": "Notifications & Expiry Alerts",
        "description": "24-hour deduplicated FCM push notification preferences and alert dispatch."
    },
    {
        "name": "Household Analytics",
        "description": "Consumption velocity, food waste prevention metrics, and category distributions."
    },
    {
        "name": "Administrative Diagnostics",
        "description": "Protected RBAC system diagnostics and telemetry (ADMIN access required)."
    }
]

app = FastAPI(
    title=settings.APP_NAME,
    version="3.0.0",
    description=(
        "**FreshGuard AI Production API Service**\n\n"
        "An AI-powered household food, freshness, and grocery management application API. "
        "Provides 35-class YOLOv8 vision object detection, multi-modal barcode/OCR parsing, "
        "dynamic freshness calculation, household inventory management, and FCM push notifications."
    ),
    openapi_tags=tags_metadata,
    contact={
        "name": "FreshGuard AI Engineering Team",
        "url": "https://github.com/neevp743-stack/FreshGuard-AI",
        "email": "engineering@freshguard.ai",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Enable CORS for Flutter mobile and web applications using configurable CORS_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def warmup_vision_model_on_startup():
    """
    Pre-warms and caches ONNX Runtime session during container boot.
    Prevents client-side timeouts during first inference request.
    """
    try:
        from app.ai.vision.inference import get_onnx_session
        session = get_onnx_session()
        if session:
            print("[STARTUP] ONNX Runtime Vision Model pre-loaded successfully.")
    except Exception as e:
        print(f"[STARTUP WARNING] ONNX Runtime Vision Model pre-load warning: {e}")

# Include Lightweight Health Router (/health and /api/v1/health)
app.include_router(health.router)

# Include API v1 Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")
app.include_router(freshness_router.router, prefix="/api/v1")
app.include_router(scanner.router, prefix="/api/v1")
app.include_router(vision_router.router, prefix="/api/v1")
app.include_router(ai_router.router, prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")
app.include_router(notifications_router.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

# Include Backward Compatibility Aliases under /api/...
app.include_router(auth.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")
app.include_router(freshness_router.router, prefix="/api")
app.include_router(scanner.router, prefix="/api")
app.include_router(vision_router.router, prefix="/api")
app.include_router(ai_router.router, prefix="/api")
app.include_router(cart.router, prefix="/api")
app.include_router(notifications_router.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(admin.router, prefix="/api")


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "tagline": "Know. Use. Refill. Waste Less.",
        "status": "online",
        "health_endpoint": "/health",
        "api_v1_docs": "/docs"
    }

@app.get("/vision-v3-test", response_class=HTMLResponse)
def get_vision_v3_test_page():
    """Serves the dedicated FreshGuard Vision V3 Staging Webcam Test Interface."""
    html_path = os.path.join(os.path.dirname(__file__), "../frontend/web/vision_v3_test.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>FreshGuard Vision V3 Test Page Not Found</h1>", status_code=404)



