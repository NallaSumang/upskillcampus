"""
Health router — system health and readiness checks.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.config import settings
from app.schemas import HealthResponse


router = APIRouter(tags=["System"])


@router.get("/api/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """
    System health check.

    Verifies the application is running and the database is reachable.
    """
    # Test database connectivity
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "unreachable"

    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        version=settings.APP_VERSION,
        database=db_status,
    )
