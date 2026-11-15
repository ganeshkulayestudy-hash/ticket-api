import pytest
from fastapi.testclient import TestClient

from main import app
from storage import tickets


@pytest.fixture(autouse=True)
def clear_tickets():
    tickets.clear()
    yield
    tickets.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def ticket(client):
    response = client.post("/tickets", json={"title": "Printer not working"})
    return response.json()
