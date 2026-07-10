"""
Asset router — REST endpoints for industrial asset management.
"""

import math
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    AssetCreate,
    AssetStatusUpdate,
    AssetBulkDelete,
    AssetResponse,
    AssetStatus,
    PaginatedResponse,
    DashboardStats,
)
from app.services import asset_service


router = APIRouter(prefix="/api/assets", tags=["Assets"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _to_response(asset) -> AssetResponse:
    """Convert ORM model to Pydantic response with camelCase fields."""
    return AssetResponse(
        id=asset.id,
        machineName=asset.machine_name,
        status=asset.status,
        uptimePercentage=asset.uptime_percentage,
        createdAt=asset.created_at,
        updatedAt=asset.updated_at,
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("", response_model=List[AssetResponse])
def list_assets(
    status: Optional[AssetStatus] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by machine name"),
    sort_by: str = Query("id", description="Sort field"),
    sort_order: str = Query("asc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    """Retrieve all industrial assets with optional filtering, search, and pagination."""
    assets, total = asset_service.get_all_assets(
        db,
        page=page,
        page_size=page_size,
        status=status,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return [_to_response(a) for a in assets]


@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    """Get aggregated dashboard statistics."""
    return asset_service.get_dashboard_stats(db)


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    """Retrieve a single asset by its ID."""
    asset = asset_service.get_asset_by_id(db, asset_id)
    return _to_response(asset)


@router.post("", response_model=AssetResponse, status_code=201)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    """Register a new factory machine."""
    asset = asset_service.create_asset(db, payload)
    return _to_response(asset)


@router.put("/{asset_id}/status", response_model=AssetResponse)
def update_status(
    asset_id: int, payload: AssetStatusUpdate, db: Session = Depends(get_db)
):
    """Update the operational status of a machine."""
    asset = asset_service.update_asset_status(db, asset_id, payload.status)
    return _to_response(asset)


@router.delete("/{asset_id}", status_code=204)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    """Remove a machine from the system."""
    asset_service.delete_asset(db, asset_id)
    return None


@router.post("/bulk-delete", status_code=200)
def bulk_delete(payload: AssetBulkDelete, db: Session = Depends(get_db)):
    """Delete multiple machines by their IDs."""
    count = asset_service.bulk_delete_assets(db, payload.ids)
    return {"deleted": count}
