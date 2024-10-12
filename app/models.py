from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, Session

from app.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    locations = relationship("DeviceLocation", back_populates="device", cascade="all, delete-orphan")
    is_deleted = Column(Boolean, default=False)

    def soft_delete(self, session: Session):
        self.is_deleted = True
        session.commit()


class DeviceLocation(Base):
    __tablename__ = "device_locations"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device", back_populates="locations")
