import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"alrt-{uuid.uuid4()}"
    )
    event_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("events.id"),
        nullable=False,
        index=True
    )
    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    # sent | seen | resolved
    status: Mapped[str] = mapped_column(String(20), default="sent")
    # app | sms | both
    delivery_method: Mapped[str] = mapped_column(String(20), default="app")
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    resolved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Relationships
    event: Mapped["Event"] = relationship("Event", back_populates="alerts")
    user: Mapped["User"] = relationship("User", back_populates="alerts")

    __table_args__ = (
        Index("ix_alerts_user_status", "user_id", "status"),
    )