from typing import Literal

from fastapi import FastAPI
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
