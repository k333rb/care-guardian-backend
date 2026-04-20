import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

FACILITY_ID = "070ca250-08ea-4239-8115-63e531caeb14"
HEADERS = {"X-Facility-ID": FACILITY_ID}


@pytest.mark.asyncio
async def test_get_facilities_returns_200():
    """GET /facilities should return 200 with a list."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/facilities")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_facilities_have_required_fields():
    """Each facility in response should have id, name, device_count, active_alert_count."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/facilities")

    assert response.status_code == 200
    data = response.json()

    if len(data) > 0:
        facility = data[0]
        assert "id" in facility
        assert "name" in facility
        assert "device_count" in facility
        assert "active_alert_count" in facility


@pytest.mark.asyncio
async def test_health_check():
    """GET /health should return ok status."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "trl_level" in data