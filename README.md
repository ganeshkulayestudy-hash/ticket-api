# Ticket API

A small support-ticket REST API built with FastAPI and Pydantic.
It uses sample data only. Built as part of a 90-day AI engineering study plan.

## Features

- Create, list, view, update, close and delete tickets
- Filter tickets by status
- Input validation with clear error messages
- One standard JSON error format for every error
- Logging of every change
- Settings read from a .env file (not stored in Git)
- 33 automated tests with pytest (fixtures and parametrized tests)

## Project structure

| File | Purpose |
|---|---|
| main.py | Creates the app and plugs everything in |
| routes.py | The ticket endpoints |
| models.py | Pydantic models for create and update |
| storage.py | In-memory ticket storage |
| config.py | Settings loaded from .env |
| errors.py | Standard error format and error logging |
| conftest.py | Shared pytest fixtures |
| test_main.py | The test suite |
| .env.example | Template for your own .env file |

## Run it locally

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    copy .env.example .env
    uvicorn main:app --reload --port 8001

Then open http://127.0.0.1:8001/docs to try the API.

## Endpoints

| Method | Path | What it does |
|---|---|---|
| GET | / | Health check |
| POST | /tickets | Create a ticket |
| GET | /tickets | List tickets (optional ?status=open or closed) |
| GET | /tickets/{id} | Get one ticket |
| PATCH | /tickets/{id} | Update title, description or priority |
| POST | /tickets/{id}/close | Close a ticket |
| DELETE | /tickets/{id} | Delete a ticket |

## Error format

Every error uses the same shape:

    {"error": {"code": 404, "message": "Ticket not found"}}

Invalid data also lists the fields that are wrong:

    {"error": {"code": 422, "message": "Validation failed",
               "details": [{"field": "title", "message": "..."}]}}

## Run the tests

    pytest

## Known limitations

- Tickets are stored in memory and disappear when the server restarts.
- Ticket ids can repeat after a delete. A real database is planned for a later week.
