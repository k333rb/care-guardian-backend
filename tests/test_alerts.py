import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from app.main import app

FACILITY_ID = "070ca250-08ea-4239-8115-63e531caeb14"
HEADERS = {"X-Facility-ID": FACILITY_ID}


@pytest.mark.asyncio
async def test_get_alerts_returns_200():
    """GET /alerts should return 200 with a list."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/alerts", headers=HEADERS)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_alerts_without_facility_uses_default():
    """GET /alerts with no header should fall back to default facility."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/alerts")

    # should still return 200 with default facility fallback
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_alerts_pagination():
    """GET /alerts should respect skip and limit query params."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/alerts", headers=HEADERS, params={"skip": 0, "limit": 5}
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5