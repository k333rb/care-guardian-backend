import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Facility(Base):
    __tablename__ = "facilities"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"fac-{uuid.uuid4()}"
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    tier: Mapped[str] = mapped_column(String(30), nullable=False)
    location: Mapped[str] = mapped_column(String(300), nullable=True)
    contact_person: Mapped[str] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships — tells SQLAlchemy how tables connect
    devices: Mapped[list] = relationship("Device", back_populates="facility")
    detection_events: Mapped[list] = relationship("DetectionEvent", back_populates="facility")
    alerts: Mapped[list] = relationship("Alert", back_populates="facility")