from zavudev import Zavudev
from app.config import get_settings

settings = get_settings()

async def notify(alert, recipient_phone: str) -> str:
    if not settings.zavu_enabled:
        # stub — log only, no real send
        print(f"[STUB] Alert notify → {recipient_phone} | facility: {alert.facility_id}")
        return "app"

    zavu = Zavudev(api_key=settings.zavu_api_key)
    result = zavu.messages.send({
        "to": recipient_phone,
        "text": (
            f"⚠️ CareGuardian Alert\n"
            f"Fall detected at facility {alert.facility_id}.\n"
            f"Confidence: {alert.confidence:.0%}\n"
            f"Time: {alert.triggered_at}"
        ),
        # no channel = Zavu auto-picks WhatsApp or SMS
    })

    # returns "whatsapp" or "sms" — log which was used
    return result.message.channel