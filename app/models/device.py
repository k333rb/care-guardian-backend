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
    household_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("households.id"),
        nullable=False,
        index=True
    )
    device_name: Mapped[str] = mapped_column(String(200), nullable=False)
    # webcam | rtsp | http
    stream_type: Mapped[str] = mapped_column(String(20), default="webcam")
    source_url: Mapped[str] = mapped_column(String(500), default="0")
    # active | inactive | offline
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    household: Mapped["Household"] = relationship("Household", back_populates="devices")
    events: Mapped[list] = relationship("Event", back_populates="device")