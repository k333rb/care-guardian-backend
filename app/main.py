from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import get_settings
from app.database import engine, Base

# Routers
from app.routers import events_router, alerts_router, facilities_router
from app.routers import detection
from app.routers import ws

import app.models

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup — create all tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print(f"✅ {settings.app_name} v{settings.app_version} | {settings.trl_level}")
    yield

    # Shutdown — dispose connection pool cleanly
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered fall detection — wearable-free, non-intrusive.",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(events_router)
app.include_router(alerts_router)
app.include_router(facilities_router)
app.include_router(detection.router)

app.include_router(ws.router)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc), "code": "validation_error"}
    )


# Health check
@app.get("/health", tags=["Health Check"])
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "trl_level": settings.trl_level,
    }