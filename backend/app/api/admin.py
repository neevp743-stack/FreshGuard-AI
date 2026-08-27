import os
import psutil
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.models.models import User
from app.schemas.schemas import AdminDiagnosticsResponse
from app.ai.vision.inference import get_vision_model_status

router = APIRouter(prefix="/admin", tags=["Admin Diagnostics"])

@router.get("/diagnostics", response_model=AdminDiagnosticsResponse)
def get_admin_diagnostics(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    ADMIN-only Operational Diagnostics Endpoint.
    Returns backend memory usage, process status, database connection state,
    and Vision AI model availability.
    Normal USER accounts receive 403 Forbidden.
    Secrets and sensitive internal configuration are strictly withheld.
    """
    # Check Database connection
    db_status = "HEALTHY"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "UNAVAILABLE"

    # Memory Usage
    process = psutil.Process(os.getpid())
    memory_mb = round(process.memory_info().rss / (1024 * 1024), 2)

    # AI Vision Status
    v_status = get_vision_model_status()
    ai_status = "READY" if v_status.model_available else "STANDBY"

    return AdminDiagnosticsResponse(
        status="OPERATIONAL" if db_status == "HEALTHY" else "DEGRADED",
        process_alive=True,
        memory_usage_mb=memory_mb,
        database_status=db_status,
        ai_vision_status=ai_status,
        ai_vision_lifecycle=v_status.lifecycle_state,
        error_count_24h=0,
        timestamp=datetime.now(timezone.utc).isoformat()
    )
