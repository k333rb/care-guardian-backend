"""
CRUD operations for facilities, devices, alerts, and events.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime
from app.models import Facility, Device, Alert, Event
from app.schemas.facilities import FacilitySummaryResponse
from app.schemas.alerts import AlertResponse


async def get_facilities_summary(
    session: AsyncSession,
    facility_id: str | None = None
) -> list[FacilitySummaryResponse]:
    """
    Get summary of facilities with device count and active alert count.
    
    Args:
        session: Database session
        facility_id: Optional filter to single facility
        
    Returns:
        List of FacilitySummaryResponse objects
    """
    # Subquery: count devices per facility
    device_count_subq = (
        select(
            Device.facility_id,
            func.count(Device.id).label("device_count")
        )
        .group_by(Device.facility_id)
        .subquery()
    )
    
    # Subquery: count active alerts per facility
    alert_count_subq = (
        select(
            Alert.facility_id,
            func.count(Alert.id).label("alert_count")
        )
        .where(Alert.status == "active")
        .group_by(Alert.facility_id)
        .subquery()
    )
    
    # Main query: join and fetch facilities
    query = select(Facility).outerjoin(device_count_subq, Facility.id == device_count_subq.c.facility_id)
    
    if facility_id:
        query = query.where(Facility.id == facility_id)
    
    result = await session.execute(query)
    facilities = result.scalars().unique().all()
    
    # Build summaries with subquery data
    summaries = []
    for facility in facilities:
        # Count devices
        dev_stmt = select(func.count(Device.id)).where(Device.facility_id == facility.id)
        dev_count = await session.execute(dev_stmt)
        device_count = dev_count.scalar() or 0
        
        # Count active alerts
        alert_stmt = select(func.count(Alert.id)).where(
            and_(Alert.facility_id == facility.id, Alert.status == "active")
        )
        alert_count_result = await session.execute(alert_stmt)
        alert_count = alert_count_result.scalar() or 0
        
        summaries.append(FacilitySummaryResponse(
            id=facility.id,
            name=facility.name,
            device_count=device_count,
            active_alert_count=alert_count,
        ))
    
    return summaries


async def get_alerts(
    session: AsyncSession,
    facility_id: str,
    skip: int = 0,
    limit: int = 50,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[AlertResponse]:
    """
    Get alerts for a facility with pagination and date range filtering.
    
    Args:
        session: Database session
        facility_id: Filter by facility
        skip: Pagination offset
        limit: Pagination limit (max 100)
        start_date: Optional filter: only alerts on or after this date
        end_date: Optional filter: only alerts on or before this date
        
    Returns:
        List of AlertResponse objects
    """
    limit = min(limit, 100)  # Cap at 100
    
    # Build where clause with optional date range
    where_conditions = [Alert.facility_id == facility_id]
    if start_date:
        where_conditions.append(Alert.triggered_at >= start_date)
    if end_date:
        where_conditions.append(Alert.triggered_at <= end_date)
    
    stmt = (
        select(Alert)
        .where(and_(*where_conditions))
        .order_by(Alert.triggered_at.desc())
        .offset(skip)
        .limit(limit)
    )
    
    result = await session.execute(stmt)
    alerts = result.scalars().all()
    
    return [
        AlertResponse(
            id=alert.id,
            facility_id=alert.facility_id,
            device_id=alert.device_id,
            status=alert.status,
            confidence=alert.confidence,
            delivery_method=alert.delivery_method,
            triggered_at=alert.triggered_at,
        )
        for alert in alerts
    ]


async def get_events(
    session: AsyncSession,
    facility_id: str,
    skip: int = 0,
    limit: int = 50,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[dict]:
    """
    Get detection events for a facility with pagination and date range filtering.
    
    Args:
        session: Database session
        facility_id: Filter by facility
        skip: Pagination offset
        limit: Pagination limit (max 100)
        start_date: Optional filter: only events on or after this date
        end_date: Optional filter: only events on or before this date
        
    Returns:
        List of event dicts with label, confidence, device_id, timestamp
    """
    limit = min(limit, 100)  # Cap at 100
    
    # Build where clause with optional date range
    where_conditions = [Event.facility_id == facility_id]
    if start_date:
        where_conditions.append(Event.timestamp >= start_date)
    if end_date:
        where_conditions.append(Event.timestamp <= end_date)
    
    stmt = (
        select(Event)
        .where(and_(*where_conditions))
        .order_by(Event.timestamp.desc())
        .offset(skip)
        .limit(limit)
    )
    
    result = await session.execute(stmt)
    events = result.scalars().all()
    
    return [
        {
            "id": event.id,
            "facility_id": event.facility_id,
            "device_id": event.device_id,
            "label": event.label,
            "confidence": event.confidence,
            "timestamp": event.timestamp,
        }
        for event in events
    ]


async def resolve_alert(
    session: AsyncSession,
    alert_id: str,
) -> AlertResponse | None:
    """
    Resolve an alert by setting status to 'resolved' and resolved_at timestamp.
    
    Args:
        session: Database session
        alert_id: Alert to resolve
        
    Returns:
        Updated AlertResponse, or None if alert not found
    """
    stmt = select(Alert).where(Alert.id == alert_id)
    result = await session.execute(stmt)
    alert = result.scalar_one_or_none()
    
    if not alert:
        return None
    
    alert.status = "resolved"
    alert.resolved_at = datetime.utcnow()
    
    await session.flush()  # Ensure changes are visible
    
    return AlertResponse(
        id=alert.id,
        facility_id=alert.facility_id,
        device_id=alert.device_id,
        status=alert.status,
        confidence=alert.confidence,
        delivery_method=alert.delivery_method,
        triggered_at=alert.triggered_at,
    )
