import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class HouseholdUser(Base):
    __tablename__ = "household_users"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"hhu-{uuid.uuid4()}"
    )
    household_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("households.id"),
        nullable=False,
        index=True
    )
    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Relationships
    household: Mapped["Household"] = relationship("Household", back_populates="household_users")
    user: Mapped["User"] = relationship("User", back_populates="household_users")