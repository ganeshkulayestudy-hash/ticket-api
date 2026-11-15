from typing import Literal
from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = ""
    priority: Literal["low", "medium", "high"] = "medium"


class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = None
    priority: Literal["low", "medium", "high"] | None = None
