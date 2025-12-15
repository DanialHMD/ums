# UMS — University Management System

Lightweight backend API for managing users, roles, students, courses, and enrollments.
Built with FastAPI and designed for simple deployment and local development.

## Features

- RESTful API endpoints for users, roles, students, courses, and enrollments
- Authentication utilities and Redis integration for session/caching (`app/core`)
- Database models and access layer (`app/models`)
- Modular route organization under `app/routes`

## Repo structure

- `app/` — application package
  - `main.py` — FastAPI application entrypoint
  - `core/` — utilities (auth, settings, Redis client)
  - `models/` — database connection and ORM/queries
  - `routes/` — API route modules
- `environment/` — local Python virtual environment (included in workspace)
- `requirements.txt` — Python dependencies

## Prerequisites

- Python 3.11 (project was developed with 3.11)
- PostgreSQL (or any DB supported by the project's DB layer)
- Redis (optional — used by `app/core/redis_client.py`)

## Quickstart (Windows)

1. Create/activate virtual environment (if not already present):

```powershell
python -m venv environment
.\environment\Scripts\Activate.ps1
# Or on cmd.exe:
.\environment\Scripts\activate.bat
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Set environment variables (example):

```powershell
$env:DATABASE_URL = "postgresql://user:pass@localhost:5432/um_db"
$env:REDIS_URL = "redis://localhost:6379/0"
$env:SECRET_KEY = "replace-with-a-secure-secret"
```

4. Run the development server:

```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API docs will be available at `http://localhost:8000/docs`.

## Configuration

Configuration values are centralized in `app/core/settings.py`. Add or override environment variables as appropriate for your deployment.

Common variables:
- `DATABASE_URL` — database connection string
- `REDIS_URL` — Redis connection string (optional)
- `SECRET_KEY` — application secret for signing tokens/sessions

## Development notes

- Routes are organized in `app/routes/*.py`. Add new resources by creating a route module and registering it in `app/main.py`.
- Database access is in `app/models`; adapt the connection string and models per your DB choice.
- `app/core/auth_utils.py` contains authentication helpers — review before deploying to production.

## Contributing

1. Fork the repo and create a branch for your feature/fix.
2. Open a pull request against `main` with a clear description.

