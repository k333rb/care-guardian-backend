import pytest
import base64
import numpy as np
import cv2
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.detection_service import DetectionResult

# ── Helpers ──────────────────────────────────────────────────────────────────

FACILITY_ID = "070ca250-08ea-4239-8115-63e531caeb14"
DEVICE_ID = "0a8c092a-2897-4a8a-8be1-21a171640f20"

def make_base64_image() -> str:
    """Generate a real 10x10 black JPEG as base64."""
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    _, buf = cv2.imencode(".jpg", img)
    return base64.b64encode(buf).decode("utf-8")

PAYLOAD = {
    "image_base64": make_base64_image(),
    "device_id": DEVICE_ID,
    "frame_ts": "2026-03-31T00:00:00Z",
}

HEADERS = {"X-Facility-ID": FACILITY_ID}

# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_detect_standing_returns_200():
    """Standing frame: 200, event logged, alert_triggered=False."""
    with patch("app.routers.detection.run_detection") as mock_detect:
        mock_detect.return_value = DetectionResult(label="standing", confidence=0.85)

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/detect-frame", headers=HEADERS, json=PAYLOAD
            )

    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "standing"
    assert data["alert_triggered"] is False
    assert data["event_id"] is not None
    assert data["monitoring_type"] == "camera_ai"
    assert 0.0 <= data["confidence"] <= 1.0


@pytest.mark.asyncio
async def test_detect_fall_triggers_alert():
    """Fall frame: 200, event logged, alert_triggered=True."""
    with patch("app.routers.detection.run_detection") as mock_detect, \
         patch("app.routers.detection.notify", new_callable=AsyncMock) as mock_notify:
        mock_detect.return_value = DetectionResult(label="fall", confidence=0.92)
        mock_notify.return_value = "app"

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/detect-frame", headers=HEADERS, json=PAYLOAD
            )

    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "fall"
    assert data["alert_triggered"] is True
    assert data["event_id"] is not None


@pytest.mark.asyncio
async def test_missing_facility_header_returns_422():
    """Missing X-Facility-ID header should return 422."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/detect-frame",
            # no X-Facility-ID header
            json=PAYLOAD,
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_base64_returns_422():
    """Garbage base64 should return 422."""
    bad_payload = {**PAYLOAD, "image_base64": "not_valid_base64!!!"}

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/detect-frame", headers=HEADERS, json=bad_payload
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_device_id_returns_422():
    """Missing device_id should return 422."""
    bad_payload = {
        "image_base64": make_base64_image(),
        "frame_ts": "2026-03-31T00:00:00Z",
        # no device_id
    }

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/detect-frame", headers=HEADERS, json=bad_payload
        )

    assert response.status_code == 422