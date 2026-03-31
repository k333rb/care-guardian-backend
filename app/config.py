from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    All configuration is read from environment variables.
    Never hardcode values here — put them in .env locally,
    and in GitHub Secrets / Supabase env for production.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ───────────────────────────────────────────
    app_name: str = "CareGuardian"
    app_version: str = "0.1.0"
    trl_level: str = "TRL4-prototype"
    debug: bool = False

    # ── Database (Supabase) ───────────────────────────
    database_url: str 

    # ── Detection ─────────────────────────────────────
    fall_confidence_threshold: float = 0.75

    # ── Multi-tenant ──────────────────────────────────
    facility_id_header: str = "X-Facility-ID"
    default_facility_id: str = "fac-butuan-medical-center"

    # ── Alerts / Zavu ──────────────────────────────────d
    sms_enabled: bool = False
    sms_api_key: str = ""
    sms_sender_name: str = "CareGuardian"
    zavu_api_key: str = ""
    zavu_enabled: bool = False
    default_test_phone: str = ""

    # ── Camera ────────────────────────────────────────
    camera_source: str = "0"
    frame_interval_ms: int = 200
    default_device_id: str = ""
    api_url: str = "http://127.0.0.1:8000"
    
    # ── CORS ──────────────────────────────────────────
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """
    Cached singleton — settings are loaded once at startup.
    Use: from app.config import get_settings; settings = get_settings()
    """
    return Settings()