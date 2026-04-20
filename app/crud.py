from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.event import Event
from app.models.alert import Alert
from app.models.household import Household
from app.models.device import Device
from app.models.user import User
import uuid
from datetime import datetime, timezone
from typing import Optional


# Events

async def create_event(
    db: AsyncSession,
    device_id: str,
    type: str,
    confidence_score: float,
    timestamp: datetime,
):
    event = Event(
        id=f"evt-{uuid.uuid4()}",
        device_id=device_id,
        type=type,
        confidence_score=confidence_score,
        monitoring_type="camera_ai",
        timestamp=timestamp,
    )
    db.add(event)
    await db.flush()
    return event


async def get_events_by_household(
    db: AsyncSession,
    household_id: str,
    skip: int = 0,
    limit: int = 50,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    q = (
        select(Event)
        .join(Device, Device.id == Event.device_id)
        .where(Device.household_id == household_id)
        .order_by(Event.timestamp.desc())
    )
    if start_date:
        q = q.where(Event.timestamp >= start_date)
    if end_date:
        q = q.where(Event.timestamp <= end_date)

    result = await db.execute(q.offset(skip).limit(limit))
    return result.scalars().all()


# Alerts

async def create_alert(
    db: AsyncSession,
    event_id: str,
    user_id: str,
    delivery_method: str = "app",
):
    alert = Alert(
        id=f"alrt-{uuid.uuid4()}",
        event_id=event_id,
        user_id=user_id,
        status="sent",
        delivery_method=delivery_method,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(alert)
    await db.flush()
    return alert

<<<<<<< HEAD
# Resolve alert
async def resolve_alert(db: AsyncSession, alert_id: str):
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        return None
    alert.status = "resolved"
    alert.resolved_at = datetime.now(timezone.utc)
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
=======
>>>>>>> feature/khervee-tests

async def get_alerts_by_household(
    db: AsyncSession,
    household_id: str,
    skip: int = 0,
    limit: int = 50,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    q = (
        select(Alert)
        .join(Event, Event.id == Alert.event_id)
        .join(Device, Device.id == Event.device_id)
        .where(Device.household_id == household_id)
        .order_by(Alert.timestamp.desc())
    )
    if start_date:
        q = q.where(Alert.timestamp >= start_date)
    if end_date:
        q = q.where(Alert.timestamp <= end_date)

    result = await db.execute(q.offset(skip).limit(limit))
    return result.scalars().all()


async def resolve_alert(db: AsyncSession, alert_id: str):
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    if alert:
        alert.status = "resolved"
        alert.resolved_at = datetime.now(timezone.utc)
        await db.flush()
    return alert


async def get_alert_by_id(db: AsyncSession, alert_id: str):
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    return result.scalar_one_or_none()


# Households

async def get_households_summary(db: AsyncSession):
    households = (
        await db.execute(select(Household))
    ).scalars().all()

    result = []
    for h in households:
        device_count = (
            await db.execute(
                select(func.count(Device.id)).where(Device.household_id == h.id)
            )
        ).scalar()

        active_alerts = (
            await db.execute(
                select(func.count(Alert.id))
                .join(Event, Event.id == Alert.event_id)
                .join(Device, Device.id == Event.device_id)
                .where(Device.household_id == h.id, Alert.status == "sent")
            )
        ).scalar()

        result.append({
            "id": h.id,
            "address": h.address,
            "latitude": h.latitude,
            "longitude": h.longitude,
            "device_count": device_count,
            "active_alert_count": active_alerts,
        })
<<<<<<< HEAD
    
    return result

# Get single facility summary with stats
async def get_facility_summary(db: AsyncSession, facility_id: str):
    total_events = (await db.execute(
        select(func.count()).where(DetectionEvent.facility_id == facility_id)
    )).scalar()
    fall_count = (await db.execute(
        select(func.count()).where(
            DetectionEvent.facility_id == facility_id,
            DetectionEvent.label == "fall"
        )
    )).scalar()
    avg_confidence = (await db.execute(
        select(func.avg(DetectionEvent.confidence))
        .where(DetectionEvent.facility_id == facility_id)
    )).scalar() or 0.0
    alert_count = (await db.execute(
        select(func.count()).where(Alert.facility_id == facility_id)
    )).scalar()
    return {
        "facility_id": facility_id,
        "total_events": total_events,
        "fall_count": fall_count,
        "alert_rate": round(fall_count / total_events, 2) if total_events else 0.0,
        "avg_confidence": round(avg_confidence, 4),
        "active_alerts": alert_count,
    }
=======
    return result


# Users

async def get_users_by_household(db: AsyncSession, household_id: str):
    from app.models.household_user import HouseholdUser
    result = await db.execute(
        select(User)
        .join(HouseholdUser, HouseholdUser.user_id == User.id)
        .where(HouseholdUser.household_id == household_id)
    )
    return result.scalars().all()
>>>>>>> feature/khervee-tests
