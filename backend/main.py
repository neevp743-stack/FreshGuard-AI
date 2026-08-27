from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api import auth, inventory, scanner, vision_router, ai_router, cart, notifications_router, analytics, health, admin

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AI-powered household food & grocery management application API"
)

# Enable CORS for Flutter mobile and web applications using configurable CORS_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Lightweight Health Router (/health and /api/v1/health)
app.include_router(health.router)

# Include API v1 Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")
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

