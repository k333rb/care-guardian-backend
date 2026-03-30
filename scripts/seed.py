import asyncio
import uuid
from app.database import AsyncSessionLocal
from app.models.facility import Facility
from app.models.device import Device

async def seed():
    async with AsyncSessionLocal() as session:
        # Seed Facility
        facility = Facility(
            id=str(uuid.uuid4()),
            name="Butuan Medical Center",
            type="hospital",
            tier="b2b_medium",
            location="Butuan City, Agusan del Norte",
            contact_person="Admin",
            is_active=True
        )
        session.add(facility)
        await session.flush()

        # Seed 2 devices
        devices = [
            Device(
                id=str(uuid.uuid4()),
                facility_id=facility.id,
                name="Ward A Camera",
                stream_type="webcam",
                source_url="0",
                is_active=True
            ),
            Device(
                id=str(uuid.uuid4()),
                facility_id=facility.id,
                name="Hallway Camera",
                stream_type="ip_camera",
                source_url="rtsp://192.168.1.100/stream",
                is_active=True
            )
        ]
        session.add_all(devices)
        await session.commit()

        print(f"✅ Seeded facility: {facility.name}")
        print(f"✅ Seeded {len(devices)} devices")
        print(f"   facility_id to share with Noralf: {facility.id}")

if __name__ == "__main__":
    asyncio.run(seed())