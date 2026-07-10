"""
Smart Factory Dashboard — FastAPI Application Entry Point.

Industrial Asset Management REST API.
Author: Nalla Sumang
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base, get_db
from app.models import Asset
from app.exceptions import register_exception_handlers
from app.routers import assets, health


# ---------------------------------------------------------------------------
# Lifecycle — create tables and seed demo data on startup
# ---------------------------------------------------------------------------

def _seed_demo_data(db) -> None:
    """Populate the database with realistic factory machines if empty."""
    if db.query(Asset).count() > 0:
        return

    demo_assets = [
        Asset(machine_name="CNC Milling Station A", status="RUNNING", uptime_percentage=97.3),
        Asset(machine_name="Hydraulic Press B2", status="RUNNING", uptime_percentage=94.1),
        Asset(machine_name="Conveyor Belt Line 4", status="MAINTENANCE", uptime_percentage=78.5),
        Asset(machine_name="Welding Robot Arm C", status="RUNNING", uptime_percentage=99.2),
        Asset(machine_name="Packaging Unit D1", status="OFFLINE", uptime_percentage=0.0),
        Asset(machine_name="Laser Cutter E3", status="RUNNING", uptime_percentage=91.8),
        Asset(machine_name="Quality Inspection Camera F", status="RUNNING", uptime_percentage=96.4),
        Asset(machine_name="Paint Spray Booth G", status="MAINTENANCE", uptime_percentage=65.0),
    ]
    db.add_all(demo_assets)
    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables and seed data on startup."""
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        _seed_demo_data(db)
    finally:
        db.close()
    yield


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Industrial Asset Management REST API — monitors, manages, and controls "
        "factory machines in real-time. Features include CRUD operations, status "
        "management, filtering, pagination, and aggregated dashboard statistics."
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
register_exception_handlers(app)

# Routers
app.include_router(assets.router)
app.include_router(health.router)
