"""
Router for detection events.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.database import get_db
from app.crud import get_events
from app.config import get_settings

router = APIRouter(prefix="/events", tags=["Events"])
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


@router.get("", response_model=list[dict])
async def list_events(
    facility_id: str = Depends(get_facility_id),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(50, ge=1, le=100, description="Pagination limit"),
    start_date: datetime | None = Query(None, description="Filter: events on or after this date (ISO 8601)"),
    end_date: datetime | None = Query(None, description="Filter: events on or before this date (ISO 8601)"),
    session: AsyncSession = Depends(get_db),
):
    """
    Get detection events for a facility with optional date range.
    
    - **X-Facility-ID** (header): Facility filter (priority over query)
    - **facility_id** (query): Alternative facility filter
    - **start_date**: ISO 8601 datetime (e.g., 2026-03-30T10:00:00)
    - **end_date**: ISO 8601 datetime (e.g., 2026-03-30T18:00:00)
    - **skip**: Pagination offset
    - **limit**: Pagination limit (max 100)
    """
    events = await get_events(
        session=session,
        facility_id=facility_id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )
    
    return events
