from pydantic import BaseModel, Field
from typing import Optional


class HouseholdSummaryResponse(BaseModel):
    """Summary of a household with device and active alert counts."""
    id: str = Field(..., description="Household ID")
    address: str = Field(..., description="Household address")
    latitude: Optional[float] = Field(default=None, description="GPS latitude")
    longitude: Optional[float] = Field(default=None, description="GPS longitude")
    device_count: int = Field(..., ge=0, description="Number of cameras installed")
    active_alert_count: int = Field(
        ...,
        ge=0,
        description="Number of unresolved alerts (status=sent)"
    )