"""
SQLAlchemy ORM models.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, func

from app.database import Base


class Asset(Base):
    """Represents an industrial machine or factory asset."""

    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    machine_name = Column(String(255), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="RUNNING")
    uptime_percentage = Column(Float, nullable=False, default=95.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<Asset(id={self.id}, name='{self.machine_name}', status='{self.status}')>"
