
generate-schema:
    uv run --project ./backend python -c "import json; from tabgrounds.main import app; print(json.dumps(app.openapi(), indent=2))" > openapi.json

run-backend:
    uv run --project ./backend uvicorn tabgrounds.main:app --reload

[working-directory: 'frontend']
run-frontend:
    bun run dev

[working-directory: 'frontend']
build-frontend:
    bun run build
