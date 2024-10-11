from sqlalchemy.orm import Session
from app.models import Device, DeviceLocation


def list_devices(db: Session):
    return db.query(Device).all()


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
