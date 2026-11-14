from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Ticket API")

tickets = []


class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = ""
    priority: Literal["low", "medium", "high"] = "medium"


@app.get("/")
def home():
    return {"message": "Ticket API is running"}


@app.post("/tickets", status_code=201)
def create_ticket(ticket: TicketCreate):
    new_ticket = {"id": len(tickets) + 1, "status": "open", **ticket.model_dump()}
    tickets.append(new_ticket)
    return new_ticket


@app.get("/tickets")
def list_tickets():
    return tickets


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")


class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = None
    priority: Literal["low", "medium", "high"] | None = None


@app.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, update: TicketUpdate):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket.update(update.model_dump(exclude_none=True))
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")
