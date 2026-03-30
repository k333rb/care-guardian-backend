from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"dev-{uuid.uuid4()}"
    )
    facility_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("facilities.id"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    stream_type: Mapped[str] = mapped_column(String(20), default="webcam")
    source_url: Mapped[str] = mapped_column(String(500), default="0")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    facility: Mapped["Facility"] = relationship("Facility", back_populates="devices")
    detection_events: Mapped[list] = relationship("DetectionEvent", back_populates="device")
    alerts: Mapped[list] = relationship("Alert", back_populates="device")