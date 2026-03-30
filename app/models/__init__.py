from sqlalchemy import Column, String, Float, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base


class Facility(Base):
    """Multi-tenant facility model."""
    __tablename__ = "facilities"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    name = Column(String, nullable=False, index=True)
    
    # Relationships
    devices = relationship("Device", back_populates="facility", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="facility", cascade="all, delete-orphan")


class Device(Base):
    """Camera/monitoring device model."""
    __tablename__ = "devices"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    facility_id = Column(String, ForeignKey("facilities.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    location = Column(String)  # e.g., "Room 101", "Hallway A"
    
    # Relationships
    facility = relationship("Facility", back_populates="devices")
    events = relationship("Event", back_populates="device", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="device", cascade="all, delete-orphan")


class Event(Base):
    """Detection event (fall/activity detection)."""
    __tablename__ = "events"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    facility_id = Column(String, ForeignKey("facilities.id"), nullable=False, index=True)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False, index=True)
    label = Column(String, nullable=False)  # 'fall', 'standing', etc.
    confidence = Column(Float, nullable=False)  # 0.0 - 1.0
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Relationships
    device = relationship("Device", back_populates="events")
    alerts = relationship("Alert", back_populates="event", cascade="all, delete-orphan")


class Alert(Base):
    """Alert triggered by detection event."""
    __tablename__ = "alerts"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    facility_id = Column(String, ForeignKey("facilities.id"), nullable=False, index=True)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False, index=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=True, index=True)
    status = Column(
        String,
        nullable=False,
        default="active",
        index=True,
    )  # 'active', 'acknowledged', 'resolved'
    confidence = Column(Float, nullable=False)  # confidence from triggering event
    delivery_method = Column(String)  # 'sms', 'push', 'dashboard', etc.
    triggered_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    resolved_at = Column(DateTime)
    
    # Relationships
    facility = relationship("Facility", back_populates="alerts")
    device = relationship("Device", back_populates="alerts")
    event = relationship("Event", back_populates="alerts")
