from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Device, DeviceLocation


def list_devices(db: Session):
    return db.query(Device).all()


def get_device(device_id: int, db: Session):
    return db.query(Device).filter(Device.id == device_id).first()


def create_device(name: str, description, db: Session):
    device = Device(name=name, description=description)
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


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


def get_last_location_by_device(db: Session):
    subquery = (
        db.query(
            DeviceLocation.device_id,
            DeviceLocation.latitude,
            DeviceLocation.longitude,
            DeviceLocation.timestamp
        )
            .order_by(DeviceLocation.device_id, DeviceLocation.timestamp.desc())
            .distinct(DeviceLocation.device_id)
            .subquery()
    )

    return db.query(subquery).all()


def save_location_data(location_data):
    from app.main import logger
    db: Session = SessionLocal()
    device = db.query(Device).filter_by(id=int(location_data['device_id'])).one_or_none()
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
