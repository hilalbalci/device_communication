import uuid
from app.tests.conftest import test_client


def test_create_device(test_client):
    lowercase_str = uuid.uuid4().hex
    query = f"""mutation MyMutation {{createDevice(name: "{lowercase_str}") {{ id name description }}}}"""
    response = test_client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["createDevice"]["name"] == lowercase_str
