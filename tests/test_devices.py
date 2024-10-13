import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Device, DeviceLocation

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


def add_test_data(db):
    device1 = Device(name="Test Device 1", description="This is a test device.")
    device2 = Device(name="Test Device 2", description="This is another test device.")

    db.add(device1)
    db.add(device2)
    db.commit()

    location1 = DeviceLocation(device_id=device1.id, latitude=1, longitude=4)
    location2 = DeviceLocation(device_id=device1.id, latitude=2, longitude=5)
    location3 = DeviceLocation(device_id=device2.id, latitude=3, longitude=6)

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
    yield db
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def test_client():
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


def test_create_device(test_client):
    lowercase_str = uuid.uuid4().hex
    query = f"""mutation MyMutation {{createDevice(name: "{lowercase_str}") {{ id name description }}}}"""
    response = test_client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["createDevice"]["name"] == lowercase_str


def test_list_locations(test_db, test_client):
    locations = test_db.query(DeviceLocation).join(Device, Device.id == DeviceLocation.device_id). \
        filter(Device.is_deleted == False)
    query = """query MyQuery {
            listLocations {
            deviceId
            latitude
            longitude
            timestamp
            }
            }"""
    response = test_client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert len(response.json()["data"]["listLocations"]) == locations.count()


def test_list_locations_by_device(test_db, test_client):
    locations = test_db.query(DeviceLocation).join(Device, Device.id == DeviceLocation.device_id).\
        filter(Device.is_deleted == False)
    device_id = locations.first().device_id
    device_locations = locations.filter(Device.id == device_id)
    query = f"""query MyQuery {{listLocationByDevice(deviceId: {device_id}) {{deviceId}}}}"""
    response = test_client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert len(response.json()["data"]["listLocationByDevice"]) == device_locations.count()
