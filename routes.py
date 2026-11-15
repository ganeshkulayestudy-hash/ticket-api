from fastapi import APIRouter, HTTPException

from models import TicketCreate, TicketUpdate
from storage import tickets

router = APIRouter(prefix="/tickets")


@router.post("", status_code=201)
def create_ticket(ticket: TicketCreate):
    new_ticket = {"id": len(tickets) + 1, "status": "open", **ticket.model_dump()}
    tickets.append(new_ticket)
    return new_ticket


@router.get("")
def list_tickets(status: str | None = None):
    if status:
        return [t for t in tickets if t["status"] == status]
    return tickets


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")


@router.patch("/{ticket_id}")
def update_ticket(ticket_id: int, update: TicketUpdate):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket.update(update.model_dump(exclude_none=True))
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")


@router.post("/{ticket_id}/close")
def close_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["status"] = "closed"
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")


@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            tickets.remove(ticket)
            return
    raise HTTPException(status_code=404, detail="Ticket not found")
