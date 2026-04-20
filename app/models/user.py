import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"usr-{uuid.uuid4()}"
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    # family | caregiver
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=True, unique=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    household_users: Mapped[list] = relationship("HouseholdUser", back_populates="user")
    alerts: Mapped[list] = relationship("Alert", back_populates="user")