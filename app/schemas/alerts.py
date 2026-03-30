from pydantic import BaseModel, Field
from datetime import datetime


class AlertResponse(BaseModel):
    """Response schema for alert events."""
    id: str = Field(..., description="Unique alert ID")
    facility_id: str = Field(..., description="Associated facility")
    device_id: str = Field(..., description="Device that triggered alert")
    status: str = Field(
        ..., 
        description="Alert status: 'triggered', 'resolved'"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Detection confidence that triggered alert"
    )
    delivery_method: str | None = Field(
        default=None,
        description="How alert was delivered ('sms', 'push', 'dashboard', etc.)"
    )
    triggered_at: datetime = Field(..., description="When alert was first triggered")
