from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AlertResponse(BaseModel):
    """Response schema for an alert targeted at a specific user."""
    id: str = Field(..., description="Unique alert ID")
    event_id: str = Field(..., description="The fall event that triggered this alert")
    user_id: str = Field(..., description="User who receives this alert")
    status: str = Field(..., description="sent | seen | resolved")
    delivery_method: str = Field(..., description="app | sms | both")
    timestamp: datetime = Field(..., description="When alert was created")
    resolved_at: Optional[datetime] = Field(
        default=None,
        description="When alert was resolved — null if still active"
    )

    model_config = {"from_attributes": True}