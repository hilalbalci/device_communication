import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models import DeviceLocation, Device
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool


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


@pytest.fixture
def db_session():
    SQLITE_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLITE_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    add_test_data(session)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides[get_db] = get_db
