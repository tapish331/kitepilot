# apps/api — FastAPI control plane

## Dev
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ./apps/api[dev]
uvicorn kitepilot_api.main:app --reload
```

## Checks
```bash
ruff check apps/api && black --check apps/api && mypy apps/api && pytest -q apps/api
```

## Docker
```bash
docker build -f apps/api/Dockerfile -t kitepilot-api:dev .
docker run -p 8000:8000 kitepilot-api:dev
```

### Database & migrations

Set a DATABASE_URL in your environment (see .env.sample).

Create/upgrade tables:
```bash
export DATABASE_URL=postgresql+psycopg://kitepilot:kitepilot@localhost:5432/kitepilot
cd apps/api
python -m pip install -e .[dev]
alembic -c alembic.ini upgrade head
```

Run integration tests (Docker required):
```bash
pytest -q apps/api/tests/integration
```
