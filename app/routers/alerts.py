from fastapi import APIRouter, Depends, HTTPException, Query, Header, Path
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.crud import get_alerts_by_household, resolve_alert, get_alert_by_id
from app.config import get_settings

router = APIRouter(prefix="/alerts", tags=["Alerts"])
settings = get_settings()


def get_household_id(
    household_id_header: Optional[str] = Header(None, alias="X-Household-ID"),
    household_id_query: Optional[str] = Query(None, alias="household_id"),
) -> str:
    return household_id_header or household_id_query or settings.default_facility_id


@router.get("", response_model=list[dict])
async def list_alerts(
    household_id: str = Depends(get_household_id),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    session: AsyncSession = Depends(get_db),
):
    """
    Get alerts for a household.
    Pass household_id as query param or X-Household-ID header.
    """
    alerts = await get_alerts_by_household(
        db=session,
        household_id=household_id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )
    return [
        {
            "id": a.id,
            "event_id": a.event_id,
            "user_id": a.user_id,
            "status": a.status,
            "delivery_method": a.delivery_method,
            "timestamp": a.timestamp,
            "resolved_at": a.resolved_at,
        }
        for a in alerts
    ]


@router.patch("/{alert_id}/resolve", response_model=dict)
async def resolve_alert_endpoint(
    alert_id: str = Path(..., description="Alert ID to resolve"),
    session: AsyncSession = Depends(get_db),
):
    """
    Resolve an alert — status moves from sent/seen → resolved.
    """
    alert = await resolve_alert(db=session, alert_id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {
        "id": alert.id,
        "event_id": alert.event_id,
        "user_id": alert.user_id,
        "status": alert.status,
        "delivery_method": alert.delivery_method,
        "timestamp": alert.timestamp,
        "resolved_at": alert.resolved_at,
    }