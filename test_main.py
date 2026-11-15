def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ticket API is running"}


def test_create_ticket(client):
    response = client.post(
        "/tickets",
        json={"title": "Printer not working", "description": "Floor 2", "priority": "high"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["status"] == "open"
    assert data["priority"] == "high"


def test_create_ticket_rejects_short_title(client):
    response = client.post("/tickets", json={"title": "ab"})
    assert response.status_code == 422


def test_list_tickets(client, ticket):
    response = client.get("/tickets")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_ticket(client, ticket):
    response = client.get(f"/tickets/{ticket['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Printer not working"


def test_get_missing_ticket_returns_404(client):
    response = client.get("/tickets/999")
    assert response.status_code == 404


def test_update_ticket(client, ticket):
    response = client.patch(f"/tickets/{ticket['id']}", json={"priority": "high"})
    assert response.status_code == 200
    assert response.json()["priority"] == "high"
    assert response.json()["title"] == "Printer not working"


def test_update_missing_ticket_returns_404(client):
    response = client.patch("/tickets/999", json={"priority": "high"})
    assert response.status_code == 404


def test_update_rejects_short_title(client, ticket):
    response = client.patch(f"/tickets/{ticket['id']}", json={"title": "ab"})
    assert response.status_code == 422


def test_close_ticket(client, ticket):
    response = client.post(f"/tickets/{ticket['id']}/close")
    assert response.status_code == 200
    assert response.json()["status"] == "closed"


def test_close_missing_ticket_returns_404(client):
    response = client.post("/tickets/999/close")
    assert response.status_code == 404


def test_delete_ticket(client, ticket):
    response = client.delete(f"/tickets/{ticket['id']}")
    assert response.status_code == 204
    assert client.get(f"/tickets/{ticket['id']}").status_code == 404


def test_delete_missing_ticket_returns_404(client):
    response = client.delete("/tickets/999")
    assert response.status_code == 404


def test_filter_tickets_by_status(client, ticket):
    client.post("/tickets", json={"title": "Second ticket"})
    client.post(f"/tickets/{ticket['id']}/close")
    open_tickets = client.get("/tickets?status=open").json()
    assert len(open_tickets) == 1
    assert open_tickets[0]["title"] == "Second ticket"


def test_app_name_comes_from_settings(client):
    from config import settings

    assert settings.app_name == "Ticket API"
    assert client.get("/").json() == {"message": "Ticket API is running"}


def test_not_found_uses_error_format(client):
    response = client.get("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"error": {"code": 404, "message": "Ticket not found"}}


def test_validation_error_uses_error_format(client):
    response = client.post("/tickets", json={"title": "ab"})
    body = response.json()
    assert response.status_code == 422
    assert body["error"]["message"] == "Validation failed"
    assert body["error"]["details"][0]["field"] == "title"


def test_create_ticket_is_logged(client, caplog):
    import logging

    caplog.set_level(logging.INFO, logger="ticket_api")
    client.post("/tickets", json={"title": "Printer not working"})
    assert "Created ticket 1" in caplog.text


import pytest


@pytest.mark.parametrize("title", ["", "a", "ab", "x" * 101])
def test_create_rejects_invalid_titles(client, title):
    response = client.post("/tickets", json={"title": title})
    assert response.status_code == 422


@pytest.mark.parametrize("priority", ["low", "medium", "high"])
def test_create_accepts_valid_priorities(client, priority):
    response = client.post("/tickets", json={"title": "Printer not working", "priority": priority})
    assert response.status_code == 201
    assert response.json()["priority"] == priority


@pytest.mark.parametrize("priority", ["urgent", "HIGH", "", 5])
def test_create_rejects_invalid_priorities(client, priority):
    response = client.post("/tickets", json={"title": "Printer not working", "priority": priority})
    assert response.status_code == 422


@pytest.mark.parametrize(
    "method, path",
    [
        ("GET", "/tickets/999"),
        ("PATCH", "/tickets/999"),
        ("POST", "/tickets/999/close"),
        ("DELETE", "/tickets/999"),
    ],
)
def test_missing_ticket_returns_error_format(client, method, path):
    response = client.request(method, path, json={"priority": "high"})
    assert response.status_code == 404
    assert response.json()["error"]["code"] == 404
