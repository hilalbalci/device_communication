import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.crud import get_last_location_of_every_device
from app.database import Base, get_db
from app.main import app
from app.models import Device, DeviceLocation

client = TestClient(app)

SQLITE_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()


app.dependency_overrides[get_db] = override_get_db


def add_test_data(db):
    device1 = Device(name="Test Device 1", description="This is a test device.")
    device2 = Device(name="Test Device 2", description="This is another test device.")

    db.add(device1)
    db.add(device2)
    db.commit()

    location1 = DeviceLocation(device_id=device1.id, latitude=42.7128, longitude=-73.0060)
    location2 = DeviceLocation(device_id=device1.id, latitude=43.7128, longitude=-74.0060)
    location3 = DeviceLocation(device_id=device2.id, latitude=44.7128, longitude=-75.0060)

    db.add(location1)
    db.add(location2)
    db.add(location3)
    db.commit()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    add_test_data(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_device():
    lowercase_str = uuid.uuid4().hex
    query = f"""mutation MyMutation {{createDevice(name: "{lowercase_str}") {{ id name description }}}}"""
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["createDevice"]["name"] == lowercase_str


def test_list_locations_by_device(test_db):
    db = TestingSessionLocal()
    locations = get_last_location_of_every_device(db)
    query = """query MyQuery {
            listLocations {
            deviceId
            latitude
            longitude
            timestamp
            }
            }"""
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert len(response.json()["data"]["listLocations"]) == len(locations)


