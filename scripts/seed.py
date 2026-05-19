import asyncio
import uuid
from app.database import AsyncSessionLocal
from app.models.household import Household
from app.models.user import User
from app.models.household_user import HouseholdUser
from app.models.device import Device
from app.models.facility import Facility
from app.models.household_facility import HouseholdFacility


async def seed():
    async with AsyncSessionLocal() as session:

        # Household
        household = Household(
            id=f"hh-{uuid.uuid4()}",
            address="123 Rizal Street, Butuan City, Agusan del Norte",
            latitude=8.9475,
            longitude=125.5406,
        )
        session.add(household)
        await session.flush()

        # Users
        users = [
            User(
                id=f"usr-{uuid.uuid4()}",
                name="Juan dela Cruz",
                role="family",
                email="juan@example.com",
                phone="09171234567",
            ),
            User(
                id=f"usr-{uuid.uuid4()}",
                name="Maria Santos",
                role="caregiver",
                email="maria@example.com",
                phone="09189876543",
            ),
        ]
        session.add_all(users)
        await session.flush()

        # Household Users (join table)
        household_users = [
            HouseholdUser(
                id=f"hhu-{uuid.uuid4()}",
                household_id=household.id,
                user_id=u.id,
            )
            for u in users
        ]
        session.add_all(household_users)
        await session.flush()

        # Devices
        devices = [
            Device(
                id=f"dev-{uuid.uuid4()}",
                household_id=household.id,
                device_name="Living Room Camera",
                stream_type="webcam",
                source_url="0",
                status="active",
            ),
            Device(
                id=f"dev-{uuid.uuid4()}",
                household_id=household.id,
                device_name="Hallway Camera",
                stream_type="rtsp",
                source_url="rtsp://192.168.1.100/stream",
                status="active",
            ),
        ]
        session.add_all(devices)
        await session.flush()

        # Nearby Facility
        facility = Facility(
            id=f"fac-{uuid.uuid4()}",
            name="Butuan Medical Center",
            type="hospital",
            latitude=8.9500,
            longitude=125.5430,
        )
        session.add(facility)
        await session.flush()

        # Household Facility link
        household_facility = HouseholdFacility(
            id=f"hhf-{uuid.uuid4()}",
            household_id=household.id,
            facility_id=facility.id,
            distance=0.35,  # km — precomputed
        )
        session.add(household_facility)

        await session.commit()

        # Summary
        print(f"✅ Seeded household : {household.address}")
        print(f"✅ Seeded users     : {[u.name for u in users]}")
        print(f"✅ Seeded devices   : {[d.device_name for d in devices]}")
        print(f"✅ Seeded facility  : {facility.name}")
        print(f"")
        print(f"   household_id : {household.id}")
        print(f"   user_id (Juan)  : {users[0].id}")
        print(f"   user_id (Maria) : {users[1].id}")
        print(f"   device_id (Living Room) : {devices[0].id}")
        print(f"   device_id (Hallway)     : {devices[1].id}")


if __name__ == "__main__":
    asyncio.run(seed())