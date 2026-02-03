## Backend

### Setup

```bash
uv sync --all-groups --project ./backend
```

### Run

```bash
uv run uvicorn tabgrounds.main:app --reload
```

### Generate OpenAPI Schema

```bash
uv run python -c "import json; from tabgrounds.main import app; print(json.dumps(app.openapi(), indent=2))" > openapi.json
```