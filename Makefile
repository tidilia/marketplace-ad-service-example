.PHONY: lint format check test migrate migrate-create run outbox seed

lint:
	uv run ruff check --fix src/ bin/

format:
	uv run ruff format src/ bin/

check: lint format

test:
	uv run pytest tests/ -v

migrate:
	uv run alembic upgrade head

migrate-create:
	uv run alembic revision --autogenerate -m "$(name)"

run:
	uv run python -m bin.api

outbox-relay:
	uv run python -m bin.outbox

seed:
	uv run python -m bin.seed
