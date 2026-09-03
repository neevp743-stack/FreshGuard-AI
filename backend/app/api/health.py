from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.schemas.schemas import HealthCheckResponse

router = APIRouter(tags=["Operational Health Probes"])

@router.get("/health", response_model=HealthCheckResponse, summary="Operational Health Probe", description="Lightweight health probe for cloud load balancers and deployment readiness.")
@router.get("/api/v1/health", response_model=HealthCheckResponse, summary="API v1 Health Probe", description="API v1 health status probe.")
def get_health_status(db: Session = Depends(get_db)):
    """
    Extremely lightweight health probe.
    Does NOT load ML models, execute AI inference, or query heavy database tables.
    Distinguishes PROCESS ALIVE from APPLICATION READY.
    """
    db_connected = False
    status_str = "READY"

    try:
        # Lightweight ping query
        db.execute(text("SELECT 1"))
        db_connected = True
    except Exception:
        db_connected = False
        status_str = "DEGRADED"

    return HealthCheckResponse(
        status=status_str,
        process_alive=True,
        database_connected=db_connected,
        version="3.0.0",
        timestamp=datetime.now(timezone.utc).isoformat()
    )
