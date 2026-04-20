import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Household(Base):
    __tablename__ = "households"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"hh-{uuid.uuid4()}"
    )
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    household_users: Mapped[list] = relationship("HouseholdUser", back_populates="household")
    devices: Mapped[list] = relationship("Device", back_populates="household")
    household_facilities: Mapped[list] = relationship("HouseholdFacility", back_populates="household")