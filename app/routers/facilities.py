"""
Router for household and facility management.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import get_households_summary

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("", response_model=list[dict])
async def list_households_summary(
    session: AsyncSession = Depends(get_db),
):
    """
    Get summary of all households with device count and active alert count.
    """
    return await get_households_summary(db=session)