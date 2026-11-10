from fastapi.testclient import TestClient

from main import app, tickets

client = TestClient(app)


def setup_function():
    tickets.clear()


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_create_ticket():
    response = client.post(
        "/tickets", json={"title": "Printer not working", "priority": "high"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["status"] == "open"


def test_short_title_is_rejected():
    response = client.post("/tickets", json={"title": "ab"})
    assert response.status_code == 422


def test_list_tickets():
    client.post("/tickets", json={"title": "Printer not working"})
    response = client.get("/tickets")
    assert len(response.json()) == 1
