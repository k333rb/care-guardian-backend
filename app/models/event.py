import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"evt-{uuid.uuid4()}"
    )
    device_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("devices.id"),
        nullable=False,
        index=True
    )
    # fall | normal
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    # always "camera_ai" — documents wearable-free monitoring
    monitoring_type: Mapped[str] = mapped_column(
        String(50),
        default="camera_ai"
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    device: Mapped["Device"] = relationship("Device", back_populates="events")
    alerts: Mapped[list] = relationship("Alert", back_populates="event")

    __table_args__ = (
        Index("ix_events_device_timestamp", "device_id", "timestamp"),
    )