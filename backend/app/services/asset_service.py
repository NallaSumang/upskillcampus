"""
Asset service — business logic layer.

Separates database operations from route handlers for testability and reuse.
"""

import math
from typing import Optional, List, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func

from app.models import Asset
from app.schemas import AssetCreate, AssetStatus, DashboardStats
from app.exceptions import AssetNotFoundError


def get_all_assets(
    db: Session,
    *,
    page: int = 1,
    page_size: int = 50,
    status: Optional[AssetStatus] = None,
    search: Optional[str] = None,
    sort_by: str = "id",
    sort_order: str = "asc",
) -> Tuple[List[Asset], int]:
    """
    Retrieve assets with filtering, search, sorting, and pagination.

    Returns:
        Tuple of (list of assets, total count matching filters).
    """
    query = db.query(Asset)

    # Filters
    if status:
        query = query.filter(Asset.status == status.value)
    if search:
        query = query.filter(Asset.machine_name.ilike(f"%{search}%"))

    # Total count (before pagination)
    total = query.count()

    # Sorting
    sort_column = getattr(Asset, sort_by, Asset.id)
    if sort_order == "desc":
        sort_column = sort_column.desc()
    query = query.order_by(sort_column)

    # Pagination
    offset = (page - 1) * page_size
    assets = query.offset(offset).limit(page_size).all()

    return assets, total


def get_asset_by_id(db: Session, asset_id: int) -> Asset:
    """Retrieve a single asset or raise AssetNotFoundError."""
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise AssetNotFoundError(asset_id)
    return asset


def create_asset(db: Session, payload: AssetCreate) -> Asset:
    """Register a new factory machine."""
    asset = Asset(
        machine_name=payload.machineName,
        status=payload.status.value,
        uptime_percentage=payload.uptimePercentage,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def update_asset_status(db: Session, asset_id: int, new_status: AssetStatus) -> Asset:
    """Update the operational status of a machine."""
    asset = get_asset_by_id(db, asset_id)
    asset.status = new_status.value
    db.commit()
    db.refresh(asset)
    return asset


def delete_asset(db: Session, asset_id: int) -> None:
    """Remove a machine from the system."""
    asset = get_asset_by_id(db, asset_id)
    db.delete(asset)
    db.commit()


def bulk_delete_assets(db: Session, ids: List[int]) -> int:
    """Delete multiple assets by ID. Returns the count of deleted rows."""
    count = db.query(Asset).filter(Asset.id.in_(ids)).delete(synchronize_session="fetch")
    db.commit()
    return count


def get_dashboard_stats(db: Session) -> DashboardStats:
    """Compute aggregated dashboard statistics."""
    total = db.query(Asset).count()
    running = db.query(Asset).filter(Asset.status == "RUNNING").count()
    maintenance = db.query(Asset).filter(Asset.status == "MAINTENANCE").count()
    offline = db.query(Asset).filter(Asset.status == "OFFLINE").count()

    avg_result = db.query(sql_func.avg(Asset.uptime_percentage)).scalar()
    avg_uptime = round(avg_result, 1) if avg_result else 0.0

    return DashboardStats(
        total_assets=total,
        running=running,
        maintenance=maintenance,
        offline=offline,
        avg_uptime=avg_uptime,
    )
