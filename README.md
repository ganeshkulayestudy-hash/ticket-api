# Ticket API

A small REST API for managing support tickets, built with Python, FastAPI and Pydantic.
It is a learning project: all data is kept in memory and is synthetic (no real data).

## Features

- Create, list, read, update, close and delete tickets
- Input validation (title length, priority values) with clear error responses
- Filter tickets by status
- Automated tests with pytest

## Run it locally

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs for the interactive API page.

## Endpoints

| Method | Path | What it does |
|--------|------|--------------|
| GET | / | Health check |
| POST | /tickets | Create a ticket |
| GET | /tickets | List tickets (optional ?status=open or closed) |
| GET | /tickets/{id} | Get one ticket |
| PATCH | /tickets/{id} | Update title, description or priority |
| POST | /tickets/{id}/close | Mark a ticket as closed |
| DELETE | /tickets/{id} | Delete a ticket |

## Run the tests

    pytest

## Known limitations

- Data is stored in memory, so it is lost when the server restarts.
- Ticket ids are not permanent after deletes. A database comes in a later week.
