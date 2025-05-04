# swift_remitly_2025

A project written as an assignment for Remitly Internship 2025


- Python 3.11
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic v2
- Docker + Docker Compose
- Pytest

How to start it?

- docker compose up --build


How to run tests?

- pytest tests.py


Endpoints

- GET /v1/swift-codes/{swiftCode}
- GET /v1/swift-codes/country/{countryISO2}
- POST /v1/swift-codes
- DELETE /v1/swift-codes/{swiftCode}
