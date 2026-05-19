from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.detection_service import handle_detection
from pydantic import BaseModel
from datetime import datetime, timezone
import base64
import numpy as np
import cv2

router = APIRouter(prefix="/detect-frame", tags=["Detection"])


class FrameRequest(BaseModel):
    image_base64: str
    device_id: str
    frame_ts: datetime | None = None


class DetectionResponse(BaseModel):
    label: str
    confidence: float
    timestamp: datetime
    monitoring_type: str
    event_id: str | None
    alert_triggered: bool


@router.post("", response_model=DetectionResponse)
async def detect_frame(
    payload: FrameRequest,
    x_facility_id: str = Header(..., alias="X-Facility-ID"),
    db: AsyncSession = Depends(get_db)
):
    # 1. Decode base64 → OpenCV frame
    try:
        img_bytes = base64.b64decode(payload.image_base64)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            raise ValueError("Invalid image")

    except Exception:
        raise HTTPException(status_code=422, detail="Invalid base64 image")

    # 2. Timestamp
    frame_ts = payload.frame_ts or datetime.now(timezone.utc)

    # 3. Run detection + event + alert (handled in service)
    result = await handle_detection(
        frame=frame,
        session=db,
        device_id=payload.device_id,
        household_id=x_facility_id
    )

    # 4. Return unified response
    return DetectionResponse(
        label=result["label"],
        confidence=result["confidence"],
        timestamp=frame_ts,
        monitoring_type="camera_ai",
        event_id=result.get("event_id"),
        alert_triggered=result["alert_triggered"]
    )