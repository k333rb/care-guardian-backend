from pydantic import BaseModel, Field


class FacilitySummaryResponse(BaseModel):
    """Summary response for a facility with device and alert counts."""
    id: str = Field(..., description="Facility ID")
    name: str = Field(..., description="Facility name")
    device_count: int = Field(..., ge=0, description="Number of monitoring devices")
    active_alert_count: int = Field(
        ...,
        ge=0,
        description="Number of currently active (non-resolved) alerts"
    )
