from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Device, DeviceLocation


def list_devices(db: Session):
    return db.query(Device).filter(Device.is_deleted == False).all()


def get_device(device_id: int, db: Session):
    return db.query(Device).filter(Device.id == device_id, Device.is_deleted == False).first()


def create_device(name: str, description, db: Session):
    device = Device(name=name, description=description)
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def delete_device(device_id: int, db: Session):
    device = db.query(Device).filter(Device.id == device_id, Device.is_deleted == False).first()
    if not device:
        return False
    device.soft_delete(db)
    return True


def get_location_history_by_device(device_id: int, db: Session):
    subquery = (
        db.query(
            DeviceLocation.device_id,
            DeviceLocation.latitude,
            DeviceLocation.longitude,
            DeviceLocation.timestamp
        )
            .filter(DeviceLocation.device_id == device_id)
            .order_by(DeviceLocation.timestamp.desc())
            .subquery()
    )

    return db.query(subquery).all()


def get_last_location_of_every_device(db: Session):
    subquery = (
        db.query(
            DeviceLocation.device_id,
            DeviceLocation.latitude,
            DeviceLocation.longitude,
            DeviceLocation.timestamp
        )
            .join(Device, Device.id == DeviceLocation.device_id)
            .filter(Device.is_deleted == False)
            .order_by(DeviceLocation.device_id, DeviceLocation.timestamp.desc())
            .distinct(DeviceLocation.device_id)
            .subquery()
    )

    results = db.query(
        subquery.c.device_id,
        subquery.c.latitude,
        subquery.c.longitude,
        subquery.c.timestamp
    ).all()

    return [
        {
            "deviceId": device_id,
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": timestamp
        }
        for device_id, latitude, longitude, timestamp in results
    ]


def save_location_data(location_data):
    from app.main import logger
    db: Session = SessionLocal()
    device = db.query(Device).filter_by(id=int(location_data['device_id']), is_deleted=False).one_or_none()
    if device:
        device_location = DeviceLocation(device_id=int(location_data['device_id']),
                                         latitude=float(location_data['latitude']),
                                         longitude=float(location_data['longitude']))
        db.add(device_location)
        db.commit()
        db.refresh(device_location)
        return device_location
    else:
        logger.error(f"Device with id {location_data['device_id']} doesnt exist.")


def list_location_by_device(device_id: int, db: Session):
    locations = db.query(
        DeviceLocation.device_id,
        DeviceLocation.latitude,
        DeviceLocation.longitude,
        DeviceLocation.timestamp
    ).join(Device, Device.id == device_id).filter(Device.is_deleted == False, DeviceLocation.device_id == device_id) \
        .order_by(DeviceLocation.timestamp.desc()).all()

    return [
        {
            "deviceId": device_id,
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": timestamp
        }
        for device_id, latitude, longitude, timestamp in locations
    ]
