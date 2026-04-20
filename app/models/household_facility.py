import uuid
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class HouseholdFacility(Base):
    __tablename__ = "household_facilities"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"hhf-{uuid.uuid4()}"
    )
    household_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("households.id"),
        nullable=False,
        index=True
    )
    facility_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("facilities.id"),
        nullable=False,
        index=True
    )
    # precomputed distance in km — avoids recalculating every query
    distance: Mapped[float] = mapped_column(Float, nullable=True)

    # Relationships
    household: Mapped["Household"] = relationship("Household", back_populates="household_facilities")
    facility: Mapped["Facility"] = relationship("Facility", back_populates="household_facilities")