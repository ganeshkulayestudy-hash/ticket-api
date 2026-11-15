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
