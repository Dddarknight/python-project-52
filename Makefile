lint:
	poetry run flake8

install:
	poetry install

test-coverage:
	poetry run pytest --cov=. --cov-report xml

build:
	poetry build

test:
	poetry run pytest
