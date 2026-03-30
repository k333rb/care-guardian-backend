"""
Router for alert management.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Header, Path
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.database import get_db
from app.crud import get_alerts, resolve_alert
from app.schemas.alerts import AlertResponse
from app.config import get_settings

router = APIRouter(prefix="/alerts", tags=["Alerts"])
settings = get_settings()


def get_facility_id(
    facility_id_header: str | None = Header(None, alias="X-Facility-ID"),
    facility_id_query: str | None = Query(None, alias="facility_id"),
) -> str:
    """
    Extract facility_id from header (priority) or query param, with fallback to default.
    
    Header takes precedence: X-Facility-ID > query param > default
    """
    return facility_id_header or facility_id_query or settings.default_facility_id


@router.get("", response_model=list[AlertResponse])
async def list_alerts(
    facility_id: str = Depends(get_facility_id),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(50, ge=1, le=100, description="Pagination limit"),
    start_date: datetime | None = Query(None, description="Filter: alerts on or after this date (ISO 8601)"),
    end_date: datetime | None = Query(None, description="Filter: alerts on or before this date (ISO 8601)"),
    session: AsyncSession = Depends(get_db),
):
    """
    Get alerts for a facility with optional date range filtering.
    
    - **X-Facility-ID** (header): Facility filter (priority over query)
    - **facility_id** (query): Alternative facility filter
    - **start_date**: ISO 8601 datetime (e.g., 2026-03-30T10:00:00)
    - **end_date**: ISO 8601 datetime (e.g., 2026-03-30T18:00:00)
    - **skip**: Pagination offset
    - **limit**: Pagination limit (max 100)
    """
    alerts = await get_alerts(
        session=session,
        facility_id=facility_id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )
    
    return alerts


@router.patch("/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert_endpoint(
    alert_id: str = Path(..., description="Alert ID to resolve"),
    session: AsyncSession = Depends(get_db),
):
    """
    Resolve an alert by setting status to 'resolved'.
    """
    result = await resolve_alert(session=session, alert_id=alert_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    await session.commit()
    return result
