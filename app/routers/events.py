from fastapi import APIRouter, Depends, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.crud import get_events_by_household
from app.config import get_settings

router = APIRouter(prefix="/events", tags=["Events"])
settings = get_settings()


def get_household_id(
    household_id_header: Optional[str] = Header(None, alias="X-Household-ID"),
    household_id_query: Optional[str] = Query(None, alias="household_id"),
) -> str:
    return household_id_header or household_id_query or settings.default_facility_id


@router.get("", response_model=list[dict])
async def list_events(
    household_id: str = Depends(get_household_id),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    session: AsyncSession = Depends(get_db),
):
    """
    Get detection events for a household.
    Pass household_id as query param or X-Household-ID header.
    """
    events = await get_events_by_household(
        db=session,
        household_id=household_id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )
    return [
        {
            "id": e.id,
            "device_id": e.device_id,
            "type": e.type,
            "confidence_score": e.confidence_score,
            "monitoring_type": e.monitoring_type,
            "timestamp": e.timestamp,
            "created_at": e.created_at,
        }
        for e in events
    ]