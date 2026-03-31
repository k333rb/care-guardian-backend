import cv2
import base64
import httpx
import asyncio
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
DEVICE_ID = os.getenv("DEFAULT_DEVICE_ID")
FACILITY_ID = os.getenv("DEFAULT_FACILITY_ID")
FRAME_INTERVAL = float(os.getenv("FRAME_INTERVAL_MS", "200")) / 1000
SOURCE = os.getenv("CAMERA_SOURCE", "0")  # "0" = webcam, or RTSP/HTTP URL

def get_source():
    # if numeric string, use as int (webcam index)
    return int(SOURCE) if SOURCE.isdigit() else SOURCE

async def send_frame(client: httpx.AsyncClient, image_b64: str):
    response = await client.post(
        f"{API_URL}/detect-frame",
        headers={"X-Facility-ID": FACILITY_ID},
        json={
            "image_base64": image_b64,
            "device_id": DEVICE_ID,
            "frame_ts": datetime.now(timezone.utc).isoformat(),
        }
    )
    result = response.json()
    print(f"[{result.get('label')}] confidence={result.get('confidence'):.2f} alert={result.get('alert_triggered')}")

async def main():
    cap = cv2.VideoCapture(get_source())
    if not cap.isOpened():
        print("❌ Could not open camera source")
        return

    print(f"✅ frame_producer running | device={DEVICE_ID} | facility={FACILITY_ID}")

    async with httpx.AsyncClient() as client:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Frame read failed, retrying...")
                await asyncio.sleep(1)
                continue

            _, buffer = cv2.imencode(".jpg", frame)
            image_b64 = base64.b64encode(buffer).decode("utf-8")

            try:
                await send_frame(client, image_b64)
            except Exception as e:
                print(f"⚠️ Send failed: {e}")

            await asyncio.sleep(FRAME_INTERVAL)

    cap.release()

if __name__ == "__main__":
    asyncio.run(main())
