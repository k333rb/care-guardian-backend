import uuid
from sqlalchemy import String, Float
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
    # hospital | clinic | emergency
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    # Relationships
    household_facilities: Mapped[list] = relationship(
        "HouseholdFacility",
        back_populates="facility"
    )