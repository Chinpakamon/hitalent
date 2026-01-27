black_formatter:
	poetry run black ./app/ ./tests/ --config pyproject.toml

black_check:
	poetry run black ./app/ ./tests/ --config pyproject.toml --check

isort_formatter:
	poetry run isort ./app/ ./tests/ --settings-path pyproject.toml

isort_check:
	poetry run isort check ./app/ ./tests/ --settings-path pyproject.toml

ruff_checker:
	poetry run ruff check . --config pyproject.toml

run_formaters: black_formatter isort_formatter
run_linters: black_check isort_check ruff_checker
run_tests:
	poetry run pytest -vvvvx

up_compose_local:
	docker compose up -d --build

down_compose_local:
	docker compose down -v
