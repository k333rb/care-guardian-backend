from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.detection_service import run_detection
from app import crud
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
    event_id: str
    alert_triggered: bool

@router.post("", response_model=DetectionResponse)
async def detect_frame(
    payload: FrameRequest,
    x_facility_id: str = Header(..., alias="X-Facility-ID"),
    db: AsyncSession = Depends(get_db)
):
    # 1. Decode base64 → cv2 frame
    try:
        img_bytes = base64.b64decode(payload.image_base64)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("Invalid image")
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid base64 image")

    # 2. Run detection
    result = run_detection(frame)

    # 3. Log DetectionEvent
    frame_ts = payload.frame_ts or datetime.now(timezone.utc)
    event = await crud.create_detection_event(
        db,
        device_id=payload.device_id,
        facility_id=x_facility_id,
        label=result.label,
        confidence=result.confidence,
        frame_ts=frame_ts
    )

    # 4. Trigger alert if fall detected
    alert_triggered = False
    if result.label == "fall":
        await crud.create_alert(
            db,
            device_id=payload.device_id,
            facility_id=x_facility_id,
            event_id=event.id,
            confidence=result.confidence,
        )
        alert_triggered = True

    return DetectionResponse(
        label=result.label,
        confidence=result.confidence,
        timestamp=frame_ts,
        monitoring_type="camera_ai",
        event_id=event.id,
        alert_triggered=alert_triggered
    )