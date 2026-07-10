"""
Pydantic schemas for request validation and response serialization.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AssetStatus(str, Enum):
    """Valid operational statuses for an industrial asset."""
    RUNNING = "RUNNING"
    MAINTENANCE = "MAINTENANCE"
    OFFLINE = "OFFLINE"


# ---------------------------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------------------------

class AssetCreate(BaseModel):
    """Schema for registering a new factory machine."""
    machineName: str = Field(..., min_length=1, max_length=255)
    status: AssetStatus = Field(default=AssetStatus.RUNNING)
    uptimePercentage: float = Field(default=95.0, ge=0.0, le=100.0)


class AssetStatusUpdate(BaseModel):
    """Schema for updating a machine's operational status."""
    status: AssetStatus


class AssetBulkDelete(BaseModel):
    """Schema for bulk-deleting machines by ID."""
    ids: List[int] = Field(..., min_length=1)


# ---------------------------------------------------------------------------
# Response Schemas
# ---------------------------------------------------------------------------

class AssetResponse(BaseModel):
    """Schema for a single asset in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    machineName: str
    status: AssetStatus
    uptimePercentage: float
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None


class PaginatedResponse(BaseModel):
    """Wrapper for paginated list responses."""
    items: List[AssetResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class DashboardStats(BaseModel):
    """Aggregated dashboard statistics."""
    total_assets: int
    running: int
    maintenance: int
    offline: int
    avg_uptime: float


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    database: str
