from app.routers.events import router as events_router
from app.routers.alerts import router as alerts_router
from app.routers.facilities import router as facilities_router

__all__ = ["events_router", "alerts_router", "facilities_router"]
