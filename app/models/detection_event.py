from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class DetectionEvent(Base):
    __tablename__ = "detection_events"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"evt-{uuid.uuid4()}"
    )
    device_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("devices.id"),
        nullable=False
    )
    facility_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("facilities.id"),
        nullable=False
    )
    label: Mapped[str] = mapped_column(String(50), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    monitoring_type: Mapped[str] = mapped_column(
        String(50),
        default="camera_ai"
    )
    frame_ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    device: Mapped["Device"] = relationship("Device", back_populates="detection_events")
    facility: Mapped["Facility"] = relationship("Facility", back_populates="detection_events")
    alert: Mapped["Alert"] = relationship("Alert", back_populates="event", uselist=False)

    __table_args__ = (
        Index("ix_detection_events_facility_frame_ts", "facility_id", "frame_ts"),
        Index("ix_detection_events_device_frame_ts", "device_id", "frame_ts"),
    )