from typing import List
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import list_devices as crud_list_devices, get_last_location_by_device, get_device as crud_get_device
from app.models import DeviceLocation, Device


def list_devices() -> List:
    db: Session = SessionLocal()
    try:
        devices = crud_list_devices(db)
        return [DeviceLocation(id=device.id, name=device.name) for device in devices]
    finally:
        db.close()


def get_device(device_id: int) -> Device:
    db: Session = SessionLocal()
    try:
        device = crud_get_device(device_id, db)
        return Device(id=device.id)
    finally:
        db.close()


def create_device():
    pass


def get_last_location() -> List:
    db: Session = SessionLocal()
    try:
        locations = get_last_location_by_device(db)
        return [
            DeviceLocation(
                latitude=loc.latitude,
                longitude=loc.longitude,
                timestamp=loc.timestamp
            )
            for loc in locations
        ]
    finally:
        db.close()
