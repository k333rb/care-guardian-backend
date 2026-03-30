from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.detection_event import DetectionEvent
from app.models.alert import Alert
from app.models.facility import Facility
from app.models.device import Device
import uuid
from datetime import datetime, timezone

# Detection Events
async def create_detection_event(db: AsyncSession, device_id: str, facility_id: str, label: str, confidence: float, frame_ts: datetime):
    event = DetectionEvent(
        id=str(uuid.uuid4()),
        device_id=device_id,
        facility_id=facility_id,
        label=label,
        confidence=confidence,
        monitoring_type="camera_ai",
        frame_ts=frame_ts,
    )
    db.add(event)
    await db.flush()
    return event

# Alerts
async def create_alert(db: AsyncSession, device_id: str, facility_id: str, event_id: str, confidence: float, delivery_method: str = "app"):
    alert = Alert(
        id=str(uuid.uuid4()),
        device_id=device_id,
        facility_id=facility_id,
        event_id=event_id,
        status="triggered",
        confidence=confidence,
        delivery_method=delivery_method,
        triggered_at=datetime.now(timezone.utc),
    )
    db.add(alert)
    await db.flush()
    return alert

# Get events by facility (paginated)
async def get_events_by_facility(db: AsyncSession, facility_id: str, skip: int = 0, limit: int = 50):
    result = await db.execute(
        select(DetectionEvent)
        .where(DetectionEvent.facility_id == facility_id)
        .order_by(DetectionEvent.created_at.desc())
        .offset(skip).limit(limit)
    )
    return result.scalars().all()

# Get alerts by facility (paginated)
async def get_alerts_by_facility(db: AsyncSession, facility_id: str, skip: int = 0, limit: int = 50):
    result = await db.execute(
        select(Alert)
        .where(Alert.facility_id == facility_id)
        .order_by(Alert.triggered_at.desc())
        .offset(skip).limit(limit)
    )
    return result.scalars().all()

# Get all facilities with device count + active alert count
async def get_facilities_summary(db: AsyncSession):
    facilities = (await db.execute(select(Facility).where(Facility.is_active == True))).scalars().all()
    result = []
    for f in facilities:
        device_count = (await db.execute(
            select(func.count()).where(Device.facility_id == f.id)
        )).scalar()
        active_alerts = (await db.execute(
            select(func.count()).where(Alert.facility_id == f.id, Alert.status == "triggered")
        )).scalar()
        result.append({
            "id": f.id,
            "name": f.name,
            "type": f.type,
            "tier": f.tier,
            "location": f.location,
            "device_count": device_count,
            "active_alert_count": active_alerts,
        })
    return result