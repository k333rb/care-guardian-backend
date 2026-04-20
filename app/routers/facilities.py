"""
Router for facility management.
"""
from fastapi import APIRouter, Depends, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import get_facilities_summary, get_facility_summary
from app.schemas.facilities import FacilitySummaryResponse
from app.config import get_settings

router = APIRouter(prefix="/facilities", tags=["Facilities"])
settings = get_settings()


def get_facility_id_optional(
    facility_id_header: str | None = Header(None, alias="X-Facility-ID"),
    facility_id_query: str | None = Query(None, alias="facility_id"),
) -> str | None:
    """
    Extract optional facility_id from header or query param.
    
    Header takes precedence: X-Facility-ID > query param > None (get all)
    """
    return facility_id_header or facility_id_query


@router.get("", response_model=list[FacilitySummaryResponse])
async def list_facilities(
    facility_id: str | None = Depends(get_facility_id_optional),
    session: AsyncSession = Depends(get_db),
):
    """
    Get summary of all facilities with device count and active alert count.
    
    - **X-Facility-ID** (header): Optional filter for single facility (priority)
    - **facility_id** (query): Alternative facility filter
    - Returns all facilities if no filter provided
    """
    summaries = await get_facilities_summary(db=session)
    
    return summaries


@router.get("/{facility_id}/summary")
async def facility_summary(
    facility_id: str,
    session: AsyncSession = Depends(get_db),
):
    """
    Get detailed summary for a specific facility including event stats and alert metrics.
    """
    return await get_facility_summary(db=session, facility_id=facility_id)
