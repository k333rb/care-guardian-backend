from pydantic import BaseModel, Field
from datetime import datetime


class DetectionFrameRequest(BaseModel):
    """Request schema for frame-based detection (webcam stream)."""
    image_base64: str = Field(
        ..., 
        description="Base64-encoded image data from camera frame"
    )
    device_id: str = Field(..., description="ID of the camera/device")
    frame_ts: datetime = Field(..., description="Timestamp when frame was captured")


class DetectionResponse(BaseModel):
    """Response schema for detection inference result."""
    label: str = Field(..., description="Activity label (e.g., 'fall', 'standing')")
    confidence: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Confidence score 0.0–1.0"
    )
    timestamp: datetime = Field(..., description="When detection was processed")
    monitoring_type: str = Field(
        default="video",
        description="Type of monitoring ('video', 'wearable', etc.)"
    )
    event_id: str | None = Field(
        default=None,
        description="Optional event ID if alert was triggered"
    )
    alert_triggered: bool = Field(
        default=False,
        description="Whether alert system was activated"
    )
