from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DetectionFrameRequest(BaseModel):
    """Request schema for frame-based detection from webcam stream."""
    image_base64: str = Field(
        ...,
        description="Base64-encoded JPEG frame from camera"
    )
    device_id: str = Field(..., description="ID of the camera sending this frame")
    frame_ts: datetime = Field(..., description="Timestamp when frame was captured")


class DetectionResponse(BaseModel):
    """Response schema after processing a detection frame."""
    event_id: str = Field(..., description="Created event ID")
    type: str = Field(..., description="fall | normal")
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Model confidence 0.0–1.0"
    )
    monitoring_type: str = Field(
        default="camera_ai",
        description="Always camera_ai — documents wearable-free monitoring"
    )
    timestamp: datetime = Field(..., description="When frame was captured")
    alert_triggered: bool = Field(
        default=False,
        description="True if confidence >= threshold and type == fall"
    )
    alert_id: Optional[str] = Field(
        default=None,
        description="Created alert ID — null if no alert was triggered"
    )