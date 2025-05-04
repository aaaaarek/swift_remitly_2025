# swift_remitly_2025

A project written as an assignment for Remitly Internship 2025

## Technologies Used

- Python 3.11
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic v2
- Docker + Docker Compose
- Pytest

## How to start it?

- docker compose up --build

## After that type in a browser

- http://localhost:8080/docs

## How to run tests?

- pytest tests.py


## Endpoints

- GET /v1/swift-codes/{swiftCode}
- GET /v1/swift-codes/country/{countryISO2}
- POST /v1/swift-codes
- DELETE /v1/swift-codes/{swiftCode}
