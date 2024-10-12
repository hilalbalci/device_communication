from typing import List

from sqlalchemy.orm import Session

from app.crud import create_device as crud_create_device
from app.crud import get_device as crud_get_device
from app.crud import get_last_location_by_device
from app.crud import list_devices as crud_list_devices
from app.database import SessionLocal
from app.models import Device, DeviceLocation


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


def create_device(name, description):
    db: Session = SessionLocal()
    try:
        device = crud_create_device(name, description, db)
        return Device(id=device.id)
    finally:
        db.close()


def list_locations() -> List:
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
