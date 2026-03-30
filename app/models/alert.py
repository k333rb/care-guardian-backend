import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"alrt-{uuid.uuid4()}"
    )
    device_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("devices.id"),
        nullable=False
    )
    facility_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("facilities.id"),
        nullable=False,
        index=True
    )
    event_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("detection_events.id"),
        nullable=False,
        unique=True  # one alert per detection event, no duplicates
    )
    status: Mapped[str] = mapped_column(String(20), default="triggered")
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    delivery_method: Mapped[str] = mapped_column(String(20), default="app")
    triggered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    delivered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    resolved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Relationships
    device: Mapped["Device"] = relationship("Device", back_populates="alerts")
    facility: Mapped["Facility"] = relationship("Facility", back_populates="alerts")
    event: Mapped["DetectionEvent"] = relationship("DetectionEvent", back_populates="alert")

    __table_args__ = (
        Index("ix_alerts_facility_status", "facility_id", "status"),
    )